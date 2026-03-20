from django.db import models
from apps.members.models import Member


class Loan(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("completed", "Completed"),
    )

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="loans")

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    reason = models.TextField()

    repayment_months = models.IntegerField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    request_date = models.DateField(auto_now_add=True)

    approval_date = models.DateField(null=True, blank=True)

    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.member.user.email} - {self.amount}"


class LoanPayment(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="payments")

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    payment_date = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    def __str__(self):

        return f"{self.loan.member.user.email} - {self.amount}"
