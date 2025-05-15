# core/urls.py

from django.urls import path
from .views import DestinationListView, DestinationDetailView, enquiry_form, thank_you

urlpatterns = [
    path('', DestinationListView.as_view(), name='destination-list'),
    #path('<slug:slug>/', DestinationDetailView.as_view(), name='destination-detail'),
    path('<int:pk>/', DestinationDetailView.as_view(), name='destination-detail'),
    path('enquiry/', enquiry_form, name='enquiry_form'),
    path('thank-you/', thank_you, name='thank_you'),

]