from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear
import datetime

from src.web.agency.models import Schedule


def total_system_income():
    income_schedules = Schedule.objects.all()
    total_income = sum(schedule.price for schedule in income_schedules)

    current_year = datetime.datetime.now().year

    monthly_income_qs = Schedule.objects.filter(schedule_date__year=current_year).annotate(
        month=TruncMonth('schedule_date')
    ).values('month').annotate(
        total_income=Sum('price')
    ).order_by('month')

    monthly_income = sum(item['total_income'] for item in monthly_income_qs)

    yearly_income_qs = Schedule.objects.annotate(
        year=TruncYear('schedule_date')
    ).values('year').annotate(
        total_income=Sum('price')
    ).order_by('year')

    yearly_income = sum(item['total_income'] for item in yearly_income_qs)

    income = {
        "total_income": total_income,
        "monthly_income": monthly_income,
        "yearly_income": yearly_income
    }

    return income
