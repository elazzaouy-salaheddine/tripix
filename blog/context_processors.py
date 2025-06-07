from .models import Post, Category, Tag

def latest_posts(request):
    return {
        'latest_posts_sidebar': Post.objects.filter(published=True).order_by('-created_at')[:3]
    }


def category_list(request):
    categories = Category.objects.all()
    
    return {
        'categories': categories
    }

def tag_list(request):
    tags = Tag.objects.all()
    
    return {
        'tags': tags
    }
    