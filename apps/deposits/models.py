from django.db import models
from apps.members.models import Member


class Deposit(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="deposits"
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    date = models.DateTimeField(auto_now_add=True)

    notes = models.TextField(blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.member.user.email} - {self.amount}"
