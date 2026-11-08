from django.contrib import admin
from .models import Event, Category

# ลงทะเบียนกิจกรรมและหมวดหมู่ให้แสดงใน Django Admin
admin.site.register(Event)
admin.site.register(Category)
