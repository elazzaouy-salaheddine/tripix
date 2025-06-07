from django.db import models
from django.utils import timezone
from django.core.validators import validate_email
from django.contrib.auth import get_user_model

User = get_user_model()

# 1. Subscriber Model
class Subscriber(models.Model):
    email = models.EmailField(unique=True, validators=[validate_email])
    name = models.CharField(max_length=150, blank=True, null=True)
    subscribed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


# 2. Tag / Category for Subscribers
class SubscriberTag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# 3. Subscriber Group / List
class SubscriberList(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    subscribers = models.ManyToManyField(Subscriber, related_name='lists')
    tags = models.ManyToManyField(SubscriberTag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# 4. Email Template
class EmailTemplate(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=255)
    html_content = models.TextField(help_text="Use template variables like {{ unsubscribe_link }}")
    plain_text_content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# 5. Email Campaign
class EmailCampaign(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    )

    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=255)
    html_content = models.TextField(blank=True, null=True)
    plain_text_content = models.TextField(blank=True, null=True)
    from_email = models.EmailField()
    from_name = models.CharField(max_length=100, blank=True, null=True)
    subscriber_lists = models.ManyToManyField(SubscriberList)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    scheduled_time = models.DateTimeField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# 6. Campaign Open Tracking
class CampaignOpen(models.Model):
    campaign = models.ForeignKey(EmailCampaign, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    opened_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.subscriber.email} - {self.campaign.name}"


# 7. Link Click Tracking
class CampaignLinkClick(models.Model):
    campaign = models.ForeignKey(EmailCampaign, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    link = models.URLField()
    clicked_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.subscriber.email} - {self.link}"


# 8. Unsubscribe
class Unsubscribe(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    campaign = models.ForeignKey(EmailCampaign, on_delete=models.SET_NULL, blank=True, null=True)
    unsubscribed_at = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.subscriber.email} unsubscribed"