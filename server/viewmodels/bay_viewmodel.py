from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class BayViewModel:
    id: int
    name: str
    is_active: bool
    
    cpu: Optional[Any]
    ssd: Optional[Any]
    
    gpu1: Optional[Any]
    gpu2: Optional[Any]
    gpu3: Optional[Any]
    
    ram1: Optional[Any]
    ram2: Optional[Any]
    ram3: Optional[Any]
    
    total_watts: int
    total_price: int
    total_ram: int
    total_vram: int
    total_processors: int
    total_storage: int
    