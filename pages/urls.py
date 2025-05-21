from django.urls import path
from .views import (
    HomeView,
    ContactView,
    AboutView,
    FaqView,
    ServicesView,
    PrivacyView,
    TermsView,
    HelpCenterView,
    BecomeAGuideView,
    TravelGuideView,
    GuideOfTheYearView,
    GuideRegistrationView,
    CreatorsView,
    TravelAgentsAdvisorsView,
)
from .dashboard_views import (
    DashboardView,
    DestinationDeleteView,
    MyEnquiryView,
    BookingDetailView,
)

""" 
Help center
About Us
Contact Us
Become A Guide
Travel Guide
Guide of the Year
Guide registration
Creators
Travel agents & advisors
"""

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

    path(
        "destination/<slug:slug>/delete/",
        DestinationDeleteView.as_view(),
        name="destination-delete",
    ),
    path(
        "my-enquiry/", MyEnquiryView.as_view(), name="my-enquiry"
    ), 
    path("my-enquiry/<int:pk>/", BookingDetailView.as_view(), name="booking-detail"),

    path('help-center/', HelpCenterView.as_view(), name='help_center'),
    path('become-a-guide/', BecomeAGuideView.as_view(), name='become_a_guide'),
    path('travel-guide/', TravelGuideView.as_view(), name='travel_guide'),
    path('guide-of-the-year/', GuideOfTheYearView.as_view(), name='guide_of_the_year'),
    path('guide-registration/', GuideRegistrationView.as_view(), name='guide_registration'),
    path('creators/', CreatorsView.as_view(), name='creators'),
    path('travel-agents/', TravelAgentsAdvisorsView.as_view(), name='travel_agents'),
]
