# EventHub

[![CI](https://github.com/6710515013/Event_HUB/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/6710515013/Event_HUB/actions/workflows/ci.yml)

ระบบรวมและสมัครกิจกรรมสำหรับนักศึกษา ผู้จัดกิจกรรม (ชมรม / หน่วยงาน) ประกาศกิจกรรมได้ในที่เดียว
นักศึกษาค้นหา ดูรายละเอียด และกดสมัคร แล้วระบบพาไปกรอก Google Forms ของผู้จัดต่อ

โปรเจกต์รายวิชา CN331 Software Engineering

**เว็บไซต์ (Render):** https://eventhub-q0cp.onrender.com

---

## สมาชิกทีม

| ชื่อ-นามสกุล | รหัสนักศึกษา |
|---|---|
| คอยรุลอามีรีน นาวี | 6710515013 |
| เอมมิตรา แสวงทรัพย์ | 6710525038 |
| ฟาร์ริดา มูลรังษี | 6710615177 |
| กัญญาภัค หอมกระจ่าง | 6710615029 |
| ภีมพิมล เชื่องชยะพันธ์ | 6710685063 |
| ณัฐชนน จีใจ | 6710615102 |

---

## ฟีเจอร์

### นักศึกษา (Student)
- ลงทะเบียน / เข้าสู่ระบบ / ออกจากระบบ
- Dashboard: ค้นหาด้วยชื่อ กรองตามวันที่และหมวดหมู่ (เลือกได้หลายหมวด)
- ดูรายละเอียดกิจกรรม พร้อมนับถอยหลังปิดรับสมัคร
- กดสมัครกิจกรรม แล้วระบบพาไปกรอก Google Forms ของผู้จัด
- ป้องกันการสมัครซ้ำ ปิดรับสมัคร และหมดเขตรับสมัคร
- ดูประวัติการสมัคร
- โปรไฟล์ แก้ไขชื่อผู้ใช้ และเปลี่ยนรหัสผ่าน

### ผู้จัดกิจกรรม (Organizer)
- สร้าง / แก้ไข / ลบกิจกรรมของตนเอง (แก้ไขของผู้จัดคนอื่นไม่ได้)
- อัปโหลดโปสเตอร์ (ไม่เกิน 5 MB) เลือกหมวดหมู่ กำหนดวันเวลา สถานที่ และจำนวนที่รับ
- เปิด / ปิดรับสมัคร และใส่ลิงก์ Google Forms
- ตรวจข้อมูลทันทีขณะกรอก เช่น วันปิดรับสมัครต้องห่างจากปัจจุบันและจากวันเริ่มกิจกรรมอย่างน้อย 24 ชั่วโมง
- Dashboard สรุปกิจกรรมและจำนวนผู้สนใจ
- โปรไฟล์ แก้ไขชื่อผู้ใช้ และเปลี่ยนรหัสผ่าน

### กติกาการสมัคร
นักศึกษากดสมัครได้ไม่จำกัดจำนวน ผู้จัดคัดเลือกตัวจริงจากคำตอบใน Google Forms
ส่วน `max_participants` คือจำนวนที่ผู้จัดจะรับ ใช้แสดงให้นักศึกษาเห็น

---

## เทคโนโลยี

| ส่วน | ใช้ |
|---|---|
| Backend | Python 3.13+, Django 6.1 |
| Frontend | Django Templates, Bootstrap 5.3, Bootstrap Icons, JavaScript |
| ฐานข้อมูล | SQLite (ในเครื่อง), PostgreSQL (Render) |
| Deploy | Render, Gunicorn, WhiteNoise |
| CI | GitHub Actions + coverage |

---

## สถาปัตยกรรม

EventHub เป็น **Modular Monolith**: เว็บ Django ตัวเดียว แบ่งงานเป็น Django app ตามหน้าที่

| App | หน้าที่ |
|---|---|
| `accounts` | User model (role: STUDENT / ORGANIZER / ADMIN), ลงทะเบียน, login, โปรไฟล์ |
| `events` | กิจกรรมและหมวดหมู่, ฝั่งผู้จัด (สร้าง/แก้/ลบ) และฝั่งนักศึกษา (ค้นหา/รายละเอียด) |
| `registrations` | การสมัครและประวัติ, Service Layer ใน `registrations/services.py` |
| `dashboard` | หน้าแรกของแต่ละ role |
| `core` | ส่วนกลาง |
| `templates/`, `static/` | `base.html`, `style.css`, `main.js` ที่ทุกหน้าใช้ร่วมกัน |

- **Service Layer:** `apply_for_event()` ใช้ `@transaction.atomic` และ `select_for_update()` กันสมัครซ้ำเมื่อกดพร้อมกัน
- **ป้องกัน N+1 Query:** ใช้ `select_related`, `prefetch_related` และ `annotate(Count(...))`
- **ความปลอดภัยฐานข้อมูล:** `UniqueConstraint(student, event)` กันสมัครซ้ำ, ลบกิจกรรมที่มีผู้สมัครไม่ได้ (`PROTECT`)

แผนภาพ C4 (Context, Container, Component) อยู่ที่ [`docs/architecture.md`](docs/architecture.md)

### ตารางในฐานข้อมูล

| ตาราง | คอลัมน์หลัก |
|---|---|
| User | username, email (unique), role, student_id |
| Event | created_by → User, title, organization_name, poster, start/end_datetime, registration_deadline, location, max_participants, status, google_form_url |
| Category | name (unique) มี 13 หมวด ใส่ไว้ใน migration |
| Event_Category | event → Event, category → Category (Many-to-Many) |
| Registration | student → User, event → Event, registered_at, unique (student, event) |

---

## ติดตั้งและรันในเครื่อง

ต้องมี Python 3.13 ขึ้นไป และ Git

```bash
git clone https://github.com/6710515013/Event_HUB.git
cd Event_HUB
```

สร้างและเปิด virtual environment

```bash
python -m venv venv
```

Windows (PowerShell):

```bash
venv\Scripts\activate
```

macOS / Linux:

```bash
source venv/bin/activate
```

ติดตั้ง package และสร้างฐานข้อมูล

```bash
pip install -r requirements.txt
```

```bash
python manage.py migrate
```

สร้างบัญชี admin (ไม่บังคับ)

```bash
python manage.py createsuperuser
```

รันเว็บ

```bash
python manage.py runserver
```

เปิด http://127.0.0.1:8000

ในเครื่องไม่ต้องตั้ง Environment Variable ระบบจะใช้ SQLite และเปิด `DEBUG` ให้เอง

---

## การทดสอบ

```bash
pip install coverage
```

```bash
coverage run manage.py test
```

```bash
coverage report
```

- Unit test (model, form), Service test (`apply_for_event`) และ View test ของทุก app
- Coverage ประมาณ 95% (เกณฑ์ขั้นต่ำ 80%)
- GitHub Actions รัน `check`, ตรวจ migration และ test พร้อมวัด coverage ทุกครั้งที่ push หรือเปิด PR เข้า `dev` / `main`
  ถ้า test ไม่ผ่านหรือ coverage ต่ำกว่า 80% CI จะขึ้นสีแดง ([`.github/workflows/ci.yml`](.github/workflows/ci.yml))

---

## Deploy บน Render

1. **New → Postgres** (Free, Region: Singapore) แล้วคัดลอก **Internal Database URL**
2. **New → Web Service** เลือก repo นี้ ตั้งค่า

| ช่อง | ค่า |
|---|---|
| Branch | `main` |
| Runtime | Python 3 |
| Build Command | `bash build.sh` |
| Start Command | `gunicorn event_hub.wsgi:application` |

3. **Environment Variables**

| ชื่อ | ค่า |
|---|---|
| `SECRET_KEY` | กด Generate |
| `DEBUG` | `False` |
| `DATABASE_URL` | Internal Database URL จากข้อ 1 |

`build.sh` จะติดตั้ง package, รวมไฟล์ static และ migrate ให้ทุกครั้งที่ deploy
ชื่อโดเมนของ Render ถูกเพิ่มใน `ALLOWED_HOSTS` และ `CSRF_TRUSTED_ORIGINS` อัตโนมัติ

ข้อจำกัดของแผน Free
- ไม่มีคนเข้า 15 นาที เว็บจะหลับ เปิดครั้งแรกรอประมาณ 1 นาที
- รูปโปสเตอร์ที่อัปโหลดจะหายเมื่อ deploy ใหม่หรือเว็บรีสตาร์ต (ข้อมูลอื่นอยู่ใน PostgreSQL ไม่หาย)

---

## โครงสร้างโปรเจกต์

```
Event_HUB/
|-- .coveragerc
|-- .gitignore
|-- build.sh   # คำสั่ง build บน Render
|-- manage.py
|-- README.md
|-- requirements.txt
|-- TEAM_GUIDELINES.md
|-- .github/   # CI (GitHub Actions)
|   `-- workflows/
|       `-- ci.yml
|-- accounts/   # ผู้ใช้, ลงทะเบียน, login, โปรไฟล์
|   |-- __init__.py
|   |-- admin.py
|   |-- apps.py
|   |-- forms.py
|   |-- models.py
|   |-- tests.py
|   |-- urls.py
|   |-- views.py
|   |-- migrations/
|   `-- templates/
|       `-- accounts/
|           |-- login.html
|           |-- login_success.html
|           |-- organizer_dashboard.html
|           |-- organizer_password_change.html
|           |-- organizer_profile.html
|           |-- organizer_profile_edit.html
|           |-- register.html
|           |-- register_success.html
|           |-- student_dashboard.html
|           |-- student_password_change.html
|           |-- student_profile.html
|           `-- student_profile_edit.html
|-- core/
|   |-- __init__.py
|   |-- admin.py
|   |-- apps.py
|   |-- models.py
|   |-- tests.py
|   |-- urls.py
|   |-- views.py
|   `-- migrations/
|-- dashboard/   # Dashboard ของ Student / Organizer
|   |-- __init__.py
|   |-- admin.py
|   |-- apps.py
|   |-- models.py
|   |-- tests.py
|   |-- urls.py
|   |-- views.py
|   |-- migrations/
|   `-- templates/
|       `-- dashboard/
|           |-- organizer_dashboard.html
|           `-- student_dashboard.html
|-- docs/   # เอกสารสถาปัตยกรรม (C4)
|   `-- architecture.md
|-- event_hub/   # ตั้งค่าโปรเจกต์ (settings, urls)
|   |-- __init__.py
|   |-- asgi.py
|   |-- settings.py
|   |-- urls.py
|   `-- wsgi.py
|-- events/   # กิจกรรมและหมวดหมู่
|   |-- __init__.py
|   |-- admin.py
|   |-- apps.py
|   |-- forms.py
|   |-- models.py
|   |-- student_views.py   # หน้าค้นหา / รายละเอียด ฝั่งนักศึกษา
|   |-- tests.py
|   |-- urls.py
|   |-- views.py
|   |-- migrations/
|   `-- templates/
|       `-- events/
|           |-- _event_card.html
|           |-- event_confirm_delete.html
|           |-- event_form.html
|           |-- event_list.html
|           |-- student_detail.html
|           `-- student_list.html
|-- registrations/   # การสมัครกิจกรรม
|   |-- __init__.py
|   |-- admin.py
|   |-- apps.py
|   |-- models.py
|   |-- services.py   # Service Layer (@transaction.atomic)
|   |-- tests.py
|   |-- urls.py
|   |-- views.py
|   |-- migrations/
|   `-- templates/
|       `-- registrations/
|           `-- registration_history.html
|-- static/   # CSS / JavaScript ส่วนกลาง
|   |-- css/
|   |   `-- style.css
|   `-- js/
|       `-- main.js
`-- templates/
    `-- base.html   # layout กลางของทุกหน้า
```

---

## การทำงานร่วมกัน (Git Flow)

```
feature/ชื่องาน  →  PR เข้า dev  →  PR เข้า main (เวอร์ชันส่งงาน)
```

- ห้าม commit ตรงเข้า `dev` หรือ `main`
- ทุก PR ต้องผ่าน CI และมีสมาชิกกด Approve อย่างน้อย 1 คนก่อน merge
- รายละเอียดเพิ่มเติมดูที่ [`TEAM_GUIDELINES.md`](TEAM_GUIDELINES.md)