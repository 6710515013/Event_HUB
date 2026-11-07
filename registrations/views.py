from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from events.models import Event
from .models import Registration


@login_required  # ต้อง login ก่อน ไม่งั้นเด้งไปหน้า login
def registration_history(request):
    """แสดงประวัติการสมัครกิจกรรมของผู้ใช้ที่ login อยู่ (เห็นเฉพาะของตัวเอง)"""
    registrations = (
        Registration.objects
        .filter(student=request.user)   # กรองเฉพาะของผู้ใช้คนนี้ ไม่ให้เห็นของคนอื่น
        .select_related('event')        # ดึง event มาพร้อมกัน ลดจำนวน query
        .order_by('-registered_at')     # สมัครล่าสุดขึ้นก่อน
    )
    return render(
        request,
        'registrations/registration_history.html',  # ต้องตรงกับ path ของ template จริง
        {'registrations': registrations},
    )

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