from django.contrib import admin
from django.core.exceptions import ValidationError

from .forms import VehicleAdminForm
from .models import Agency, Vehicle, Schedule, Booking, Seat


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'contact_phone', 'contact_email', 'address')


class VehicleAdmin(admin.ModelAdmin):
    form = VehicleAdminForm

    def save_model(self, request, obj, form, change):
        try:
            obj.save()
        except ValidationError as e:
            form.add_error('driver', e.message)
            return
        super().save_model(request, obj, form, change)


admin.site.register(Vehicle, VehicleAdmin)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'vehicle', 'departure_time', 'arrival_time', 'destination', 'price', 'available_seats')


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('schedule', 'seat_number', 'is_booked')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'schedule', 'seat', 'payment_status', 'booking_date')
