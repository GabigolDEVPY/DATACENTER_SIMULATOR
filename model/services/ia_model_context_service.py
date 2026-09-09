from decimal import Decimal
from model.models import AIModel
from django.shortcuts import get_object_or_404
from user.services.inventory_services import InventoryService
from dataclasses import dataclass
from enum import Enum

class status(Enum):
    training = 1
    

@dataclass
class IaModelViewModel:
    id: int
    name: str
    level: int
    price: int
    base_revenue: Decimal
    status: str
    # specs
    mark_model: str
    gpu_vram: int
    ram_gb: int
    storage_gb: int
    params: int


class IaModelContextServices:
    @staticmethod
    def get_ia_models(user_id):
        ia_models_user = InventoryService(user_id=user_id).get_ia_models().select_related("model", "model__mark_model")
        user_model_ids = ia_models_user.values_list("model_id", flat=True)
        
        ia_models = AIModel.objects.filter(level=1).exclude(id__in=user_model_ids).select_related("mark_model")
              
        user_ia_models = [
            IaModelViewModel(
                id = ia_model.model.id,
                name = ia_model.model.name,
                level = ia_model.model.level,
                price = ia_model.model.price,
                base_revenue = ia_model.model.base_revenue,
                status = ia_model.status,
                mark_model = ia_model.model.mark_model.name,
                gpu_vram = ia_model.model.gpu_vram,
                ram_gb = ia_model.model.ram_gb,
                storage_gb = ia_model.model.storage_gb,
                params = ia_model.model.params
            )
            for ia_model in ia_models_user
        ]
        
        return user_ia_models, ia_models
    
    @staticmethod
    def get_ia_model(user_id, model_id):
        ia_models_user = (
            InventoryService(user_id=user_id)
            .get_ia_models()
            .select_related("model", "model__mark_model")
        )

        ia_model = ia_models_user.filter(model_id=model_id).first()

        if ia_model:
            model = ia_model.model
            status = ia_model.status
        else:
            model = get_object_or_404(
                AIModel.objects.select_related("mark_model"),
                id=model_id
            )
            status = False

        return IaModelViewModel(
            id=model.id,
            name=model.name,
            level=model.level,
            price=model.price,
            base_revenue=model.base_revenue,
            status=status,
            mark_model=model.mark_model.name,
            gpu_vram=model.gpu_vram,
            ram_gb=model.ram_gb,
            storage_gb=model.storage_gb,
            params=model.params,
        )