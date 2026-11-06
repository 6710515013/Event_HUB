# นำเข้า TestCase สำหรับสร้างและรัน Unit Test ของ Django
from django.test import TestCase

# นำเข้า reverse สำหรับแปลงชื่อ URL เป็น URL Path
from django.urls import reverse

# นำเข้า get_user_model เพื่อเรียกใช้ User Model ของโปรเจกต์
from django.contrib.auth import get_user_model


# เรียกใช้ User Model ที่โปรเจกต์กำหนดไว้
User = get_user_model()


# สร้างคลาสสำหรับทดสอบการทำงานของ Student และ Organizer Dashboard
class DashboardTests(TestCase):

    # setUp() ทำงานก่อนเริ่ม Test แต่ละกรณี
    # ใช้สำหรับเตรียมข้อมูลที่จำเป็นในการทดสอบ
    def setUp(self):

        # สร้างบัญชีผู้ใช้ที่มี Role เป็น Student
        self.student = User.objects.create_user(
            username="student_test",          # กำหนด Username ของ Student
            email="student@example.com",      # กำหนด Email ของ Student
            password="testpassword123",       # กำหนด Password ของ Student
            role="STUDENT"                    # กำหนด Role เป็น Student
        )

        # สร้างบัญชีผู้ใช้ที่มี Role เป็น Organizer
        self.organizer = User.objects.create_user(
            username="organizer_test",        # กำหนด Username ของ Organizer
            email="organizer@example.com",    # กำหนด Email ของ Organizer
            password="testpassword123",       # กำหนด Password ของ Organizer
            role="ORGANIZER"                  # กำหนด Role เป็น Organizer
        )

    # ทดสอบว่าผู้ใช้ที่ยังไม่ได้ Login
    # ไม่สามารถเข้าหน้า Student Dashboard ได้
    def test_student_dashboard_requires_login(self):

        # ส่ง GET Request ไปยัง URL ของ Student Dashboard
        response = self.client.get(
            reverse("dashboard:student_dashboard")
        )

        # ตรวจสอบว่าระบบ Redirect ผู้ใช้ไปหน้า Login
        # HTTP 302 หมายถึงมีการ Redirect
        self.assertEqual(response.status_code, 302)

    # ทดสอบว่าผู้ใช้ที่ยังไม่ได้ Login
    # ไม่สามารถเข้าหน้า Organizer Dashboard ได้
    def test_organizer_dashboard_requires_login(self):

        # ส่ง GET Request ไปยัง URL ของ Organizer Dashboard
        response = self.client.get(
            reverse("dashboard:organizer_dashboard")
        )

        # ตรวจสอบว่าระบบ Redirect ผู้ใช้ไปหน้า Login
        # HTTP 302 หมายถึงมีการ Redirect
        self.assertEqual(response.status_code, 302)

    # ทดสอบว่า Student ที่ Login แล้ว
    # สามารถเข้าหน้า Student Dashboard ได้
    def test_student_can_access_student_dashboard(self):

        # กำหนดให้ Test Client Login เป็น Student
        # force_login() ใช้จำลองสถานะ Login โดยไม่ต้องกรอก Username และ Password
        self.client.force_login(self.student)

        # ส่ง GET Request ไปยัง URL ของ Student Dashboard
        response = self.client.get(
            reverse("dashboard:student_dashboard")
        )

        # ตรวจสอบว่า Dashboard ตอบกลับ HTTP 200 OK
        # หมายถึงสามารถเข้าถึงหน้า Dashboard ได้สำเร็จ
        self.assertEqual(response.status_code, 200)

        # ตรวจสอบว่า Response ใช้ Template Student Dashboard ถูกต้อง
        self.assertTemplateUsed(
            response,
            "dashboard/student_dashboard.html"
        )

    # ทดสอบว่า Organizer ที่ Login แล้ว
    # สามารถเข้าหน้า Organizer Dashboard ได้
    def test_organizer_can_access_organizer_dashboard(self):

        # กำหนดให้ Test Client Login เป็น Organizer
        self.client.force_login(self.organizer)

        # ส่ง GET Request ไปยัง URL ของ Organizer Dashboard
        response = self.client.get(
            reverse("dashboard:organizer_dashboard")
        )

        # ตรวจสอบว่า Dashboard ตอบกลับ HTTP 200 OK
        # หมายถึงสามารถเข้าถึงหน้า Dashboard ได้สำเร็จ
        self.assertEqual(response.status_code, 200)

        # ตรวจสอบว่า Response ใช้ Template Organizer Dashboard ถูกต้อง
        self.assertTemplateUsed(
            response,
            "dashboard/organizer_dashboard.html"
        )

    # ทดสอบว่า Student ไม่สามารถเข้าหน้า Organizer Dashboard ได้
    def test_student_cannot_access_organizer_dashboard(self):

        # กำหนดให้ Test Client Login เป็น Student
        self.client.force_login(self.student)

        # ส่ง GET Request ไปยัง URL ของ Organizer Dashboard
        response = self.client.get(
            reverse("dashboard:organizer_dashboard")
        )

        # ตรวจสอบว่าระบบปฏิเสธการเข้าถึง
        # HTTP 403 Forbidden หมายถึงผู้ใช้ไม่มีสิทธิ์เข้าถึง
        self.assertEqual(response.status_code, 403)

    # ทดสอบว่า Organizer ไม่สามารถเข้าหน้า Student Dashboard ได้
    def test_organizer_cannot_access_student_dashboard(self):

        # กำหนดให้ Test Client Login เป็น Organizer
        self.client.force_login(self.organizer)

        # ส่ง GET Request ไปยัง URL ของ Student Dashboard
        response = self.client.get(
            reverse("dashboard:student_dashboard")
        )

        # ตรวจสอบว่าระบบปฏิเสธการเข้าถึง
        # HTTP 403 Forbidden หมายถึงผู้ใช้ไม่มีสิทธิ์เข้าถึง
        self.assertEqual(response.status_code, 403)