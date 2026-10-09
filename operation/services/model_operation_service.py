from operation.models import IaInstallationTask
from django.utils import timezone
from datetime import timedelta
from operation.tasks import finish_model_installation
from django.db import transaction


class InstallationService:

    @staticmethod
    def start(instance, time):
        print("entrou aqui")

        duration_seconds = float(time)

        finished_at = timezone.now() + timedelta(
            seconds=duration_seconds
        )

        instance.finished_at = finished_at
        instance.save(update_fields=["finished_at"])

        transaction.on_commit(
            lambda: finish_model_installation.apply_async(
                args=[instance.pk],
                countdown=duration_seconds,
            )
        )
        
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