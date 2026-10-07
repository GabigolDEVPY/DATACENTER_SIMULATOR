from operation.models import IaInstallationTask
from django.utils import timezone
from datetime import timedelta

class InstallationService:

    @staticmethod
    def start(instance, time):
        finished_at = timezone.now() + timedelta(seconds=time) # hora de termino


        task = IaInstallationTask.objects.create(
            ai_instance=instance,
            finished_at=finished_at
        )

        return task