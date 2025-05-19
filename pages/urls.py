from django.urls import path
from .views import (
    HomeView,
    ContactView,
    AboutView,
    FaqView,
    ServicesView,
    PrivacyView,
    TermsView,
)
from .dashboard_views import (
    DashboardView,
    DestinationDeleteView,
    MyEnquiryView,
    BookingDetailView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),  # URL for the about page
    path("contact/", ContactView.as_view(), name="contact"),  # URL for the contact page
    path(
        "services/", ServicesView.as_view(), name="services"
    ),  # URL for the services page
    path("faq/", FaqView.as_view(), name="faq"),  # URL for the FAQ page
    path("terms/", TermsView.as_view(), name="terms"),  # URL for the terms page
    path(
        "privacy/", PrivacyView.as_view(), name="privacy"
    ),  # URL for the privacy policy page
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    # path('destination/<slug:slug>/edit/', DestinationUpdateView.as_view(), name='destination-update'),
    path(
        "destination/<slug:slug>/delete/",
        DestinationDeleteView.as_view(),
        name="destination-delete",
    ),
    path(
        "my-enquiry/", MyEnquiryView.as_view(), name="my-enquiry"
    ),  # URL for the my enquiry page
    path("my-enquiry/<int:pk>/", BookingDetailView.as_view(), name="booking-detail"),
    # Add more URL patterns as needed
]
