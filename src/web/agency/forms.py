from django import forms
from django.core.exceptions import ValidationError
from .models import Vehicle


class VehicleAdminForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'

    def clean_driver(self):
        driver = self.cleaned_data.get('driver')
        if driver and not driver.is_driver:
            raise ValidationError("The selected user is not a driver.")
        return driver
