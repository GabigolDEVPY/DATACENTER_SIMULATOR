from django.db import models
from user.models import InventoryItem
from user.models import User



# Create your models here.
class Rack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="racks")
    name = models.CharField(max_length=80, blank=False)
    bay = models.IntegerField(blank=False, null=False)


    def __str__(self):
        return f" {self.name}"


class Bay(models.Model):
    name = models.CharField(max_length=80, blank=False)
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE, related_name="bays")

    class WattsTier(models.TextChoices):
        VERY_LOW = "1KW", "Very Low (1KW)"
        LOW = "2KW", "Low (2KW)"
        MEDIUM = "4KW", "Medium (4KW)"
        HIGH = "8KW", "HIGH (8KW)"
        VERY_HIGH = "16KW", "HIGH (16KW)"

    is_active = models.BooleanField(default=False)
    watts = models.CharField(max_length=10, choices=WattsTier.choices, default=WattsTier.LOW)

    WATTS_PRICE = {
        WattsTier.VERY_LOW: 12000,
        WattsTier.LOW: 28000,
        WattsTier.MEDIUM: 58000,
        WattsTier.HIGH: 120000,
        WattsTier.VERY_HIGH: 280000,
    }

    ram = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, null=True, blank=True, related_name="ram_bay")
    cpu = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, null=True, blank=True, related_name="cpu_bay")
    gpu = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, null=True, blank=True, related_name="gpu_bay")
    ssd = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, null=True, blank=True, related_name="ssd_bay")

    @property
    def price(self):
        return self.WATTS_PRICE.get(self.watts, 0)

    @property
    def get_cpu(self):
        return self.cpu.item.cpu if self.cpu else None

    @property
    def get_gpu(self):
        return self.gpu.item.gpu if self.gpu else None

    @property
    def get_ram(self):
        return self.ram.item.ram if self.ram else None

    @property
    def get_ssd(self):
        return self.ssd.item.ssd if self.ssd else None

    def __str__(self):
        return f" {self.name}"
