from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("register/success/", views.register_success, name="register_success"),
    
    path("login/", views.user_login, name="login"),
    path("login/success/", views.login_success, name="login_success"),
    
    path("logout/", views.user_logout, name="logout"),
    
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
    path("organizer/dashboard/", views.organizer_dashboard, name="organizer_dashboard"),

    # --- Organizer Profile ---
    path('organizer/profile/', views.organizer_profile, name='organizer_profile'),                           # แสดงข้อมูลโปรไฟล์
    path('organizer/profile/edit/', views.organizer_profile_edit, name='organizer_profile_edit'),            # แก้ไขข้อมูล
    path('organizer/profile/password/', views.organizer_password_change, name='organizer_password_change'),  # เปลี่ยนรหัสผ่าน

    # --- Student Profile ---
    path('student/profile/', views.student_profile, name='student_profile'),                                  # แสดงข้อมูลโปรไฟล์
    path('student/profile/edit/', views.student_profile_edit, name='student_profile_edit'),                   # แก้ไขข้อมูล
    path('student/profile/password/', views.student_password_change, name='student_password_change'),         # เปลี่ยนรหัสผ่าน
]
