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

    def __str__(self):
        return f"{self.user.username}"