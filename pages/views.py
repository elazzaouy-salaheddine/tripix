from django.views.generic import TemplateView
from blog.models import Post
from destinations.models import Destination, TopDestination
from meta.views import MetadataMixin
from .models import GuideOfTheYear, ContactInfo, PrivacyPolicy, TermsAndConditions, FAQ, AboutPage, TravelGuide
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import ContactForm
from django.shortcuts import get_object_or_404


class HomeView(TemplateView):
    template_name = 'pages/home.html'  # specifies the template to use
    
    # Optional: Add context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home Page'
        context['welcome_message'] = 'Welcome to our website!'
        context['latest_posts'] = Post.objects.filter(published=True).order_by('-created_at')[:3]
        context["awesome_tours"] = Destination.objects.filter(published=True).order_by('-created_at')[:5]
        context["top_destinations"] = TopDestination.objects.select_related('destination').all()
        return context


class AboutView(TemplateView):
    template_name = 'pages/about.html'

    meta = {
        'title': 'About Us - Okatrip Travel',
        'description': 'Learn more about our mission and values at Okatrip.',
        'og_description': 'Discover how Okatrip is making travel unforgettable.',
        'twitter_title': 'About | Okatrip',
        'keywords': ['travel', 'about us', 'Okatrip', 'tour guide'],
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Load the first AboutPage instance
        about_page = AboutPage.objects.first()
        if about_page:
            context['about_page'] = about_page
            context['travel_guides'] = about_page.travel_guides.all().order_by('order')
        else:
            context['about_page'] = None
            context['travel_guides'] = []

        context['title'] = 'About Us'
        context['description'] = 'Learn more about our company and mission.'
        return context

class ContactView(FormView):
    template_name = 'pages/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')  # Redirect to same page or another success page

    meta = {
        'title': 'Contact Us - Tripix Travel',
        'description': 'Learn more about our mission and values at Tripix.',
        'og_description': 'Discover how Tripix is making travel unforgettable.',
        'twitter_title': 'Contact | Tripix',
        'keywords': ['travel', 'contact us', 'Tripix', 'tour guide'],
    }

    def form_valid(self, form):
        form.save()  # Save the ContactMessage
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact Us'
        # Load dynamic contact data (assumes only one ContactInfo entry)
        try:
            contact_data = ContactInfo.objects.prefetch_related(
                'phone_numbers', 'emails', 'social_links'
            ).first()
        except ContactInfo.DoesNotExist:
            contact_data = None

        context['contact_data'] = contact_data
        return context

        

class ServicesView(TemplateView):
    template_name = 'pages/services.html'  # specifies the template to use
    meta = {
        'title': 'Our Services - Tripix Travel',
        'description': 'Explore the services we offer at Tripix.',
        'og_description': 'Discover the range of travel services provided by Tripix.',
        'twitter_title': 'Our Services | Tripix',
        'keywords': ['travel', 'services', 'Tripix', 'tour guide'],
    }
    # Optional: Add context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Our Services'
        context['services_list'] = ['Service 1', 'Service 2', 'Service 3']
        return context

class FaqView(TemplateView):
    template_name = 'pages/faq.html'  # specifies the template to use
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all active FAQs ordered by their specified order
        faqs = FAQ.objects.filter(is_active=True).order_by('order')
        
        # Get unique categories from active FAQs
        categories = FAQ.objects.filter(is_active=True).values_list(
            'category', flat=True
        ).distinct()
        
        # Split FAQs into two roughly equal lists for left and right columns
        faq_count = faqs.count()
        split_index = (faq_count + 1) // 2  # Round up for odd numbers
        
        context.update({
            'title': 'Frequently Asked Questions',
            'meta_title': 'FAQ - Tripix Travel',
            'meta_description': 'Find answers to common questions about our travel services',
            'og_description': 'Get help with your travel plans with our comprehensive FAQ',
            'twitter_title': 'FAQ | Tripix Travel',
            'keywords': ['travel FAQ', 'Tripix questions', 'tour information'],
            'faqs_left': faqs[:split_index],
            'faqs_right': faqs[split_index:],
            'categories': categories,
        })
        return context


