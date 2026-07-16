


class BalanceService:
    @staticmethod
    def get_total_balance(user):
        value = 0
        racks = user.racks.all()
        for rack in racks:
            for bay in rack.bays.all():
                value += (
                    (bay.get_cpu.get_power() / 10000) +
                    (bay.get_gpu.get_power() / 10000) +
                    (bay.get_ram.get_power() / 10000) +
                    (bay.get_ssd.get_power() / 10000)  
                )
        return value