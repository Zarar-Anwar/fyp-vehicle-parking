from django.views.generic import TemplateView

# Create your views here.


class HomeView(TemplateView):
    template_name = 'website/home.html'


class CarsView(TemplateView):
    template_name = 'website/cars.html'


class AboutView(TemplateView):
    template_name = 'website/about.html'


class ContactView(TemplateView):
    template_name = 'website/contact.html'


class TermsAndConditionsView(TemplateView):
    template_name = 'website/terms_and_conditions.html'


class FaqsView(TemplateView):
    template_name = 'website/faqs.html'

