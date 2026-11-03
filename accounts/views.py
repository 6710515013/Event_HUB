from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def register(request):

    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

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
                return redirect("student_dashboard")

            elif user.role == "ORGANIZER":
                return redirect("organizer_dashboard")

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