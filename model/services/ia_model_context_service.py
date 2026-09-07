from decimal import Decimal
from model.models import AIModel
from django.shortcuts import get_object_or_404
from user.services.inventory_services import InventoryService
from dataclasses import dataclass

@dataclass
class IaModelViewModel:
    id: int
    name: str
    level: int
    price: int
    base_revenue: Decimal
    is_running: bool
    # specs
    mark_model: str
    gpu_vram: int
    ram_gb: int
    storage_gb: int
    params: int


class IaModelContextServices:
    @staticmethod
    def get_ia_models(user_id):
        ia_models_user = InventoryService(user_id=user_id).get_ia_models()
        ia_models = AIModel.objects.filter(level=1)
              
        user_ia_models = [
            IaModelViewModel(
                id = ia_model.model.id,
                name = ia_model.model.name,
                level = ia_model.model.level,
                price = ia_model.model.price,
                base_revenue = ia_model.model.base_revenue,
                is_running = ia_model.is_running,
                mark_model = ia_model.model.mark_model.name,
                gpu_vram = ia_model.model.gpu_vram,
                ram_gb = ia_model.model.ram_gb,
                storage_gb = ia_model.model.storage_gb,
                params = ia_model.model.params
            )
            for ia_model in ia_models_user
        ]
        
        return user_ia_models, ia_models