from django.urls import path
from .views import admin_dashboard, dashboard, member_dashboard

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("admin/", admin_dashboard, name="admin_dashboard"),
    path("member/", member_dashboard, name="member_dashboard"),
]
