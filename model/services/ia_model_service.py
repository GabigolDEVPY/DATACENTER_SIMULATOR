from decimal import Decimal

from model.services.models_service import ModelsService
from server.services.bay_service import BayService
from operation.services.model_operation_service import InstallationService


class IaModelService:

    @staticmethod
    def install_ia_model(user_id, model_id, bay_id):
        models_service = ModelsService(user_id)

        instance = models_service.get_user_model(model_id)

        if not instance:
            raise ValueError("Modelo não encontrado")

        model = instance.model

        bay_service = BayService(bay_id=bay_id)

        bay_service.allocate_space_for_model(
            model,
            model.storage_gb
        )

        ssd = bay_service._get_component("ssd")

        time = (
            Decimal(str(model.storage_gb))
            * Decimal("1024")
            / Decimal(str(ssd.speed))
            * Decimal("12")
        )
        
        #criar a instância da instalação
        InstallationService.start(instance, time)

        progress_per_second = Decimal("100") / time

        instance.status = "installing"
        instance.save(update_fields=["status"])

        return float(progress_per_second)