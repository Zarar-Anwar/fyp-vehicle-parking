from django.urls import path
from .views import (
    DashboardView,
    UserListView, UserPasswordResetView, UserDetailView, UserUpdateView, AgencyListView, AgencyDetailView,
    AgencyUpdateView, VehicleListView, VehicleDetailView, VehicleUpdateView
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

    # Vehlicle
    path('vehicle/', VehicleListView.as_view(), name='vehicle-list'),
    path('vehicle/<int:pk>/', VehicleDetailView.as_view(), name='vehicle-detail'),
    path('vehicle/<int:pk>/change/', VehicleUpdateView.as_view(), name='vehicle-update'),

]
