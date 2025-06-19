# urls.py
from django.urls import path
from .views import ProfileDetailView, ProfileUpdateView

urlpatterns = [
    path('<slug:slug>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('<slug:slug>/edit/', ProfileUpdateView.as_view(), name='profile-edit'),
]
