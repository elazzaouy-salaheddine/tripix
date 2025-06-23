from django.contrib import admin
from .models import (
    ContactMessage,
    ProjectLogo,
    GuideOfTheYear,
    ContactInfo,
    PhoneNumber,
    EmailAddress,
    SocialLink,
    Partner,
    TermsAndConditions,
    PrivacyPolicy,
    FAQ,
    AboutPage,
    TravelGuide,
)
from django.utils.html import format_html


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_number", "email", "subject", "created_at")
    search_fields = ("name", "phone_number", "email", "subject")
    readonly_fields = ("created_at",)


@admin.register(ProjectLogo)
class ProjectLogoAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(GuideOfTheYear)
class GuideOfTheYearAdmin(admin.ModelAdmin):
    list_display = ("guide", "year", "title", "is_featured", "date_awarded")
    list_filter = ("year", "is_featured")
    search_fields = (
        "guide__username",
        "guide__first_name",
        "guide__last_name",
        "title",
    )
    ordering = ("-year",)

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.photo.url,
            )
        return "-"

    photo_preview.short_description = "Photo"
    list_display = (
        "guide",
        "year",
        "title",
        "is_featured",
        "date_awarded",
        "photo_preview",
    )


class PhoneNumberInline(admin.TabularInline):
    model = PhoneNumber
    extra = 1


class EmailAddressInline(admin.TabularInline):
    model = EmailAddress
    extra = 1


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    inlines = [PhoneNumberInline, EmailAddressInline, SocialLinkInline]


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "website", "is_active", "order")
    list_editable = ("is_active", "order")


@admin.register(TermsAndConditions)
class TermsAdmin(admin.ModelAdmin):
    list_display = ('title', 'version', 'is_active', 'last_updated')
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('title',)}

@admin.register(PrivacyPolicy)
class PrivacyAdmin(admin.ModelAdmin):
    list_display = ('title', 'version', 'is_active', 'last_updated')
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('title',)}

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order', 'is_active')
    list_filter = ('category', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

class TravelGuideInline(admin.StackedInline):
    model = TravelGuide
    extra = 1
    fields = (
        'name', 'photo', 'title', 'bio',
        'expertise', 'languages',
        'facebook', 'instagram',
        'is_featured', 'order'
    )
    ordering = ('order',)
    show_change_link = True

@admin.register(AboutPage)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'last_updated')
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'is_active')
        }),
        ('Content', {
            'fields': ('content', 'mission_statement', 'values', 'history')
        }),
        ('Media', {
            'fields': ('team_photo',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        })
    )
    inlines = [TravelGuideInline]