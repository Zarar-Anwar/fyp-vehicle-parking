from django.urls import path

from src.web.website.views import HomeView, CarsView, FaqsView, AboutView, ContactView, TermsAndConditionsView, \
    CarDetailsView

app_name = "website"

urlpatterns = [

    path('', HomeView.as_view(), name='home'),
    path('cars/', CarsView.as_view(), name='cars'),
    path('cars/details/', CarDetailsView.as_view(), name='car-details'),
    path('faqs/', FaqsView.as_view(), name='faqs'),
    path('about-us/', AboutView.as_view(), name='about-us'),
    path('contact-us/', ContactView.as_view(), name='contact-us'),
    path('terms-and-conditions/', TermsAndConditionsView.as_view(), name='terms-and-conditions'),

]
