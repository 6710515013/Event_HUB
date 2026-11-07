from django.contrib.auth.decorators import login_required
from django.db import DatabaseError
from django.shortcuts import render

from .models import Registration


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