from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField  # supports image upload

# Create your models here.


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class ProjectLogo(models.Model):
    """
    Model to store different versions of project logos
    """
    name = models.CharField(max_length=100, help_text="Logo identifier (e.g., main, dark, icon)")
    logo = models.ImageField(
        upload_to='project/logos/',
        validators=[FileExtensionValidator(['png', 'svg', 'jpg', 'jpeg'])]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Project Logo"
        verbose_name_plural = "Project Logos"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} Logo"


class GuideOfTheYear(models.Model):
    guide = models.ForeignKey(User, on_delete=models.CASCADE, related_name='awards')
    year = models.PositiveIntegerField()
    title = models.CharField(max_length=255, default="Guide of the Year")
    description = RichTextUploadingField()
    photo = models.ImageField(upload_to='guide_awards/photos/', null=True, blank=True)
    date_awarded = models.DateField(auto_now_add=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ['-year']
        unique_together = ('guide', 'year')  # Prevent duplicates
        verbose_name = "Guide of the Year"
        verbose_name_plural = "Guides of the Year"

    def __str__(self):
        return f"{self.guide.get_full_name()} - {self.year}"


class ContactInfo(models.Model):
    subtitle = models.CharField(max_length=100, default="contact us")
    title = models.CharField(max_length=200, default="Get in touch with us")
    address = models.TextField()
    customer_service_title = models.CharField(max_length=100, default="Customer Service")
    careers_title = models.CharField(max_length=100, default="Careers")

    def __str__(self):
        return "Contact Info"

class PhoneNumber(models.Model):
    contact_info = models.ForeignKey(ContactInfo, on_delete=models.CASCADE, related_name='phone_numbers')
    number = models.CharField(max_length=20)

    def __str__(self):
        return self.number

class EmailAddress(models.Model):
    contact_info = models.ForeignKey(ContactInfo, on_delete=models.CASCADE, related_name='emails')
    email = models.EmailField()

    def __str__(self):
        return self.email

class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('x-twitter', 'X (Twitter)'),
        ('instagram', 'Instagram'),
        ('facebook', 'facebook'),
        ('linkedin', 'linkedin'),
        ('vimeo', 'Vimeo'),
        # Add more if needed
    ]

    contact_info = models.ForeignKey(ContactInfo, on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    url = models.URLField()

    def __str__(self):
        return f"{self.platform.title()} - {self.url}"
