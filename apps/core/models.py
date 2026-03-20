from django.db import models


class Fund(models.Model):

    total_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Fund Balance: {self.total_balance}"
