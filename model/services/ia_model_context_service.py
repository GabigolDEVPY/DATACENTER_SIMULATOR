from model.viewmodels.ia_model_view_model import IaModelViewModel
from model.services.model_service import ModelService
from user.models import User
from server.models import Bay
from server.services.bay_service import BayService



class IaModelContextServices:
    @staticmethod
    def get_ia_models(user_id):
        service = ModelService(user_id=user_id)
        user_ia_models = [
            IaModelViewModel.from_model(item.model, status=item.status)
            for item in service.get_user_models() 
            ]
        
        available_ia_models = [
            IaModelViewModel.from_model(model, status="stopped")
            for model in service.get_available_models()
        ]
        
        return {"user_ia_models": user_ia_models, "ia_models": available_ia_models}
    
    
    
    @staticmethod
    def get_ia_model(user_id, model_id):
        context = {}
        service = ModelService(user_id)
        ia_model = service.get_user_model(model_id)

        if ia_model:
            model_view = IaModelViewModel.from_model(ia_model.model, status=ia_model.status)
            bays = Bay.objects.filter(rack__user_id=user_id)
            bays_avaliable = []
            
            for bay in bays:
                bay_mod = BayService(bay.id)
                model_view_alocatte = bay_mod.get_allocate_space_storage()
                bay_storage_availabe = bay_mod.get_total_storage() - model_view_alocatte
                if bay_storage_availabe >= model_view.storage_gb:
                    bays_avaliable.append(bay)
            context["bays_avaliable"] = bays_avaliable
            
            
        else:
            model = service.get_model_or_404(model_id)
            model_view = IaModelViewModel.from_model(model, status=None)        
            
                
        context["model"] = model_view
        return context
    