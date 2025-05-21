# forms.py

from django import forms
from .models import Enquiry

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = [
            'name', 'email', 'phone', 'Country', 
            'NoofAdults', 'NoofChildren', 'EnquirySubject', 
            'message', 'destination'
        ]
        widgets = {
            'destination': forms.HiddenInput(),
            'NoofAdults': forms.NumberInput(attrs={
                'min': 0,
                'placeholder': 'Enter number of adults'
            }),
            'NoofChildren': forms.NumberInput(attrs={
                'min': 0,
                'placeholder': 'Enter number of children'
            }),
            'EnquirySubject': forms.TextInput(attrs={
                'placeholder': 'Enter your enquiry subject'
            }),
            'Country': forms.TextInput(attrs={
                'placeholder': 'Enter your country of residence'
            }),
            'message': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Type your message here...'
            }),
        }
        labels = {
            'Country': 'Country of Residence',
            'NoofAdults': 'Number of Adults',
            'NoofChildren': 'Number of Children',
            'EnquirySubject': 'Enquiry Subject',
        }
        help_texts = {
            'phone': 'Include country code if international',
            'NoofChildren': 'Children under 12 years old',
        }