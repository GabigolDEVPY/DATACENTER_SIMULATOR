from server.models import Bay
from user.models import InventoryItem
import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer



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
    def change_status(id, user):
        bay = Bay.objects.filter(id=id).first()       
        bay.is_active = not bay.is_active
        bay.save()
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{user.id}",
            {"type": "power_update", "message_type": "refresh_power", "data": {}}
        )
        
        return bay
    