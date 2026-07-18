from django.db import models
from hardware.models import Hardware
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    money = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    actual_rate = models.DecimalField(max_digits=65, decimal_places=2, default=0)
    last_refresh_balance = models.DateTimeField(null=True, default=timezone.now)


class Inventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Inventory of {self.user.username} (ID: {self.id})"



class InventoryItem(models.Model):
    Inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    item = models.ForeignKey(Hardware, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_equiped = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} x {self.item.model} (Equipped: {self.is_equiped})"
