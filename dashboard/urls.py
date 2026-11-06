
from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path(
        "student/",
        views.student_dashboard,
        name="student_dashboard"
    ),
    path(
        "organizer/",
        views.organizer_dashboard,
        name="organizer_dashboard"
    ),
]
