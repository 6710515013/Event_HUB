
from django import forms
from .models import Event
from datetime import timedelta
from django.utils import timezone


class EventForm(forms.ModelForm):

    class Meta:
        model = Event

        fields = [
            "organization_name",
            "poster",
            "title",
            "description",
            "categories",
            "start_datetime",
            "end_datetime",
            "registration_deadline",
            "location",
            "max_participants",
            "status",
            "google_form_url",
        ]

        labels = {
            "organization_name": "ชื่อชมรม / หน่วยงาน",
            "poster": "โปสเตอร์กิจกรรม",
            "title": "ชื่อกิจกรรม",
            "description": "รายละเอียดกิจกรรม",
            "categories": "หมวดหมู่กิจกรรม",
            "start_datetime": "วันและเวลาเริ่มกิจกรรม",
            "end_datetime": "วันและเวลาสิ้นสุดกิจกรรม",
            "registration_deadline": "วันและเวลาปิดรับสมัคร",
            "location": "สถานที่จัดกิจกรรม",
            "max_participants": "จำนวนผู้เข้าร่วมสูงสุด",
            "status": "สถานะกิจกรรม",
            "google_form_url": "ลิงก์ Google Forms สำหรับลงทะเบียน",
        }

        widgets = {
            "organization_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "title": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4
                }
            ),

            "categories": forms.CheckboxSelectMultiple(),

            "start_datetime": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local"
                },
                format="%Y-%m-%dT%H:%M"
            ),

            "end_datetime": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local"
                },
                format="%Y-%m-%dT%H:%M"
            ),

            "registration_deadline": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local"
                },
                format="%Y-%m-%dT%H:%M"
            ),

            "location": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "max_participants": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1
                }
            ),

            "status": forms.Select(
                attrs={"class": "form-select"}
            ),

            "google_form_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://forms.google.com/..."
                }
            ),
        }

    def clean_poster(self):
        poster = self.cleaned_data.get("poster")

        if poster and poster.size > 5 * 1024 * 1024:
            raise forms.ValidationError(
                "ขนาดไฟล์โปสเตอร์ต้องไม่เกิน 5 MB"
            )

        return poster

    def clean(self):
        cleaned_data = super().clean()

        registration_deadline = cleaned_data.get("registration_deadline")

        # ตรวจสอบเฉพาะตอนสร้างกิจกรรมใหม่
        if self.instance._state.adding:
            if registration_deadline:
                minimum_deadline = timezone.now() + timedelta(hours=24)

                if registration_deadline < minimum_deadline:
                    self.add_error(
                        "registration_deadline",
                        "ต้องกำหนดวันปิดรับสมัครล่วงหน้าจากเวลาสร้างกิจกรรมอย่างน้อย 24 ชั่วโมง"
                    )

        return cleaned_data