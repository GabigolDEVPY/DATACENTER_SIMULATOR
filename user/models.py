from django.db import models
from hardware.models import Hardware
from model.models import AIModel
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    money = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    energy = models.PositiveIntegerField(default=0)
    actual_energy_rate = models.DecimalField(max_digits=65, decimal_places=2, default=0)
    actual_rate = models.DecimalField(max_digits=65, decimal_places=2, default=0)
    last_refresh_balance = models.DateTimeField(null=True, default=timezone.now)


class Inventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Inventory of {self.user.username} (ID: {self.id})"



class InventoryItem(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    item = models.ForeignKey(Hardware, on_delete=models.CASCADE)
    is_equiped = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.item.model} (Equipped: {self.is_equiped})"
    
    
    
class InventoryIaModel(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="ia_models")
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    is_running = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.model.name} (Equipped: {self.is_running})"