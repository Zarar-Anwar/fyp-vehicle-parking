from django.core.paginator import Paginator
from django.views.generic import TemplateView, DetailView, ListView

from src.web.agency.models import Vehicle, Seat


# Create your views here.


class HomeView(TemplateView):
    template_name = 'website/home.html'


class CarsView(ListView):
    model = Vehicle
    context_object_name = 'buses'
    template_name = 'website/cars.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vehicle_list = Vehicle.objects.all()
        paginator = Paginator(vehicle_list, 2)  # Display 5 items per page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class CarDetailsView(DetailView):
    model = Vehicle
    context_object_name = 'bus'
    template_name = 'website/car_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seats = Seat.objects.filter(vehicle=self.object)
        total_seats = seats.count()

        half_seats = total_seats // 2

        seat_1 = seats[:half_seats]
        seat_2 = seats[half_seats:]

        context['seat_1'] = seat_1
        context['seat_2'] = seat_2
        return context


class AboutView(TemplateView):
    template_name = 'website/about.html'


class ContactView(TemplateView):
    template_name = 'website/contact.html'


class TermsAndConditionsView(TemplateView):
    template_name = 'website/terms_and_conditions.html'
