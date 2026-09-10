from decimal import Decimal
from dataclasses import dataclass

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
    
    @classmethod
    def from_model(cls, model, status):
        return cls(
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
