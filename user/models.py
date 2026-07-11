from django.db import models
from hardware.models import Hardware



class Inventory(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Inventory of {self.user.username} (ID: {self.id})"



class InventoryItem(models.Model):
    Inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    # reference the user's items
    item = models.ForeignKey(Hardware, on_delete=models.CASCADE)
    # quantity of items
    quantity = models.IntegerField()
    # if item already in used
    is_equiped = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.quantity} x {self.item.model} (Equipped: {self.is_equiped})"