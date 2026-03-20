from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Member


def edit_member(request, member_id):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Invalid request"}, status=400)

    member = get_object_or_404(Member, id=member_id)

    name = request.POST.get("name", "").strip()
    total_deposited_str = request.POST.get("total_deposited", "").strip()
    loan_balance_str = request.POST.get("current_loan_balance", "").strip()
    is_active = request.POST.get("is_active") == "True"

    # Convert safely
    try:
        total_deposited = float(total_deposited_str)
    except ValueError:
        total_deposited = 0

    try:
        current_loan_balance = float(loan_balance_str)
    except ValueError:
        current_loan_balance = 0

    if not name:
        return JsonResponse({"success": False, "error": "Name is required"})

    try:
        # Update user fields
        member.user.name = name
        member.user.is_active = is_active
        member.user.save()

        # Update member fields
        member.total_deposited = total_deposited
        member.current_loan_balance = current_loan_balance
        member.save()

        return JsonResponse(
            {
                "success": True,
                "updated": {
                    "id": member.id,
                    "name": name,
                    "total_deposited": total_deposited,
                    "current_loan_balance": current_loan_balance,
                    "is_active": is_active,
                },
            }
        )

    except Exception as e:
        return JsonResponse({"success": False, "error": "Server error"})
