from django.contrib import admin
from django.urls import path, include

from home_view import home

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("members/", include("apps.members.urls")),
    path("deposits/", include("apps.deposits.urls")),
    path("loans/", include("apps.loans.urls")),
    path("dashboard/", include("apps.dashboard.urls")),
    path("reports/", include("apps.reports.urls")),
    path("accounts/", include("allauth.urls")),
]
