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
    is_active = models.BooleanField(default=False)
    last_time_active = models.DateTimeField(null=True)


    cpu = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, null=True, blank=True, related_name="cpu_bay")
    ssd = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, null=True, blank=True, related_name="ssd_bay")
    
    gpu1 = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, null=True, blank=True, related_name="gpu_bay1")
    gpu2 = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, null=True, blank=True, related_name="gpu_bay2")
    gpu3 = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, null=True, blank=True, related_name="gpu_bay3")
    
    ram1 = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, null=True, blank=True, related_name="ram_bay1")
    ram2 = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, null=True, blank=True, related_name="ram_bay2")
    ram3 = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, null=True, blank=True, related_name="ram_bay3")


    @property
    def components(self):
            return filter(None, [self.get_cpu, self.get_ssd, self.get_gpu1, self.get_gpu2, self.get_gpu3, self.get_ram1, self.get_ram2, self.get_ram3])
     
    
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

