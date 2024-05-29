from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from src.web.accounts.models import User


class AgencyBranchData(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)


class Agency(AgencyBranchData):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='agency_logos/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='agency_covers/', null=True, blank=True)
    company_name = models.CharField(max_length=255)
    description = models.TextField()
    company_city = models.CharField(max_length=255)
    website = models.URLField(max_length=255, null=True, blank=True)
    instagram = models.URLField(max_length=255, null=True, blank=True)
    facebook = models.URLField(max_length=255, null=True, blank=True)
    twitter = models.URLField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Agencies'
        ordering = ['name']

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    driver = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vehicle_driver')
    registration_number = models.CharField(max_length=20)
    model = models.CharField(max_length=100)
    fare_rates = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='vehicle_images/', null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Vehicles'

    def __str__(self):
        return f"{self.model} - {self.registration_number}"

    def save(self, *args, **kwargs):
        if self.driver and not self.driver.is_driver:
            raise ValidationError("The selected user is not a driver.")
        super().save(*args, **kwargs)


class Schedule(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    destination = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.PositiveIntegerField()
    schedule_date = models.DateField()
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Schedules'
        ordering = ['vehicle', 'destination']

    def __str__(self):
        return f"{self.vehicle.model} Schedule to {self.destination}"

    def update_status(self):
        if self.schedule_date < date.today():
            self.status = False
            self.save()

    @classmethod
    def update_all_statuses(cls):
        cls.objects.filter(schedule_date__lt=date.today(), status=True).update(status=False)


class Referral(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=20, unique=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Referrals'

    def __str__(self):
        return f"Referral code: {self.code}"


class Seat(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='seats')
    seat_number = models.PositiveIntegerField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Bus {self.vehicle.model} - Seat {self.seat_number}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)
    payment_status = models.BooleanField(default=False)
    booking_date = models.DateTimeField(auto_now_add=True)
    referral = models.ForeignKey(Referral, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Bookings'
        ordering = ['user', 'schedule']

    def __str__(self):
        return f"Booking by {self.user} for {self.schedule}"


@receiver(post_save, sender=Vehicle)
def create_seats(sender, instance, created, **kwargs):
    if created:
        for i in range(1, instance.number_of_seats + 1):
            Seat.objects.create(bus=instance, seat_number=i)
