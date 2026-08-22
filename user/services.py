from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from decimal import Decimal
from django.utils import timezone

class UserService:
    @staticmethod 
    def get_total_rate(user):
        value = 0
        energy_rate = 0
        racks = user.racks.all()
        for rack in racks:
            for bay in rack.bays.all():
                if bay.is_active:
                    
                    components = [bay.get_cpu,bay.get_gpu,bay.get_ram,bay.get_ssd]
                    
                    if any(component is None for component in components):
                        continue
                    
                    value += float(bay.get_cpu.get_power() +bay.get_gpu.get_power() +bay.get_ram.get_power() + bay.get_ssd.get_power()  ) * 0.000001
                    energy_rate += bay.get_energy_rate
                    
                else: 
                    continue
                
        return value, (energy_rate * 0.00001)
    
    @staticmethod
    def refresh_balance(user):
        now = timezone.now()
        seconds = int((now - user.last_refresh_balance).total_seconds() + 1)
        
        new_rate, new_energy_rate = UserService.get_total_rate(user)
        
        new_balance = user.money + (seconds * user.actual_rate)
        new_energy = user.energy + (seconds * user.actual_energy_rate)
        
        
        user.last_refresh_balance = now
        
        user.money = new_balance
        user.actual_rate = new_rate
        user.energy = new_energy
        user.actual_rate = new_energy_rate
        
        user.save(update_fields=["money", "last_refresh_balance", "actual_rate"])
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{user.id}",
            {
             "type": "power_update",
             "message_type": "refresh_balance",
             "balance": float(new_balance),
             "rate_money": float(new_rate),
             "energy": float(new_energy),
             "rate_energy": float(new_energy_rate)
            }
        )
        