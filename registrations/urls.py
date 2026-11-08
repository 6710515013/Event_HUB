
from django.urls import path
from . import views

app_name = 'registrations'

urlpatterns = [
    path('history/', views.registration_history, name='history'),
    path('<int:event_id>/apply/', views.registration_apply, name='apply'),
]
