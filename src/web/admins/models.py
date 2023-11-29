from django.db import models


class Vehicle(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    capacity = models.IntegerField()
    fare_rates = models.DecimalField(max_digits=8, decimal_places=2)
    registration_details = models.TextField()
    status = models.CharField(max_length=20, default='available')

    def __str__(self):
        return f"{self.make} {self.model} - {self.status}"


class Queue(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    queue_number = models.IntegerField()
    arrival_time = models.DateTimeField(auto_now_add=True)
    departure_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Queue {self.queue_number} - {self.vehicle}"