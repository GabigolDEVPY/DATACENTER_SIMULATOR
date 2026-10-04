from django.db import models

# Create your models here.
class IaInstallationTask(models.Model):
    ai_instance = models.ForeignKey("model.AIInstance", on_delete=models.CASCADE, related_name="installation_tasks")
    allocate_bay = models.ForeignKey("server.StorageAllocation", on_delete=models.CASCADE, related_name="installation_tasks")
    
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Installation Task for AI Instance: {self.ai_instance.model.name} on Bay: {self.allocate_bay.bay.name}"