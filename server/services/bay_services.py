from server.models import Bay
from user.models import InventoryItem
from user.services import UserService



class BayService:
    @staticmethod
    def get_bay_detail(id):
        bay = Bay.objects.filter(id=id).first()
        context = {"bay": bay, 
                   "rams": InventoryItem.objects.filter(item__ram__isnull=False, item__ram__is_active=False),
                   "cpus": InventoryItem.objects.filter(item__cpu__isnull=False, item__cpu__is_active=False),
                   "gpus": InventoryItem.objects.filter(item__gpu__isnull=False, item__gpu__is_active=False),
                   "ssds": InventoryItem.objects.filter(item__ssd__isnull=False, item__ssd__is_active=False),
                   }
        return context
        
        
    @staticmethod
    def change_status(id, user):
        bay = Bay.objects.filter(id=id).first()       
        bay.is_active = not bay.is_active
        bay.save(update_fields=["is_active"])
        UserService.refresh_balance(user)
        return bay
    