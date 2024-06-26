from datetime import date

import stripe
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import F
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView
import json

from core import settings
from src.web.accounts.models import User
from src.web.agency.models import Vehicle, Seat, Booking, Schedule


# Create your views here.


class HomeView(TemplateView):
    template_name = 'website/home.html'


class CarsView(ListView):
    model = Schedule
    context_object_name = 'buses'
    template_name = 'website/cars.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle_list = Schedule.objects.all()
        paginator = Paginator(vehicle_list, 2)  # Display 5 items per page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class CarDetailsView(DetailView):
    model = Schedule
    context_object_name = 'bus'
    template_name = 'website/car_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        schedule = Schedule.objects.get(vehicle=self.object.vehicle)
        seats = Seat.objects.filter(schedule=schedule)
        total_seats = seats.count()

        half_seats = total_seats // 2

        seat_1 = seats[:half_seats]
        seat_2 = seats[half_seats:]

        context['seat_1'] = seat_1
        context['seat_2'] = seat_2
        context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


class AboutView(TemplateView):
    template_name = 'website/about.html'


class ContactView(TemplateView):
    template_name = 'website/contact.html'


class TermsAndConditionsView(TemplateView):
    template_name = 'website/terms_and_conditions.html'


"""STRIPE"""

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            fare_rates = data.get('fare_rates')
            seat_number = data.get('seat_number')

            if not fare_rates or fare_rates == 'null':
                return HttpResponseBadRequest("Invalid fare rates.")

            fare_rates = float(fare_rates)  # Convert fare_rates to float if it's valid

            YOUR_DOMAIN = "http://localhost:8000"
            user_id = self.request.user.id

            # Log user ID for debugging
            print(f"User ID: {user_id}")

            if user_id is None:
                return HttpResponseBadRequest("User not authenticated.")

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Bus Ticket',
                            },
                            'unit_amount': int(fare_rates * 100),  # convert to cents
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/success/?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=YOUR_DOMAIN + '/cancel/',
                metadata={
                    'seat_number': seat_number,
                    'user_id': user_id
                }
            )

            try:
                seat = Seat.objects.get(seat_number=seat_number)
            except Seat.DoesNotExist:
                return HttpResponseBadRequest("Seat does not exist.")

            schedule = seat.schedule

            if schedule.available_seats <= 0:
                raise ValidationError("No available seats for this schedule.")

            # Mark the seat as booked and create a booking
            schedule.available_seats -= 1
            schedule.save()

            return JsonResponse({
                'id': checkout_session.id,
                'user_id': user_id
            })
        except ValidationError as e:
            return HttpResponseBadRequest(str(e))
        except Exception as e:
            return HttpResponseBadRequest(str(e))


def SuccessView(request):
    session_id = request.GET.get('session_id')

    if not session_id:
        return HttpResponseBadRequest("Session ID is missing.")

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        seat_number = session.metadata.get('seat_number')
        user_id = session.metadata.get('user_id')

        # Log session metadata for debugging
        print(f"Session Metadata: seat_number={seat_number}, user_id={user_id}")

        if not user_id:
            return HttpResponseBadRequest("User ID is missing in session metadata.")

        user = User.objects.get(id=user_id)
        print(user)

        if not seat_number:
            return HttpResponseBadRequest("Seat number is missing in session metadata.")

        try:
            seat = Seat.objects.get(seat_number=seat_number)
        except Seat.DoesNotExist:
            return HttpResponseBadRequest("Seat does not exist.")

        seat.is_booked = True
        seat.save()

        schedule = Schedule.objects.get(id=seat.schedule.id)

        booking = Booking.objects.create(
            user=user,
            schedule=schedule,
            seat=seat,
            payment_status=True
        )

        booking.save()

        messages.success(request, "Payment Successful")
        return render(request, 'website/home.html')
    except stripe.error.StripeError as e:
        return HttpResponseBadRequest(f"Stripe Error: {str(e)}")
    except Exception as e:
        return HttpResponseBadRequest(str(e))


def CancelView(request):
    messages.error(request, "Payment Cancelled")
    return render(request, 'website/car_details.html')
