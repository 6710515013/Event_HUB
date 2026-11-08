from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404

from events.models import Event
from .models import Registration
from .services import RegistrationError, apply_for_event


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
    """รับคำขอสมัคร แล้วส่งให้ services.apply_for_event จัดการ logic"""

    if request.user.role != "STUDENT":
        return redirect("events:browse_event_list")

    event = get_object_or_404(Event, pk=event_id)

    try:
        apply_for_event(request.user, event.id)
    except RegistrationError as error:
        messages.error(request, str(error))
        return redirect("events:browse_event_detail", event_id=event.id)

    messages.success(request, "บันทึกการสมัครเรียบร้อยแล้ว")
    return redirect(event.google_form_url)