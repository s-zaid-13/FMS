from apps.members.models import Member
from .models import Loan, LoanPayment
from apps.notifications.services import send_notification_email
from django.shortcuts import get_object_or_404
from apps.core.models import Fund
from django.utils import timezone
from django.http import JsonResponse


def request_loan(request):

    if request.method == "POST":

        member = Member.objects.get(user=request.user)

        amount_str = request.POST.get("amount", "").strip()
        reason = request.POST.get("reason", "").strip()
        months_str = request.POST.get("repayment_months", "").strip()

        try:
            amount = float(amount_str)
        except (ValueError, TypeError):
            amount = 0

        try:
            months = int(months_str)
        except (ValueError, TypeError):
            months = 0

        pending_loan_exists = Loan.objects.filter(
            member=member, status="pending"
        ).exists()

        if pending_loan_exists:
            return JsonResponse(
                {
                    "success": False,
                    "error": "You already have a loan request pending. Please wait for approval.",
                }
            )
        if member.current_loan_balance > 0:
            return JsonResponse(
                {"success": False, "error": "You already have an outstanding loan."}
            )
        try:
            loan = Loan.objects.create(
                member=member,
                amount=amount,
                reason=reason,
                repayment_months=months,
                remaining_balance=amount,
            )

            send_notification_email(
                "Loan Request Submitted",
                f"Dear {member.user.name or 'Member'}, your loan request for {loan.amount:,.2f} has been submitted successfully and is currently under review.",
                member.user.email,
            )

            return JsonResponse(
                {
                    "success": True,
                    "loan": {
                        "amount": loan.amount,
                        "remaining_balance": loan.remaining_balance,
                        "status": loan.status,
                    },
                }
            )

        except Exception:
            return JsonResponse({"success": False, "error": "Server error"})

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


def repay_loan(request, loan_id):

    if request.method == "POST":

        loan = get_object_or_404(Loan, id=loan_id)

        amount_str = request.POST.get("amount", "").strip()

        # Convert safely
        try:
            amount = float(amount_str)
        except (ValueError, TypeError):
            amount = 0

        if amount > loan.remaining_balance:
            return JsonResponse(
                {"success": False, "error": "Amount exceeds remaining loan."}
            )

        try:
            payment = LoanPayment.objects.create(
                loan=loan,
                amount=amount,
            )
            return JsonResponse(
                {
                    "success": True,
                    "payment": {
                        "amount": amount,
                        "loan_id": loan.id,
                        "status": payment.status,
                        "date": payment.payment_date.strftime("%B %d, %Y, %I:%M %p"),
                    },
                },
            )
        except Exception:
            return JsonResponse({"success": False, "error": "Server error"})

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


def approve_loan(request, loan_id):

    if request.method == "POST":

        loan = get_object_or_404(Loan, id=loan_id)

        if loan.status == "approved":
            return JsonResponse({"success": False, "error": "Already approved"})

        fund = Fund.objects.first()

        # ⚠️ Optional safety (recommended)
        if fund.total_balance < loan.amount:
            return JsonResponse(
                {"success": False, "error": "Insufficient fund balance"}
            )

        loan.status = "approved"
        loan.approval_date = timezone.now()
        loan.save()

        fund.total_balance -= loan.amount
        fund.save()

        member = loan.member
        member.current_loan_balance += loan.amount
        member.save()

        send_notification_email(
            "Loan Approved",
            f"Dear {member.user.name or 'Member'}, your loan request for {loan.amount:,.2f} has been approved. The amount has been processed to your account.",
            member.user.email,
        )

        return JsonResponse(
            {
                "success": True,
                "pending_count": Loan.objects.filter(status="pending").count(),
            }
        )

    return JsonResponse({"success": False}, status=400)


def reject_loan(request, loan_id):

    if request.method == "POST":

        loan = get_object_or_404(Loan, id=loan_id)

        if loan.status == "rejected":
            return JsonResponse({"success": False, "error": "Already rejected"})

        loan.status = "rejected"
        loan.save()

        member = loan.member

        send_notification_email(
            "Loan Rejected",
            f"Dear {member.user.name or 'Member'}, we regret to inform you that your loan request for {loan.amount:,.2f} was not approved.",
            member.user.email,
        )

        return JsonResponse(
            {
                "success": True,
                "pending_count": Loan.objects.filter(status="pending").count(),
            }
        )

    return JsonResponse({"success": False}, status=400)


def approve_repayment(request, repay_id):

    if request.method == "POST":

        payment = get_object_or_404(LoanPayment, id=repay_id)

        # ✅ Prevent duplicate processing
        if payment.status == "approved":
            return JsonResponse({"success": False, "error": "Already approved"})

        loan = payment.loan
        fund = Fund.objects.first()

        # ✅ Prevent overpayment issues
        if payment.amount > loan.remaining_balance:
            return JsonResponse(
                {"success": False, "error": "Amount exceeds remaining balance"}
            )

        # 🔥 Core Logic
        loan.remaining_balance -= payment.amount
        fund.total_balance += payment.amount

        if loan.remaining_balance <= 0:
            loan.remaining_balance = 0
            loan.status = "completed"

        loan.save()
        fund.save()

        member = loan.member
        member.current_loan_balance -= payment.amount
        member.save()

        payment.status = "approved"
        payment.save()

        send_notification_email(
            "Repayment Received",
            f"Dear {member.user.name or 'Member'}, your repayment of {payment.amount:,.2f} has been received successfully and applied to your loan balance.",
            member.user.email,
        )

        return JsonResponse(
            {
                "success": True,
                "pending_count": LoanPayment.objects.filter(status="pending").count(),
            }
        )

    return JsonResponse({"success": False}, status=400)


def reject_repayment(request, repay_id):

    if request.method == "POST":

        payment = get_object_or_404(LoanPayment, id=repay_id)

        if payment.status == "rejected":
            return JsonResponse({"success": False, "error": "Already rejected"})

        payment.status = "rejected"
        payment.save()

        member = payment.loan.member

        send_notification_email(
            "Repayment Rejected",
            f"Dear {member.user.name or 'Member'}, your repayment of {payment.amount:,.2f} could not be processed. Please review and try again or contact support(help.access.team@gmail.com).",
            member.user.email,
        )

        return JsonResponse(
            {
                "success": True,
                "pending_count": LoanPayment.objects.filter(status="pending").count(),
            }
        )

    return JsonResponse({"success": False}, status=400)
