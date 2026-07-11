from django.core.management.base import BaseCommand
from hardware.models import CPU, GPU, RAM, SSD, Brand


class Command(BaseCommand):
    help = "Popula a base de dados com hardwares e especificações reais atualizadas, com foco em IA/Deep Learning"

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
            "Western Digital",
        ]

        brands = {}
        for name in brand_names:
            brand, _ = Brand.objects.get_or_create(name=name)
            brands[name] = brand

        self.stdout.write(self.style.SUCCESS("Marcas mapeadas com sucesso!"))

        # 2. Dados de CPUs (Campos herdados + específicos)
        # Mantidas as melhores CPUs "consumer" (bom p/ pré-processamento/pipeline)
        # e adicionadas CPUs de servidor/workstation usadas em setups de IA
        # (muitos núcleos/threads, suporte a mais lanes PCIe e RAM ECC).
        cpus_data = [
            {"model": "Ryzen 7 5700X", "brand": brands["AMD"], "price": 1100, "watts": 65, "cores": 8, "threads": 16, "ghz": 4.6, "score_bottleneck": 145},
            {"model": "Ryzen 7 7800X3D", "brand": brands["AMD"], "price": 2600, "watts": 120, "cores": 8, "threads": 16, "ghz": 5.0, "score_bottleneck": 240},
            {"model": "Ryzen 9 9950X", "brand": brands["AMD"], "price": 4600, "watts": 170, "cores": 16, "threads": 32, "ghz": 5.7, "score_bottleneck": 320},
            {"model": "Core i7-14700K", "brand": brands["Intel"], "price": 2700, "watts": 125, "cores": 20, "threads": 28, "ghz": 5.6, "score_bottleneck": 260},
            {"model": "Core Ultra 9 285K", "brand": brands["Intel"], "price": 4100, "watts": 125, "cores": 24, "threads": 24, "ghz": 5.7, "score_bottleneck": 300},
            {"model": "Threadripter PRO 7975WX", "brand": brands["AMD"], "price": 22000, "watts": 350, "cores": 32, "threads": 64, "ghz": 5.3, "score_bottleneck": 480},
            {"model": "Threadripper PRO 7995WX", "brand": brands["AMD"], "price": 47000, "watts": 350, "cores": 96, "threads": 192, "ghz": 5.1, "score_bottleneck": 600},
            {"model": "EPYC 9354", "brand": brands["AMD"], "price": 15000, "watts": 280, "cores": 32, "threads": 64, "ghz": 3.8, "score_bottleneck": 430},
            {"model": "EPYC 9654", "brand": brands["AMD"], "price": 39000, "watts": 360, "cores": 96, "threads": 192, "ghz": 3.7, "score_bottleneck": 560},
            {"model": "EPYC 9965 (Turin)", "brand": brands["AMD"], "price": 68000, "watts": 500, "cores": 192, "threads": 384, "ghz": 3.7, "score_bottleneck": 700},
            {"model": "Xeon w9-3495X", "brand": brands["Intel"], "price": 32000, "watts": 350, "cores": 56, "threads": 112, "ghz": 4.8, "score_bottleneck": 520},
            {"model": "Xeon Platinum 8592+", "brand": brands["Intel"], "price": 45000, "watts": 350, "cores": 64, "threads": 128, "ghz": 3.9, "score_bottleneck": 555},
            {"model": "Ryzen 5 9600X", "brand": brands["AMD"], "price": 1700, "watts": 65, "cores": 6, "threads": 12, "ghz": 5.4, "score_bottleneck": 155},
            {"model": "Core Ultra 7 265K", "brand": brands["Intel"], "price": 2400, "watts": 125, "cores": 20, "threads": 20, "ghz": 5.5, "score_bottleneck": 250},
            {"model": "Threadripper PRO 9995WX", "brand": brands["AMD"], "price": 55000, "watts": 350, "cores": 96, "threads": 192, "ghz": 5.4, "score_bottleneck": 640},
            {"model": "Xeon 6980P", "brand": brands["Intel"], "price": 58000, "watts": 500, "cores": 128, "threads": 256, "ghz": 3.2, "score_bottleneck": 610},
        ]

        # 3. Dados de GPUs (Campos herdados + específicos)
        # Mantidas GPUs gamer/prosumer mais relevantes p/ IA local (VRAM alta)
        # e adicionada a linha de datacenter (A100, H100, H100 NVL, H200, B200)
        # com preços aproximados de mercado (compra, não aluguel de nuvem).
        gpus_data = [
            {"model": "RTX 4070 SUPER", "brand": brands["NVIDIA"], "price": 4300, "watts": 220, "vram": 12, "mhz": 2475.0, "score_bottleneck": 240},
            {"model": "RTX 5070 Ti", "brand": brands["NVIDIA"], "price": 6900, "watts": 300, "vram": 16, "mhz": 2452.0, "score_bottleneck": 320},
            {"model": "RTX 5080", "brand": brands["NVIDIA"], "price": 9800, "watts": 360, "vram": 16, "mhz": 2617.0, "score_bottleneck": 390},
            {"model": "RTX 5090", "brand": brands["NVIDIA"], "price": 17000, "watts": 575, "vram": 32, "mhz": 2400.0, "score_bottleneck": 500},
            {"model": "RTX 4090", "brand": brands["NVIDIA"], "price": 15500, "watts": 450, "vram": 24, "mhz": 2520.0, "score_bottleneck": 470},
            {"model": "RTX 6000 Ada Generation", "brand": brands["NVIDIA"], "price": 42000, "watts": 300, "vram": 48, "mhz": 2505.0, "score_bottleneck": 520},
            {"model": "RTX PRO 6000 Blackwell", "brand": brands["NVIDIA"], "price": 62000, "watts": 600, "vram": 96, "mhz": 2617.0, "score_bottleneck": 610},
            {"model": "A100 80GB SXM4", "brand": brands["NVIDIA"], "price": 88000, "watts": 400, "vram": 80, "mhz": 1410.0, "score_bottleneck": 700},
            {"model": "H100 80GB SXM5", "brand": brands["NVIDIA"], "price": 175000, "watts": 700, "vram": 80, "mhz": 1980.0, "score_bottleneck": 900},
            {"model": "H100 NVL", "brand": brands["NVIDIA"], "price": 195000, "watts": 700, "vram": 94, "mhz": 1980.0, "score_bottleneck": 930},
            {"model": "H200 141GB SXM5", "brand": brands["NVIDIA"], "price": 210000, "watts": 700, "vram": 141, "mhz": 1980.0, "score_bottleneck": 980},
            {"model": "B200 192GB", "brand": brands["NVIDIA"], "price": 260000, "watts": 1000, "vram": 192, "mhz": 2100.0, "score_bottleneck": 1200},
            {"model": "B300 (Blackwell Ultra) 288GB", "brand": brands["NVIDIA"], "price": 300000, "watts": 1400, "vram": 288, "mhz": 2200.0, "score_bottleneck": 1450},
            {"model": "Rubin R200 288GB", "brand": brands["NVIDIA"], "price": 400000, "watts": 1200, "vram": 288, "mhz": 2400.0, "score_bottleneck": 2200},
            {"model": "RX 7900 XTX", "brand": brands["AMD"], "price": 6700, "watts": 355, "vram": 24, "mhz": 2500.0, "score_bottleneck": 340},
            {"model": "Instinct MI300X", "brand": brands["AMD"], "price": 82000, "watts": 750, "vram": 192, "mhz": 2100.0, "score_bottleneck": 850},
            {"model": "RTX 4060 Ti", "brand": brands["NVIDIA"], "price": 2550, "watts": 165, "vram": 16, "mhz": 2535.0, "score_bottleneck": 210},
            {"model": "RTX 5070", "brand": brands["NVIDIA"], "price": 5600, "watts": 250, "vram": 12, "mhz": 2512.0, "score_bottleneck": 280},
            {"model": "L40S", "brand": brands["NVIDIA"], "price": 32000, "watts": 350, "vram": 48, "mhz": 2520.0, "score_bottleneck": 480},
            {"model": "Instinct MI400", "brand": brands["AMD"], "price": 190000, "watts": 1000, "vram": 288, "mhz": 2300.0, "score_bottleneck": 1350},
        ]

        # 4. Dados de RAMs (Campos herdados + específicos)
        # Mantidos os kits DDR5 gamer/prosumer e adicionados kits de alta
        # capacidade (64GB/128GB por módulo) usados em workstations de IA
        # para dataset em memória e treinos que dependem de RAM do sistema.
        rams_data = [
            {"model": "Corsair Vengeance DDR5", "brand": brands["Corsair"], "price": 890, "watts": 6, "gb": 32, "mhz": 6000},
            {"model": "Corsair Dominator Platinum DDR5", "brand": brands["Corsair"], "price": 1950, "watts": 8, "gb": 64, "mhz": 6400},
            {"model": "G.Skill Trident Z5 RGB", "brand": brands["G.Skill"], "price": 1200, "watts": 7, "gb": 32, "mhz": 7200},
            {"model": "Kingston Fury Renegade Pro DDR5 ECC RDIMM", "brand": brands["Kingston"], "price": 3400, "watts": 9, "gb": 64, "mhz": 5600},
            {"model": "Kingston Server Premier DDR5 ECC RDIMM 128GB", "brand": brands["Kingston"], "price": 6800, "watts": 10, "gb": 128, "mhz": 5600},
            {"model": "Samsung DDR5 ECC RDIMM 128GB", "brand": brands["Samsung"], "price": 7200, "watts": 10, "gb": 128, "mhz": 5600},
            {"model": "SK Hynix DDR5 ECC RDIMM 256GB", "brand": brands["SK Hynix"], "price": 13500, "watts": 12, "gb": 256, "mhz": 5600},
            {"model": "Micron DDR5 ECC RDIMM 96GB", "brand": brands["Micron"], "price": 5600, "watts": 9, "gb": 96, "mhz": 6400},
            {"model": "Kingston Fury Beast DDR5", "brand": brands["Kingston"], "price": 480, "watts": 5, "gb": 16, "mhz": 5600},
            {"model": "Kingston Fury Beast RGB DDR5", "brand": brands["Kingston"], "price": 920, "watts": 6, "gb": 32, "mhz": 6000},
            {"model": "Crucial Pro DDR5", "brand": brands["Crucial"], "price": 850, "watts": 6, "gb": 32, "mhz": 6000},
            {"model": "Kioxia/SK Hynix DDR5 ECC RDIMM 512GB", "brand": brands["SK Hynix"], "price": 24000, "watts": 14, "gb": 512, "mhz": 6400},
        ]

        # 5. Dados de SSDs (Campos herdados + específicos)
        # Mantidos SSDs consumer rápidos e adicionados SSDs enterprise NVMe
        # de alta capacidade/endurance, usados para datasets, checkpoints
        # de treino e cache de modelos em servidores de IA.
        ssds_data = [
            {"model": "Kingston KC3000", "brand": brands["Kingston"], "price": 680, "watts": 5, "gb": 1024, "speed": 7000},
            {"model": "Samsung 990 PRO", "brand": brands["Samsung"], "price": 1400, "watts": 6, "gb": 2000, "speed": 7450},
            {"model": "Crucial T705 PCIe 5.0", "brand": brands["Crucial"], "price": 2500, "watts": 10, "gb": 2000, "speed": 14500},
            {"model": "Samsung PM9A3 Enterprise NVMe 3.84TB", "brand": brands["Samsung"], "price": 9800, "watts": 12, "gb": 3840, "speed": 6800},
            {"model": "Kioxia CM7 Enterprise NVMe 7.68TB", "brand": brands["Kioxia"], "price": 18500, "watts": 14, "gb": 7680, "speed": 14000},
            {"model": "Solidigm D5-P5336 Enterprise NVMe 15.36TB", "brand": brands["Solidigm"], "price": 26000, "watts": 15, "gb": 15360, "speed": 7000},
            {"model": "Micron 9550 Enterprise NVMe 7.68TB", "brand": brands["Micron"], "price": 19500, "watts": 16, "gb": 7680, "speed": 14000},
            {"model": "Kingston NV3", "brand": brands["Kingston"], "price": 290, "watts": 4, "gb": 500, "speed": 5000},
            {"model": "Samsung 990 EVO Plus", "brand": brands["Samsung"], "price": 750, "watts": 4, "gb": 1000, "speed": 7150},
            {"model": "WD Black SN8100", "brand": brands["Western Digital"], "price": 1600, "watts": 8, "gb": 2000, "speed": 14900},
            {"model": "Solidigm D5-P5336 Enterprise NVMe 30.72TB", "brand": brands["Solidigm"], "price": 48000, "watts": 18, "gb": 30720, "speed": 7000},
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

        self.stdout.write(self.style.SUCCESS("\nBase de dados de hardware (foco IA) populada com sucesso!"))