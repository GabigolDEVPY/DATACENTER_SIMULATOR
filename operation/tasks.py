
from celery import shared_task
from django.db import transaction
from django.utils import timezone

from operation.models import ModelOperation
from model.models import AIInstance


@shared_task
def finish_model_installation(operation_id):
    with transaction.atomic():
        operation = (
            ModelOperation.objects
            .select_for_update()
            .get(pk=operation_id)
        )

        # Evita finalizar uma operação cancelada ou já concluída.
        if operation.status != "installing":
            return

        instance = AIInstance.objects.get(
            pk=operation.instance_id
        )

        instance.status = AIInstance.Status.installed
        instance.save(update_fields=["status"])

        operation.status = "finished"
        operation.finished_at = timezone.now()
        operation.save(
            update_fields=["status", "finished_at"]
        )
