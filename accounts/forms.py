
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import PasswordChangeForm

class RegistrationForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        label="Email"
    )

    role = forms.ChoiceField(
        choices=[
            (User.Role.STUDENT, "Student"),
            (User.Role.ORGANIZER, "Organizer"),
        ],
        label="Account Type"
    )

    student_id = forms.CharField(
        max_length=20,
        required=False,
        label="Student ID"
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "student_id",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "This email is already registered."
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        role = cleaned_data.get("role")
        student_id = cleaned_data.get("student_id")

        if role == User.Role.STUDENT and not student_id:
            self.add_error(
                "student_id",
                "Student ID is required for students."
            )

        return cleaned_data

class OrganizerAccountForm(forms.ModelForm):
    """ฟอร์มแก้ไขข้อมูลบัญชี (แก้ได้เฉพาะ username)"""

    class Meta:
        model = User
        # แก้ได้แค่ username: email / student_id / role ไม่อยู่ใน fields
        # จึงแก้ผ่านฟอร์มนี้ไม่ได้ (ปลอดภัยฝั่ง server)
        fields = ['username']
        labels = {'username': 'ชื่อผู้ใช้'}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    # หมายเหตุ: username ซ้ำ Django ตรวจให้อัตโนมัติเพราะเป็น unique field


class OrganizerPasswordChangeForm(PasswordChangeForm):
    """ฟอร์มเปลี่ยนรหัสผ่าน (ต้องใส่รหัสเดิมก่อน) ใช้ของ Django ที่ตรวจความปลอดภัยให้"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ใส่คลาส Bootstrap ให้ทุกช่องในฟอร์ม
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class StudentAccountForm(OrganizerAccountForm):
    """ฟอร์มแก้ข้อมูลบัญชี Student (พฤติกรรมเดียวกับ Organizer)"""
    pass


class StudentPasswordChangeForm(OrganizerPasswordChangeForm):
    """ฟอร์มเปลี่ยนรหัสผ่าน Student (พฤติกรรมเดียวกับ Organizer)"""
    pass