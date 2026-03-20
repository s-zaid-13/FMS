from django.urls import path
from . import views

urlpatterns = [
    path("deposits/", views.export_deposits_report, name="export_deposits_report"),
    path("loans/", views.export_loans_report, name="export_loans_report"),
    path("members/", views.export_members_report, name="export_members_report"),
]
