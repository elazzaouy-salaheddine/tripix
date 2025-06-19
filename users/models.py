from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    organization_name = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True) 
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def save(self, *args, **kwargs):
        if self.organization_name and not self.slug:
            base_slug = slugify(self.organization_name)
            slug = base_slug
            counter = 1
            while Profile.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)