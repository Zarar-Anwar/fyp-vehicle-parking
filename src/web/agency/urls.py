from django.urls import path

from src.web.agency.views import DashboardView, BookingView, ProfileView, ReviewsView, WishlistView, SettingView, \
    OrdersView, TravellersView, TravelAgentsView, InvoicesView, PaymentsView, CurrencyView, SubscriberView, \
    LocationView, VehicleView, EditProfileView

app_name = "agency"

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('booking/', BookingView.as_view(), name="booking"),
    path('orders/', OrdersView.as_view(), name="orders"),
    path('vehicle/', VehicleView.as_view(), name="vehicle"),

    path('travellers/', TravellersView.as_view(), name="travellers"),

    path('profile/', ProfileView.as_view(), name="profile"),
    path('edit/profile/', EditProfileView.as_view(), name="edit_profile"),
    path('reviews/', ReviewsView.as_view(), name="reviews"),
    path('wishlist/', WishlistView.as_view(), name="wishlist"),

    path('travel-agents/', TravelAgentsView.as_view(), name="travel-agents"),

    path('invoices/', InvoicesView.as_view(), name="invoices"),
    path('payments/', PaymentsView.as_view(), name="payments"),
    path('currency/', CurrencyView.as_view(), name="currency"),
    path('subscriber/', SubscriberView.as_view(), name="subscriber"),

    path('location/', LocationView.as_view(), name="location"),

    path('setting/', SettingView.as_view(), name="setting"),
]
