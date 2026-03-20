from django.urls import path
from .views import approve_deposit, create_deposit, reject_deposit

urlpatterns = [
    path("new/", create_deposit, name="create_deposit"),
    path("approve_deposit/<int:deposit_id>/", approve_deposit, name="approve_deposit"),
    path("reject_deposit/<int:deposit_id>/", reject_deposit, name="reject_deposit"),
]
