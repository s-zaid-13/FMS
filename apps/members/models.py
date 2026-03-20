from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class Member(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="member_profile"
    )

    total_deposited = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    current_loan_balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name
