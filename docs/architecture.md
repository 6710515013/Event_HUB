# EventHub Architecture (C4 Model)

EventHub เป็น Modular Monolith: เว็บ Django ตัวเดียว แบ่งงานเป็น Django app ตามหน้าที่
และแยก business logic ของการสมัครกิจกรรมไว้ใน Service Layer (`registrations/services.py`)

## Level 1: System Context

ใครใช้ระบบ และระบบคุยกับระบบภายนอกอะไรบ้าง

```mermaid
flowchart LR
    student["👤 นักศึกษา<br/>ค้นหาและสมัครกิจกรรม"]
    organizer["👤 ผู้จัดกิจกรรม<br/>ชมรม / หน่วยงาน"]
    eventhub["EventHub<br/>ระบบรวมและสมัครกิจกรรมนักศึกษา"]
    gforms["Google Forms<br/>ระบบภายนอก: เก็บข้อมูลผู้สมัคร"]

    student -- "ค้นหา ดูรายละเอียด กดสมัคร ดูประวัติ" --> eventhub
    organizer -- "สร้าง แก้ไข ลบ ปิดรับสมัครกิจกรรม" --> eventhub
    eventhub -- "พาไปกรอกแบบฟอร์มหลังกดสมัคร" --> gforms
    organizer -. "คัดเลือกผู้สมัครจากคำตอบในฟอร์ม" .-> gforms

    classDef person fill:#EA580C,stroke:#9A3412,color:#fff
    classDef system fill:#1F2937,stroke:#111827,color:#fff
    classDef external fill:#9CA3AF,stroke:#6B7280,color:#fff
    class student,organizer person
    class eventhub system
    class gforms external
```

## Level 2: Container

ข้างในระบบ EventHub ที่ deploy บน Render ประกอบด้วยอะไรบ้าง

```mermaid
flowchart TB
    student["👤 นักศึกษา"]
    organizer["👤 ผู้จัดกิจกรรม"]

    subgraph render["Render (Cloud PaaS)"]
        web["Web Application<br/>Django 6.1 + Gunicorn<br/>หน้าเว็บ Bootstrap 5, WhiteNoise เสิร์ฟ static"]
        db[("PostgreSQL<br/>ผู้ใช้ กิจกรรม หมวดหมู่ การสมัคร")]
        media[("Media Storage<br/>ไฟล์โปสเตอร์กิจกรรม")]
    end

    gforms["Google Forms<br/>ระบบภายนอก"]
    github["GitHub Actions<br/>CI: รัน test + coverage"]

    student -- "HTTPS" --> web
    organizer -- "HTTPS" --> web
    web -- "อ่าน / เขียนข้อมูล (Django ORM)" --> db
    web -- "อัปโหลด / เปิดรูปโปสเตอร์" --> media
    web -- "redirect ไปฟอร์มสมัคร" --> gforms
    github -. "ตรวจทุก push / PR ก่อน merge" .-> web

    classDef person fill:#EA580C,stroke:#9A3412,color:#fff
    classDef container fill:#1F2937,stroke:#111827,color:#fff
    classDef external fill:#9CA3AF,stroke:#6B7280,color:#fff
    class student,organizer person
    class web,db,media container
    class gforms,github external
```

ในเครื่องนักพัฒนาใช้ SQLite แทน PostgreSQL (เลือกจาก `DATABASE_URL` ใน `event_hub/settings.py`)

## Level 3: Component (ภายใน Web Application)

แต่ละ Django app ทำอะไร และเรียกกันอย่างไร

```mermaid
flowchart TB
    subgraph web["Web Application (Django)"]
        accounts["accounts<br/>ลงทะเบียน login/logout<br/>โปรไฟล์ เปลี่ยนรหัสผ่าน<br/>User model + role"]
        events["events<br/>ผู้จัด: สร้าง แก้ไข ลบกิจกรรม<br/>นักศึกษา: ค้นหา ดูรายละเอียด"]
        registrations["registrations<br/>views: รับคำขอสมัคร, ประวัติ"]
        services["registrations/services.py<br/>Service Layer: apply_for_event<br/>@transaction.atomic"]
        dashboard["dashboard<br/>หน้าแรกของแต่ละ role<br/>ค้นหา + กรองหมวดหมู่"]
        ui["templates + static<br/>base.html, style.css, main.js"]
    end

    db[("Database")]

    registrations -- "เรียก" --> services
    services -- "ตรวจสถานะ / วันปิดรับ<br/>สร้าง Registration" --> db
    events -- "Event, Category" --> db
    accounts -- "User" --> db
    dashboard -- "อ่าน Event + จำนวนผู้สมัคร<br/>(select_related / prefetch_related)" --> db
    accounts & events & registrations & dashboard -- "render" --> ui
```

## การตัดสินใจหลักและเหตุผล

| เรื่อง | เลือก | เหตุผล |
|---|---|---|
| รูปแบบระบบ | Modular Monolith | ทีม 6 คน แบ่งงานตาม Django app ได้ชัด deploy ตัวเดียว ไม่ซับซ้อน |
| การสมัคร | Service Layer + `@transaction.atomic` + `select_for_update` | กันสมัครซ้ำเมื่อกดพร้อมกัน และแยก logic ให้ทดสอบได้โดยไม่ผ่านหน้าเว็บ |
| จำนวนผู้สมัคร | ไม่จำกัด | ผู้จัดคัดเลือกจริงผ่าน Google Forms ส่วน `max_participants` คือจำนวนที่ผู้จัดจะรับ |
| ป้องกัน N+1 Query | `select_related` / `prefetch_related` / `annotate` | หน้า dashboard และประวัติการสมัครดึงข้อมูลที่เกี่ยวข้องใน query เดียว |
| ค่าลับ | Environment Variables บน Render | `SECRET_KEY`, `DEBUG`, `DATABASE_URL` ไม่อยู่ในโค้ด |
| เวลา | `TIME_ZONE = Asia/Bangkok`, `USE_TZ = True` | เก็บเป็น UTC ในฐานข้อมูล แสดงผลเป็นเวลาไทย |