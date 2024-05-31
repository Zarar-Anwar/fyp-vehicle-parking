from django.contrib import admin

from .models import Agency, Vehicle, Schedule, Booking, Seat


@admin.register(Agency)
class AgencyAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'contact_phone', 'contact_email', 'address')


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'registration_number', 'model', 'capacity')


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