class TermsView(TemplateView):
    template_name = 'pages/terms.html'  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        terms = get_object_or_404(TermsAndConditions.objects.filter(is_active=True))
        
        context.update({
            'title': terms.title,
            'page': terms,
            'meta_title': terms.meta_title or terms.title,
            'meta_description': terms.meta_description,
            'og_description': terms.og_description,
            'twitter_title': terms.twitter_title,
            'keywords': terms.keywords,
        })
        return context

class PrivacyView(TemplateView):
    template_name = 'pages/privacy.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        privacy_policy = get_object_or_404(PrivacyPolicy.objects.filter(is_active=True))
        
        context.update({
            'title': privacy_policy.title,
            'page': privacy_policy,
            'meta_title': privacy_policy.meta_title or privacy_policy.title,
            'meta_description': privacy_policy.meta_description,
            'og_description': privacy_policy.og_description,
            'twitter_title': privacy_policy.twitter_title,
            'keywords': privacy_policy.keywords,
        })
        return context
class HelpCenterView(TemplateView):
    template_name = "pages/help_center.html"
    meta = {
        'title': 'About Us - Tripix Travel',
        'description': 'Learn more about our mission and values at Tripix.',
        'og_description': 'Discover how Tripix is making travel unforgettable.',
        'twitter_title': 'About | Tripix',
        'keywords': ['travel', 'about us', 'Tripix', 'tour guide'],
    }

class BecomeAGuideView(TemplateView):
    template_name = "pages/become_a_guide.html"
    meta = {
        'title': 'About Us - Tripix Travel',
        'description': 'Learn more about our mission and values at Tripix.',
        'og_description': 'Discover how Tripix is making travel unforgettable.',
        'twitter_title': 'About | Tripix',
        'keywords': ['travel', 'about us', 'Tripix', 'tour guide'],
    }



class TravelGuideView(TemplateView):
    template_name = "pages/travel_guide.html"
    meta = {
        'title': 'About Us - Tripix Travel',
        'description': 'Learn more about our mission and values at Tripix.',
        'og_description': 'Discover how Tripix is making travel unforgettable.',
        'twitter_title': 'About | Tripix',
        'keywords': ['travel', 'about us', 'Tripix', 'tour guide'],
    }
class GuideOfTheYearView(TemplateView):
    template_name = "pages/guide_of_the_year.html"
    meta = {
        'title': 'About Us - Tripix Travel',
        'description': 'Learn more about our mission and values at Tripix.',
        'og_description': 'Discover how Tripix is making travel unforgettable.',
        'twitter_title': 'About | Tripix',
        'keywords': ['travel', 'about us', 'Tripix', 'tour guide'],
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['guide_of_the_year'] = GuideOfTheYear.objects.all()
        return context
class GuideRegistrationView(TemplateView):
    template_name = "pages/guide_registration.html"
    meta = {
        'title': 'About Us - Tripix Travel',
        'description': 'Learn more about our mission and values at Tripix.',
        'og_description': 'Discover how Tripix is making travel unforgettable.',
        'twitter_title': 'About | Tripix',
        'keywords': ['travel', 'about us', 'Tripix', 'tour guide'],
    }
class CreatorsView(TemplateView):
    template_name = "pages/creators.html"
    meta = {
        'title': 'About Us - Tripix Travel',
        'description': 'Learn more about our mission and values at Tripix.',
        'og_description': 'Discover how Tripix is making travel unforgettable.',
        'twitter_title': 'About | Tripix',
        'keywords': ['travel', 'about us', 'Tripix', 'tour guide'],
    }
class TravelAgentsAdvisorsView(TemplateView):
    template_name = "pages/travel_agents.html"
    meta = {
        'title': 'About Us - Tripix Travel',
        'description': 'Learn more about our mission and values at Tripix.',
        'og_description': 'Discover how Tripix is making travel unforgettable.',
        'twitter_title': 'About | Tripix',
        'keywords': ['travel', 'about us', 'Tripix', 'tour guide'],
    }