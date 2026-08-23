from django.core.management.base import BaseCommand
from hardware.models import CPU, GPU, RAM, SSD, Brand


class Command(BaseCommand):
    help = "Popula a base de dados com hardwares e especificacoes reais atualizadas, com foco em IA/Deep Learning, incluindo hardware ainda nao lancado e nivel de raridade"

    def handle(self, *args, **options):
        # 1. Gerenciamento Dinamico de Marcas (Sem IDs fixos)
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

        # Escala de raridade utilizada (quantidade de pecas por nivel, dentro
        # de cada categoria - CPU, GPU, RAM, SSD - da mais forte para a mais fraca):
        #   iris        -> 2 pecas (as 2 mais fortes)
        #   pearlescent -> 3 pecas (as 3 seguintes)
        #   legendary   -> 4 pecas
        #   ancestral   -> 5 pecas
        #   epic        -> 6 pecas
        #   very-rare   -> 7 pecas
        #   uncommon    -> 8 pecas
        #   common      -> 9 pecas (as 9 mais fracas)
        #   Total: 2+3+4+5+6+7+8+9 = 44 pecas por categoria
        #
        # O preco tambem segue estritamente o poder/desempenho: dentro de cada
        # categoria, a peca mais forte tem sempre o maior preco, a segunda mais
        # forte tem o segundo maior preco, e assim por diante -- sem excecoes
        # (nunca uma peca mais forte custa menos que uma mais fraca).

        # 2. Dados de CPUs (44 modelos - real + itens ainda no papel)
        cpus_data = [
            {"model": "Ryzen 7 5700X", "brand": brands["AMD"], "price": 1050, "watts": 65, "cores": 8, "threads": 16, "ghz": 4.6, "score_bottleneck": 145, "rarity": "common"},
            {"model": "Ryzen 7 7800X3D", "brand": brands["AMD"], "price": 2400, "watts": 120, "cores": 8, "threads": 16, "ghz": 5.0, "score_bottleneck": 240, "rarity": "uncommon"},
            {"model": "Ryzen 9 9950X", "brand": brands["AMD"], "price": 4600, "watts": 170, "cores": 16, "threads": 32, "ghz": 5.7, "score_bottleneck": 320, "rarity": "uncommon"},
            {"model": "Core i7-14700K", "brand": brands["Intel"], "price": 2700, "watts": 125, "cores": 20, "threads": 28, "ghz": 5.6, "score_bottleneck": 260, "rarity": "uncommon"},
            {"model": "Core Ultra 9 285K", "brand": brands["Intel"], "price": 4100, "watts": 125, "cores": 24, "threads": 24, "ghz": 5.7, "score_bottleneck": 300, "rarity": "uncommon"},
            {"model": "Threadripter PRO 7975WX", "brand": brands["AMD"], "price": 24000, "watts": 350, "cores": 32, "threads": 64, "ghz": 5.3, "score_bottleneck": 480, "rarity": "epic"},
            {"model": "Threadripper PRO 7995WX", "brand": brands["AMD"], "price": 47000, "watts": 350, "cores": 96, "threads": 192, "ghz": 5.1, "score_bottleneck": 600, "rarity": "ancestral"},
            {"model": "EPYC 9354", "brand": brands["AMD"], "price": 14000, "watts": 280, "cores": 32, "threads": 64, "ghz": 3.8, "score_bottleneck": 430, "rarity": "epic"},
            {"model": "EPYC 9654", "brand": brands["AMD"], "price": 44000, "watts": 360, "cores": 96, "threads": 192, "ghz": 3.7, "score_bottleneck": 560, "rarity": "ancestral"},
            {"model": "EPYC 9965 (Turin)", "brand": brands["AMD"], "price": 68000, "watts": 500, "cores": 192, "threads": 384, "ghz": 3.7, "score_bottleneck": 700, "rarity": "legendary"},
            {"model": "Xeon w9-3495X", "brand": brands["Intel"], "price": 32000, "watts": 350, "cores": 56, "threads": 112, "ghz": 4.8, "score_bottleneck": 520, "rarity": "epic"},
            {"model": "Xeon Platinum 8592+", "brand": brands["Intel"], "price": 40000, "watts": 350, "cores": 64, "threads": 128, "ghz": 3.9, "score_bottleneck": 555, "rarity": "ancestral"},
            {"model": "Ryzen 5 9600X", "brand": brands["AMD"], "price": 1250, "watts": 65, "cores": 6, "threads": 12, "ghz": 5.4, "score_bottleneck": 155, "rarity": "common"},
            {"model": "Core Ultra 7 265K", "brand": brands["Intel"], "price": 2600, "watts": 125, "cores": 20, "threads": 20, "ghz": 5.5, "score_bottleneck": 250, "rarity": "uncommon"},
            {"model": "Threadripper PRO 9995WX", "brand": brands["AMD"], "price": 62000, "watts": 350, "cores": 96, "threads": 192, "ghz": 5.4, "score_bottleneck": 640, "rarity": "legendary"},
            {"model": "Xeon 6980P", "brand": brands["Intel"], "price": 55000, "watts": 500, "cores": 128, "threads": 256, "ghz": 3.2, "score_bottleneck": 610, "rarity": "ancestral"},
            {"model": "Ryzen 5 8500G", "brand": brands["AMD"], "price": 950, "watts": 65, "cores": 6, "threads": 12, "ghz": 5.0, "score_bottleneck": 130, "rarity": "common"},
            {"model": "Ryzen 5 7600", "brand": brands["AMD"], "price": 1100, "watts": 65, "cores": 6, "threads": 12, "ghz": 5.2, "score_bottleneck": 150, "rarity": "common"},
            {"model": "Ryzen 7 9700X", "brand": brands["AMD"], "price": 2200, "watts": 65, "cores": 8, "threads": 16, "ghz": 5.5, "score_bottleneck": 235, "rarity": "uncommon"},
            {"model": "Ryzen 9 9900X", "brand": brands["AMD"], "price": 3400, "watts": 120, "cores": 12, "threads": 24, "ghz": 5.6, "score_bottleneck": 290, "rarity": "uncommon"},
            {"model": "Ryzen 9 9950X3D", "brand": brands["AMD"], "price": 4800, "watts": 170, "cores": 16, "threads": 32, "ghz": 5.7, "score_bottleneck": 335, "rarity": "very-rare"},
            {"model": "Core i5-14600K", "brand": brands["Intel"], "price": 1900, "watts": 125, "cores": 14, "threads": 20, "ghz": 5.3, "score_bottleneck": 210, "rarity": "uncommon"},
            {"model": "Core Ultra 5 245K", "brand": brands["Intel"], "price": 1800, "watts": 125, "cores": 14, "threads": 14, "ghz": 5.2, "score_bottleneck": 200, "rarity": "common"},
            {"model": "Xeon w7-3465X", "brand": brands["Intel"], "price": 15000, "watts": 350, "cores": 28, "threads": 56, "ghz": 4.7, "score_bottleneck": 450, "rarity": "epic"},
            {"model": "Xeon Platinum 8580", "brand": brands["Intel"], "price": 39000, "watts": 350, "cores": 60, "threads": 120, "ghz": 3.8, "score_bottleneck": 540, "rarity": "epic"},
            {"model": "EPYC 9174F", "brand": brands["AMD"], "price": 6800, "watts": 320, "cores": 16, "threads": 32, "ghz": 4.4, "score_bottleneck": 400, "rarity": "very-rare"},
            {"model": "EPYC 9755", "brand": brands["AMD"], "price": 45000, "watts": 500, "cores": 128, "threads": 256, "ghz": 3.4, "score_bottleneck": 590, "rarity": "ancestral"},
            {"model": "Threadripper 7970X", "brand": brands["AMD"], "price": 22000, "watts": 350, "cores": 32, "threads": 64, "ghz": 5.3, "score_bottleneck": 465, "rarity": "epic"},
            {"model": "Threadripper 7960X", "brand": brands["AMD"], "price": 12000, "watts": 350, "cores": 24, "threads": 48, "ghz": 5.3, "score_bottleneck": 420, "rarity": "very-rare"},
            {"model": "Ryzen 10 11950X3D (Zen 6, especulativo)", "brand": brands["AMD"], "price": 9500, "watts": 170, "cores": 20, "threads": 40, "ghz": 6.0, "score_bottleneck": 410, "rarity": "very-rare"},
            {"model": "Ryzen Threadripper PRO 11995WX (Zen 6, especulativo)", "brand": brands["AMD"], "price": 75000, "watts": 400, "cores": 128, "threads": 256, "ghz": 5.6, "score_bottleneck": 720, "rarity": "pearlescent"},
            {"model": "EPYC 'Venice' 10995 (Zen 6, especulativo)", "brand": brands["AMD"], "price": 89000, "watts": 500, "cores": 256, "threads": 512, "ghz": 3.9, "score_bottleneck": 780, "rarity": "pearlescent"},
            {"model": "Core Ultra 9 385K (Panther Lake, especulativo)", "brand": brands["Intel"], "price": 5200, "watts": 125, "cores": 28, "threads": 28, "ghz": 5.9, "score_bottleneck": 350, "rarity": "very-rare"},
            {"model": "Xeon 'Diamond Rapids' 7900P (especulativo)", "brand": brands["Intel"], "price": 63000, "watts": 500, "cores": 144, "threads": 288, "ghz": 3.6, "score_bottleneck": 660, "rarity": "legendary"},
            {"model": "Xeon 'Coral Rapids' AI Max (especulativo)", "brand": brands["Intel"], "price": 70000, "watts": 600, "cores": 176, "threads": 352, "ghz": 3.5, "score_bottleneck": 710, "rarity": "pearlescent"},
            {"model": "Ryzen AI Max+ 495 (especulativo)", "brand": brands["AMD"], "price": 5400, "watts": 140, "cores": 20, "threads": 40, "ghz": 5.8, "score_bottleneck": 380, "rarity": "very-rare"},
            {"model": "Threadripper PRO 'Shimada Peak Ultra' 12995WX (especulativo)", "brand": brands["AMD"], "price": 92000, "watts": 450, "cores": 160, "threads": 320, "ghz": 5.7, "score_bottleneck": 810, "rarity": "iris"},
            {"model": "Core Ultra X9 395K (Nova Lake, especulativo)", "brand": brands["Intel"], "price": 5600, "watts": 130, "cores": 32, "threads": 32, "ghz": 6.1, "score_bottleneck": 400, "rarity": "very-rare"},
            {"model": "EPYC 'Verano' 11995 (Zen 7, especulativo)", "brand": brands["AMD"], "price": 98000, "watts": 550, "cores": 320, "threads": 640, "ghz": 4.0, "score_bottleneck": 900, "rarity": "iris"},
            {"model": "Xeon 'Clearwater Forest' E9 (especulativo)", "brand": brands["Intel"], "price": 58000, "watts": 500, "cores": 288, "threads": 288, "ghz": 3.0, "score_bottleneck": 640, "rarity": "legendary"},
            {"model": "Ryzen 3 8300G", "brand": brands["AMD"], "price": 720, "watts": 65, "cores": 4, "threads": 8, "ghz": 4.9, "score_bottleneck": 95, "rarity": "common"},
            {"model": "Core i3-14100", "brand": brands["Intel"], "price": 690, "watts": 60, "cores": 4, "threads": 8, "ghz": 4.7, "score_bottleneck": 90, "rarity": "common"},
            {"model": "Ryzen 5 7500F", "brand": brands["AMD"], "price": 980, "watts": 65, "cores": 6, "threads": 12, "ghz": 5.0, "score_bottleneck": 140, "rarity": "common"},
            {"model": "Core i5-13400F", "brand": brands["Intel"], "price": 1700, "watts": 65, "cores": 10, "threads": 16, "ghz": 4.6, "score_bottleneck": 165, "rarity": "common"},
        ]


        # 3. Dados de GPUs (44 modelos - real + itens ainda no papel)
        gpus_data = [
            {"model": "RTX 4070 SUPER", "brand": brands["NVIDIA"], "price": 4200, "watts": 220, "vram": 12, "mhz": 2475.0, "score_bottleneck": 240, "rarity": "common"},
            {"model": "RTX 5070 Ti", "brand": brands["NVIDIA"], "price": 6900, "watts": 300, "vram": 16, "mhz": 2452.0, "score_bottleneck": 320, "rarity": "uncommon"},
            {"model": "RTX 5080", "brand": brands["NVIDIA"], "price": 14000, "watts": 360, "vram": 16, "mhz": 2617.0, "score_bottleneck": 390, "rarity": "uncommon"},
            {"model": "RTX 5090", "brand": brands["NVIDIA"], "price": 24000, "watts": 575, "vram": 32, "mhz": 2400.0, "score_bottleneck": 500, "rarity": "very-rare"},
            {"model": "RTX 4090", "brand": brands["NVIDIA"], "price": 19000, "watts": 450, "vram": 24, "mhz": 2520.0, "score_bottleneck": 470, "rarity": "very-rare"},
            {"model": "RTX 6000 Ada Generation", "brand": brands["NVIDIA"], "price": 25000, "watts": 300, "vram": 48, "mhz": 2505.0, "score_bottleneck": 520, "rarity": "very-rare"},
            {"model": "RTX PRO 6000 Blackwell", "brand": brands["NVIDIA"], "price": 45000, "watts": 600, "vram": 96, "mhz": 2617.0, "score_bottleneck": 610, "rarity": "epic"},
            {"model": "A100 80GB SXM4", "brand": brands["NVIDIA"], "price": 62000, "watts": 400, "vram": 80, "mhz": 1410.0, "score_bottleneck": 700, "rarity": "epic"},
            {"model": "H100 80GB SXM5", "brand": brands["NVIDIA"], "price": 175000, "watts": 700, "vram": 80, "mhz": 1980.0, "score_bottleneck": 900, "rarity": "ancestral"},
            {"model": "H100 NVL", "brand": brands["NVIDIA"], "price": 190000, "watts": 700, "vram": 94, "mhz": 1980.0, "score_bottleneck": 930, "rarity": "ancestral"},
            {"model": "H200 141GB SXM5", "brand": brands["NVIDIA"], "price": 195000, "watts": 700, "vram": 141, "mhz": 1980.0, "score_bottleneck": 980, "rarity": "ancestral"},
            {"model": "B200 192GB", "brand": brands["NVIDIA"], "price": 210000, "watts": 1000, "vram": 192, "mhz": 2100.0, "score_bottleneck": 1200, "rarity": "legendary"},
            {"model": "B300 (Blackwell Ultra) 288GB", "brand": brands["NVIDIA"], "price": 260000, "watts": 1400, "vram": 288, "mhz": 2200.0, "score_bottleneck": 1450, "rarity": "legendary"},
            {"model": "Rubin R200 288GB", "brand": brands["NVIDIA"], "price": 480000, "watts": 1200, "vram": 288, "mhz": 2400.0, "score_bottleneck": 2200, "rarity": "pearlescent"},
            {"model": "RX 7900 XTX", "brand": brands["AMD"], "price": 9800, "watts": 355, "vram": 24, "mhz": 2500.0, "score_bottleneck": 340, "rarity": "uncommon"},
            {"model": "Instinct MI300X", "brand": brands["AMD"], "price": 88000, "watts": 750, "vram": 192, "mhz": 2100.0, "score_bottleneck": 850, "rarity": "ancestral"},
            {"model": "RTX 4060 Ti", "brand": brands["NVIDIA"], "price": 2600, "watts": 165, "vram": 16, "mhz": 2535.0, "score_bottleneck": 210, "rarity": "common"},
            {"model": "RTX 5070", "brand": brands["NVIDIA"], "price": 5600, "watts": 250, "vram": 12, "mhz": 2512.0, "score_bottleneck": 280, "rarity": "common"},
            {"model": "L40S", "brand": brands["NVIDIA"], "price": 22000, "watts": 350, "vram": 48, "mhz": 2520.0, "score_bottleneck": 480, "rarity": "very-rare"},
            {"model": "Instinct MI400", "brand": brands["AMD"], "price": 220000, "watts": 1000, "vram": 288, "mhz": 2300.0, "score_bottleneck": 1350, "rarity": "legendary"},
            {"model": "RTX 4060", "brand": brands["NVIDIA"], "price": 2100, "watts": 115, "vram": 8, "mhz": 2460.0, "score_bottleneck": 170, "rarity": "common"},
            {"model": "RTX 4070 Ti SUPER", "brand": brands["NVIDIA"], "price": 11000, "watts": 285, "vram": 16, "mhz": 2610.0, "score_bottleneck": 350, "rarity": "uncommon"},
            {"model": "RTX 5060 Ti", "brand": brands["NVIDIA"], "price": 3400, "watts": 180, "vram": 16, "mhz": 2572.0, "score_bottleneck": 230, "rarity": "common"},
            {"model": "RX 7800 XT", "brand": brands["AMD"], "price": 6700, "watts": 263, "vram": 16, "mhz": 2430.0, "score_bottleneck": 290, "rarity": "common"},
            {"model": "RX 7600 XT", "brand": brands["AMD"], "price": 2550, "watts": 190, "vram": 16, "mhz": 2470.0, "score_bottleneck": 200, "rarity": "common"},
            {"model": "Radeon PRO W7900", "brand": brands["AMD"], "price": 17000, "watts": 295, "vram": 48, "mhz": 2500.0, "score_bottleneck": 460, "rarity": "uncommon"},
            {"model": "RTX A6000", "brand": brands["NVIDIA"], "price": 15500, "watts": 300, "vram": 48, "mhz": 1800.0, "score_bottleneck": 440, "rarity": "uncommon"},
            {"model": "RTX 4500 Ada", "brand": brands["NVIDIA"], "price": 7900, "watts": 210, "vram": 24, "mhz": 2580.0, "score_bottleneck": 330, "rarity": "uncommon"},
            {"model": "L4", "brand": brands["NVIDIA"], "price": 4300, "watts": 72, "vram": 24, "mhz": 2040.0, "score_bottleneck": 260, "rarity": "common"},
            {"model": "A40", "brand": brands["NVIDIA"], "price": 14000, "watts": 300, "vram": 48, "mhz": 1740.0, "score_bottleneck": 400, "rarity": "uncommon"},
            {"model": "Instinct MI250X", "brand": brands["AMD"], "price": 78000, "watts": 560, "vram": 128, "mhz": 1700.0, "score_bottleneck": 720, "rarity": "epic"},
            {"model": "Instinct MI210", "brand": brands["AMD"], "price": 34000, "watts": 300, "vram": 64, "mhz": 1700.0, "score_bottleneck": 560, "rarity": "very-rare"},
            {"model": "RTX 6090 Ti (Rubin, especulativo)", "brand": brands["NVIDIA"], "price": 68000, "watts": 600, "vram": 48, "mhz": 2900.0, "score_bottleneck": 720, "rarity": "epic"},
            {"model": "RTX 6080 (Rubin, especulativo)", "brand": brands["NVIDIA"], "price": 32000, "watts": 400, "vram": 24, "mhz": 2800.0, "score_bottleneck": 560, "rarity": "very-rare"},
            {"model": "Rubin Ultra R300 (especulativo)", "brand": brands["NVIDIA"], "price": 550000, "watts": 1500, "vram": 384, "mhz": 2600.0, "score_bottleneck": 2600, "rarity": "iris"},
            {"model": "Rubin CPX (especulativo)", "brand": brands["NVIDIA"], "price": 205000, "watts": 800, "vram": 128, "mhz": 2500.0, "score_bottleneck": 1050, "rarity": "ancestral"},
            {"model": "Feynman F1 (pós-Rubin, especulativo)", "brand": brands["NVIDIA"], "price": 3500000, "watts": 1600, "vram": 512, "mhz": 2700.0, "score_bottleneck": 3000, "rarity": "iris"},
            {"model": "Instinct MI500X (especulativo)", "brand": brands["AMD"], "price": 400000, "watts": 1200, "vram": 432, "mhz": 2400.0, "score_bottleneck": 1600, "rarity": "pearlescent"},
            {"model": "Instinct MI450 (especulativo)", "brand": brands["AMD"], "price": 260000, "watts": 1100, "vram": 288, "mhz": 2350.0, "score_bottleneck": 1420, "rarity": "legendary"},
            {"model": "Radeon RX 10900 XTX (UDNA, especulativo)", "brand": brands["AMD"], "price": 30000, "watts": 500, "vram": 32, "mhz": 2700.0, "score_bottleneck": 540, "rarity": "very-rare"},
            {"model": "Radeon PRO W9900 (especulativo)", "brand": brands["AMD"], "price": 42000, "watts": 350, "vram": 64, "mhz": 2650.0, "score_bottleneck": 600, "rarity": "epic"},
            {"model": "RTX PRO 8000 Blackwell Ultra (especulativo)", "brand": brands["NVIDIA"], "price": 82000, "watts": 700, "vram": 128, "mhz": 2700.0, "score_bottleneck": 780, "rarity": "epic"},
            {"model": "GB300 NVL144 Superchip GPU (especulativo)", "brand": brands["NVIDIA"], "price": 300000, "watts": 1400, "vram": 288, "mhz": 2200.0, "score_bottleneck": 1500, "rarity": "pearlescent"},
            {"model": "Arc B770", "brand": brands["Intel"], "price": 3200, "watts": 190, "vram": 16, "mhz": 2450.0, "score_bottleneck": 220, "rarity": "common"},
        ]


        # 4. Dados de RAMs (44 modelos - real + itens ainda no papel)
        rams_data = [
            {"model": "Corsair Vengeance DDR5", "brand": brands["Corsair"], "price": 920, "watts": 6, "mhz": 6000, "gb": 32, "rarity": "common"},
            {"model": "Corsair Dominator Platinum DDR5", "brand": brands["Corsair"], "price": 2700, "watts": 8, "mhz": 6400, "gb": 64, "rarity": "very-rare"},
            {"model": "G.Skill Trident Z5 RGB", "brand": brands["G.Skill"], "price": 1400, "watts": 7, "mhz": 7200, "gb": 32, "rarity": "uncommon"},
            {"model": "Kingston Fury Renegade Pro DDR5 ECC RDIMM", "brand": brands["Kingston"], "price": 2200, "watts": 9, "mhz": 5600, "gb": 64, "rarity": "uncommon"},
            {"model": "Kingston Server Premier DDR5 ECC RDIMM 128GB", "brand": brands["Kingston"], "price": 6800, "watts": 10, "mhz": 5600, "gb": 128, "rarity": "epic"},
            {"model": "Samsung DDR5 ECC RDIMM 128GB", "brand": brands["Samsung"], "price": 5600, "watts": 10, "mhz": 5600, "gb": 128, "rarity": "epic"},
            {"model": "SK Hynix DDR5 ECC RDIMM 256GB", "brand": brands["SK Hynix"], "price": 19500, "watts": 12, "mhz": 5600, "gb": 256, "rarity": "ancestral"},
            {"model": "Micron DDR5 ECC RDIMM 96GB", "brand": brands["Micron"], "price": 3800, "watts": 9, "mhz": 6400, "gb": 96, "rarity": "epic"},
            {"model": "Kingston Fury Beast DDR5", "brand": brands["Kingston"], "price": 480, "watts": 5, "mhz": 5600, "gb": 16, "rarity": "common"},
            {"model": "Kingston Fury Beast RGB DDR5", "brand": brands["Kingston"], "price": 900, "watts": 6, "mhz": 6000, "gb": 32, "rarity": "common"},
            {"model": "Crucial Pro DDR5", "brand": brands["Crucial"], "price": 890, "watts": 6, "mhz": 6000, "gb": 32, "rarity": "common"},
            {"model": "Kioxia/SK Hynix DDR5 ECC RDIMM 512GB", "brand": brands["SK Hynix"], "price": 58000, "watts": 14, "mhz": 6400, "gb": 512, "rarity": "legendary"},
            {"model": "Corsair Vengeance DDR5 16GB", "brand": brands["Corsair"], "price": 480, "watts": 5, "mhz": 5600, "gb": 16, "rarity": "common"},
            {"model": "G.Skill Ripjaws S5 DDR5", "brand": brands["G.Skill"], "price": 1200, "watts": 6, "mhz": 6400, "gb": 32, "rarity": "uncommon"},
            {"model": "G.Skill Trident Z5 Neo DDR5", "brand": brands["G.Skill"], "price": 1300, "watts": 7, "mhz": 6800, "gb": 32, "rarity": "uncommon"},
            {"model": "Corsair Vengeance DDR5 96GB", "brand": brands["Corsair"], "price": 3600, "watts": 8, "mhz": 6000, "gb": 96, "rarity": "very-rare"},
            {"model": "Kingston Fury Renegade DDR5", "brand": brands["Kingston"], "price": 1350, "watts": 7, "mhz": 7200, "gb": 32, "rarity": "uncommon"},
            {"model": "Crucial DDR5 Laptop SODIMM 32GB", "brand": brands["Crucial"], "price": 850, "watts": 4, "mhz": 5600, "gb": 32, "rarity": "common"},
            {"model": "Micron DDR5 RDIMM 32GB", "brand": brands["Micron"], "price": 620, "watts": 6, "mhz": 5200, "gb": 32, "rarity": "common"},
            {"model": "Samsung DDR5 ECC RDIMM 64GB", "brand": brands["Samsung"], "price": 2100, "watts": 9, "mhz": 5600, "gb": 64, "rarity": "uncommon"},
            {"model": "SK Hynix DDR5 ECC RDIMM 96GB", "brand": brands["SK Hynix"], "price": 3400, "watts": 9, "mhz": 6000, "gb": 96, "rarity": "very-rare"},
            {"model": "Kingston Server Premier DDR5 ECC RDIMM 64GB", "brand": brands["Kingston"], "price": 1950, "watts": 8, "mhz": 5200, "gb": 64, "rarity": "uncommon"},
            {"model": "Micron DDR5 ECC RDIMM 32GB", "brand": brands["Micron"], "price": 700, "watts": 6, "mhz": 5600, "gb": 32, "rarity": "common"},
            {"model": "Crucial Pro DDR5 64GB", "brand": brands["Crucial"], "price": 2600, "watts": 7, "mhz": 6000, "gb": 64, "rarity": "very-rare"},
            {"model": "Kioxia/SK Hynix DDR5 ECC RDIMM 384GB", "brand": brands["SK Hynix"], "price": 30000, "watts": 13, "mhz": 6000, "gb": 384, "rarity": "legendary"},
            {"model": "Samsung DDR5 ECC RDIMM 256GB", "brand": brands["Samsung"], "price": 16000, "watts": 11, "mhz": 5600, "gb": 256, "rarity": "ancestral"},
            {"model": "Western Digital (SanDisk) DDR5 SODIMM 16GB", "brand": brands["Western Digital"], "price": 400, "watts": 4, "mhz": 5200, "gb": 16, "rarity": "common"},
            {"model": "Corsair Dominator Titanium DDR5", "brand": brands["Corsair"], "price": 3100, "watts": 8, "mhz": 7200, "gb": 64, "rarity": "very-rare"},
            {"model": "G.Skill Trident Z5 RGB 128GB Kit", "brand": brands["G.Skill"], "price": 7200, "watts": 10, "mhz": 6400, "gb": 128, "rarity": "epic"},
            {"model": "Samsung DDR6 Extreme 32GB (especulativo)", "brand": brands["Samsung"], "price": 1700, "watts": 6, "mhz": 10000, "gb": 32, "rarity": "uncommon"},
            {"model": "SK Hynix DDR6 RDIMM 128GB (especulativo)", "brand": brands["SK Hynix"], "price": 13800, "watts": 12, "mhz": 9600, "gb": 128, "rarity": "ancestral"},
            {"model": "SK Hynix DDR6 ECC RDIMM 512GB (especulativo)", "brand": brands["SK Hynix"], "price": 95000, "watts": 16, "mhz": 9200, "gb": 512, "rarity": "pearlescent"},
            {"model": "Micron DDR6 ECC RDIMM 256GB (especulativo)", "brand": brands["Micron"], "price": 42000, "watts": 14, "mhz": 9600, "gb": 256, "rarity": "legendary"},
            {"model": "Corsair Dominator DDR6 (especulativo)", "brand": brands["Corsair"], "price": 5400, "watts": 9, "mhz": 10400, "gb": 64, "rarity": "epic"},
            {"model": "G.Skill Trident Z6 RGB (especulativo)", "brand": brands["G.Skill"], "price": 3300, "watts": 8, "mhz": 11000, "gb": 48, "rarity": "very-rare"},
            {"model": "Kingston Fury DDR6 Renegade (especulativo)", "brand": brands["Kingston"], "price": 3200, "watts": 8, "mhz": 10600, "gb": 48, "rarity": "very-rare"},
            {"model": "Kingston Server Premier DDR6 ECC RDIMM 1TB (especulativo)", "brand": brands["Kingston"], "price": 98000, "watts": 20, "mhz": 8800, "gb": 1024, "rarity": "pearlescent"},
            {"model": "Samsung DDR6 ECC RDIMM 1TB (especulativo)", "brand": brands["Samsung"], "price": 110000, "watts": 20, "mhz": 9000, "gb": 1024, "rarity": "iris"},
            {"model": "Micron DDR6 CXL Pooled Memory 2TB (especulativo)", "brand": brands["Micron"], "price": 140000, "watts": 28, "mhz": 8000, "gb": 2048, "rarity": "iris"},
            {"model": "Crucial DDR6 Pro 64GB (especulativo)", "brand": brands["Crucial"], "price": 3900, "watts": 8, "mhz": 9800, "gb": 64, "rarity": "epic"},
            {"model": "Western Digital HBM-Class Cache DIMM 128GB (especulativo)", "brand": brands["Western Digital"], "price": 13500, "watts": 15, "mhz": 8800, "gb": 128, "rarity": "ancestral"},
            {"model": "SK Hynix HBM4 Stack Module 192GB (especulativo)", "brand": brands["SK Hynix"], "price": 25000, "watts": 30, "mhz": 12000, "gb": 192, "rarity": "legendary"},
            {"model": "Samsung HBM4E Stack Module 288GB (especulativo)", "brand": brands["Samsung"], "price": 62000, "watts": 34, "mhz": 12800, "gb": 288, "rarity": "pearlescent"},
            {"model": "Micron HBM4 Stack Module 192GB (especulativo)", "brand": brands["Micron"], "price": 24000, "watts": 30, "mhz": 12000, "gb": 192, "rarity": "ancestral"},
        ]


        # 5. Dados de SSDs (44 modelos - real + itens ainda no papel)
        ssds_data = [
            {"model": "Kingston KC3000", "brand": brands["Kingston"], "price": 850, "watts": 5, "gb": 1024, "speed": 7000, "rarity": "common"},
            {"model": "Samsung 990 PRO", "brand": brands["Samsung"], "price": 1300, "watts": 6, "gb": 2000, "speed": 7450, "rarity": "uncommon"},
            {"model": "Crucial T705 PCIe 5.0", "brand": brands["Crucial"], "price": 3900, "watts": 10, "gb": 2000, "speed": 14500, "rarity": "very-rare"},
            {"model": "Samsung PM9A3 Enterprise NVMe 3.84TB", "brand": brands["Samsung"], "price": 2500, "watts": 12, "gb": 3840, "speed": 6800, "rarity": "uncommon"},
            {"model": "Kioxia CM7 Enterprise NVMe 7.68TB", "brand": brands["Kioxia"], "price": 18500, "watts": 14, "gb": 7680, "speed": 14000, "rarity": "epic"},
            {"model": "Solidigm D5-P5336 Enterprise NVMe 15.36TB", "brand": brands["Solidigm"], "price": 17800, "watts": 15, "gb": 15360, "speed": 7000, "rarity": "epic"},
            {"model": "Micron 9550 Enterprise NVMe 7.68TB", "brand": brands["Micron"], "price": 16200, "watts": 16, "gb": 7680, "speed": 14000, "rarity": "epic"},
            {"model": "Kingston NV3", "brand": brands["Kingston"], "price": 290, "watts": 4, "gb": 500, "speed": 5000, "rarity": "common"},
            {"model": "Samsung 990 EVO Plus", "brand": brands["Samsung"], "price": 750, "watts": 4, "gb": 1000, "speed": 7150, "rarity": "common"},
            {"model": "WD Black SN8100", "brand": brands["Western Digital"], "price": 4600, "watts": 8, "gb": 2000, "speed": 14900, "rarity": "very-rare"},
            {"model": "Solidigm D5-P5336 Enterprise NVMe 30.72TB", "brand": brands["Solidigm"], "price": 48000, "watts": 18, "gb": 30720, "speed": 7000, "rarity": "ancestral"},
            {"model": "Kingston NV2", "brand": brands["Kingston"], "price": 220, "watts": 3, "gb": 500, "speed": 3500, "rarity": "common"},
            {"model": "Kingston KC3000 2TB", "brand": brands["Kingston"], "price": 1150, "watts": 6, "gb": 2000, "speed": 7000, "rarity": "uncommon"},
            {"model": "Samsung 990 EVO", "brand": brands["Samsung"], "price": 500, "watts": 4, "gb": 1000, "speed": 5000, "rarity": "common"},
            {"model": "Samsung 9100 PRO", "brand": brands["Samsung"], "price": 4200, "watts": 9, "gb": 2000, "speed": 14800, "rarity": "very-rare"},
            {"model": "Crucial T500", "brand": brands["Crucial"], "price": 900, "watts": 6, "gb": 1000, "speed": 7400, "rarity": "common"},
            {"model": "Crucial P310", "brand": brands["Crucial"], "price": 600, "watts": 3, "gb": 1000, "speed": 6600, "rarity": "common"},
            {"model": "WD Black SN850X", "brand": brands["Western Digital"], "price": 1250, "watts": 6, "gb": 2000, "speed": 7300, "rarity": "uncommon"},
            {"model": "WD Blue SN5000", "brand": brands["Western Digital"], "price": 550, "watts": 4, "gb": 1000, "speed": 5500, "rarity": "common"},
            {"model": "Kioxia Exceria Plus G4", "brand": brands["Kioxia"], "price": 680, "watts": 5, "gb": 1000, "speed": 7000, "rarity": "common"},
            {"model": "Solidigm P44 Pro", "brand": brands["Solidigm"], "price": 1100, "watts": 6, "gb": 2000, "speed": 7000, "rarity": "uncommon"},
            {"model": "Micron 4600", "brand": brands["Micron"], "price": 1400, "watts": 7, "gb": 2000, "speed": 10000, "rarity": "uncommon"},
            {"model": "Kioxia CD8P Enterprise NVMe 3.84TB", "brand": brands["Kioxia"], "price": 3600, "watts": 11, "gb": 3840, "speed": 6900, "rarity": "very-rare"},
            {"model": "Samsung PM1743 Enterprise NVMe 7.68TB", "brand": brands["Samsung"], "price": 12800, "watts": 13, "gb": 7680, "speed": 13000, "rarity": "epic"},
            {"model": "Micron 7450 Enterprise NVMe 3.84TB", "brand": brands["Micron"], "price": 2200, "watts": 10, "gb": 3840, "speed": 6800, "rarity": "uncommon"},
            {"model": "Solidigm D5-P5430 Enterprise NVMe 7.68TB", "brand": brands["Solidigm"], "price": 8600, "watts": 12, "gb": 7680, "speed": 6300, "rarity": "very-rare"},
            {"model": "Kingston DC3000ME Enterprise NVMe 3.2TB", "brand": brands["Kingston"], "price": 1600, "watts": 10, "gb": 3200, "speed": 6800, "rarity": "uncommon"},
            {"model": "WD Ultrastar DC SN861 Enterprise NVMe 15.36TB", "brand": brands["Western Digital"], "price": 25500, "watts": 16, "gb": 15360, "speed": 7100, "rarity": "ancestral"},
            {"model": "Kioxia CM7 Enterprise NVMe 15.36TB", "brand": brands["Kioxia"], "price": 34000, "watts": 17, "gb": 15360, "speed": 14000, "rarity": "ancestral"},
            {"model": "Micron 9550 Enterprise NVMe 30.72TB", "brand": brands["Micron"], "price": 62000, "watts": 20, "gb": 30720, "speed": 14000, "rarity": "legendary"},
            {"model": "Samsung PM9D3a Enterprise NVMe 61.44TB", "brand": brands["Samsung"], "price": 88000, "watts": 22, "gb": 61440, "speed": 13000, "rarity": "legendary"},
            {"model": "Crucial T910 PCIe 6.0 (especulativo)", "brand": brands["Crucial"], "price": 26000, "watts": 12, "gb": 4000, "speed": 28000, "rarity": "ancestral"},
            {"model": "Samsung 9900 PRO PCIe 6.0 (especulativo)", "brand": brands["Samsung"], "price": 19500, "watts": 12, "gb": 4000, "speed": 27000, "rarity": "ancestral"},
            {"model": "WD Black SN9100 PCIe 6.0 (especulativo)", "brand": brands["Western Digital"], "price": 15200, "watts": 11, "gb": 4000, "speed": 26500, "rarity": "epic"},
            {"model": "Kingston KC4000 PCIe 6.0 (especulativo)", "brand": brands["Kingston"], "price": 8900, "watts": 10, "gb": 2000, "speed": 25000, "rarity": "very-rare"},
            {"model": "Kioxia CD9Q Enterprise NVMe PCIe 6.0 30.72TB (especulativo)", "brand": brands["Kioxia"], "price": 88000, "watts": 22, "gb": 30720, "speed": 26000, "rarity": "legendary"},
            {"model": "Solidigm D7-P5810 Enterprise PCIe 6.0 61.44TB (especulativo)", "brand": brands["Solidigm"], "price": 112000, "watts": 25, "gb": 61440, "speed": 26500, "rarity": "pearlescent"},
            {"model": "Micron 9650 Enterprise NVMe PCIe 6.0 61.44TB (especulativo)", "brand": brands["Micron"], "price": 175000, "watts": 26, "gb": 61440, "speed": 27000, "rarity": "pearlescent"},
            {"model": "Samsung PM9E3 Enterprise NVMe PCIe 6.0 122.88TB (especulativo)", "brand": brands["Samsung"], "price": 320000, "watts": 30, "gb": 122880, "speed": 26000, "rarity": "iris"},
            {"model": "SK Hynix PEB110 Enterprise QLC 122.88TB (especulativo)", "brand": brands["SK Hynix"], "price": 105000, "watts": 28, "gb": 122880, "speed": 12000, "rarity": "pearlescent"},
            {"model": "Kioxia LC9 QLC Enterprise 245.76TB (especulativo)", "brand": brands["Kioxia"], "price": 190000, "watts": 32, "gb": 245760, "speed": 11000, "rarity": "iris"},
            {"model": "Solidigm D5-P5336 QLC 61.44TB", "brand": brands["Solidigm"], "price": 52000, "watts": 20, "gb": 61440, "speed": 7000, "rarity": "legendary"},
            {"model": "WD Gold Enterprise NVMe 7.68TB", "brand": brands["Western Digital"], "price": 9800, "watts": 13, "gb": 7680, "speed": 6900, "rarity": "epic"},
            {"model": "Kingston DC3000ME Enterprise NVMe 6.4TB", "brand": brands["Kingston"], "price": 7400, "watts": 12, "gb": 6400, "speed": 6900, "rarity": "very-rare"},
        ]


        # --- Insercao e Atualizacao Segura no Banco ---

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