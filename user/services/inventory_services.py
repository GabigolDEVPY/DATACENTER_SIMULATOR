from model.models import AIInstance
from user.models import Inventory, InventoryItem
from server.models import Rack, Bay

class InventoryService:
    def __init__(self, user_id):
        self.user_id = user_id
        self.inventory = Inventory.objects.filter(user=user_id).first()
    
    #hardware items
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
            "cpus": self.get_cpus(),
            "rams": self.get_rams(),
            "ssds": self.get_ssds(),
            "gpus": self.get_gpus()
        }
        
    # ia model instances
    def get_ia_models(self):
        return AIInstance.objects.filter(user_id=self.user_id)

    def get_inventory_summary(self):
        inventory = []
        for rack in Rack.objects.filter(user_id=self.user_id, is_selected=False).prefetch_related("bays"):
            inventory.append(
            {
                "id": rack.id,
                "nome": rack.name,
                "icone": "<svg>...</svg>",
                "desc": f"rack com {rack.bays.count()} baias",
                "qtd": 1,
                "nivel": 1,
            })
        return inventory