
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Event(models.Model):

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        CLOSED = "CLOSED", "Closed"

    categories = models.ManyToManyField(
        Category,
        related_name="events",
        blank=True
    )

    # ผู้ใช้ที่สร้างกิจกรรม
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_events"
    )

    # ชื่อชมรมหรือองค์กร
    organization_name = models.CharField(max_length=150)

    # รูปโปสเตอร์กิจกรรม
    poster = models.ImageField(
        upload_to="event_posters/",
        blank=True,
        null=True
    )
    
    # ข้อมูลกิจกรรม
    title = models.CharField(max_length=200)
    description = models.TextField()

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    registration_deadline = models.DateTimeField()

    location = models.CharField(max_length=255)

    # จำนวนผู้เข้าร่วมสูงสุด
    max_participants = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    # สถานะการรับสมัคร
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.OPEN
    )

    # ลิงก์แบบฟอร์มสมัครภายนอก
    google_form_url = models.URLField()

    # วันเวลาที่สร้างและแก้ไขข้อมูล
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()

        if (
            self.start_datetime
            and self.end_datetime
            and self.end_datetime <= self.start_datetime
        ):
            raise ValidationError({
                "end_datetime": "End time must be later than start time."
            })

        if (
            self.registration_deadline
            and self.start_datetime
            and self.registration_deadline > self.start_datetime
        ):
            raise ValidationError({
                "registration_deadline":
                    "Registration deadline must not be later than event start time."
            })

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]