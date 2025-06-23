# blog/urls.py

from django.urls import path
from .views import (

    PostListView, PostDetailView, 
    PostsByCategoryView, PostsByTagView, 
    AuthorListView, AuthorDetailView, PostSearchView
) 

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('search/', PostSearchView.as_view(), name='post-search'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('category/<slug:slug>/', PostsByCategoryView.as_view(), name='posts-by-category'),
    path('tag/<slug:slug>/', PostsByTagView.as_view(), name='posts-by-tag'),
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('authors/<slug:slug>/', AuthorDetailView.as_view(), name='author-detail'),

]