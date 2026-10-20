from model.models import AIInstance
from user.models import Inventory, InventoryItem
from server.models import Rack, Bay,  UserCeilingCooler, UserEnergyEquipment

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
                "type": "rack",
                "price": 1000,
            })
        for bay in Bay.objects.filter(user=self.user_id, is_selected=False):
            inventory.append(
            {
                "id": bay.id,
                "nome": bay.name,
                "icone": "<svg>...</svg>",
                "desc": f"baya de servidor",
                "qtd": 1,
                "nivel": 1,
                "type": "bay",
                "price": 1000,
            })
        components = [
            ("cpu", self.get_cpus()),
            ("gpu", self.get_gpus()),
            ("ram", self.get_rams()),
            ("ssd", self.get_ssds()),
        ]

        for component_type, items in components:
            for item in items.select_related("item", "item__brand"):
                hardware = item.item

                inventory.append({
                    "id": item.id,
                    "nome": f"{hardware.model}",
                    "icone": "<svg>...</svg>",
                    "desc": hardware.type,
                    "qtd": 1,
                    "nivel": 1,
                    "type": component_type,
                    "price": hardware.price,
                })
                
        for cooler in UserCeilingCooler.objects.filter(user_id=self.user_id).select_related("cooler"):
            inventory.append({
                "id": cooler.id,
                "nome": f"Cooler",
                "icone": "<svg>...</svg>",
                "desc": "Cooler de teto",
                "qtd": 1,
                "nivel": cooler.level,
                "type": "cooler",
                "price": cooler.cooler.price,
            })
        for equipment in UserEnergyEquipment.objects.filter(user_id=self.user_id).select_related("equipment"):
            inventory.append({
                "id": equipment.id,
                "nome": f"{equipment.name}",
                "icone": "<svg>...</svg>",
                "desc": "Equipamento de energia",
                "qtd": 1,
                "nivel": equipment.level,
                "type": equipment.type,
                "price": equipment.equipment.price,
            })
        
        return inventory
