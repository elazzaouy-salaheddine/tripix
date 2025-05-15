# blog/templatetags/blog_extras.py

from django import template
from blog.models import Post

register = template.Library()

@register.inclusion_tag('pages/latest_posts.html')
def show_latest_posts(count=3):
    posts = Post.objects.filter(published=True).order_by('-created_at')[:count]
    return {'latest_posts': posts}