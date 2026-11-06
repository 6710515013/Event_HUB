
from django.urls import path
from . import views

app_name = 'registrations'

urlpatterns = [
    path('history/', views.registration_history, name='history'),
]
