from django.db import models
from django.utils.text import slugify
import uuid
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()

# Tag Model
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# Destination Model
class Destination(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='destinations')  # ManyToMany relation
    slug = models.SlugField(unique=True, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    accommodation = models.CharField(max_length=200, blank=True, null=True)
    best_season = models.CharField(max_length=200, blank=True, null=True)
    duration_days = models.IntegerField(blank=True, null=True)
    elevation = models.CharField(max_length=100, blank=True, null=True)
    tour_types = models.CharField(max_length=200, blank=True, null=True)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def included_cost_items(self):
        return self.cost_items.filter(is_included=True)

    @property
    def excluded_cost_items(self):
        return self.cost_items.filter(is_included=False)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) + '-' + str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)
# Itinerary Model
class Itinerary(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=True, blank=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='itineraries')
    day = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return f"Day {self.day} - {self.title}"


# Cost Include/Exclude Model
class CostIncludeExclude(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='cost_items')
    is_included = models.BooleanField(default=True)
    item = models.CharField(max_length=255)

    def __str__(self):
        return f"{'Included' if self.is_included else 'Excluded'}: {self.item}"


# FAQ Model
class FAQ(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question


# Related Trip Model
class RelatedTrip(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='related_trips')
    name = models.CharField(max_length=200)
    image = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Tour Map Model
class TourMap(models.Model):
    destination = models.OneToOneField(Destination, on_delete=models.CASCADE, related_name='tour_map')
    map_link = models.URLField(null=True, blank=True)  # e.g., Google Maps embed URL

    def __str__(self):
        return f"Map for {self.destination.name}"


# Enquiry Form Submission
class Enquiry(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    Country = models.CharField(max_length=100, blank=True, null=True)
    NoofAdults = models.IntegerField(blank=True, null=True)
    NoofChildren = models.IntegerField(blank=True, null=True)
    EnquirySubject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Enquiry from {self.name}"
    

class TopDestination(models.Model):
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0, blank=True)
    label = models.CharField(max_length=50, blank=True, help_text="e.g., Best Seller, Popular")

    class Meta:
        ordering = ['order']
        verbose_name = 'Top Destination'
        verbose_name_plural = 'Top Destinations'

    def __str__(self):
        return f"{self.destination.name} - {self.label or 'Featured'}"

