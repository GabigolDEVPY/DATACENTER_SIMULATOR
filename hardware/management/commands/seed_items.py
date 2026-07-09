from django.core.management.base import BaseCommand
from hardware.models import CPU, GPU, RAM, SSD, Brand


class Command(BaseCommand):
    help = "Popula a base de dados com hardwares e especificações reais atualizadas"

    def handle(self, *args, **options):
        # 1. Gerenciamento Dinâmico de Marcas (Sem IDs fixos)
        brand_names = [
            "AMD",
            "Intel",
            "NVIDIA",
            "Samsung",
            "Micron",
            "SK Hynix",
            "Kingston",
            "Solidigm",
            "Kioxia",
            "Crucial",
            "Corsair",
            "G.Skill",
        ]
        
        brands = {}
        for name in brand_names:
            brand, _ = Brand.objects.get_or_create(name=name)
            brands[name] = brand

        self.stdout.write(self.style.SUCCESS("Marcas mapeadas com sucesso!"))

        # 2. Dados de CPUs (Campos herdados + específicos)
        cpus_data = [
            {"model": "Ryzen 5 5600", "brand": brands["AMD"], "price": 750, "watts": 65, "cores": 6, "threads": 12, "ghz": 4.4, "score_bottleneck": 120},
            {"model": "Ryzen 7 5700X", "brand": brands["AMD"], "price": 1100, "watts": 65, "cores": 8, "threads": 16, "ghz": 4.6, "score_bottleneck": 145},
            {"model": "Ryzen 7 7800X3D", "brand": brands["AMD"], "price": 2600, "watts": 120, "cores": 8, "threads": 16, "ghz": 5.0, "score_bottleneck": 240},
            {"model": "Ryzen 9 7950X", "brand": brands["AMD"], "price": 3400, "watts": 170, "cores": 16, "threads": 32, "ghz": 5.7, "score_bottleneck": 300},
            {"model": "Ryzen 9 9950X", "brand": brands["AMD"], "price": 4600, "watts": 170, "cores": 16, "threads": 32, "ghz": 5.7, "score_bottleneck": 320},
            {"model": "Core i5-14600K", "brand": brands["Intel"], "price": 1950, "watts": 125, "cores": 14, "threads": 20, "ghz": 5.3, "score_bottleneck": 200},
            {"model": "Core i7-14700K", "brand": brands["Intel"], "price": 2700, "watts": 125, "cores": 20, "threads": 28, "ghz": 5.6, "score_bottleneck": 260},
            {"model": "Core Ultra 9 285K", "brand": brands["Intel"], "price": 4100, "watts": 125, "cores": 24, "threads": 24, "ghz": 5.7, "score_bottleneck": 300},
        ]

        # 3. Dados de GPUs (Campos herdados + específicos)
        gpus_data = [
            {"model": "RTX 4060", "brand": brands["NVIDIA"], "price": 1900, "watts": 115, "vram": 8, "mhz": 2460.0, "score_bottleneck": 180},
            {"model": "RTX 4060 Ti", "brand": brands["NVIDIA"], "price": 2550, "watts": 165, "vram": 16, "mhz": 2535.0, "score_bottleneck": 210},
            {"model": "RTX 4070 SUPER", "brand": brands["NVIDIA"], "price": 4300, "watts": 220, "vram": 12, "mhz": 2475.0, "score_bottleneck": 240},
            {"model": "RTX 5070", "brand": brands["NVIDIA"], "price": 5600, "watts": 250, "vram": 12, "mhz": 2512.0, "score_bottleneck": 280},
            {"model": "RTX 5070 Ti", "brand": brands["NVIDIA"], "price": 6900, "watts": 300, "vram": 16, "mhz": 2452.0, "score_bottleneck": 320},
            {"model": "RTX 5080", "brand": brands["NVIDIA"], "price": 9800, "watts": 360, "vram": 16, "mhz": 2617.0, "score_bottleneck": 390},
            {"model": "RTX 5090", "brand": brands["NVIDIA"], "price": 17000, "watts": 575, "vram": 32, "mhz": 2400.0, "score_bottleneck": 500},
            {"model": "RX 7700 XT", "brand": brands["AMD"], "price": 3100, "watts": 245, "vram": 12, "mhz": 2544.0, "score_bottleneck": 215},
            {"model": "RX 7800 XT", "brand": brands["AMD"], "price": 3800, "watts": 263, "vram": 16, "mhz": 2430.0, "score_bottleneck": 230},
            {"model": "RX 7900 XTX", "brand": brands["AMD"], "price": 6700, "watts": 355, "vram": 24, "mhz": 2500.0, "score_bottleneck": 340},
        ]

        # 4. Dados de RAMs (Campos herdados + específicos)
        rams_data = [
            {"model": "Kingston Fury Beast DDR5", "brand": brands["Kingston"], "price": 480, "watts": 5, "gb": 16, "mhz": 5600},
            {"model": "Kingston Fury Beast RGB DDR5", "brand": brands["Kingston"], "price": 920, "watts": 6, "gb": 32, "mhz": 6000},
            {"model": "Corsair Vengeance DDR5", "brand": brands["Corsair"], "price": 890, "watts": 6, "gb": 32, "mhz": 6000},
            {"model": "Corsair Dominator Platinum DDR5", "brand": brands["Corsair"], "price": 1950, "watts": 8, "gb": 64, "mhz": 6400},
            {"model": "G.Skill Trident Z5 RGB", "brand": brands["G.Skill"], "price": 1200, "watts": 7, "gb": 32, "mhz": 7200},
        ]

        # 5. Dados de SSDs (Campos herdados + específicos)
        ssds_data = [
            {"model": "Kingston NV3", "brand": brands["Kingston"], "price": 290, "watts": 4, "gb": 500, "speed": 5000},
            {"model": "Kingston KC3000", "brand": brands["Kingston"], "price": 680, "watts": 5, "gb": 1024, "speed": 7000},
            {"model": "Samsung 990 EVO Plus", "brand": brands["Samsung"], "price": 750, "watts": 4, "gb": 1000, "speed": 7150},
            {"model": "Samsung 990 PRO", "brand": brands["Samsung"], "price": 1400, "watts": 6, "gb": 2000, "speed": 7450},
            {"model": "Crucial T705 PCIe 5.0", "brand": brands["Crucial"], "price": 2500, "watts": 10, "gb": 2000, "speed": 14500},
        ]

        # --- Inserção e Atualização Segura no Banco ---

        # Processando CPUs
        for item in cpus_data:
            CPU.objects.update_or_create(
                model=item["model"],
                defaults={**item, "type": "CPU", "is_active": True}
            )
        self.stdout.write(self.style.SUCCESS(f"Processado: {len(cpus_data)} modelos de CPU."))

        # Processando GPUs
        for item in gpus_data:
            GPU.objects.update_or_create(
                model=item["model"],
                defaults={**item, "type": "GPU", "is_active": True}
            )
        self.stdout.write(self.style.SUCCESS(f"Processado: {len(gpus_data)} modelos de GPU."))

        # Processando RAMs
        for item in rams_data:
            RAM.objects.update_or_create(
                model=item["model"],
                defaults={**item, "type": "RAM", "is_active": True}
            )
        self.stdout.write(self.style.SUCCESS(f"Processado: {len(rams_data)} modelos de RAM."))

        # Processando SSDs
        for item in ssds_data:
            SSD.objects.update_or_create(
                model=item["model"],
                defaults={**item, "type": "SSD", "is_active": True}
            )
        self.stdout.write(self.style.SUCCESS(f"Processado: {len(ssds_data)} modelos de SSD."))

        self.stdout.write(self.style.SUCCESS("\nBase de dados de hardware populada com sucesso!"))