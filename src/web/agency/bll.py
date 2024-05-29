from src.web.agency.models import Schedule


def agency_income(agency):
    income_schedules = Schedule.objects.filter(vehicle__agency=agency)
    total_income = sum(schedule.price for schedule in income_schedules)

    return total_income
