from django.conf import settings
from django.db import models


class Certificate(models.Model):
    cert_id = models.CharField(max_length=50, unique=True, primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='certificates',
    )
    student_name = models.CharField(max_length=255)
    course_name = models.CharField(max_length=255)
    course_slug = models.CharField(max_length=200, blank=True, db_index=True)
    issue_date = models.CharField(max_length=50)
    image_url = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'certificates'

    def __str__(self):
        return f"{self.student_name} - {self.cert_id}"
