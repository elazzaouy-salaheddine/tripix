from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField  # supports image upload
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.utils.text import slugify
import uuid

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
    

class Partner(models.Model):
    name = models.CharField(max_length=100, blank=True)
    logo = models.ImageField(upload_to='partners/logos/')
    website = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Order for display in the slider")

    class Meta:
        ordering = ['order']
        verbose_name = "Partner"
        verbose_name_plural = "Partners"

    def __str__(self):
        return self.name or "Partner #{}".format(self.id)



class PageBaseModel(models.Model):
    """Base model for all pages with common fields"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = RichTextField()
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=100, blank=True)
    meta_description = models.TextField(blank=True)
    og_description = models.TextField(blank=True)
    twitter_title = models.TextField(blank=True)
    keywords = models.TextField(blank=True)
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(f'page-{self.slug}')

class TermsAndConditions(PageBaseModel):
    """Terms and Conditions page model"""
    acceptance_required = models.BooleanField(
        default=False,
        help_text="Require users to accept these terms"
    )
    version = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Terms and Conditions"
        verbose_name_plural = "Terms and Conditions"

class PrivacyPolicy(PageBaseModel):
    """Privacy Policy page model"""
    version = models.CharField(max_length=20)
    data_controller = models.CharField(max_length=200, blank=True)
    contact_email = models.EmailField(blank=True)

    class Meta:
        verbose_name = "Privacy Policy"
        verbose_name_plural = "Privacy Policies"

class FAQ(PageBaseModel):
    """Frequently Asked Questions model"""
    category = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['order', 'title']

class AboutPage(PageBaseModel):
    """About Us page model"""
    team_photo = models.ImageField(
        upload_to='about/team/',
        blank=True,
        null=True
    )
    mission_statement = RichTextField(blank=True)
    values = RichTextField(blank=True)
    history = RichTextField(blank=True)

    class Meta:
        verbose_name = "About Page"
        verbose_name_plural = "About Pages"


class TravelGuide(models.Model):
    about_page = models.ForeignKey(
        'AboutPage',
        on_delete=models.CASCADE,
        related_name='travel_guides'
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='guides/', blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, help_text="e.g., Senior Desert Guide")
    bio = models.TextField(blank=True)
    expertise = models.CharField(max_length=255, blank=True, help_text="e.g., Sahara, Atlas Mountains")
    languages = models.CharField(max_length=255, blank=True, help_text="e.g., English, French, Arabic, Tamazight")
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Travel Guide"
        verbose_name_plural = "Travel Guides"

    def __str__(self):
        return self.name
