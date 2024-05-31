from django.urls import path

from src.web.website.views import HomeView, CarsView, AboutView, ContactView, TermsAndConditionsView, \
    CarDetailsView, CreateCheckoutSessionView, SuccessView, CancelView

app_name = "website"

urlpatterns = [

    path('', HomeView.as_view(), name='home'),
    path('cars/', CarsView.as_view(), name='cars'),
    path('cars/details/<int:pk>', CarDetailsView.as_view(), name='car-details'),
    path('about-us/', AboutView.as_view(), name='about-us'),
    path('contact-us/', ContactView.as_view(), name='contact-us'),
    path('terms-and-conditions/', TermsAndConditionsView.as_view(), name='terms-and-conditions'),

]

urlpatterns += [
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('success/', SuccessView, name='success'),
    path('cancel/', CancelView, name='cancel'),
]
