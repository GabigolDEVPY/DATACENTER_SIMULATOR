from model.viewmodels.ia_model_view_model import IaModelViewModel
from model.services.model_service import ModelService



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
        service = ModelService(user_id)
        ia_model = service.get_user_model(model_id)

        if ia_model:
            model_view = IaModelViewModel.from_model(ia_model.model, status=ia_model.status)
            
        else:
            model = service.get_model_or_404(model_id)
            model_view = IaModelViewModel.from_model(model, status=None)        
            

        return {"model": model_view}