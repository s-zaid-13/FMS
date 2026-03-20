from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from apps.members.models import Member
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from apps.notifications.services import send_notification_email


@receiver(post_save, sender=User)
def create_member_profile(sender, instance, created, **kwargs):

    if created and instance.role == "member":

        Member.objects.create(user=instance)


@receiver(user_signed_up)
def create_member_on_signup(request, user, **kwargs):

    if not hasattr(user, "member"):
        Member.objects.create(user=user)
        user.is_active = True
        user.role = "member"
        user.name = user.first_name
        user.save()
        send_notification_email(
            "Welcome to Community Fund System",
            f"Hi {user.first_name or 'User'}, your account has been successfully created. You can now log in and start managing your deposits, loans, and contributions.For any kind of help you can contact us through email(help.access.team@gmail.com)",
            user.email,
        )
