from django.contrib import admin
from .models import Loan, LoanPayment


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):

    list_display = (
        "member",
        "amount",
        "status",
        "repayment_months",
        "remaining_balance",
    )

    list_filter = ("status",)


@admin.register(LoanPayment)
class LoanPaymentAdmin(admin.ModelAdmin):

    list_display = ("loan", "amount", "status", "payment_date")
