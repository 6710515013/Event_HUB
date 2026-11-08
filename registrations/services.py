from django.db import transaction
from django.utils import timezone

from events.models import Event
from .models import Registration


class RegistrationError(Exception):
    """สมัครกิจกรรมไม่ได้ ข้อความใน error ใช้แสดงให้ผู้ใช้เห็นได้เลย"""


@transaction.atomic
def apply_for_event(student, event_id):
    """
    Business logic ของการสมัครกิจกรรม แยกออกจาก view

    - ล็อกแถวกิจกรรมไว้ระหว่างตรวจ (select_for_update) กันสองคำขอเข้ามาพร้อมกัน
    - ถ้าขั้นตอนไหนพัง transaction.atomic จะยกเลิกทั้งหมด ไม่มีข้อมูลครึ่งๆ กลางๆ
    """
    event = Event.objects.select_for_update().get(pk=event_id)

    if event.status != Event.Status.OPEN:
        raise RegistrationError("กิจกรรมนี้ปิดรับสมัครแล้ว")

    if timezone.now() > event.registration_deadline:
        raise RegistrationError("กิจกรรมนี้หมดเขตรับสมัครแล้ว")

    registration, created = Registration.objects.get_or_create(
        student=student,
        event=event,
    )
    if not created:
        raise RegistrationError("คุณสมัครกิจกรรมนี้แล้ว")

    return registration