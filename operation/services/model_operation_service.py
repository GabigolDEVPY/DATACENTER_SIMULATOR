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

        transaction.on_commit(
            lambda: finish_model_installation.apply_async(
                args=[task.pk],
                countdown=duration_seconds,
            )
        )

        return task
    
    @staticmethod
    def get_status(instance):
        task = IaInstallationTask.objects.filter(ai_instance=instance).first()

        if not task or not task.finished_at or not task.started_at:
            return None, None

        total_time = (task.finished_at - task.started_at).total_seconds()

        if total_time <= 0:
            return 100.0, 1

        elapsed_time = (timezone.now() - task.started_at).total_seconds()

        progress = min(max((elapsed_time / total_time) * 100, 0),100)

        interval = 100 / total_time

        return progress, interval