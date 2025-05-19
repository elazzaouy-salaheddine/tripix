# views.py

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.urls import reverse_lazy
from destinations.models import (
    Destination,
    Itinerary,
    CostIncludeExclude,
    FAQ,
    RelatedTrip,
    TourMap,
)
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.exceptions import PermissionDenied
from destinations.models import Destination, Enquiry
from .forms import (
    DestinationForm,
    ItineraryForm,
    CostItemForm,
    FAQForm,
    RelatedTripForm,
    TourMapForm,
    ItineraryFormSet,
    CostItemFormSet,
    FAQFormSet,
    RelatedTripFormSet,
)


class OwnerRequiredMixin:
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.created_by != self.request.user:
            raise PermissionDenied(
                "You do not have permission to edit this destination."
            )
        return obj


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["user_destinations"] = Destination.objects.filter(
            created_by=self.request.user
        ).order_by("-created_at")

        return context


class DestinationDeleteView(OwnerRequiredMixin, DeleteView):
    model = Destination
    template_name = "dashboard/destination_confirm_delete.html"
    success_url = reverse_lazy("dashboard")


class MyEnquiryView(LoginRequiredMixin, ListView):
    model = Enquiry
    template_name = "dashboard/my_bookings.html"
    context_object_name = "bookings"

    def get_queryset(self):
        # Get all destinations created by the current user
        user_destinations = Destination.objects.filter(created_by=self.request.user)

        # Get all bookings/enquiries for those destinations
        return Enquiry.objects.filter(destination__in=user_destinations).select_related(
            "destination"
        )


class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Enquiry
    template_name = "dashboard/booking_detail.html"
    context_object_name = "booking"

    def get_queryset(self):
        # Get user's destinations
        user_destinations = Destination.objects.filter(created_by=self.request.user)
        return Enquiry.objects.filter(destination__in=user_destinations).select_related(
            "destination"
        )

    def get(self, request, *args, **kwargs):
        # Ensure the user owns the destination this booking belongs to
        self.object = self.get_object()
        if not self.object.destination.created_by == self.request.user:
            raise PermissionDenied("You do not have permission to view this booking.")
        return super().get(request, *args, **kwargs)
