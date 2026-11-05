# ใช้ Decorator เพื่อตรวจสอบว่าผู้ใช้ Login แล้วหรือไม่
from django.contrib.auth.decorators import login_required

# ใช้ส่ง HTTP 403 Forbidden เมื่อผู้ใช้ไม่มีสิทธิ์เข้าถึงหน้า
from django.http import HttpResponseForbidden

# ใช้แสดง Template พร้อมส่งข้อมูลไปยังหน้าเว็บ
from django.shortcuts import render

#from types import SimpleNamespace #test ข้อมูลปลอม


# กำหนดให้ผู้ใช้ต้อง Login ก่อนเข้าหน้า Student Dashboard
# หากยังไม่ได้ Login จะถูก Redirect ไปยัง URL ที่ชื่อว่า "login"
@login_required(login_url="login")
def student_dashboard(request):
    
    # ตรวจสอบว่า Role ของผู้ใช้เป็น STUDENT หรือไม่
    # หากไม่ใช่ Student จะไม่อนุญาตให้เข้าถึงหน้านี้
    if request.user.role != "STUDENT":
        # ส่งสถานะ HTTP 403 Forbidden กลับไปยังผู้ใช้
        return HttpResponseForbidden(
            "You do not have permission to access this page."
        )
        
    # กำหนดข้อมูลที่จะส่งไปแสดงผลใน Template
    context = {
        # ส่งข้อมูลผู้ใช้ที่ Login อยู่ในปัจจุบัน
        "user": request.user,
        
        # ระบุ Role สำหรับนำไปแสดงผลในหน้า Dashboard
        "dashboard_role": "Student",
        
        # รายการกิจกรรมที่ Student สมัครไว้
        # ใช้ List ว่างไว้ก่อนจนกว่าจะเชื่อมกับข้อมูลจริง
        "my_activities": [],
        
        # รายการกิจกรรมที่กำลังจะมาถึง
        "upcoming_events": [],
        
        # ประวัติการสมัครกิจกรรมของ Student
        "registration_history": [],
    }

    # แสดง Template Student Dashboard
    # พร้อมส่งข้อมูล context ไปให้ Template
    return render(
        request,
        "dashboard/student_dashboard.html",
        context
    )

# กำหนดให้ผู้ใช้ต้อง Login ก่อนเข้าหน้า Organizer Dashboard
@login_required(login_url="login")
def organizer_dashboard(request):

    # ตรวจสอบว่า Role ของผู้ใช้เป็น ORGANIZER หรือไม่
    # หากไม่ใช่ Organizer จะไม่อนุญาตให้เข้าถึงหน้านี้
    if request.user.role != "ORGANIZER":
        # ส่งสถานะ HTTP 403 Forbidden กลับไปยังผู้ใช้
        return HttpResponseForbidden(
            "You do not have permission to access this page."
        )

    # กำหนดข้อมูลที่จะส่งไปแสดงผลใน Template
    context = {
        # ส่งข้อมูลผู้ใช้ที่ Login อยู่ในปัจจุบัน
        "user": request.user,
        
        # ระบุ Role สำหรับนำไปแสดงผลในหน้า Dashboard
        "dashboard_role": "Organizer",
        
        # จำนวนกิจกรรมที่ Organizer สร้าง
        # ใช้ค่า 0 ไว้ก่อนจนกว่าจะเชื่อมกับข้อมูลจริง
        "total_events": 0,
        
        # รายการกิจกรรมที่ Organizer สร้าง
        "my_events": [],
        
        # รายการกิจกรรมที่กำลังจะมาถึง
        "upcoming_events": [],
    }

    # แสดง Template Organizer Dashboard
    # พร้อมส่งข้อมูล context ไปให้ Template
    return render(
        request,
        "dashboard/organizer_dashboard.html",
        context
    )




#code test
# @login_required(login_url="login")
# def student_dashboard(request):

