from django.views.generic import DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from django.urls import reverse_lazy
from .forms import ProfileForm  # You’ll create this next
from destinations.models import Destination
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'account/profile_detail.html'
    context_object_name = 'profile'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add destinations created by this profile's user
        context['destinations'] = Destination.objects.filter(created_by=self.object.user, published=True)
        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'account/profile_edit.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        # Limit editing to the logged-in user
        return Profile.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('profile-detail', kwargs={'slug': self.object.slug})
