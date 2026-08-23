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
    last_time_active = models.DateTimeField(null=True)

    WATTS_PRICE = {
        WattsTier.VERY_LOW: 12000,
        WattsTier.LOW: 28000,
        WattsTier.MEDIUM: 58000,
        WattsTier.HIGH: 120000,
        WattsTier.VERY_HIGH: 280000,
    }

    cpu = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, null=True, blank=True, related_name="cpu_bay")
    ssd = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, null=True, blank=True, related_name="ssd_bay")
    
    gpu1 = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, null=True, blank=True, related_name="gpu_bay1")
    gpu2 = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, null=True, blank=True, related_name="gpu_bay2")
    gpu3 = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, null=True, blank=True, related_name="gpu_bay3")
    
    ram1 = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, null=True, blank=True, related_name="ram_bay1")
    ram2 = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, null=True, blank=True, related_name="ram_bay2")
    ram3 = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, null=True, blank=True, related_name="ram_bay3")

    @property
    def get_power(self):
        power =(self.cpu.get_power() + self.gpu1.get_power() + self.gpu2.get_power() + self.gpu3.get_power() + self.ssd.get_power() + self.ram1.get_power() + self.ram2.get_power() + self.ram3.get_power())
        return power

    @property
    def get_energy_rate(self):
        energy_rate =(self.get_cpu.get_energy_rate() + self.get_gpu1.get_energy_rate() + self.get_gpu2.get_energy_rate() + self.get_gpu3.get_energy_rate() + self.get_ssd.get_energy_rate() + self.get_ram1.get_energy_rate() + self.get_ram2.get_energy_rate() + self.get_ram3.get_energy_rate())
        return energy_rate

    @property
    def price(self):
        return self.WATTS_PRICE.get(self.watts, 0)


    # get das peças
    @property
    def get_ssd(self):
        return self.ssd.item.ssd if self.ssd else None

    def __str__(self):
        return f" {self.name}"

    # get das partes do bay
    @property
    def get_cpu(self):
        return self.cpu.item.cpu if self.cpu else None

    @property
    def get_gpu1(self):
        return self.gpu1.item.gpu if self.gpu1 else None

    @property
    def get_gpu2(self):
        return self.gpu2.item.gpu if self.gpu2 else None

    @property
    def get_gpu3(self):
        return self.gpu3.item.gpu if self.gpu3 else None

    @property
    def get_ram1(self):
        return self.ram1.item.ram if self.ram1 else None

    @property
    def get_ram2(self):
        return self.ram2.item.ram if self.ram2 else None

    @property
    def get_ram3(self):
        return self.ram3.item.ram if self.ram3 else None

