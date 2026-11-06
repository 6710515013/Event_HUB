
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone

from events.models import Event, Category
from registrations.models import Registration

from events.student_views import get_filtered_events

# หมวดหมู่กิจกรรมทั้ง 13 ประเภท
CATEGORY_NAMES = [
    "การศึกษา/อบรม",
    "เทคโนโลยี/ไอที/โปรแกรมมิ่ง",
    "กีฬา/การแข่งขัน",
    "ศิลปะวัฒนธรรม",
    "ดนตรี/ความบันเทิง",
    "จิตอาสาบำเพ็ญประโยชน์",
    "พบปะสร้างเครือข่าย",
    "ธุรกิจ/อาชีพ/หางาน",
    "ศาสนา/พัฒนาจิตใจ",
    "สิ่งแวดล้อม/อนุรักษ์ธรรมชาติ",
    "ท่องเที่ยว",
    "สุขภาพ/พัฒนาตนเอง",
    "เทศกาล",
]



@login_required(login_url="login")
def student_dashboard(request):

    # ตรวจสอบสิทธิ์ Student
    if request.user.role != "STUDENT":
        return HttpResponseForbidden(
            "You do not have permission to access this page."
        )

    now = timezone.now()

    # รับค่าจากช่องค้นหาและตัวกรอง
    search_query = request.GET.get("q", "").strip()
    selected_date = request.GET.get("date", "").strip()
    selected_categories = request.GET.getlist("category")

    # ใช้ระบบ Search และ Date Filter ของ Person 3
    events = get_filtered_events(request)

    # เพิ่มข้อมูลจำนวนผู้ลงทะเบียนและ Category
    events = events.prefetch_related(
        "categories"
    ).annotate(
        registration_count=Count("registrations", distinct=True)
    )

    # กรองตามประเภทกิจกรรมที่เลือกหลายประเภท
    if selected_categories:
        events = events.filter(
            categories__id__in=selected_categories
        ).distinct()

    # เรียงกิจกรรมตามวันที่สร้างล่าสุด
    events = events.order_by("-created_at")

    # ดึงเฉพาะ 13 หมวดหมู่ที่กำหนดสำหรับ Dropdown
    categories = Category.objects.filter(
        name__in=CATEGORY_NAMES
    ).order_by("id")

    # ประวัติการลงทะเบียนของ Student
    registrations = Registration.objects.filter(
        student=request.user
    ).select_related(
        "event"
    ).order_by("-registered_at")

    # เก็บ ID กิจกรรมที่ลงทะเบียนแล้ว
    registered_event_ids = set(
        registrations.values_list("event_id", flat=True)
    )

    # กิจกรรมที่ Student ลงทะเบียนแล้ว
    my_activities = Event.objects.filter(
        registrations__student=request.user
    ).distinct().order_by("start_datetime")

    # กิจกรรมที่กำลังจะมาถึง
    upcoming_events = Event.objects.filter(
        start_datetime__gte=now
    ).order_by("start_datetime")

    # ส่งข้อมูลไปยัง Template
    context = {
        "user": request.user,
        "dashboard_role": "Student",

        # ข้อมูลกิจกรรมและตัวกรอง
        "events": events,
        "categories": categories,
        "search_query": search_query,
        "selected_date": selected_date,
        "selected_categories": selected_categories,

        # ข้อมูลการลงทะเบียน
        "my_activities": my_activities,
        "upcoming_events": upcoming_events,
        "registration_history": registrations,
        "registered_event_ids": registered_event_ids,

        "now": now,
    }

    return render(
        request,
        "dashboard/student_dashboard.html",
        context
    )


@login_required(login_url="login")
def organizer_dashboard(request):

    # ตรวจสอบสิทธิ์ Organizer
    if request.user.role != "ORGANIZER":
        return HttpResponseForbidden(
            "You do not have permission to access this page."
        )

    now = timezone.now()

    # กิจกรรมที่ Organizer คนนี้เป็นผู้สร้าง
    my_events = Event.objects.filter(
        created_by=request.user
    ).annotate(
        registration_count=Count("registrations", distinct=True)
    ).order_by("-created_at")

    # กิจกรรมที่กำลังจะมาถึง
    upcoming_events = my_events.filter(
        start_datetime__gte=now
    ).order_by("start_datetime")

    context = {
        "user": request.user,
        "dashboard_role": "Organizer",
        "total_events": my_events.count(),
        "my_events": my_events,
        "upcoming_events": upcoming_events,
    }

    return render(
        request,
        "dashboard/organizer_dashboard.html",
        context
    )