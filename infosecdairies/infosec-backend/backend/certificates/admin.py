from django.contrib import admin
from .models import Certificate

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('cert_id', 'student_name', 'course_name', 'issue_date')
    search_fields = ('cert_id', 'student_name')
    list_filter = ('course_name', 'issue_date')
