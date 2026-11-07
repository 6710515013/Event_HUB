from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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