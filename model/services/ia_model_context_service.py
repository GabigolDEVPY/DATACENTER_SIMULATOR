from model.services.models_service import ModelsService
from model.viewmodels.bay_option_view_model import BayOption
from model.viewmodels.ia_model_view_model import IaModelViewModel
from server.models import Bay
from server.services.bay_service import BayService


class IaModelContextService:
    @staticmethod
    # modelos da tela inicial de modelos, modelos do usuário de modelos não adquiridos
    def get_ia_models(user_id):
        models_service = ModelsService(user_id=user_id)

        return {
            "user_ia_models": [
                IaModelViewModel.from_model(instance.model, status=instance.status)
                for instance in models_service.get_user_models()
            ],
            "ia_models": [
                IaModelViewModel.from_model(model, status="stopped")
                for model in models_service.get_available_models()
            ],
        }


    @classmethod
    def get_model_context(cls, user_id, model_id):
        models_service = ModelsService(user_id)
        instance = models_service.get_user_model(model_id)

        if not instance:
            model = models_service.get_model_or_404(model_id)
            return {"model": IaModelViewModel.from_model(model, status=None)}

        model = instance.model
        model_view = IaModelViewModel.from_model(model, status=instance.status)
        context = {"model": model_view}

        if model_view.status == "not_installed":
            context["bays_avaliable"] = cls._get_bays_for_install(user_id, model)
            
        elif model_view.status == "stopped":
            context["bays_avaliable"] = cls._get_bays_for_run(user_id, model)

        return context
    
    
    @staticmethod
    def _get_user_bay_services(user_id):
        bays = Bay.objects.filter(rack__user_id=user_id).select_related(
            *BayService.SELECT_RELATED
        )
        return [BayService(bay=bay) for bay in bays]

    @classmethod
    def _get_bays_for_install(cls, user_id, model_view):
        return [
            BayOption(bay_service.bay, None)
            for bay_service in cls._get_user_bay_services(user_id)
            if bay_service.has_storage_for(model_view.storage_gb)
        ]

    @classmethod
    def _get_bays_for_run(cls, user_id, model):
        """Bays livres para rodar o modelo, já com o máximo de instâncias possíveis."""
        return [
            BayOption(bay_service.bay, bay_service.get_max_instances_available(model))
            for bay_service in cls._get_user_bay_services(user_id)
            if bay_service.has_storage_for(model.storage_gb)
        ]

    
    @staticmethod
    def install_ia_model(user_id, data):
        service = ModelsService(user_id)
        
        ia_instance = service.get_user_model(data.get("ia_model_id"))  # retorna um AIInstance
        BayService(bay_id=data.get("bay_id")).allocate_space_for_model(ia_instance.model, ia_instance.model.storage_gb) #cria uma alocação do modelo dentro da bay
        ia_instance.status = "installing"
        ia_instance.save(update_fields=["status"])
        time = 1
              
        return time
        
        