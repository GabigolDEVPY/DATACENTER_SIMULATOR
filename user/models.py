from django.db import models


from hardware.models import Hardware

# Create your models here.
class InventoryItem(models.Model):
    item = models.ForeignKey(Hardware, on_delete=models.CASCADE)