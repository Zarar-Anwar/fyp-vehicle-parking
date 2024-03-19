from django.db import models

from src.web.agency.models import Vehicle


class Queue(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    queue_number = models.IntegerField()
    arrival_time = models.DateTimeField(auto_now_add=True)
    departure_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Queue {self.queue_number} - {self.vehicle}"
