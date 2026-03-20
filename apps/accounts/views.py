from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm, OTPVerifyForm
from django.contrib.auth import login
from .services import send_otp
from django.utils.crypto import get_random_string
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit
from apps.notifications.services import send_notification_email
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()


def send_verification_otp(request, user):
    otp = get_random_string(length=6, allowed_chars="0123456789")

    request.session["signup_otp"] = otp
    request.session["signup_otp_email"] = user.email
    request.session["signup_otp_expiry"] = (
        timezone.now() + timedelta(minutes=1)
    ).timestamp()
    request.session["signup_user_id"] = user.id
    send_otp(user, otp)


@ratelimit(key="ip", rate="2/5m", block=True)
def resend_otp(request):
    email = request.session.get("signup_email")

    if not email:
        return JsonResponse({"success": False})

    user = User.objects.filter(email=email).first()

    if user:
        send_verification_otp(request, user)
        return JsonResponse({"success": True})

    return JsonResponse({"success": False})


def signup_view(request):

    if request.method == "POST":

        form = SignupForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            user.role = "member"
            user.is_active = False
            user.save()

            send_verification_otp(request, user)
            request.session["signup_email"] = user.email

            return redirect("verify_otp")

    else:

        form = SignupForm()

    return render(request, "auth/signup.html", {"form": form})


@ratelimit(key="ip", rate="3/m", block=True)
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            login(request, user)

            return redirect("dashboard")

    else:
        form = LoginForm()

    return render(request, "auth/login.html", {"form": form})


def verify_otp(request):
    email = request.session.get("signup_email")
    if not email:
        return JsonResponse(
            {"success": False, "redirect": True, "url": "accounts/signup/"}
        )

    if request.method == "POST":
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data["otp"]

            stored_otp = request.session.get("signup_otp")
            stored_email = request.session.get("signup_otp_email")
            expiry = request.session.get("signup_otp_expiry")
            user_id = request.session.get("signup_user_id")

            if not expiry or timezone.now().timestamp() > expiry:
                request.session.flush()
                return JsonResponse(
                    {
                        "success": False,
                        "error": "OTP has expired. Please click 'Resend OTP'.",
                    }
                )

            if stored_email == email and stored_otp == entered_otp:
                try:
                    user = User.objects.get(id=user_id, email=email)
                    user.is_active = True
                    user.save()
                    send_notification_email(
                        "Welcome to Community Fund System",
                        f"Hi {user.name or 'User'}, your account has been successfully created. You can now log in and start managing your deposits, loans, and contributions. For any kind of help you can contact us through email(help.access.team@gmail.com).",
                        user.email,
                    )

                    for key in [
                        "signup_otp",
                        "signup_otp_email",
                        "signup_otp_expiry",
                        "signup_user_id",
                        "signup_email",
                    ]:
                        if key in request.session:
                            del request.session[key]

                    login(request, user)

                    return JsonResponse(
                        {"success": True, "redirect": True, "url": "/dashboard/"}
                    )

                except User.DoesNotExist:
                    return JsonResponse({"success": False, "error": "User not found."})

            return JsonResponse(
                {"success": False, "error": "Invalid OTP. Please try again."}
            )
    else:
        form = OTPVerifyForm()
        return render(request, "auth/verify_otp.html", {"form": form})

    return JsonResponse({"success": False, "error": "GET not allowed."})


@login_required
def logout_view(request):
    logout(request)
    list(messages.get_messages(request))
    messages.success(request, "Successfully logged out!")
    return redirect("login")
