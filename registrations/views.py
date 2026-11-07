
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from events.models import Event
from .models import Registration


@login_required
def registration_history(request):
    """แสดงประวัติการสมัครกิจกรรมของผู้ใช้ที่ login อยู่"""
    registrations = (
        Registration.objects
        .filter(student=request.user)
        .select_related('event')
        .order_by('-registered_at')
    )

    return render(
        request,
        'registrations/registration_history.html',
        {'registrations': registrations},
    )


@login_required
@require_POST
def registration_apply(request, event_id):
    """บันทึกการสมัครกิจกรรมและส่งผู้สมัครไป Google Forms"""

    event = get_object_or_404(Event, pk=event_id)

    # ตรวจสอบว่ากิจกรรมยังเปิดรับสมัคร
    if event.status != Event.Status.OPEN:
        messages.error(request, 'กิจกรรมนี้ปิดรับสมัครแล้ว')
        return redirect(
            'events:browse_event_detail',
            event_id=event.id
        )

    # ตรวจสอบวันปิดรับสมัคร
    if timezone.now() > event.registration_deadline:
        messages.error(request, 'กิจกรรมนี้หมดเขตรับสมัครแล้ว')
        return redirect(
            'events:browse_event_detail',
            event_id=event.id
        )

    # ตรวจสอบการสมัครซ้ำ
    if Registration.objects.filter(
        student=request.user,
        event=event
    ).exists():
        messages.warning(request, 'คุณสมัครกิจกรรมนี้แล้ว')
        return redirect(
            'events:browse_event_detail',
            event_id=event.id
        )

    # บันทึกข้อมูลการสมัคร
    try:
        with transaction.atomic():
            Registration.objects.create(
                student=request.user,
                event=event
            )
    except IntegrityError:
        messages.warning(request, 'คุณสมัครกิจกรรมนี้แล้ว')
        return redirect(
            'events:browse_event_detail',
            event_id=event.id
        )

    messages.success(request, 'บันทึกการสมัครเรียบร้อยแล้ว')

    # ส่งไปยัง Google Forms
    return redirect(event.google_form_url)

