import csv
from django.http import HttpResponse
from apps.deposits.models import Deposit
from apps.members.models import Member
from apps.loans.models import Loan


def export_deposits_report(request):

    response = HttpResponse(content_type="text/csv")

    response["Content-Disposition"] = 'attachment; filename="deposits_report.csv"'

    writer = csv.writer(response)

    writer.writerow(["Member", "Amount", "Status", "Date"])

    deposits = Deposit.objects.select_related("member")

    for d in deposits:

        writer.writerow([d.member.user.name, d.amount, d.status, d.date])

    return response


def export_loans_report(request):

    response = HttpResponse(content_type="text/csv")

    response["Content-Disposition"] = 'attachment; filename="loans_report.csv"'

    writer = csv.writer(response)

    writer.writerow(["Member", "Amount", "Status", "Remaining"])

    loans = Loan.objects.select_related("member")

    for l in loans:

        writer.writerow([l.member.user.name, l.amount, l.status, l.remaining_balance])

    return response


def export_members_report(request):

    response = HttpResponse(content_type="text/csv")

    response["Content-Disposition"] = 'attachment; filename="members_report.csv"'

    writer = csv.writer(response)

    writer.writerow(["Name", "Email", "Total Deposited", "Loan Balance"])

    members = Member.objects.select_related("user")

    for m in members:

        writer.writerow(
            [m.user.name, m.user.email, m.total_deposited, m.current_loan_balance]
        )

    return response
