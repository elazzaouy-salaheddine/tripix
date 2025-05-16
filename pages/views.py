from django.views.generic import TemplateView
from blog.models import Post
from destinations.models import Destination, TopDestination

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
    
    # Optional: Add context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'About Us'
        context['description'] = 'Learn more about our company and mission.'
        return context

class ContactView(TemplateView):
    template_name = 'pages/contact.html'  # specifies the template to use
    
    # Optional: Add context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact Us'
        context['contact_info'] = 'Feel free to reach out to us!'
        return context

class ServicesView(TemplateView):
    template_name = 'pages/services.html'  # specifies the template to use
    
    # Optional: Add context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Our Services'
        context['services_list'] = ['Service 1', 'Service 2', 'Service 3']
        return context

class FaqView(TemplateView):
    template_name = 'pages/faq.html'  # specifies the template to use
    
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
    
    # Optional: Add context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Terms and Conditions'
        context['terms'] = 'Please read our terms and conditions carefully.'
        return context  
class PrivacyView(TemplateView):
    template_name = 'pages/privacy.html'  # specifies the template to use
    
    # Optional: Add context data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Privacy Policy'
        context['privacy_info'] = 'Your privacy is important to us.'
        return context