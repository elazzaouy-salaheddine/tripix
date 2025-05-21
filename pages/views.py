from django.views.generic import TemplateView
from blog.models import Post
from destinations.models import Destination, TopDestination
from meta.views import MetadataMixin



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
    template_name = 'pages/about.html'  # specifies the template to use
    meta = {
        'title': 'About Us - Tripix Travel',
        'description': 'Learn more about our mission and values at Tripix.',
        'og_description': 'Discover how Tripix is making travel unforgettable.',
        'twitter_title': 'About | Tripix',
        'keywords': ['travel', 'about us', 'Tripix', 'tour guide'],
    }
    # Optional: Add context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'About Us'
        context['description'] = 'Learn more about our company and mission.'
        return context

class ContactView(TemplateView):
    template_name = 'pages/contact.html'  # specifies the template to use
    meta = {
        'title': 'Contact Us - Tripix Travel',
        'description': 'Learn more about our mission and values at Tripix.',
        'og_description': 'Discover how Tripix is making travel unforgettable.',
        'twitter_title': 'Contact | Tripix',
        'keywords': ['travel', 'contact us', 'Tripix', 'tour guide'],
    }
    # Optional: Add context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact Us'
        context['contact_info'] = 'Feel free to reach out to us!'
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
    meta = {
        'title': 'FAQ Us - Tripix Travel',
        'description': 'Learn more about our mission and values at Tripix.',
        'og_description': 'Discover how Tripix is making travel unforgettable.',
        'twitter_title': 'FAQ | Tripix',
        'keywords': ['travel', 'FAQ', 'Tripix', 'tour guide'],
    }
    # Optional: Add context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Frequently Asked Questions'
        context['faq_list'] = [
            {'question': 'What is our return policy?', 'answer': 'You can return items within 30 days.'},
            {'question': 'How do I track my order?', 'answer': 'You will receive a tracking number via email.'},
        ]
        return context

class TermsView(TemplateView):
    template_name = 'pages/terms.html'  # specifies the template to use
    meta = {
        'title': 'About Us - Tripix Travel',
        'description': 'Learn more about our mission and values at Tripix.',
        'og_description': 'Discover how Tripix is making travel unforgettable.',
        'twitter_title': 'About | Tripix',
        'keywords': ['travel', 'about us', 'Tripix', 'tour guide'],
    }
    # Optional: Add context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Terms and Conditions'
        context['terms'] = 'Please read our terms and conditions carefully.'
        return context

class PrivacyView(TemplateView):
    template_name = 'pages/privacy.html'  # specifies the template to use
    meta = {
        'title': 'About Us - Tripix Travel',
        'description': 'Learn more about our mission and values at Tripix.',
        'og_description': 'Discover how Tripix is making travel unforgettable.',
        'twitter_title': 'About | Tripix',
        'keywords': ['travel', 'about us', 'Tripix', 'tour guide'],
    }
    # Optional: Add context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Privacy Policy'
        context['privacy_info'] = 'Your privacy is important to us.'
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