#     if request.user.role != "STUDENT":
#         return HttpResponseForbidden(
#             "You do not have permission to access this page."
#         )

#     # Temporary test data for Student Dashboard

#     my_activities = [
#         SimpleNamespace(
#             title="Python Programming Workshop",
#             description=(
#                 "ฝึกเขียนโปรแกรม Python "
#                 "ตั้งแต่พื้นฐานจนถึงการประยุกต์ใช้งาน"
#             ),
#         ),
#         SimpleNamespace(
#             title="Web Development Bootcamp",
#             description=(
#                 "เรียนรู้การพัฒนาเว็บไซต์ด้วย HTML, CSS "
#                 "และ Django"
#             ),
#         ),
#     ]

#     upcoming_events = [
#         SimpleNamespace(
#             title="Faculty Tech Talk",
#             description=(
#                 "กิจกรรมแลกเปลี่ยนความรู้ด้านเทคโนโลยี "
#                 "และนวัตกรรมทางวิศวกรรม"
#             ),
#         ),
#         SimpleNamespace(
#             title="Computer Engineering Open House",
#             description=(
#                 "กิจกรรมเปิดบ้านภาควิชาวิศวกรรมคอมพิวเตอร์ "
#                 "พร้อมกิจกรรม Workshop"
#             ),
#         ),
#         SimpleNamespace(
#             title="AI Innovation Workshop",
#             description=(
#                 "เรียนรู้การประยุกต์ใช้ AI "
#                 "เพื่อแก้ปัญหาในชีวิตประจำวัน"
#             ),
#         ),
#     ]

#     registration_history = [
#         SimpleNamespace(
#             event=SimpleNamespace(
#                 title="Python Programming Workshop"
#             ),
#         ),
#         SimpleNamespace(
#             event=SimpleNamespace(
#                 title="Web Development Bootcamp"
#             ),
#         ),
#         SimpleNamespace(
#             event=SimpleNamespace(
#                 title="Faculty Tech Talk"
#             ),
#         ),
#     ]

#     context = {
#         "user": request.user,
#         "dashboard_role": "Student",
#         "my_activities": my_activities,
#         "upcoming_events": upcoming_events,
#         "registration_history": registration_history,
#     }

#     return render(
#         request,
#         "dashboard/student_dashboard.html",
#         context
#     )


# @login_required(login_url="login")
# def organizer_dashboard(request):

#     if request.user.role != "ORGANIZER":
#         return HttpResponseForbidden(
#             "You do not have permission to access this page."
#         )

#     # Temporary test data for Organizer Dashboard
#     my_events = [
#         SimpleNamespace(
#             title="Python Workshop",
#             description=(
#                 "A hands-on workshop introducing "
#                 "Python programming."
#             ),
#             registration_count=25,
#         ),
#         SimpleNamespace(
#             title="Web Development Bootcamp",
#             description=(
#                 "Learn the fundamentals of modern "
#                 "web development."
#             ),
#             registration_count=18,
#         ),
#         SimpleNamespace(
#             title="Faculty Tech Talk",
#             description=(
#                 "Explore new technologies and "
#                 "engineering innovations."
#             ),
#             registration_count=40,
#         ),
#     ]

#     upcoming_events = [
#         SimpleNamespace(
#             title="Python Workshop",
#             description=(
#                 "Date: 20 November 2026 | "
#                 "Location: Computer Engineering Lab"
#             ),
#         ),
#         SimpleNamespace(
#             title="Web Development Bootcamp",
#             description=(
#                 "Date: 25 November 2026 | "
#                 "Location: Faculty Auditorium"
#             ),
#         ),
#     ]

#     context = {
#         "user": request.user,
#         "dashboard_role": "Organizer",
#         "total_events": len(my_events),
#         "my_events": my_events,
#         "upcoming_events": upcoming_events,
#     }

#     return render(
#         request,
#         "dashboard/organizer_dashboard.html",
#         context
#     )
