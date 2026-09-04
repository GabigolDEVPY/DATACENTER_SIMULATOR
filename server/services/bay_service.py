from server.models import Bay
from server.viewmodels.bay_viewmodel import BayViewModel
from django.shortcuts import get_object_or_404
from user.services import inventory_services
from user.models import InventoryItem
from django.db import transaction


class BayService:
    def __init__(self, bay_id):
        self.bay = get_object_or_404(Bay.objects.select_related(
            "cpu__item__cpu",
            "ssd__item__ssd",
            "gpu1__item__gpu",
            "gpu2__item__gpu",
            "gpu3__item__gpu",
            "ram1__item__ram",
            "ram2__item__ram",
            "ram3__item__ram"
        ), id=bay_id )
    
        self.components = list(filter(None, [
            self.bay.cpu.item.cpu if self.bay.cpu else None,
            self.bay.ssd.item.ssd if self.bay.ssd else None,
            self.bay.gpu1.item.gpu if self.bay.gpu1 else None,
            self.bay.gpu2.item.gpu if self.bay.gpu2 else None,
            self.bay.gpu3.item.gpu if self.bay.gpu3 else None,
            self.bay.ram1.item.ram if self.bay.ram1 else None,
            self.bay.ram2.item.ram if self.bay.ram2 else None,
            self.bay.ram3.item.ram if self.bay.ram3 else None,
            ]))
    
        
    def get_power(self):
        power = sum(item.get_power() for item in self.components)
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
        total_processors = self.bay.cpu.item.cpu.cores if self.bay.cpu else 0
        return total_processors
    
    def get_total_storage(self):
        total_storage = self.bay.ssd.item.ssd.ssd_gb if self.bay.ssd else 0
        return total_storage
    
    def change_status(self):    
        self.bay.is_active = not self.bay.is_active
        self.bay.save(update_fields=["is_active"])
    
    
    def get_view_model(self):
        return BayViewModel(
           id=self.bay.id,
           name=self.bay.name,
           is_active=self.bay.is_active,

           cpu=self.bay.cpu.item.cpu if self.bay.cpu else None,
           ssd=self.bay.ssd.item.ssd if self.bay.ssd else None,
           gpu1=self.bay.gpu1.item.gpu if self.bay.gpu1 else None,
           gpu2=self.bay.gpu2.item.gpu if self.bay.gpu2 else None,
           gpu3=self.bay.gpu3.item.gpu if self.bay.gpu3 else None,
           ram1=self.bay.ram1.item.ram if self.bay.ram1 else None,
           ram2=self.bay.ram2.item.ram if self.bay.ram2 else None,
           ram3=self.bay.ram3.item.ram if self.bay.ram3 else None,

           total_watts=self.get_total_watts(),
           total_price=self.get_total_price(),
           total_ram=self.get_total_ram(),
           total_vram=self.get_total_vram(),
           total_processors=self.get_total_processors(),
           total_storage=self.get_total_storage(),      
                 
        )        
        
    def change_status(self):
        self.bay.is_active = not self.bay.is_active
        self.bay.save(update_fields="is_active")
        return self.get_view_model()

    def change_component(self, data):
        type = data.get("action")
        component = data.get("component")
        
        if type == "change" and not self.bay.is_active:
            with transaction.atomic():
                new_component = get_object_or_404(InventoryItem, id=data.get("component_id"), is_equiped=False)
                
                old_component = getattr(self.bay, component)
                
                if old_component:
                    old_component.is_equiped = False
                    old_component.save(update_fields=["is_equiped"])
                

                                
                new_component.is_equiped = True
                new_component.save(update_fields=["is_equiped"])
                
                setattr(self.bay, component, new_component)
                
                self.bay.save()

            
        return self.get_view_model()