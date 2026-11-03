
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        ORGANIZER = "ORGANIZER", "Organizer"
        ADMIN = "ADMIN", "Admin"

    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.STUDENT
    )

    student_id = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username
