from model.models import AIInstance, AIModel
from django.shortcuts import get_object_or_404


class ModelsService:
    def __init__(self, user_id):
        self.user_id = user_id
        self.user_ia_models = AIInstance.objects.filter(user_id=user_id).select_related("model", "model__mark_model")
        
    def get_user_models(self):
        return self.user_ia_models
    
    def get_available_models(self):
        user_model_ids = self.user_ia_models.values_list("model_id", flat=True)
        avaliable_ia_models = AIModel.objects.filter(level=1).exclude(id__in=user_model_ids).select_related("mark_model")  
        return avaliable_ia_models
    
    def get_user_model(self, model_id):
        user_ia_model = self.user_ia_models.filter(model_id=model_id).first()
        return user_ia_model     
           
    def get_model_or_404(self, model_id):
        return get_object_or_404(AIModel.objects.select_related("mark_model"), id=model_id)
