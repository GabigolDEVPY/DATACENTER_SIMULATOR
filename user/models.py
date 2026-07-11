from django.db import models
from hardware.models import Hardware

class Inventory(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    

class InventoryItem(models.Model):
    Inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    # reference the user's items
    item = models.ForeignKey(Hardware, on_delete=models.CASCADE)
    # quantity of items
    quantity = models.IntegerField(max_length=10)
    # if item already in used
    is_equiped = models.BooleanField(default=False)
    