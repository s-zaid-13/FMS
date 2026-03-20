from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from apps.notifications.services import send_notification_email
from apps.members.models import Member
from .models import Deposit
from apps.core.models import Fund


def create_deposit(request):

    if request.method == "POST":
        member = Member.objects.get(user=request.user)
        amount_str = request.POST.get("amount", "").strip()
        notes = request.POST.get("notes", "").strip()

        try:
            amount = float(amount_str)
        except (ValueError, TypeError):
            amount = 0

        deposit = Deposit.objects.create(
            member=member,
            amount=amount,
            notes=notes,
        )
        return JsonResponse(
            {
                "success": True,
                "deposit": {
                    "amount": deposit.amount,
                    "date": deposit.date.strftime("%B %d, %Y, %I:%M %p"),
                    "status": deposit.status,
                },
            }
        )

    return JsonResponse({"error": "Invalid request"}, status=400)


def approve_deposit(request, deposit_id):

    if request.method == "POST":

        deposit = get_object_or_404(Deposit, id=deposit_id)
        fund = Fund.objects.first()

        if deposit.status == "approved":
            return JsonResponse({"success": False, "error": "Already approved"})

        deposit.status = "approved"
        deposit.save()

        member = deposit.member

        member.total_deposited += deposit.amount
        fund.total_balance += deposit.amount

        fund.save()
        member.save()

        send_notification_email(
            "Deposit Approved",
            f"Dear { member.user.name or 'User'}, your deposit of {deposit.amount} has been successfully approved and added to your account balance.",
            member.user.email,
        )
        pending_count = Deposit.objects.filter(status="pending").count()

        return JsonResponse({"success": True, "pending_count": pending_count})

    return JsonResponse({"success": False}, status=400)


def reject_deposit(request, deposit_id):

    if request.method == "POST":

        deposit = get_object_or_404(Deposit, id=deposit_id)

        if deposit.status == "rejected":
            return JsonResponse({"success": False, "error": "Already rejected"})

        deposit.status = "rejected"
        deposit.save()

        member = deposit.member

        send_notification_email(
            "Deposit Rejected",
            f"Dear {member.user.name or 'Member'}, your deposit of {deposit.amount:,.2f} could not be approved. Please contact support(help.access.team@gmail.com) or try again if needed.",
            member.user.email,
        )

        return JsonResponse(
            {
                "success": True,
                "pending_count": Deposit.objects.filter(status="pending").count(),
            }
        )

    return JsonResponse({"success": False}, status=400)
