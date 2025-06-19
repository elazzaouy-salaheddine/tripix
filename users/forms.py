from django import forms
from .models import Profile
from allauth.account.forms import SignupForm


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar','organization_name']



class CustomSignupForm(SignupForm):
    organization_name = forms.CharField(max_length=255, required=False, label='Organization Name')

    def save(self, request):
        user = super().save(request)
        user.profile.organization_name = self.cleaned_data['organization_name']
        user.profile.save()
        return user
