from operation.models import IaInstallationTask
from django.utils import timezone
from datetime import timedelta

class InstallationService:

    @staticmethod
    def start(instance, time):
        print("entrou aqui")
        finished_at = timezone.now() + timedelta(seconds=float(time)) # hora de termino


        task = IaInstallationTask.objects.create(
            ai_instance=instance,
            finished_at=finished_at,
            time=time
        )

        return task
    
    def get_status(instance):
        task = IaInstallationTask.objects.filter(ai_instance=instance).first()
        actual_time = task.finished_at - task.started_at
        if timezone.now() >= task.finished_at:
            return None
        return task.time