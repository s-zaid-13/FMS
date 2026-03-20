from django.contrib import admin
from .models import Deposit


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ("member", "amount", "status", "date")
    list_filter = ("status",)
