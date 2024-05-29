from msilib.schema import ListView

from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from src.web.accounts.forms import IncompleteAgencyForm, UserForm, VehicleForm
from src.web.admins.filters import BookingFilter
from src.web.agency.bll import agency_income
from src.web.agency.models import Booking, Agency, Vehicle

from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required

"""DASHBOARD"""


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'agency/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicles'] = Vehicle.objects.filter(agency__owner=self.request.user)
        context['booking'] = Booking.objects.filter(schedule__vehicle__agency__owner=self.request.user)
        agency = get_object_or_404(Agency, owner=self.request.user)
        context['income'] = agency_income(agency)
        return context


"""VEHICLE SETTINGS"""


@method_decorator(login_required, name='dispatch')
class VehicleView(ListView):
    model = Vehicle
    template_name = 'agency/vehicle.html'

    def get_queryset(self):
        agency = get_object_or_404(Agency, owner=self.request.user)
        return Vehicle.objects.filter(agency=agency)


class VehicleUpdateView(UpdateView):
    model = Vehicle
    form_class = VehicleForm  # Use your VehicleForm
    template_name = 'agency/edit_vehicle.html'  # Specify your template
    success_url = reverse_lazy('agency:vehicle')


class VehicleDeleteView(DeleteView):
    model = Vehicle
    success_url = reverse_lazy('agency:vehicle')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return self.get_success_url()


@method_decorator(login_required, name='dispatch')
class TravellersView(TemplateView):
    template_name = 'agency/travellers.html'


@method_decorator(login_required, name='dispatch')
class TravelAgentsView(TemplateView):
    template_name = 'agency/travel_agents.html'


"""TRANSACTIONS"""


@method_decorator(login_required, name='dispatch')
class OrdersView(TemplateView):
    template_name = 'agency/orders.html'


@method_decorator(login_required, name='dispatch')
class InvoicesView(ListView):
    model = Booking
    template_name = "agency/invoices.html"
    context_object_name = "booking"
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(InvoicesView, self).get_context_data(**kwargs)
        booking_filter = BookingFilter(self.request.GET, queryset=Booking.objects.filter())
        context['booking_filter_form'] = booking_filter.form

        paginator = Paginator(booking_filter.qs, 50)
        page_number = self.request.GET.get('page')
        booking_page_object = paginator.get_page(page_number)

        context['booking_list'] = booking_page_object
        return context


@method_decorator(login_required, name='dispatch')
class PaymentsView(TemplateView):
    template_name = 'agency/payments.html'


@method_decorator(login_required, name='dispatch')
class CurrencyView(TemplateView):
    template_name = 'agency/currency.html'


"""SETTINGS"""


@method_decorator(login_required, name='dispatch')
class EditProfileView(View):
    template_name = 'agency/edit_profile.html'
    form_class = IncompleteAgencyForm

    def get(self, request):
        user = request.user
        agency_instance = get_object_or_404(Agency, owner=user)
        form = self.form_class(instance=agency_instance)
        return render(request, template_name=self.template_name, context={"form": form})

    def post(self, request):
        user = request.user
        agency_instance = get_object_or_404(Agency, owner=user)
        form = self.form_class(request.POST, request.FILES, instance=agency_instance)
        if form.is_valid():
            form.save()
            return render(request, template_name=self.template_name, context={"form": form})
        else:
            return render(request, template_name=self.template_name, context={"form": form})


@method_decorator(login_required, name='dispatch')
class SettingView(View):
    template_name = 'agency/setting.html'
    form = UserForm

    def get(self, request):
        form = self.form(instance=request.user)
        return render(request, template_name=self.template_name, context={"form": form})

    def post(self, request):
        form = self.form(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data Updated Successfully')
            return redirect('agency:setting')
        else:
            messages.error(request, "Error While Updating")
            return render(request, template_name=self.template_name, context={"form": form})


@method_decorator(login_required, name='dispatch')
class ProfileView(TemplateView):
    template_name = 'agency/profile.html'
