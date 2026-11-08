"""
Django settings for event_hub project.
"""

import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

# กำหนดตำแหน่งโฟลเดอร์หลักของโปรเจกต์
BASE_DIR = Path(__file__).resolve().parent.parent


# ==================================================
# Security Settings
# ==================================================

# อ่าน SECRET_KEY จาก Environment Variable
# ค่าเริ่มต้นนี้ใช้เฉพาะตอนพัฒนาในเครื่องเท่านั้น
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-local-development-only-change-this-key'
)

# อ่าน DEBUG จาก Environment Variable
# หากไม่ได้กำหนด จะเปิด DEBUG สำหรับการพัฒนาในเครื่อง
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

# ห้ามใช้ SECRET_KEY สำรองใน Production
if not DEBUG and not os.environ.get('SECRET_KEY'):
    raise ImproperlyConfigured(
        'กรุณากำหนด SECRET_KEY ใน Environment Variables'
    )

# กำหนดโดเมนที่อนุญาตให้เข้าถึงเว็บไซต์
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        'ALLOWED_HOSTS',
        'localhost,127.0.0.1'
    ).split(',')
    if host.strip()
]

# กำหนดแหล่งที่มาที่อนุญาตให้ส่งคำขอแบบ CSRF
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')
    if origin.strip()
]


# ==================================================
# Application Definition
# ==================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Project Apps
    'accounts',
    'events',
    'registrations',
    'dashboard',
    'core',
]


# ==================================================
# Middleware
# ==================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # ให้ WhiteNoise จัดการ Static Files ใน Production
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'event_hub.urls'


# ==================================================
# Templates
# ==================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # โฟลเดอร์ Templates กลางของโปรเจกต์
        'DIRS': [BASE_DIR / 'templates'],

        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'event_hub.wsgi.application'


# ==================================================
# Database
# ==================================================

# หากมี DATABASE_URL จะใช้ PostgreSQL จาก Render
# หากไม่มี จะใช้ SQLite สำหรับพัฒนาในเครื่อง
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=not DEBUG,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# ==================================================
# Password Validation
# ==================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ==================================================
# Internationalization
# ==================================================

LANGUAGE_CODE = 'en-us'

# ใช้เวลาไทยเพื่อให้วันและเวลากิจกรรมตรงกับประเทศไทย
TIME_ZONE = 'Asia/Bangkok'

USE_I18N = True
USE_TZ = True


# ==================================================
# Static Files
# ==================================================

# URL สำหรับเรียก CSS, JavaScript และรูปภาพที่เป็น Static Files
STATIC_URL = '/static/'

# โฟลเดอร์ Static Files ที่มีอยู่ในโปรเจกต์
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# โฟลเดอร์ปลายทางที่ collectstatic จะรวบรวมไฟล์ไว้
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ใช้ WhiteNoise จัดเก็บ Static Files ใน Production
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}


# ==================================================
# Media Files
# ==================================================

# URL และตำแหน่งเก็บไฟล์ที่ผู้ใช้อัปโหลด เช่น รูปโปสเตอร์กิจกรรม
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ==================================================
# Email
# ==================================================

# ใช้ Console Email Backend ในเครื่องสำหรับทดสอบ
# สามารถเปลี่ยนเป็น SMTP ผ่าน Environment Variable ภายหลังได้

# ใช้ MAILERS ตามรูปแบบของ Django 6.1
# ค่าเริ่มต้นใช้ Console Email Backend สำหรับทดสอบในเครื่อง
MAILERS = {
    'default': {
        'BACKEND': os.environ.get(
            'EMAIL_BACKEND',
            'django.core.mail.backends.console.EmailBackend' 
            ),
    },
}


# ==================================================
# Custom User Model
# ==================================================

# ใช้ User Model ที่โปรเจกต์สร้างไว้
AUTH_USER_MODEL = 'accounts.User'


# ==================================================
# Default Primary Key
# ==================================================

# กำหนดชนิด Primary Key เริ่มต้นของ Django
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'