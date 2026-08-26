from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from decimal import Decimal
from django.utils import timezone

class UserService:
    
    @staticmethod
    def refresh_balance(user):
        now = timezone.now()
        seconds = int((now - user.last_refresh_balance).total_seconds() + 1)
        
        new_rate, new_energy_rate = 0, 0
        
        new_balance = user.money + (seconds * user.actual_rate)
        new_energy = user.energy + (seconds * user.actual_energy_rate)
        
        
        user.last_refresh_balance = now
        
        user.money = new_balance
        user.actual_rate = new_rate
        user.energy = new_energy
        
        user.save(update_fields=["money", "last_refresh_balance", "actual_rate"])
        
        channel_layer = get_channel_layer()
        
        # chamar o socket pra atualizar os stats da navbar do usuário
        async_to_sync(channel_layer.group_send)(
            f"user_{user.id}",
            {
            "type": "stats_update",
            "message_type": "refresh_balance",
            "balance": float(new_balance),
            "rate_money": float(new_rate),
            "energy": float(new_energy),
            "rate_energy": float(new_energy_rate)
            }
        )
