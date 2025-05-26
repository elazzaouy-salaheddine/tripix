# signals.py

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import GalleryImage

@receiver(pre_save, sender=GalleryImage)
def limit_gallery_images(sender, instance, **kwargs):
    destination = instance.destination
    if not instance.pk:  # Only check on creation, not update
        if destination.gallery_images.count() >= 10:
            raise ValidationError("Cannot upload more than 10 images per destination.")