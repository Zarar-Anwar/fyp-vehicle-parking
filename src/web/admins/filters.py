import django_filters
from django.forms import TextInput

from src.web.accounts.models import User
from src.web.agency.models import Agency, Vehicle


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'username'}), lookup_expr='icontains')
    first_name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'first name'}), lookup_expr='icontains')
    last_name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'last name'}), lookup_expr='icontains')
    email = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'email'}), lookup_expr='icontains')

    class Meta:
        model = User
        fields = {}


class AgencyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'name'}), lookup_expr='icontains')
    description = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'description'}), lookup_expr='icontains')

    class Meta:
        model = Agency
        fields = {}
        exclude = ['user', 'company_registration_number', 'vat_number', 'address', 'contact_phone',
                   'company_postal_code', 'company_city', 'company_state', 'website', 'instagram', 'facebook',
                   'twitter']
        # exclude = ['user', 'company_registration_number', 'vat_number', 'address', 'contact_phone',
        #            'company_postal_code', 'company_city', 'company_state', 'website', 'instagram', 'facebook',
        #            'twitter', 'logo', 'cover_image', 'tagline', 'description', 'contact_email', 'contact_phone',


class VehicleFilter(django_filters.FilterSet):
    registration_number = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'registration number'}), lookup_expr='icontains')
    model = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'model'}), lookup_expr='icontains')
    class Meta:
        model = Vehicle
        fields = {}
        exclude = ['user', 'company_registration_number', 'vat_number', 'address', 'contact_phone',
                   'company_postal_code', 'company_city', 'company_state', 'website', 'instagram', 'facebook',
                   'twitter']
        # exclude = ['user', 'company_registration_number', 'vat_number', 'address', 'contact_phone',
        #            'company_postal_code', 'company_city', 'company_state', 'website', 'instagram', 'facebook',
        #            'twitter', 'logo', 'cover_image', 'tagline', 'description', 'contact_email', 'contact_phone',