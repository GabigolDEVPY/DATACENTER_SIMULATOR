
from celery import shared_task
from django.db import transaction
from django.utils import timezone

from operation.models import IaInstallationTask
from model.models import AIInstance


@shared_task
def finish_model_installation(operation_id):
    with transaction.atomic():
        operation = (
            IaInstallationTask.objects
            .select_for_update()
            .get(pk=operation_id)
        )

        instance = operation.ai_instance

        # Atualiza o status da instância, não da operação.
        instance.status = AIInstance.Status.stopped
        instance.save(update_fields=["status"])

        # Exclui o registro da operação concluída.
        operation.delete()
