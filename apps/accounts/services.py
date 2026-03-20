from django.core.mail import send_mail
from django.conf import settings


def send_otp(user, otp):

    send_mail(
        subject="Your Verification Code - CF",
        message=f"Your OTP is: {otp}\n\nThis code will expire in 1 minutes.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
