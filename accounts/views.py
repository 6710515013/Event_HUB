from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
#---------
from functools import wraps

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from .forms import (
    OrganizerAccountForm, OrganizerPasswordChangeForm,
    StudentAccountForm, StudentPasswordChangeForm,
)
from .models import User

def register(request):

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("register_success")

    else:
        form = RegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )


def register_success(request):
    return render(request, "accounts/register_success.html")

def user_login(request):

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.role == "STUDENT":
                return redirect("dashboard:student_dashboard")
            
            elif user.role == "ORGANIZER":
                return redirect("dashboard:organizer_dashboard")
            
            else:
                return redirect("login_success")

    else:
        form = AuthenticationForm()

    return render(
        request,
        "accounts/login.html",
        {"form": form}
    )

def login_success(request):
    return render(request, "accounts/login_success.html")


def user_logout(request):
    logout(request)
    return redirect("login")

@login_required(login_url="login")
def student_dashboard(request):

    if request.user.role != "STUDENT":
        return HttpResponseForbidden("You do not have permission to access this page.")

    return render(request, "accounts/student_dashboard.html")


@login_required(login_url="login")
def organizer_dashboard(request):

    if request.user.role != "ORGANIZER":
        return HttpResponseForbidden("You do not have permission to access this page.")

    return render(request, "accounts/organizer_dashboard.html")

# =====================================================================
# Profile ของ Organizer และ Student (Sprint 2)
# =====================================================================

# role ที่เข้าหน้าแต่ละประเภทได้ (ต้องตรงกับค่าที่เก็บใน DB ของทีม)
ORGANIZER_PROFILE_ROLES = ('ORGANIZER',)
STUDENT_PROFILE_ROLES = ('STUDENT',)


def role_only(*allowed_roles):
    """
    สร้าง decorator ตรวจสิทธิ์ฝั่ง server ตาม role ที่กำหนด
    - ยังไม่ login -> เด้งไปหน้า login (จำหน้าที่ต้องการไว้กลับมาหลัง login)
    - login แล้วแต่ role ไม่อยู่ในรายการ -> 403 Forbidden
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path(), login_url=reverse('login'))
            if request.user.role not in allowed_roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


# decorator สำเร็จรูปสำหรับแต่ละบทบาท
organizer_only = role_only(*ORGANIZER_PROFILE_ROLES)
student_only = role_only(*STUDENT_PROFILE_ROLES)


# ---------------------------- Organizer ------------------------------

@organizer_only
def organizer_profile(request):
    """หน้าแสดงข้อมูลโปรไฟล์ Organizer (อ่านอย่างเดียว) มีปุ่มแก้ไข และปุ่ม logout"""
    return render(request, 'accounts/organizer_profile.html', {'profile_user': request.user})


@organizer_only
def organizer_profile_edit(request):
    """หน้าแก้ไข username แล้วบันทึกลง database"""
    # ดึงข้อมูลสดจาก DB กัน request.user ถูกแก้ค้างในหน่วยความจำเมื่อฟอร์มไม่ผ่าน
    profile_user = User.objects.get(pk=request.user.pk)

    if request.method == 'POST':
        form = OrganizerAccountForm(request.POST, instance=profile_user)
        if form.is_valid():
            form.save()  # บันทึกลง database
            messages.success(request, 'บันทึกข้อมูลเรียบร้อยแล้ว')
            return redirect('organizer_profile')  # กลับหน้าแสดงข้อมูล (เห็นข้อมูลใหม่)
    else:
        form = OrganizerAccountForm(instance=profile_user)  # เปิดหน้าครั้งแรก: ใส่ข้อมูลเดิม

    return render(request, 'accounts/organizer_profile_edit.html', {'form': form})


@organizer_only
def organizer_password_change(request):
    """หน้าเปลี่ยนรหัสผ่าน (ต้องใส่รหัสเดิม) สำเร็จแล้วกลับหน้าแก้ไขข้อมูล"""
    if request.method == 'POST':
        form = OrganizerPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # ต่อ session ใหม่ ไม่งั้นเปลี่ยนรหัสแล้วจะถูก logout เอง
            update_session_auth_hash(request, user)
            messages.success(request, 'เปลี่ยนรหัสผ่านสำเร็จ')
            return redirect('organizer_profile_edit')
    else:
        form = OrganizerPasswordChangeForm(request.user)

    return render(request, 'accounts/organizer_password_change.html', {'form': form})


# ----------------------------- Student -------------------------------

@student_only
def student_profile(request):
    """หน้าแสดงข้อมูลโปรไฟล์ Student (อ่านอย่างเดียว) มีปุ่มประวัติการสมัคร / แก้ไข / logout"""
    return render(request, 'accounts/student_profile.html', {'profile_user': request.user})


@student_only
def student_profile_edit(request):
    """หน้าแก้ไข username แล้วบันทึกลง database"""
    profile_user = User.objects.get(pk=request.user.pk)

    if request.method == 'POST':
        form = StudentAccountForm(request.POST, instance=profile_user)
        if form.is_valid():
            form.save()
            messages.success(request, 'บันทึกข้อมูลเรียบร้อยแล้ว')
            return redirect('student_profile')
    else:
        form = StudentAccountForm(instance=profile_user)

    return render(request, 'accounts/student_profile_edit.html', {'form': form})


@student_only
def student_password_change(request):
    """หน้าเปลี่ยนรหัสผ่าน (ต้องใส่รหัสเดิม) สำเร็จแล้วกลับหน้าแก้ไขข้อมูล"""
    if request.method == 'POST':
        form = StudentPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # ต่อ session ใหม่ ไม่ให้ถูก logout
            messages.success(request, 'เปลี่ยนรหัสผ่านสำเร็จ')
            return redirect('student_profile_edit')
    else:
        form = StudentPasswordChangeForm(request.user)

    return render(request, 'accounts/student_password_change.html', {'form': form})