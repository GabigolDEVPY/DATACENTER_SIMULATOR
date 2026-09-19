from django.db import models

class MarkModel(models.Model):
    name = models.CharField(max_length=100)

# Create your models here.
class AIModel(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=1)
    mark_model = models.ForeignKey(MarkModel, on_delete=models.CASCADE, related_name='ai_models')
    # Requisitos de hardware
    gpu_vram = models.IntegerField()         
    ram_gb = models.IntegerField()           
    storage_gb = models.IntegerField()      
    price = models.BigIntegerField()
    base_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    params = models.BigIntegerField() 
    
    def __str__(self):
        return f"{self.name} level: {self.level}"
    
    
class AIInstance(models.Model):
    class Status(models.TextChoices):
        stopped = "stopped", "Stopped"
        running = "running", "Running"
        training = "training", "Training"
        moving = "moving", "Moving"
        not_installed = "not_installed", "Not Installed"
    
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="ai_instances")
    
    model = models.ForeignKey(AIModel,on_delete=models.CASCADE,related_name="instances")


    status = models.CharField(max_length=20, choices=Status.choices, default=Status.not_installed)
    started_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.model.name} (Status: {self.status})"
    
    
class AIInstanceBay(models.Model):
    ai_instance = models.ForeignKey(AIInstance, on_delete=models.CASCADE, related_name="allocated_bays")
    bay = models.ForeignKey("server.Bay",on_delete=models.CASCADE,related_name="ai_allocations")
    
    def __str__(self):
        return f"AI Instance: {self.ai_instance.model.name} allocated to Bay: {self.bay.name}"