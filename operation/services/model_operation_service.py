from operation.models import IaInstallationTask
from django.utils import timezone
from datetime import timedelta
from operation.tasks import finish_model_installation
from django.db import transaction


class InstallationService:

    @staticmethod
    def start(instance, time):
        duration_seconds = float(time)

        finished_at = timezone.now() + timedelta(
            seconds=duration_seconds
        )

        task = IaInstallationTask.objects.create(
            ai_instance=instance,
            finished_at=finished_at,
            time=time,
        )
        print("duration", duration_seconds)

        transaction.on_commit(
            lambda: finish_model_installation.apply_async(
                args=[task.pk],
                countdown=duration_seconds,
            )
        )

        return task
    
    def get_status(instance):
        task = IaInstallationTask.objects.filter(ai_instance=instance).first()
        if not task or not task.finished_at:
            return None

        remaining_time = (task.finished_at - timezone.now()).total_seconds()
        return max(remaining_time, 0)