from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from events.models import Event
from .models import Registration
from .services import RegistrationError, apply_for_event

User = get_user_model()


def make_event(organizer, **overrides):
    """สร้างกิจกรรมสำหรับทดสอบ ค่า default คือเปิดรับและยังไม่หมดเขต"""
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


class RegistrationServiceTests(TestCase):
    """ทดสอบ business logic ใน services.py โดยตรง"""

    def setUp(self):
        self.student = User.objects.create_user(
            username="stu", email="stu@example.com", password="pw12345678", role="STUDENT"
        )
        self.organizer = User.objects.create_user(
            username="org", email="org@example.com", password="pw12345678", role="ORGANIZER"
        )

    def test_apply_success_creates_registration(self):
        event = make_event(self.organizer)
        apply_for_event(self.student, event.id)
        self.assertTrue(Registration.objects.filter(student=self.student, event=event).exists())

    def test_apply_twice_is_rejected(self):
        event = make_event(self.organizer)
        apply_for_event(self.student, event.id)
        with self.assertRaises(RegistrationError):
            apply_for_event(self.student, event.id)
        self.assertEqual(Registration.objects.count(), 1)

    def test_apply_closed_event_is_rejected(self):
        event = make_event(self.organizer, status=Event.Status.CLOSED)
        with self.assertRaises(RegistrationError):
            apply_for_event(self.student, event.id)
        self.assertEqual(Registration.objects.count(), 0)

    def test_apply_after_deadline_is_rejected(self):
        event = make_event(self.organizer, registration_deadline=timezone.now() - timedelta(hours=1))
        with self.assertRaises(RegistrationError):
            apply_for_event(self.student, event.id)
        self.assertEqual(Registration.objects.count(), 0)


class RegistrationViewTests(TestCase):
    """ทดสอบหน้าเว็บ: สมัคร และประวัติการสมัคร"""

    def setUp(self):
        self.student = User.objects.create_user(
            username="stu", email="stu@example.com", password="pw12345678", role="STUDENT"
        )
        self.other = User.objects.create_user(
            username="stu2", email="stu2@example.com", password="pw12345678", role="STUDENT"
        )
        self.organizer = User.objects.create_user(
            username="org", email="org@example.com", password="pw12345678", role="ORGANIZER"
        )
        self.event = make_event(self.organizer)

    def test_apply_requires_login(self):
        response = self.client.post(reverse("registrations:apply", args=[self.event.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Registration.objects.count(), 0)

    def test_apply_rejects_get(self):
        self.client.login(username="stu", password="pw12345678")
        response = self.client.get(reverse("registrations:apply", args=[self.event.id]))
        self.assertEqual(response.status_code, 405)

    def test_student_apply_redirects_to_google_form(self):
        self.client.login(username="stu", password="pw12345678")
        response = self.client.post(reverse("registrations:apply", args=[self.event.id]))
        self.assertRedirects(response, self.event.google_form_url, fetch_redirect_response=False)
        self.assertEqual(Registration.objects.count(), 1)

    def test_apply_error_goes_back_to_detail(self):
        self.event.status = Event.Status.CLOSED
        self.event.save()
        self.client.login(username="stu", password="pw12345678")
        response = self.client.post(reverse("registrations:apply", args=[self.event.id]))
        self.assertRedirects(response, reverse("events:browse_event_detail", args=[self.event.id]))
        self.assertEqual(Registration.objects.count(), 0)

    def test_organizer_cannot_apply(self):
        self.client.login(username="org", password="pw12345678")
        self.client.post(reverse("registrations:apply", args=[self.event.id]))
        self.assertEqual(Registration.objects.count(), 0)

    def test_apply_unknown_event_returns_404(self):
        self.client.login(username="stu", password="pw12345678")
        response = self.client.post(reverse("registrations:apply", args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_history_shows_only_own_registrations(self):
        other_event = make_event(self.organizer, title="กิจกรรมของคนอื่น")
        Registration.objects.create(student=self.student, event=self.event)
        Registration.objects.create(student=self.other, event=other_event)
        self.client.login(username="stu", password="pw12345678")
        response = self.client.get(reverse("registrations:history"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "กิจกรรมทดสอบ")
        self.assertNotContains(response, "กิจกรรมของคนอื่น")