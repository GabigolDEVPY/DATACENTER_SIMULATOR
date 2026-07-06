from django.core.management.base import BaseCommand
from hardware.models import CPU, GPU, RAM, SSD, Brand


class Command(BaseCommand):
    help = "Popula o banco com CPUs, GPUs, RAMs, SSDs e Brands"

    def handle(self, *args, **options):
        brands = {
            "NVIDIA": 1,
            "AMD": 2,
            "Intel": 3,
            "Samsung": 4,
            "Micron": 5,
            "SK Hynix": 6,
            "Kingston Server": 7,
            "Solidigm": 8,
            "Kioxia": 9,
            "Kingston": 10,
        }

        # Cria as Brands no banco (id fixo pra bater com o dict acima)
        Brand.objects.bulk_create(
            [Brand(id=brand_id, name=name) for name, brand_id in brands.items()],
            ignore_conflicts=True,
        )

        pecas = [
            # ===========================
            # GPUs
            # ===========================

            {
                "type": "GPU",
                "model": "NVIDIA GB200 Grace Blackwell",
                "brand": brands["NVIDIA"],
                "price": 70000,
                "watts": 2700,
                "is_active": True,
                "score_bottleneck": 3000,
            },
            {
                "type": "GPU",
                "model": "NVIDIA B200",
                "brand": brands["NVIDIA"],
                "price": 35000,
                "watts": 1000,
                "is_active": True,
                "score_bottleneck": 2500,
            },
            {
                "type": "GPU",
                "model": "NVIDIA H200 SXM",
                "brand": brands["NVIDIA"],
                "price": 40000,
                "watts": 700,
                "is_active": True,
                "score_bottleneck": 2000,
            },
            {
                "type": "GPU",
                "model": "AMD Instinct MI325X",
                "brand": brands["AMD"],
                "price": 30000,
                "watts": 750,
                "is_active": True,
                "score_bottleneck": 2000,
            },
            {
                "type": "GPU",
                "model": "AMD Instinct MI300X",
                "brand": brands["AMD"],
                "price": 25000,
                "watts": 750,
                "is_active": True,
                "score_bottleneck": 1800,
            },
            {
                "type": "GPU",
                "model": "NVIDIA H100 SXM",
                "brand": brands["NVIDIA"],
                "price": 30000,
                "watts": 700,
                "is_active": True,
                "score_bottleneck": 1800,
            },
            {
                "type": "GPU",
                "model": "NVIDIA H100 PCIe",
                "brand": brands["NVIDIA"],
                "price": 27000,
                "watts": 350,
                "is_active": True,
                "score_bottleneck": 1600,
            },
            {
                "type": "GPU",
                "model": "NVIDIA A100 80GB",
                "brand": brands["NVIDIA"],
                "price": 18000,
                "watts": 400,
                "is_active": True,
                "score_bottleneck": 1200,
            },
            {
                "type": "GPU",
                "model": "AMD Instinct MI250X",
                "brand": brands["AMD"],
                "price": 15000,
                "watts": 560,
                "is_active": True,
                "score_bottleneck": 1200,
            },
            {
                "type": "GPU",
                "model": "NVIDIA L40S",
                "brand": brands["NVIDIA"],
                "price": 9000,
                "watts": 350,
                "is_active": True,
                "score_bottleneck": 800,
            },

            # ===========================
            # CPUs
            # ===========================

            {
                "type": "CPU",
                "model": "AMD EPYC 9965",
                "brand": brands["AMD"],
                "price": 15000,
                "watts": 500,
                "is_active": True,
                "score_bottleneck": 3000,
            },
            {
                "type": "CPU",
                "model": "AMD EPYC 9755",
                "brand": brands["AMD"],
                "price": 13000,
                "watts": 500,
                "is_active": True,
                "score_bottleneck": 2500,
            },
            {
                "type": "CPU",
                "model": "Intel Xeon 6980P",
                "brand": brands["Intel"],
                "price": 13000,
                "watts": 500,
                "is_active": True,
                "score_bottleneck": 2500,
            },
            {
                "type": "CPU",
                "model": "AMD EPYC 9655",
                "brand": brands["AMD"],
                "price": 11500,
                "watts": 400,
                "is_active": True,
                "score_bottleneck": 2000,
            },
            {
                "type": "CPU",
                "model": "AMD EPYC 9654",
                "brand": brands["AMD"],
                "price": 11000,
                "watts": 360,
                "is_active": True,
                "score_bottleneck": 1900,
            },
            {
                "type": "CPU",
                "model": "Intel Xeon Platinum 8592+",
                "brand": brands["Intel"],
                "price": 10000,
                "watts": 350,
                "is_active": True,
                "score_bottleneck": 1600,
            },
            {
                "type": "CPU",
                "model": "AMD EPYC 9554",
                "brand": brands["AMD"],
                "price": 8500,
                "watts": 360,
                "is_active": True,
                "score_bottleneck": 1600,
            },
            {
                "type": "CPU",
                "model": "Intel Xeon Platinum 8480+",
                "brand": brands["Intel"],
                "price": 8000,
                "watts": 350,
                "is_active": True,
                "score_bottleneck": 1400,
            },
            {
                "type": "CPU",
                "model": "AMD EPYC 9454",
                "brand": brands["AMD"],
                "price": 6000,
                "watts": 290,
                "is_active": True,
                "score_bottleneck": 1200,
            },
            {
                "type": "CPU",
                "model": "Intel Xeon Gold 6548Y+",
                "brand": brands["Intel"],
                "price": 4200,
                "watts": 250,
                "is_active": True,
                "score_bottleneck": 800,
            },

            # ===========================
            # RAMs
            # ===========================

            {
                "type": "RAM",
                "model": "Samsung DDR5 ECC RDIMM 512GB",
                "brand": brands["Samsung"],
                "price": 4500,
                "watts": 18,
                "is_active": True,
            },
            {
                "type": "RAM",
                "model": "Micron DDR5 ECC RDIMM 512GB",
                "brand": brands["Micron"],
                "price": 4400,
                "watts": 18,
                "is_active": True,
            },
            {
                "type": "RAM",
                "model": "SK Hynix DDR5 ECC RDIMM 256GB",
                "brand": brands["SK Hynix"],
                "price": 2400,
                "watts": 15,
                "is_active": True,
            },
            {
                "type": "RAM",
                "model": "Samsung DDR5 ECC RDIMM 256GB",
                "brand": brands["Samsung"],
                "price": 2350,
                "watts": 15,
                "is_active": True,
            },
            {
                "type": "RAM",
                "model": "Micron DDR5 ECC RDIMM 128GB",
                "brand": brands["Micron"],
                "price": 1200,
                "watts": 12,
                "is_active": True,
            },
            {
                "type": "RAM",
                "model": "Samsung DDR5 ECC RDIMM 128GB",
                "brand": brands["Samsung"],
                "price": 1150,
                "watts": 12,
                "is_active": True,
            },
            {
                "type": "RAM",
                "model": "SK Hynix DDR5 ECC RDIMM 96GB",
                "brand": brands["SK Hynix"],
                "price": 850,
                "watts": 11,
                "is_active": True,
            },
            {
                "type": "RAM",
                "model": "Micron DDR5 ECC RDIMM 64GB",
                "brand": brands["Micron"],
                "price": 450,
                "watts": 10,
                "is_active": True,
            },
            {
                "type": "RAM",
                "model": "Samsung DDR5 ECC RDIMM 64GB",
                "brand": brands["Samsung"],
                "price": 430,
                "watts": 10,
                "is_active": True,
            },
            {
                "type": "RAM",
                "model": "Kingston Server DDR5 ECC RDIMM 32GB",
                "brand": brands["Kingston Server"],
                "price": 220,
                "watts": 8,
                "is_active": True,
            },

            # ===========================
            # SSDs
            # ===========================

            {
                "type": "SSD",
                "model": "Solidigm D5-P5336 122TB",
                "brand": brands["Solidigm"],
                "price": 12000,
                "watts": 25,
                "is_active": True,
            },
            {
                "type": "SSD",
                "model": "Micron 6550 ION 122TB",
                "brand": brands["Micron"],
                "price": 11500,
                "watts": 25,
                "is_active": True,
            },
            {
                "type": "SSD",
                "model": "Samsung PM1743 30.72TB",
                "brand": brands["Samsung"],
                "price": 4500,
                "watts": 20,
                "is_active": True,
            },
            {
                "type": "SSD",
                "model": "Kioxia CM7 30.72TB",
                "brand": brands["Kioxia"],
                "price": 4300,
                "watts": 20,
                "is_active": True,
            },
            {
                "type": "SSD",
                "model": "Micron 7450 PRO 30.72TB",
                "brand": brands["Micron"],
                "price": 4100,
                "watts": 18,
                "is_active": True,
            },
            {
                "type": "SSD",
                "model": "Samsung PM9A3 15.36TB",
                "brand": brands["Samsung"],
                "price": 2200,
                "watts": 14,
                "is_active": True,
            },
            {
                "type": "SSD",
                "model": "Solidigm D7-P5520 15.36TB",
                "brand": brands["Solidigm"],
                "price": 2100,
                "watts": 14,
                "is_active": True,
            },
            {
                "type": "SSD",
                "model": "Micron 7450 PRO 7.68TB",
                "brand": brands["Micron"],
                "price": 1100,
                "watts": 12,
                "is_active": True,
            },
            {
                "type": "SSD",
                "model": "Samsung PM893 3.84TB",
                "brand": brands["Samsung"],
                "price": 550,
                "watts": 6,
                "is_active": True,
            },
            {
                "type": "SSD",
                "model": "Kingston DC600M 1.92TB",
                "brand": brands["Kingston"],
                "price": 280,
                "watts": 4,
                "is_active": True,
            },
        ]

        def clean(peca):
            """Troca 'brand' (int) por 'brand_id' (int), que é o que o Django espera."""
            peca = peca.copy()
            peca["brand_id"] = peca.pop("brand")
            return peca

        GPU_DICT = [clean(gpu) for gpu in pecas if gpu["type"] == "GPU"]
        CPU_DICT = [clean(cpu) for cpu in pecas if cpu["type"] == "CPU"]
        SSD_DICT = [clean(ssd) for ssd in pecas if ssd["type"] == "SSD"]
        RAM_DICT = [clean(ram) for ram in pecas if ram["type"] == "RAM"]

        GPU.objects.bulk_create([GPU(**gpu) for gpu in GPU_DICT])
        CPU.objects.bulk_create([CPU(**cpu) for cpu in CPU_DICT])
        SSD.objects.bulk_create([SSD(**ssd) for ssd in SSD_DICT])
        RAM.objects.bulk_create([RAM(**ram) for ram in RAM_DICT])

        self.stdout.write(self.style.SUCCESS("Seed concluído com sucesso!"))