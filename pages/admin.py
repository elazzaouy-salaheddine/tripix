from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'subject', 'created_at')
    search_fields = ('name', 'phone_number', 'email', 'subject')
    readonly_fields = ('created_at',)