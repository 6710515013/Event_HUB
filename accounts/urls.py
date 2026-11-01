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
]
