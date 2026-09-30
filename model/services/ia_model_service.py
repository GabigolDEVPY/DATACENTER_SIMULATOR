from model.services.models_service import ModelsService
from server.services.bay_service import BayService

class IaModelService:
    @staticmethod
    def install_ia_model(user_id, data):
        models_service = ModelsService(user_id)
        
        instance = models_service.get_user_model(data.get("ia_model_id"))  # retorna um AIInstance
        
        if not instance:
            raise ValueError("Modelo não encontrado")
        
        model = instance.model
        
        bay_service = BayService(bay_id=data.get("ia_model_id"))
        
        bay_service.allocate_space_for_model(model, model.storage_gb) #cria uma alocação do modelo dentro da bay
        
        instance.status = "installing"
        
        instance.save(update_fields=["status"])
        time = 1
              
        return time
        