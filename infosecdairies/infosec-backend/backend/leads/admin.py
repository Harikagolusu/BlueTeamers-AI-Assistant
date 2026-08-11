from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'course_name', 'country', 'city', 'status', 'user_link', 'created_at']
    list_filter = ['status', 'course_name', 'created_at']
    search_fields = ['name', 'email', 'phone', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'user']
    list_editable = ['status']

    @admin.display(description='Registered User')
    def user_link(self, obj):
        if obj.user:
            return obj.user.email
        return '—'
