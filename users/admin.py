from django.contrib import admin
from .models import Profile
from django.utils.html import format_html

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_full_name', 'avatar')
    search_fields = ('user__username', 'user__first_name', 'user__email')

    def user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;">', obj.avatar.url)
        return "–"
    
    user_full_name.short_description = 'Full Name'
    avatar_preview.short_description = 'Avatar Preview'