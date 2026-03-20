from django.urls import path
from .views import edit_member

urlpatterns = [
    path("admin/member/edit/<int:member_id>/", edit_member, name="edit_member"),
]
