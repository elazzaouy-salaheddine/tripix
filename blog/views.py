# blog/views.py

from django.views.generic import ListView, DetailView
from .models import Post, Category, Tag
from .forms import CommentForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils.text import slugify
from django.db import models

User = get_user_model()


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    #paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(published=True).order_by('-created_at')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_posts'] = Post.objects.filter(
            tags__in=self.object.tags.all()
        ).exclude(id=self.object.id).distinct()[:3]
        context['comments'] = self.object.comments.filter(approved=True)
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.approved = True  # wait for admin approval
            comment.save()
            return redirect('post-detail', slug=self.object.slug)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class PostsByCategoryView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    #paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(
            category__slug=self.kwargs['slug'],
            published=True
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Posts in Category: {Category.objects.get(slug=self.kwargs['slug']).name}"
        return context

class PostsByTagView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    #paginate_by = 6

    def get_queryset(self):
        return Post.objects.filter(
            tags__slug=self.kwargs['slug'],
            published=True
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Posts Tagged: {Tag.objects.get(slug=self.kwargs['slug']).name}"
        return context

# TODO: FIX THIS SEARCHE views
class PostSearchView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                models.Q(title__icontains=query) |
                models.Q(content__icontains=query) |
                models.Q(tags__name__icontains=query)
            ).distinct().order_by('-created_at')
        return Post.objects.none()  # Empty queryset if no query


class AuthorListView(ListView):
    model = User
    template_name = 'blog/author_list.html'
    context_object_name = 'authors'

    def get_queryset(self):
        # Only show users who have published at least one post
        return User.objects.filter(post__published=True).distinct()


class AuthorDetailView(DetailView):
    model = User
    template_name = 'blog/author_detail.html'
    context_object_name = 'author'
    slug_field = 'slug'  # Field to search against
    slug_url_kwarg = 'slug'  # URL parameter name

    def get_object(self, queryset=None):
        """
        Override to search by full name or username (slugified)
        """
        slug = self.kwargs.get(self.slug_url_kwarg)
        for user in User.objects.filter(post__published=True).distinct():
            if slugify(user.get_full_name()) == slug or slugify(user.username) == slug:
                return user
        return get_object_or_404(User, id=-1)  # Return 404 if not found
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author=self.object, published=True)
        return context