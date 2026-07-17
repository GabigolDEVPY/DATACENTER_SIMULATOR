from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from decimal import Decimal

class UserService:
    @staticmethod 
    def get_total_rate(user):
        value = 0
        racks = user.racks.all()
        for rack in racks:
            for bay in rack.bays.all():
                value += float(
                    bay.get_cpu.get_power() +
                    bay.get_gpu.get_power() +
                    bay.get_ram.get_power() +
                    bay.get_ssd.get_power()  
                ) * 0.000001
        return value
    
    @staticmethod
    def refresh_balance(user):   
        new_balance = float(user.money)
        new_rate = UserService.get_total_rate(user)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{user.id}",
            {"type": "power_update",
             "message_type": "refresh_balance",
             "balance": new_balance,
             "rate": new_rate
                 }
        )
        