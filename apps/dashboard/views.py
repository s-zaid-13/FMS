from django.shortcuts import render
from apps.members.models import Member
from apps.deposits.models import Deposit
from apps.loans.models import Loan, LoanPayment
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from apps.core.models import Fund
from apps.core.permissions import admin_required, member_required
from django.contrib.auth.decorators import login_required
import json


@login_required
def dashboard(request):
    if request.user.role == "admin":
        return admin_dashboard(request)
    else:
        return member_dashboard(request)


@admin_required
def admin_dashboard(request):

    # Deposits
    deposits_by_month = (
        Deposit.objects.filter(status="approved")
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    # Repayments
    repayments_by_month = (
        LoanPayment.objects.filter(status="approved")
        .annotate(month=TruncMonth("payment_date"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    months = []
    monthly_deposits = []
    monthly_repayments = []

    for d in deposits_by_month:
        months.append(d["month"].strftime("%b"))
        monthly_deposits.append(float(d["total"]))

    repay_dict = {r["month"]: float(r["total"]) for r in repayments_by_month}

    for d in deposits_by_month:
        monthly_repayments.append(repay_dict.get(d["month"], 0))

    active_amount = (
        Loan.objects.filter(status="approved").aggregate(total=Sum("amount"))["total"]
        or 0
    )

    pending_amount = (
        Loan.objects.filter(status="pending").aggregate(total=Sum("amount"))["total"]
        or 0
    )

    repaid_amount = (
        LoanPayment.objects.filter(status="approved").aggregate(total=Sum("amount"))[
            "total"
        ]
        or 0
    )

    context = {
        "members": Member.objects.count(),
        "total_deposits": Deposit.objects.filter(status="approved").aggregate(
            Sum("amount")
        )["amount__sum"]
        or 0,
        "active_loans": Loan.objects.filter(status="approved").count(),
        "outstanding_loans": Loan.objects.filter(status="approved").aggregate(
            Sum("remaining_balance")
        )["remaining_balance__sum"]
        or 0,
        "pending_deposits": Deposit.objects.filter(status="pending").count(),
        "pending_loans": Loan.objects.filter(status="pending").count(),
        "pending_repayments": LoanPayment.objects.filter(status="pending").count(),
        "deposit_requests": Deposit.objects.filter(status="pending"),
        "loan_requests": Loan.objects.filter(status="pending"),
        "repayment_requests": LoanPayment.objects.filter(status="pending"),
        "members_list": Member.objects.select_related("user"),
        "deposits": Deposit.objects.select_related("member")
        .exclude(status__in=["rejected", "pending"])
        .order_by("-date")[:10],
        "loans": Loan.objects.select_related("member")
        .exclude(status__in=["rejected", "pending"])
        .order_by("-created_at")[:5],
        "repayments": LoanPayment.objects.select_related("loan")
        .exclude(status__in=["rejected", "pending"])
        .order_by("-payment_date")[:5],
        "fund_balance": (
            Fund.objects.first().total_balance if Fund.objects.exists() else 0
        ),
    }

    context.update(
        {
            "active_amount": float(active_amount),
            "pending_amount": float(pending_amount),
            "total_repaid_amount": float(repaid_amount),
            "months": json.dumps(months),
            "monthly_deposits": monthly_deposits,
            "monthly_repayments": monthly_repayments,
        }
    )
    return render(request, "dashboard/admin_dashboard.html", context)


@member_required
def member_dashboard(request):

    member = Member.objects.get(user=request.user)

    deposits_by_month = (
        Deposit.objects.filter(member=member, status="approved")
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    months = []
    monthly_totals = []

    for d in deposits_by_month:

        months.append(d["month"].strftime("%b"))

        monthly_totals.append(float(d["total"]))

    repayments_by_month = (
        LoanPayment.objects.filter(loan__member=member, status="approved")
        .annotate(month=TruncMonth("payment_date"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    monthly_repayments = []

    repay_dict = {r["month"]: float(r["total"]) for r in repayments_by_month}

    for d in deposits_by_month:
        monthly_repayments.append(repay_dict.get(d["month"], 0))

    deposits = Deposit.objects.filter(member=member).order_by("-date")[:5]

    loans = Loan.objects.filter(member=member).order_by("-created_at")[:5]

    payments = LoanPayment.objects.filter(loan__member=member).order_by(
        "-payment_date"
    )[:5]

    total_loan_taken = (
        Loan.objects.filter(member=member, status="approved").aggregate(
            total=Sum("amount")
        )["total"]
        or 0
    )

    deposit_count = Deposit.objects.filter(member=member, status="approved").count()

    active_loans = Loan.objects.filter(member=member, status="approved").count()
    context = {
        "member": member,
        "deposits": deposits,
        "loans": loans,
        "payments": payments,
        "active_loans": active_loans,
        "deposit_count": deposit_count,
        "fund_balance": (
            Fund.objects.first().total_balance if Fund.objects.exists() else 0
        ),
        "months": json.dumps(months),
        "monthly_deposits": monthly_totals,
    }
    context.update(
        {
            "monthly_repayments": monthly_repayments,
            "total_loan_taken": float(total_loan_taken),
        }
    )

    return render(request, "dashboard/member_dashboard.html", context)
