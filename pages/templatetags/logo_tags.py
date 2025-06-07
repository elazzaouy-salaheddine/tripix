# core/templatetags/logo_tags.py
from django import template
from pages.models import ProjectLogo

register = template.Library()

@register.simple_tag
def get_logo(name):
    try:
        return ProjectLogo.objects.get(name=name, is_active=True).logo.url
    except ProjectLogo.DoesNotExist:
        return "/static/img/logo-v2.svg"  # Fallback logo