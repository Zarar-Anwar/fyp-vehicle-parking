from django.db.models import Sum
from src.web.agency.models import Schedule, Booking, Vehicle


def agency_income(agency):
    income_schedules = Schedule.objects.filter(vehicle__agency=agency)
    total_income = \
    Booking.objects.filter(schedule__in=income_schedules, payment_status=True).aggregate(total=Sum('schedule__price'))[
        'total']

    return total_income or 0


def driver_income(driver):
    driver_vehicles = Vehicle.objects.filter(driver=driver)
    income_schedules = Schedule.objects.filter(vehicle__in=driver_vehicles)
    total_income = \
    Booking.objects.filter(schedule__in=income_schedules, payment_status=True).aggregate(total=Sum('schedule__price'))[
        'total']

    return total_income or 0  # Return 0 if total_income is None
