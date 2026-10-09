from django.db import models

# Create your models here.
class IaInstallationTask(models.Model):
    ai_instance = models.ForeignKey("model.AIInstance", on_delete=models.CASCADE, related_name="installation_tasks")
    time = models.FloatField(null=True, blank=True)
    
    started_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Installation Task for AI Instance: {self.ai_instance.model.name}"