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
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.brand.name} {self.model}"


class CPU(Hardware):
    cores = models.IntegerField()
    threads = models.IntegerField()
    ghz = models.FloatField()
    score_bottleneck = models.IntegerField()

    def get_power(self):
        return (
            self.cores * 50 +
            self.threads * 80 +
            self.ghz * 100 +
            self.score_bottleneck * 300
        )
        


class GPU(Hardware):
    score_bottleneck = models.IntegerField()
    vram = models.IntegerField()
    mhz = models.FloatField()

    def get_power(self):
        return (
            self.vram * 200 +
            self.mhz +
            self.score_bottleneck * 500
        )


class RAM(Hardware):
    gb = models.IntegerField()
    mhz = models.IntegerField()

    def get_power(self):
        return (
            self.gb * 300 +
            self.mhz * 2
        )


class SSD(Hardware):
    gb = models.IntegerField()
    speed = models.IntegerField()

    def get_power(self):
        return (
            self.gb * 5 +
            self.speed * 3
        )