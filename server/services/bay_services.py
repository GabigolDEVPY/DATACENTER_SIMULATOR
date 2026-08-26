from server.models import Bay
from user.services.inventory_services import InventoryService


class BayService:
    def __init__(self, bay_id):
        self.bay = Bay.objects.filter(id=bay_id).first()
    
    @property
    def id(self):
        return self.bay.id
    
    @property
    def components(self):
        return self.bay.components
        
    def get_power(self):
        power = sum(item.get_power for item in self.components)
        return power

    def get_total_watts(self):
        total_watts = sum(getattr(item, "watts", 0) for item in self.components)
        return total_watts

    def get_total_price(self):
        total_price = sum(getattr(item, "price", 0) for item in self.components)
        return total_price
    
    def get_total_ram(self):
        total_ram = sum(getattr(item, "ram_gb", 0) for item in self.components)
        return total_ram
    
    def get_total_vram(self):
        total_vram = sum(getattr(item, "vram", 0) for item in self.components)
        return total_vram
    
    def get_total_processors(self):
        total_processors = self.bay.get_cpu.cores if self.bay.get_cpu else 0
        return total_processors
    
    def get_total_storage(self):
        total_storage = self.bay.get_ssd.ssd_gb if self.bay.get_ssd else 0
        return total_storage
    
    def change_status(self):    
        self.bay.is_active = not self.bay.is_active
        self.bay.save(update_fields=["is_active"])
    
    
    def get_bay_detail(self, user_id):
        inventory = InventoryService(user_id=user_id)
        context = {"bay": self, 
                   "rams": inventory.get_rams(),
                   "cpus": inventory.get_cpus(),
                   "gpus": inventory.get_cpus(),
                   "ssds": inventory.get_ssds(),
                   }
        return context
        
        