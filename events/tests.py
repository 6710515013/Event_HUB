from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import EventForm
from .models import Event

User = get_user_model()


def make_event(organizer, **overrides):
    now = timezone.now()
    data = {
        "created_by": organizer,
        "organization_name": "ชุมนุมทดสอบ",
        "title": "กิจกรรมทดสอบ",
        "description": "รายละเอียด",
        "start_datetime": now + timedelta(days=5),
        "end_datetime": now + timedelta(days=5, hours=3),
        "registration_deadline": now + timedelta(days=3),
        "location": "อาคารเรียนรวม",
        "max_participants": 30,
        "status": Event.Status.OPEN,
        "google_form_url": "https://forms.google.com/test",
    }
    data.update(overrides)
    return Event.objects.create(**data)


def form_data(**overrides):
    """ข้อมูลฟอร์มสร้างกิจกรรมที่ถูกต้อง"""
    now = timezone.localtime()
    data = {
        "organization_name": "ชุมนุมทดสอบ",
        "title": "กิจกรรมใหม่",
        "description": "รายละเอียด",
        "start_datetime": (now + timedelta(days=5)).strftime("%Y-%m-%dT%H:%M"),
        "end_datetime": (now + timedelta(days=5, hours=3)).strftime("%Y-%m-%dT%H:%M"),
        "registration_deadline": (now + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M"),
        "location": "อาคารเรียนรวม",
        "max_participants": 30,
        "status": "OPEN",
        "google_form_url": "https://forms.google.com/test",
    }
    data.update(overrides)
    return data


class EventModelTests(TestCase):

    def setUp(self):
        self.organizer = User.objects.create_user(
            username="org", email="org@example.com", password="pw12345678", role="ORGANIZER"
        )

    def test_end_before_start_is_invalid(self):
        event = make_event(self.organizer)
        event.end_datetime = event.start_datetime - timedelta(hours=1)
        with self.assertRaises(ValidationError):
            event.full_clean()

    def test_deadline_too_close_to_start_is_invalid(self):
        event = make_event(self.organizer)
        event.registration_deadline = event.start_datetime - timedelta(hours=2)
        with self.assertRaises(ValidationError):
            event.full_clean()

    def test_str_returns_title(self):
        self.assertEqual(str(make_event(self.organizer)), "กิจกรรมทดสอบ")


class EventFormTests(TestCase):

    def test_valid_form(self):
        self.assertTrue(EventForm(data=form_data()).is_valid())

    def test_deadline_less_than_24_hours_from_now_is_invalid(self):
        soon = (timezone.localtime() + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M")
        form = EventForm(data=form_data(registration_deadline=soon))
        self.assertFalse(form.is_valid())
        self.assertIn("registration_deadline", form.errors)


class OrganizerEventViewTests(TestCase):

    def setUp(self):
        self.organizer = User.objects.create_user(
            username="org", email="org@example.com", password="pw12345678", role="ORGANIZER"
        )
        self.other_organizer = User.objects.create_user(
            username="org2", email="org2@example.com", password="pw12345678", role="ORGANIZER"
        )
        self.student = User.objects.create_user(
            username="stu", email="stu@example.com", password="pw12345678", role="STUDENT"
        )
        self.event = make_event(self.organizer)

    def test_student_cannot_open_create_page(self):
        self.client.login(username="stu", password="pw12345678")
        self.assertEqual(self.client.get(reverse("events:event_create")).status_code, 403)

    def test_organizer_can_create_event(self):
        self.client.login(username="org", password="pw12345678")
        self.assertEqual(self.client.get(reverse("events:event_create")).status_code, 200)
        response = self.client.post(reverse("events:event_create"), form_data())
        self.assertRedirects(response, reverse("dashboard:organizer_dashboard"))
        created = Event.objects.get(title="กิจกรรมใหม่")
        self.assertEqual(created.created_by, self.organizer)

    def test_invalid_create_stays_on_form(self):
        self.client.login(username="org", password="pw12345678")
        response = self.client.post(reverse("events:event_create"), form_data(title=""))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Event.objects.filter(title="").exists())

    def test_event_list_shows_only_own_events(self):
        make_event(self.other_organizer, title="ของคนอื่น")
        self.client.login(username="org", password="pw12345678")
        response = self.client.get(reverse("events:event_list"))
        self.assertContains(response, "กิจกรรมทดสอบ")
        self.assertNotContains(response, "ของคนอื่น")

    def test_student_cannot_open_event_list(self):
        self.client.login(username="stu", password="pw12345678")
        self.assertEqual(self.client.get(reverse("events:event_list")).status_code, 403)

    def test_organizer_can_edit_own_event(self):
        self.client.login(username="org", password="pw12345678")
        url = reverse("events:event_edit", args=[self.event.id])
        self.assertEqual(self.client.get(url).status_code, 200)
        response = self.client.post(url, form_data(title="ชื่อใหม่"))
        self.assertRedirects(response, reverse("events:event_list"))
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, "ชื่อใหม่")

    def test_cannot_edit_other_organizers_event(self):
        self.client.login(username="org2", password="pw12345678")
        response = self.client.get(reverse("events:event_edit", args=[self.event.id]))
        self.assertEqual(response.status_code, 404)

    def test_student_cannot_edit(self):
        self.client.login(username="stu", password="pw12345678")
        response = self.client.get(reverse("events:event_edit", args=[self.event.id]))
        self.assertEqual(response.status_code, 403)

    def test_organizer_can_delete_own_event(self):
        self.client.login(username="org", password="pw12345678")
        url = reverse("events:event_delete", args=[self.event.id])
        self.assertEqual(self.client.get(url).status_code, 200)
        response = self.client.post(url)
        self.assertRedirects(response, reverse("events:event_list"))
        self.assertFalse(Event.objects.filter(pk=self.event.id).exists())

    def test_student_cannot_delete(self):
        self.client.login(username="stu", password="pw12345678")
        response = self.client.post(reverse("events:event_delete", args=[self.event.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Event.objects.filter(pk=self.event.id).exists())


class StudentBrowseTests(TestCase):

    def setUp(self):
        self.organizer = User.objects.create_user(
            username="org", email="org@example.com", password="pw12345678", role="ORGANIZER"
        )
        User.objects.create_user(
            username="stu", email="stu@example.com", password="pw12345678", role="STUDENT"
        )
        self.open_event = make_event(self.organizer, title="Workshop Python")
        self.closed_event = make_event(self.organizer, title="ปิดแล้ว", status=Event.Status.CLOSED)
        self.client.login(username="stu", password="pw12345678")

    def test_browse_shows_only_open_events(self):
        response = self.client.get(reverse("events:browse_event_list"))
        self.assertContains(response, "Workshop Python")
        self.assertNotContains(response, "ปิดแล้ว")

    def test_search_by_title(self):
        response = self.client.get(reverse("events:browse_event_list"), {"q": "python"})
        self.assertContains(response, "Workshop Python")

    def test_search_no_result(self):
        response = self.client.get(reverse("events:browse_event_list"), {"q": "ไม่มีจริง"})
        self.assertNotContains(response, "Workshop Python")

    def test_filter_by_date(self):
        date = timezone.localtime(self.open_event.start_datetime).date().isoformat()
        response = self.client.get(reverse("events:browse_event_list"), {"date": date})
        self.assertContains(response, "Workshop Python")

    def test_detail_page(self):
        response = self.client.get(reverse("events:browse_event_detail", args=[self.open_event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["can_register"])

    def test_detail_closed_event_cannot_register(self):
        response = self.client.get(reverse("events:browse_event_detail", args=[self.closed_event.id]))
        self.assertFalse(response.context["can_register"])

    def test_detail_unknown_event_returns_404(self):
        response = self.client.get(reverse("events:browse_event_detail", args=[9999]))
        self.assertEqual(response.status_code, 404)