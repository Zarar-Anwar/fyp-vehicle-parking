from django.contrib import admin

from src.web.admins.models import Vehicle, Queue


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'capacity', 'fare_rates', 'registration_details', 'status')


@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'queue_number', 'arrival_time', 'departure_time')
