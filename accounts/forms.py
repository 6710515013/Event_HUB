
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


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
