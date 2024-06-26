from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear
import datetime

from src.web.agency.models import Booking

def total_system_income():
    # Sum total income from all bookings with completed payments
    total_income = Booking.objects.filter(payment_status=True).aggregate(total_income=Sum('schedule__price'))['total_income'] or 0

    current_year = datetime.datetime.now().year

    # Calculate monthly income for the current year
    monthly_income_qs = Booking.objects.filter(
        payment_status=True, schedule__schedule_date__year=current_year
    ).annotate(
        month=TruncMonth('schedule__schedule_date')
    ).values('month').annotate(
        total_income=Sum('schedule__price')
    ).order_by('month')

    monthly_income = {item['month'].strftime('%Y-%m'): item['total_income'] or 0 for item in monthly_income_qs}

    # Calculate yearly income
    yearly_income_qs = Booking.objects.filter(payment_status=True).annotate(
        year=TruncYear('schedule__schedule_date')
    ).values('year').annotate(
        total_income=Sum('schedule__price')
    ).order_by('year')

    yearly_income = {item['year'].strftime('%Y'): item['total_income'] or 0 for item in yearly_income_qs}

    # Extracting exact numeric values as integers
    total_income = int(total_income)
    monthly_income = {key: int(value) for key, value in monthly_income.items()}
    yearly_income = {key: int(value) for key, value in yearly_income.items()}

    income = {
        "total_income": total_income,
        "monthly_income": monthly_income,
        "yearly_income": yearly_income
    }

    return income
