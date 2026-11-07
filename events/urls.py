
from django.urls import path
from . import views, browse_views

app_name = "events"

urlpatterns = [
    # Organizer: จัดการกิจกรรม
    path("", views.event_list, name="event_list"),
    path("create/", views.event_create, name="event_create"),
    path("<int:event_id>/edit/", views.event_edit, name="event_edit"),
    path("<int:event_id>/delete/", views.event_delete, name="event_delete"),

    # Student: ดูและค้นหากิจกรรม
    path("browse/", browse_views.event_list, name="browse_event_list"),
    path("<int:event_id>/", browse_views.event_detail, name="browse_event_detail"),
]
