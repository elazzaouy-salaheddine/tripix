# core/views.py

from django.views.generic import ListView, DetailView
from .models import Destination
from django.shortcuts import render, redirect
from django.views.generic.edit import FormMixin
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
    

class DestinationDetailView(FormMixin, DetailView):
    model = Destination
    template_name = 'destinations/destination_details.html'
    context_object_name = 'destination'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    form_class = EnquiryForm
    def get_success_url(self):
        return reverse('destination-list')

    def get_initial(self):
        initial = super().get_initial()
        initial['destination'] = self.object.id
        return initial

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.destination = self.object
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_trips'] = self.object.related_trips.all()[:4]
        context['form'] = self.get_form() 
        return context
    

def thank_you(request):
    return render(request, 'destinations/thank_you.html')