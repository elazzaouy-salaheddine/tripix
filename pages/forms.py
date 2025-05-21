# forms.py

from django import forms
from destinations.models import (
    Destination,
    Itinerary,
    CostIncludeExclude,
    FAQ,
    RelatedTrip,
    TourMap,

)
from pages.models import ContactMessage
from django.forms import inlineformset_factory


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = [
            "name",
            "image",
            "slug",
            "location",
            "accommodation",
            "best_season",
            "duration_days",
            "elevation",
            "tour_types",
            "old_price",
            "price",
            "overview",
            "published",
            "tags",
        ]


class ItineraryForm(forms.ModelForm):
    class Meta:
        model = Itinerary
        fields = ["day", "title", "description"]


class CostItemForm(forms.ModelForm):
    class Meta:
        model = CostIncludeExclude
        fields = ["is_included", "item"]


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ["question", "answer"]


class RelatedTripForm(forms.ModelForm):
    class Meta:
        model = RelatedTrip
        fields = ["name", "image", "description"]


class TourMapForm(forms.ModelForm):
    class Meta:
        model = TourMap
        fields = ["map_link"]


ItineraryFormSet = inlineformset_factory(
    Destination, Itinerary, form=ItineraryForm, extra=1, can_delete=True
)

CostItemFormSet = inlineformset_factory(
    Destination, CostIncludeExclude, form=CostItemForm, extra=1, can_delete=True
)

FAQFormSet = inlineformset_factory(
    Destination, FAQ, form=FAQForm, extra=1, can_delete=True
)

RelatedTripFormSet = inlineformset_factory(
    Destination, RelatedTrip, form=RelatedTripForm, extra=1, can_delete=True
)


class ContactForm(forms.ModelForm):

    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
