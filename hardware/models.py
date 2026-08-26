from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class Hardware(models.Model):
    type = models.CharField(max_length=300)
    model = models.CharField(max_length=100)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
    price = models.IntegerField()
    watts = models.IntegerField()
    rarity = models.CharField(max_length=30)
    is_active = models.BooleanField(default=False)
    
        
    def __str__(self):
        return f"{self.brand.name} {self.model}"


class CPU(Hardware):
    cores = models.IntegerField()
    threads = models.IntegerField()
    cpu_ghz = models.FloatField()
    cpu_score_bottleneck = models.IntegerField()

    @property
    def get_power(self):
        return (
            self.cores * 50 +
            self.threads * 80 +
            self.cpu_ghz * 100 +
            self.score_bottleneck * 300
        )
    


class GPU(Hardware):
    gpu_score_bottleneck = models.IntegerField()
    vram = models.IntegerField()
    gpu_mhz = models.FloatField()

    @property
    def get_power(self):
        return (
            self.vram * 200 +
            self.gpu_mhz +
            self.gpu_score_bottleneck * 500
        )
    

class RAM(Hardware):
    ram_gb = models.IntegerField()
    ram_mhz = models.IntegerField()

    @property
    def get_power(self):
        return (
            self.ram_gb * 300 +
            self.ram_mhz * 2
        )



class SSD(Hardware):
    ssd_gb = models.IntegerField()
    speed = models.IntegerField()

    @property
    def get_power(self):
        return (
            self.ssd_gb * 5 +
            self.speed * 3
        )
    