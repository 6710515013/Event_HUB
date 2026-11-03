# EventHub – Team Guidelines

เอกสารข้อตกลงและแนวทางการทำงานร่วมกันของทีมพัฒนา EventHub

## 1. วัตถุประสงค์

เพื่อกำหนดแนวทางการทำงานร่วมกันของสมาชิกทั้ง 6 คน ให้ทุกคนเข้าใจโครงสร้างโปรเจกต์ ขอบเขตความรับผิดชอบ และวิธีใช้ Git/GitHub ในทิศทางเดียวกัน

## 2. กติกาการใช้ Git Branch

เราใช้ `main` เป็น Branch หลักสำหรับเก็บโค้ดที่ผ่านการตรวจสอบแล้ว

**ข้อตกลง**
- ห้ามแก้ไขหรือ Commit งานโดยตรงบน `main`
- สมาชิกแต่ละคนต้องทำงานบน Feature Branch ของตัวเอง
- ทุก Branch ต้องสร้างจาก `main` เวอร์ชันล่าสุด
- ตั้งชื่อ Branch ตามรูปแบบ `feature/ชื่องาน`
- เมื่อทำงานเสร็จต้อง Push ขึ้น GitHub และเปิด Pull Request (PR) เข้า `main`
- ห้าม Merge PR ของตัวเองโดยไม่ผ่านการตรวจสอบจากสมาชิกในทีม
- ก่อนเริ่มงานใหม่ ให้ตรวจสอบว่า Branch ของตัวเองเป็นเวอร์ชันล่าสุดตามความเหมาะสม

## 3. การแบ่งหน้าที่และ Branch

| สมาชิก | หน้าที่ | Branch |
|---|---|---|
| คนที่ 1 | Organizer Profile & Account Management | `feature/organizer-profile` |
| คนที่ 2 | Event Management | `feature/event-management` |
| คนที่ 3 | Event Browsing | `feature/event-browsing` |
| คนที่ 4 | Registration System | `feature/registration` |
| คนที่ 5 | Dashboard | `feature/dashboard` |
| คนที่ 6 | UI/UX & Integration | `feature/ui-integration` |

## 4. ขอบเขตความรับผิดชอบของแต่ละคน

### Person 1: Organizer Profile & Account Management
รับผิดชอบ:
- แสดงข้อมูลโปรไฟล์ Organizer
- แก้ไขข้อมูลส่วนตัว Organizer
- ตรวจสอบสิทธิ์การเข้าถึงหน้า Organizer
- เชื่อมโยง Organizer กับกิจกรรมที่ตนเองสร้าง

ไฟล์หลัก: `accounts/forms.py`, `accounts/views.py`, `accounts/urls.py` และ Templates ที่เกี่ยวข้อง

### Person 2: Event Management
รับผิดชอบ:
- สร้างกิจกรรม
- แก้ไขและลบกิจกรรมของตนเอง
- กำหนดชื่อชุมนุม/องค์กรขณะสร้างกิจกรรม
- กำหนดรายละเอียด วันเวลา สถานที่ และจำนวนผู้เข้าร่วม
- เปิดและปิดรับสมัคร
- รองรับลิงก์ Google Forms ภายนอก (ถ้ามี)

ไฟล์หลัก: `events/models.py`, `events/views.py`, `events/urls.py` และ Templates ที่เกี่ยวข้อง

### Person 3: Event Browsing
รับผิดชอบ:
- แสดงรายการกิจกรรมที่เปิดรับสมัคร
- ค้นหาและกรองกิจกรรม
- แสดงรายละเอียดกิจกรรม
- แสดงปุ่มสมัครเข้าร่วมกิจกรรม
- รองรับการสมัครผ่านระบบภายในหรือลิงก์ภายนอกตามที่กำหนด

ไฟล์หลัก: ส่วน Student-facing ของ `events/views.py`, URLs และ Templates ที่เกี่ยวข้อง

### Person 4: Registration System
รับผิดชอบ:
- ระบบสมัครเข้าร่วมกิจกรรมภายในเว็บไซต์
- ป้องกันการสมัครกิจกรรมซ้ำ
- ตรวจสอบจำนวนที่นั่ง
- ตรวจสอบสถานะการเปิดรับสมัคร
- เก็บประวัติการสมัคร

ไฟล์หลัก: `registrations/models.py`, `registrations/views.py`, `registrations/urls.py` และ Templates ที่เกี่ยวข้อง

### Person 5: Dashboard
รับผิดชอบ:
- Dashboard สำหรับ Student
- Dashboard สำหรับ Organizer
- แสดงข้อมูลกิจกรรมและประวัติการสมัครที่เกี่ยวข้อง
- สรุปข้อมูลตามสิทธิ์ของผู้ใช้งาน

