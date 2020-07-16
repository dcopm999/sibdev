from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Customer(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.PositiveSmallIntegerField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.customer}: {self.item}"

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        unique_together = (("customer", "item", "date"),)
