from django.urls import path

from .views import (
    approve_loan,
    approve_repayment,
    reject_loan,
    reject_repayment,
    request_loan,
    repay_loan,
)

urlpatterns = [
    path("request/", request_loan, name="request_loan"),
    path("repay/<int:loan_id>/", repay_loan, name="repay_loan"),
    path("approve_loan/<int:loan_id>/", approve_loan, name="approve_loan"),
    path(
        "approve_repayment/<int:repay_id>/", approve_repayment, name="approve_repayment"
    ),
    path("reject_loan/<int:loan_id>/", reject_loan, name="reject_loan"),
    path(
        "reject_repayment/<int:repay_id>/",
        reject_repayment,
        name="reject_repayment",
    ),
]
