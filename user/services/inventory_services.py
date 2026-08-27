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
            item__gpu__is_active=False
            )
        
    def get_rams(self):
        return InventoryItem.objects.filter(
            inventory=self.inventory, item__ram__isnull=False,
            item__ram__is_active=False
            )
    
    def get_ssds(self):
        return InventoryItem.objects.filter(
            inventory=self.inventory,item__ssd__isnull=False,
            item__ssd__is_active=False
            )
        
        
        
    