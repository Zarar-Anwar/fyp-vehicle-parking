from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import (
    TemplateView, ListView, DetailView, UpdateView, CreateView
)

from src.web.accounts.models import User
# from faker_data import initialization
from src.web.admins.filters import UserFilter, AgencyFilter, VehicleFilter
from src.web.agency.models import Agency, Vehicle

admin_decorators = [login_required, user_passes_test(lambda u: u.is_superuser)]


@method_decorator(admin_decorators, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'admins/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['users_count_data'] = list(User.objects.values_list('id', flat=True))
        # context = calculate_statistics(context)
        # initialization(init=False, mid=False, end=False)
        return context


""" USERS """


@method_decorator(admin_decorators, name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'admins/user_list.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        user_filter = UserFilter(self.request.GET, queryset=User.objects.filter())
        context['user_filter_form'] = user_filter.form

        paginator = Paginator(user_filter.qs, 50)
        page_number = self.request.GET.get('page')
        user_page_object = paginator.get_page(page_number)

        context['user_list'] = user_page_object
        return context


@method_decorator(admin_decorators, name='dispatch')
class UserDetailView(DetailView):
    model = User
    template_name = 'admins/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return context


@method_decorator(admin_decorators, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = [
        'profile_image', 'first_name', 'last_name',
        'email', 'username', 'phone_number', 'is_active'
    ]
    template_name = 'admins/user_update_form.html'

    def get_success_url(self):
        return reverse('admins:user-detail', kwargs={'pk': self.object.pk})


@method_decorator(admin_decorators, name='dispatch')
class UserPasswordResetView(View):

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = AdminPasswordChangeForm(user=user)
        return render(request, 'admins/admin_password_reset.html', {'form': form, 'object': user})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = AdminPasswordChangeForm(data=request.POST, user=user)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, f"{user.get_full_name()}'s password changed successfully.")
        return render(request, 'admins/admin_password_reset.html', {'form': form, 'object': user})


# Agency

class AgencyListView(ListView):
    model = Agency
    template_name = 'admins/agency_list.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(AgencyListView, self).get_context_data(**kwargs)
        agency_filter = AgencyFilter(self.request.GET, queryset=Agency.objects.filter())
        context['agency_filter_form'] = agency_filter.form

        paginator = Paginator(agency_filter.qs, 50)
        page_number = self.request.GET.get('page')
        agency_page_object = paginator.get_page(page_number)

        context['agency_list'] = agency_page_object
        return context


class AgencyDetailView(DetailView):
    model = Agency
    template_name = 'admins/agency_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        agency = get_object_or_404(Agency, pk=self.kwargs['pk'])
        return context


class AgencyUpdateView(UpdateView):
    model = Agency
    fields = [
        'name',
        'logo', 'cover_image', 'contact_email', 'contact_phone', 'address'
    ]
    template_name = 'admins/agency_update_form.html'

    def get_success_url(self):
        return reverse('admins:agency-detail', kwargs={'pk': self.object.pk})


# Vehicle

class VehicleListView(ListView):
    model = Vehicle
    template_name = 'admins/vehicle_list.html'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(VehicleListView, self).get_context_data(**kwargs)
        vehicle_filter = VehicleFilter(self.request.GET, queryset=Vehicle.objects.filter())
        context['vehicle_filter_form'] = vehicle_filter.form

        paginator = Paginator(vehicle_filter.qs, 50)
        page_number = self.request.GET.get('page')
        vehicle_page_object = paginator.get_page(page_number)

        context['vehicle_list'] = vehicle_page_object
        return context


class VehicleAddView(CreateView):
    model = Vehicle
    fields = ['agency', 'driver', 'registration_number', 'model', 'fare_rates', 'capacity', 'image']
    template_name = 'admins/vehicle_add_form.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['driver'].queryset = get_user_model().objects.filter(is_driver=True)
        return form


class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = 'admins/vehicle_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehicle'] = get_object_or_404(Vehicle, pk=self.kwargs['pk'])
        return context


class VehicleUpdateView(UpdateView):
    model = Vehicle
    fields = [
        'registration_number', 'model', 'capacity', 'image', 'is_active'
    ]
    template_name = 'admins/vehicle_update_form.html'

    def get_success_url(self):
        return reverse('admins:vehicle-detail', kwargs={'pk': self.object.pk})
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     vehicle = get_object_or_404(Vehicle, pk=self.kwargs['pk'])
    #     return context
    #
    # def get_success_url(self):
    #     return reverse('admins:vehicle-detail', kwargs={'pk': self.object.pk})
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     vehicle = get_object_or_404(Vehicle, pk=self.kwargs['pk'])
    #     return context
    #
