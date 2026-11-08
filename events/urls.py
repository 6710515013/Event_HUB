# นำเข้า path เพื่อใช้กำหนด URL ของแต่ละหน้า
from django.urls import path

# นำเข้า views ของ Organizer และ student_views ของ Student
from . import views, student_views

# กำหนดชื่อแอป เพื่อให้เรียก URL ผ่าน events: ได้
app_name = "events"

# กำหนด URL ทั้งหมดของแอป events
urlpatterns = [
    # ==============================
    # Organizer: จัดการกิจกรรม
    # ==============================

    # หน้าแสดงรายการกิจกรรมสำหรับ Organizer
    path("", views.event_list, name="event_list"),

    # หน้าเพิ่มกิจกรรมใหม่
    path("create/", views.event_create, name="event_create"),

    # หน้าแก้ไขกิจกรรม โดยรับหมายเลข ID ของกิจกรรม
    path("<int:event_id>/edit/", views.event_edit, name="event_edit"),

    # หน้าลบกิจกรรม โดยรับหมายเลข ID ของกิจกรรม
    path("<int:event_id>/delete/", views.event_delete, name="event_delete"),

    # ==============================
    # Student: ดูและค้นหากิจกรรม
    # ==============================

    # หน้าแสดงรายการกิจกรรมที่เปิดรับสมัคร
    path("browse/", student_views.event_list, name="browse_event_list"),

    # หน้าแสดงรายละเอียดกิจกรรม โดยรับหมายเลข ID ของกิจกรรม
    path("<int:event_id>/", student_views.event_detail, name="browse_event_detail"),
]