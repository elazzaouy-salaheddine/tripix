# email_marketing/forms.py
from django import forms
from django.core.validators import validate_email
from .models import Subscriber

class SubscribeForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Email Address'
        }),
        validators=[validate_email]
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        # Optional: Check if email already exists
        if Subscriber.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already subscribed.")
        return email