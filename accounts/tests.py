from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


def register_data(**overrides):
    data = {
        "username": "newstudent",
        "first_name": "สมชาย",
        "last_name": "ใจดี",
        "email": "new@example.com",
        "role": "STUDENT",
        "student_id": "6710000000",
        "password1": "Strong-pass-123",
        "password2": "Strong-pass-123",
    }
    data.update(overrides)
    return data


class RegisterTests(TestCase):

    def test_register_page_loads(self):
        self.assertEqual(self.client.get(reverse("register")).status_code, 200)

    def test_register_student_success(self):
        response = self.client.post(reverse("register"), register_data())
        self.assertRedirects(response, reverse("register_success"))
        user = User.objects.get(username="newstudent")
        self.assertEqual(user.role, "STUDENT")
        # สมัครเสร็จแล้วยังไม่ login อัตโนมัติ
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_register_success_page_loads(self):
        self.assertEqual(self.client.get(reverse("register_success")).status_code, 200)

    def test_student_must_have_student_id(self):
        response = self.client.post(reverse("register"), register_data(student_id=""))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newstudent").exists())

    def test_organizer_does_not_need_student_id(self):
        self.client.post(reverse("register"), register_data(role="ORGANIZER", student_id=""))
        self.assertTrue(User.objects.filter(username="newstudent", role="ORGANIZER").exists())

    def test_duplicate_email_is_rejected(self):
        User.objects.create_user(username="old", email="new@example.com", password="pw12345678")
        response = self.client.post(reverse("register"), register_data(email="NEW@example.com"))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newstudent").exists())

    def test_password_mismatch_is_rejected(self):
        self.client.post(reverse("register"), register_data(password2="Other-pass-123"))
        self.assertFalse(User.objects.filter(username="newstudent").exists())


class LoginLogoutTests(TestCase):

    def setUp(self):
        User.objects.create_user(username="stu", email="stu@example.com", password="pw12345678", role="STUDENT")
        User.objects.create_user(username="org", email="org@example.com", password="pw12345678", role="ORGANIZER")
        User.objects.create_user(username="adm", email="adm@example.com", password="pw12345678", role="ADMIN")

    def test_login_page_loads(self):
        self.assertEqual(self.client.get(reverse("login")).status_code, 200)

    def test_student_goes_to_student_dashboard(self):
        response = self.client.post(reverse("login"), {"username": "stu", "password": "pw12345678"})
        self.assertRedirects(response, reverse("dashboard:student_dashboard"))

    def test_organizer_goes_to_organizer_dashboard(self):
        response = self.client.post(reverse("login"), {"username": "org", "password": "pw12345678"})
        self.assertRedirects(response, reverse("dashboard:organizer_dashboard"))

    def test_other_role_goes_to_login_success(self):
        response = self.client.post(reverse("login"), {"username": "adm", "password": "pw12345678"})
        self.assertRedirects(response, reverse("login_success"), fetch_redirect_response=False)

    def test_wrong_password_stays_on_login(self):
        response = self.client.post(reverse("login"), {"username": "stu", "password": "wrong"})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout(self):
        self.client.login(username="stu", password="pw12345678")
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)


class ProfileTests(TestCase):

    def setUp(self):
        User.objects.create_user(username="stu", email="stu@example.com", password="pw12345678", role="STUDENT")
        User.objects.create_user(username="org", email="org@example.com", password="pw12345678", role="ORGANIZER")

    def test_profile_requires_login(self):
        response = self.client.get(reverse("student_profile"))
        self.assertEqual(response.status_code, 302)

    def test_student_profile_pages(self):
        self.client.login(username="stu", password="pw12345678")
        for name in ["student_profile", "student_profile_edit", "student_password_change"]:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200, name)

    def test_organizer_profile_pages(self):
        self.client.login(username="org", password="pw12345678")
        for name in ["organizer_profile", "organizer_profile_edit", "organizer_password_change"]:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200, name)

    def test_student_cannot_open_organizer_profile(self):
        self.client.login(username="stu", password="pw12345678")
        self.assertEqual(self.client.get(reverse("organizer_profile")).status_code, 403)

    def test_student_edit_username(self):
        self.client.login(username="stu", password="pw12345678")
        response = self.client.post(reverse("student_profile_edit"), {"username": "stu_new"})
        self.assertRedirects(response, reverse("student_profile"))
        self.assertTrue(User.objects.filter(username="stu_new").exists())

    def test_organizer_edit_username(self):
        self.client.login(username="org", password="pw12345678")
        response = self.client.post(reverse("organizer_profile_edit"), {"username": "org_new"})
        self.assertRedirects(response, reverse("organizer_profile"))

    def test_student_change_password(self):
        self.client.login(username="stu", password="pw12345678")
        self.client.post(reverse("student_password_change"), {
            "old_password": "pw12345678",
            "new_password1": "Brand-new-pass-1",
            "new_password2": "Brand-new-pass-1",
        })
        self.assertTrue(User.objects.get(username="stu").check_password("Brand-new-pass-1"))

    def test_organizer_change_password_wrong_old(self):
        self.client.login(username="org", password="pw12345678")
        response = self.client.post(reverse("organizer_password_change"), {
            "old_password": "wrong",
            "new_password1": "Brand-new-pass-1",
            "new_password2": "Brand-new-pass-1",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.get(username="org").check_password("pw12345678"))