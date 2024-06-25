from django.urls import path

from src.web.agency.views import DashboardView, ProfileView, SettingView, \
    TravellersView, InvoicesView, PaymentsView, CurrencyView, VehicleView, EditProfileView, \
    TravelAgentsView, VehicleUpdateView, VehicleDeleteView

app_name = "agency"

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('vehicle/', VehicleView.as_view(), name="vehicle"),
    path('update/vehicle/<int:pk>', VehicleUpdateView.as_view(), name="update-vehicle"),
    path('delete/vehicle/<int:pk>', VehicleDeleteView.as_view(), name="delete-vehicle"),

    path('travellers/', TravellersView.as_view(), name="travellers"),
    path('travel-agents/', TravelAgentsView.as_view(), name="travel-agents"),

    path('profile/', ProfileView.as_view(), name="profile"),
    path('edit/profile/', EditProfileView.as_view(), name="edit_profile"),

    path('invoices/', InvoicesView.as_view(), name="invoices"),
    path('payments/', PaymentsView.as_view(), name="payments"),
    path('currency/', CurrencyView.as_view(), name="currency"),

    path('setting/', SettingView.as_view(), name="setting"),
]
