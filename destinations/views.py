# core/views.py

from django.views.generic import ListView, DetailView
from .models import Destination
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import EnquiryForm


class DestinationListView(ListView):
    model = Destination
    template_name = 'destinations/destinations_list.html'
    context_object_name = 'destinations'
    paginate_by = 9  # Optional pagination

    def get_queryset(self):
        # Always order by a field to ensure consistent pagination
        return Destination.objects.order_by('-updated_at')  # or '-created_at', etc.
    

class DestinationDetailView(DetailView):
    model = Destination
    template_name = 'destinations/destination_details.html'
    context_object_name = 'destination'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get current destination
        destination = self.object

        # Add related trips (excluding itself if needed)
        context['related_trips'] = destination.related_trips.all()[:4]

        # Optionally fetch other related data if not accessed via reverse relations
        # e.g. destination.itineraries.all(), destination.cost_items.all(), etc.
        return context

def enquiry_form(request):
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you')  # Create a thank you page
    else:
        destination_id = request.GET.get('destination')
        form = EnquiryForm(initial={'destination': destination_id})

    return render(request, 'destinations/enquiry_form.html', {'form': form})


def thank_you(request):
    return render(request, 'destinations/thank_you.html')