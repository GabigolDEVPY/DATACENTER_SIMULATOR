from server.models import Bay
from user.models import InventoryItem



class BayService:
    
    @staticmethod
    def get_bay_detail(id):
        bay = Bay.objects.filter(id=id).first()
        context = {"bay": bay, 
                   "rams": InventoryItem.objects.filter(item__ram__isnull=False),
                   "cpus": InventoryItem.objects.filter(item__cpu__isnull=False),
                   "gpus": InventoryItem.objects.filter(item__gpu__isnull=False),
                   "ssds": InventoryItem.objects.filter(item__ssd__isnull=False),
                   }
        return context
        
    @staticmethod
    def change_status(id):
        bay = Bay.objects.filter(id=id).first()       
        bay.is_active = not bay.is_active
        bay.save()
        return bay
    