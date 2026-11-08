# Create your models here.

from django.conf import settings
from django.db import models


class Registration(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='registrations'
    )

    event = models.ForeignKey(
        'events.Event',
        on_delete=models.PROTECT,
        related_name='registrations'
    )

    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'event'],
                name='unique_student_event'
            )
        ]

    def __str__(self):
        return f'{self.student} - {self.event}'
