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
        power =(
            (self.get_cpu.get_power() if self.get_cpu else 0 )+
            (self.get_gpu1.get_power() if self.get_gpu1 else 0)+
            (self.get_gpu2.get_power() if self.get_gpu2 else 0)+
            (self.get_gpu3.get_power() if self.get_gpu3 else 0)+
            (self.get_ssd.get_power() if self.get_ssd else 0)+
            (self.get_ram1.get_power() if self.get_ram1 else 0)+
            (self.get_ram2.get_power() if self.get_ram2 else 0)+
            (self.get_ram3.get_power() if self.get_ram3 else 0)
        )
        return power

    @property
    def get_total_watts(self):
        watts = (
            (self.get_cpu.watts if self.get_cpu else 0 )+
            (self.get_gpu1.watts if self.get_gpu1 else 0)+
            (self.get_gpu2.watts if self.get_gpu2 else 0)+
            (self.get_gpu3.watts if self.get_gpu3 else 0)+
            (self.get_ssd.watts if self.get_ssd else 0)+
            (self.get_ram1.watts if self.get_ram1 else 0)+
            (self.get_ram2.watts if self.get_ram2 else 0)+
            (self.get_ram3.watts if self.get_ram3 else 0)
        )
        return watts

    @property
    def get_total_price(self):
        price = (
            (self.get_cpu.price if self.get_cpu else 0 )+
            (self.get_gpu1.price if self.get_gpu1 else 0)+
            (self.get_gpu2.price if self.get_gpu2 else 0)+
            (self.get_gpu3.price if self.get_gpu3 else 0)+
            (self.get_ssd.price if self.get_ssd else 0)+
            (self.get_ram1.price if self.get_ram1 else 0)+
            (self.get_ram2.price if self.get_ram2 else 0)+
            (self.get_ram3.price if self.get_ram3 else 0)
        )
        return price
    
    @property 
    def get_total_ram(self):
        total_ram = 0
        
        if self.get_ram1:
            total_ram += self.get_ram1.gb
        if self.get_ram2:
            total_ram += self.get_ram2.gb
        if self.get_ram3:
            total_ram += self.get_ram3.gb
            
        return total_ram
    
    @property
    def get_total_vram(self):
        total_vram = 0
        if self.get_gpu1:
            total_vram += self.get_gpu1.vram
        if self.get_gpu2:
            total_vram += self.get_gpu2.vram
        if self.get_gpu3:
            total_vram += self.get_gpu3.vram
        return total_vram
    
    @property
    def get_total_processors(self):
        total_processors = (self.get_cpu.cores)
        return total_processors
    
    @property
    def get_total_storage(self):
        total_storage = (self.get_ssd.gb)
        return total_storage
    


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

