import uuid

from django.conf import settings
from django.db import models

from apps.courses.models import Course


class Certificate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='earned_certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='issued_certificates')
    certificate_id = models.CharField(max_length=64, unique=True, editable=False)
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-issued_at']
        unique_together = ('user', 'course')

    def __str__(self):
        return f'{self.certificate_id} - {self.user.email}'

    def save(self, *args, **kwargs):
        if not self.certificate_id:
            self.certificate_id = f'BILOL-{uuid.uuid4().hex[:12].upper()}'
        super().save(*args, **kwargs)
