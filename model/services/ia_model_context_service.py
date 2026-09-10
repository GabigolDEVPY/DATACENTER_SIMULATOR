from django.shortcuts import get_object_or_404
from model.models import AIModel
from user.services.inventory_services import InventoryService
from model.viewmodels.ia_model_view_model import IaModelViewModel



class IaModelContextServices:
    @staticmethod
    def get_ia_models(user_id):
        ia_models_user = InventoryService(user_id=user_id).get_ia_models().select_related("model", "model__mark_model")
        user_model_ids = ia_models_user.values_list("model_id", flat=True)
        
        avaliable_ia_models = AIModel.objects.filter(level=1).exclude(id__in=user_model_ids).select_related("mark_model")
              
        user_ia_models = [
            IaModelViewModel.from_model(item.model, status=item.status)
            for item in ia_models_user
        ]
        
        avaliable_ia_models = [
            IaModelViewModel.from_model(model, status="stopped")
            for model in avaliable_ia_models
        ]
        
        return user_ia_models, avaliable_ia_models
    
    
    
    
    
    @staticmethod
    def get_ia_model(user_id, model_id):
        ia_model = (
            InventoryService(user_id=user_id)
            .get_ia_models()
            .select_related("model", "model__mark_model")
            .filter(model_id=model_id)
            .first()
        )


        if ia_model:
            return IaModelViewModel.from_model(ia_model.model, status=ia_model.status)
        

        model = get_object_or_404(
            AIModel.objects.select_related("mark_model"),
            id=model_id
        )

        return IaModelViewModel.from_model(model, status=None)