from django.urls import path
from .views import HomeView, ContactView, AboutView, FaqView, ServicesView , PrivacyView, TermsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),  # URL for the about page
    path('contact/', ContactView.as_view(), name='contact'),  # URL for the contact page
    path('services/', ServicesView.as_view(), name='services'),  # URL for the services page
    path('faq/', FaqView.as_view(), name='faq'),  # URL for the FAQ page
    path('terms/', TermsView.as_view(), name='terms'),  # URL for the terms page
    path('privacy/', PrivacyView.as_view(), name='privacy'),  # URL for the privacy policy page
    
    # Add more URL patterns as needed
]