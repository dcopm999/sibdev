from customers import models
from django.contrib import admin


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("customer", "item", "date")
