from django.contrib import admin
from .models import Destination, Tag, Itinerary, CostIncludeExclude, FAQ, RelatedTrip, TourMap, Enquiry, TopDestination
from django.utils.html import format_html


class ItineraryInline(admin.TabularInline):
    model = Itinerary
    extra = 1
    fields = ('day', 'title', 'description')


class CostIncludeExcludeInline(admin.TabularInline):
    model = CostIncludeExclude
    extra = 1
    fields = ('is_included', 'item')


class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1
    fields = ('question', 'answer')


class RelatedTripInline(admin.TabularInline):
    model = RelatedTrip
    extra = 1
    fields = ('name', 'image', 'description')


class TourMapInline(admin.StackedInline):
    model = TourMap
    can_delete = False
    verbose_name_plural = 'Tour Map'
    fields = ('map_link',)


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'duration_days', 'price')
    search_fields = ('name', 'location', 'overview')
    list_filter = ('tags', 'location', 'duration_days')
    prepopulated_fields = {'slug': ('name',)}  # only if you add a slug field
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" />'.format(obj.image.url))
        return "(No image)"

    image_preview.short_description = "Image Preview"
    fieldsets = (
        (None, {
            'fields': ('name', 'image', 'overview', 'slug')
        }),
        ('Details', {
            'fields': ('location', 'accommodation', 'best_season', 'duration_days', 'elevation', 'tour_types','old_price', 'price')
        }),
        ('Tags', {
            'fields': ('tags',)
        }),
    )

    inlines = [
        ItineraryInline,
        CostIncludeExcludeInline,
        FAQInline,
        RelatedTripInline,
        TourMapInline,
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'destination', 'created_at')
    list_filter = ('destination', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(TopDestination)
class TopDestinationAdmin(admin.ModelAdmin):
    list_display = ('destination', 'label', 'order')
    list_editable = ('label', 'order')
    search_fields = ('destination__name',)