from django.contrib import admin

from src.web.admins.models import Queue


@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'queue_number', 'arrival_time', 'departure_time')