ไฟล์หลัก: `dashboard/views.py`, `dashboard/urls.py` และ Templates ที่เกี่ยวข้อง

### Person 6: UI/UX & Integration
รับผิดชอบ:
- ออกแบบหน้าเว็บส่วนกลาง
- จัดทำ Navbar, Sidebar และ Footer
- ดูแล `base.html`
- จัดการ CSS และ JavaScript ส่วนกลาง
- ประสานการเชื่อมต่อ URL ระหว่าง Apps
- ตรวจสอบและทดสอบการรวมโค้ดจากสมาชิก

ไฟล์หลัก: `templates/base.html`, `static/`, `core/` และไฟล์ส่วนกลางตามที่ทีมตกลงกัน

## 5. กติกาการแก้ไขไฟล์ร่วมกัน

เพื่อป้องกัน Merge Conflict และปัญหาจากการแก้ไขไฟล์เดียวกัน

- สมาชิกต้องรับผิดชอบไฟล์ตามขอบเขตที่กำหนด
- หากจำเป็นต้องแก้ไขไฟล์ที่เป็นของสมาชิกคนอื่น ต้องแจ้งและตกลงกันก่อน
- `accounts/models.py` ดูแลโดยผู้รับผิดชอบระบบบัญชี
- `events/models.py` ดูแลโดย Person 2
- `registrations/models.py` ดูแลโดย Person 4
- `event_hub/settings.py` และ `event_hub/urls.py` ให้ Person 6 ประสานการแก้ไข
- การแก้ไข Models และ Migrations ต้องแจ้งทีมก่อนเสมอ
- ห้ามสร้าง Migration ซ้ำซ้อนหรือแก้ไข Migration ของสมาชิกคนอื่นโดยไม่ประสานงาน

## 6. ข้อตกลงด้านระบบ EventHub

ทุกคนต้องเข้าใจแนวทางการทำงานของระบบร่วมกัน

1. ผู้ใช้งานมี Role ได้แก่ Student, Organizer และ Admin
2. Organizer สามารถสร้างกิจกรรมได้ โดยกรอกชื่อชุมนุมหรือองค์กรเป็นข้อความ ไม่ต้องสร้างระบบจัดการชุมนุมแยก
3. Organizer สามารถจัดการเฉพาะกิจกรรมของตนเอง
4. Student เห็นกิจกรรมที่เปิดรับสมัครเท่านั้น
5. เมื่อปิดรับสมัคร กิจกรรมจะไม่แสดงในรายการกิจกรรมที่เปิดรับสมัคร แต่ข้อมูลกิจกรรมและประวัติการสมัครยังคงอยู่
6. ระบบสมัครภายในต้องป้องกันการสมัครซ้ำและตรวจสอบจำนวนผู้เข้าร่วม
7. กิจกรรมสามารถใช้ระบบสมัครภายในหรือส่งผู้ใช้ไปยัง Google Forms ภายนอกได้ตามที่กำหนด

## 7. แนวทางการ Commit

ตั้งชื่อ Commit ให้สื่อความหมายและเข้าใจง่าย เช่น

- `feat: add organizer profile page`
- `feat: implement event creation`
- `fix: prevent duplicate registration`
- `style: improve navbar layout`
- `docs: update README`

ควร Commit เป็นระยะ ไม่ควรรวมงานทั้งหมดไว้ใน Commit เดียว

## 8. ขั้นตอนการส่งงาน

1. ตรวจสอบ Branch ของตัวเอง
2. ทดสอบโค้ดก่อน Push
3. Commit งานพร้อมข้อความที่สื่อความหมาย
4. Push Branch ขึ้น GitHub
5. เปิด Pull Request โดยเลือก Base เป็น `main`
6. ให้สมาชิกตรวจสอบโค้ดก่อน Merge
7. หลัง Merge ให้สมาชิกอัปเดต `main` ในเครื่องก่อนเริ่มงานรอบถัดไป

## 9. ข้อควรระวัง

- ห้าม Push ไฟล์ `venv/`, `__pycache__/` หรือ `db.sqlite3` ขึ้น GitHub
- ห้ามเปิดเผยรหัสผ่านหรือ Secret ใน Repository
- ห้ามแก้ไขโค้ดของสมาชิกคนอื่นโดยไม่แจ้ง
- หากพบปัญหาให้แจ้งทีมก่อนแก้ไขส่วนที่เกี่ยวข้อง
- หากมีการเปลี่ยนแปลงโครงสร้าง Database หรือ API ต้องแจ้งสมาชิกที่เกี่ยวข้อง

---

**เป้าหมายของทีม:** ทำงานร่วมกันอย่างเป็นระบบ แบ่งความรับผิดชอบชัดเจน และช่วยกันรักษาคุณภาพของโปรเจกต์ EventHub