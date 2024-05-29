from django.urls import path
from .views import (
    DashboardView,
    UserListView, UserPasswordResetView, UserDetailView, UserUpdateView, AgencyListView, AgencyDetailView,
    AgencyUpdateView, VehicleListView, VehicleDetailView, VehicleUpdateView, VehicleAddView, DriverListView,
    BookingListView, ScheduleListView
)

app_name = 'admins'
urlpatterns = [

    path('', DashboardView.as_view(), name='dashboard'),

    path('user/', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('user/<int:pk>/change/', UserUpdateView.as_view(), name='user-update'),
    path('user/<int:pk>/password/reset/', UserPasswordResetView.as_view(), name='user-password-reset-view'),

    # Agency
    path('agency/', AgencyListView.as_view(), name='agency-list'),
    path('agency/<int:pk>/', AgencyDetailView.as_view(), name='agency-detail'),
    path('agency/<int:pk>/change/', AgencyUpdateView.as_view(), name='agency-update'),

    # Vehicle
    path('vehicle/', VehicleListView.as_view(), name='vehicle-list'),
    path('vehicle/add/', VehicleAddView.as_view(), name='vehicle-add'),
    path('vehicle/<int:pk>/', VehicleDetailView.as_view(), name='vehicle-detail'),
    path('vehicle/<int:pk>/change/', VehicleUpdateView.as_view(), name='vehicle-update'),

    # Driver
    path('driver-list/', DriverListView.as_view(), name='driver-list'),

    # Booking
    path('booking-list/', BookingListView.as_view(), name='booking-list'),
    path('schedule-list/', ScheduleListView.as_view(), name='schedule-list'),

]
