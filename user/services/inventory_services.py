from user.models import Inventory, InventoryItem

class InventoryService:
    def __init__(self, user_id):
        self.inventory = Inventory.objects.filter(user=user_id).first()
    
    def get_cpus(self):
        cpus = InventoryItem.objects.filter(
            inventory=self.inventory, item__cpu__isnull=False,
            is_equiped=False
            )
        return cpus
        
    def get_gpus(self):
        return InventoryItem.objects.filter(
            inventory=self.inventory,item__gpu__isnull=False,
            is_equiped=False
            )
        
    def get_rams(self):
        return InventoryItem.objects.filter(
            inventory=self.inventory, item__ram__isnull=False,
            is_equiped=False
            )
    
    def get_ssds(self):
        return InventoryItem.objects.filter(
            inventory=self.inventory,item__ssd__isnull=False,
            is_equiped=False
            )
        
    def get_components(self):
        return {
            "cpus": self.get_cpus,
            "rams": self.get_rams,
            "ssds": self.get_ssds,
            "gpus": self.get_gpus
        }
        
        
        
    