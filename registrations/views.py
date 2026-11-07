from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.db import DatabaseError
from events.models import Event
from .models import Registration

@login_required(login_url="login")
@require_POST
def registration_apply(request, event_id):

    if request.user.role != "STUDENT":
        return redirect("events:browse_event_list")

    event = get_object_or_404(Event, pk=event_id)

    if event.status != Event.Status.OPEN:
        messages.error(request, "กิจกรรมนี้ปิดรับสมัครแล้ว")
        return redirect(
            "events:browse_event_detail",
            event_id=event.id
        )

    if timezone.now() > event.registration_deadline:
        messages.error(request, "กิจกรรมนี้หมดเขตรับสมัครแล้ว")
        return redirect(
            "events:browse_event_detail",
            event_id=event.id
        )

    if Registration.objects.filter(
        student=request.user,
        event=event
    ).exists():
        messages.warning(request, "คุณสมัครกิจกรรมนี้แล้ว")
        return redirect(
            "events:browse_event_detail",
            event_id=event.id
        )

    Registration.objects.create(
        student=request.user,
        event=event
    )

    messages.success(request, "บันทึกการสมัครเรียบร้อยแล้ว")

    return redirect(event.google_form_url)

#--------ประวัติการกดสมัครกิจกรรม---------

@login_required  # ต้อง login ก่อน
def registration_history(request):
    """แสดงประวัติการสมัครกิจกรรมของผู้ใช้ที่ login อยู่ (เห็นเฉพาะของตัวเอง)"""
    try:
        registrations = list(
            Registration.objects
            .filter(student=request.user)   # เฉพาะของผู้ใช้คนนี้
            .select_related('event')        # ดึง event มาพร้อมกัน (ใช้แสดงชื่อกิจกรรม)
            .order_by('-registered_at')     # สมัครล่าสุดขึ้นก่อน
        )
    except DatabaseError:
        # ตารางยังไม่ถูกสร้าง (ยังไม่ migrate) -> แสดงว่าไม่มีข้อมูล หน้าไม่พัง
        registrations = []

    return render(
        request,
        'registrations/registration_history.html',
        {'registrations': registrations},
    )