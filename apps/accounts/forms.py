from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate


class SignupForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["name", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            # Important: authenticate ko email pass karo (username nahi)
            user = authenticate(email=email, password=password)

            if user is None:
                raise forms.ValidationError(
                    "Invalid email or password. Please try again."
                )

            if not user.is_active:
                raise forms.ValidationError(
                    "Your account is not active. Please verify your email first."
                )

            cleaned_data["user"] = user  # for view to use later

        return cleaned_data


class OTPVerifyForm(forms.Form):
    otp = forms.CharField(max_length=6, required=True)
