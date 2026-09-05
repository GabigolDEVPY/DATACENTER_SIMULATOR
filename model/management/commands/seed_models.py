from django.core.management.base import BaseCommand
from model.models import AIModel, MarkModel
from decimal import Decimal


class Command(BaseCommand):
    help = "Popula a base de dados com marcas e modelos de IA reais e futuros, com especificacoes reais de hardware necessario para inferencia/treinamento"

    def handle(self, *args, **options):
        # ==================== 1. Gerenciamento de Marcas ====================
        brand_names = [
            "Microsoft", "Meta", "Alibaba", "Google", "Google DeepMind",
            "HuggingFace", "EleutherAI", "TII", "Stability AI", "Mistral AI",
            "OpenAI", "Anthropic", "01.AI", "DeepSeek", "Databricks", "Cohere",
            "xAI", "Black Forest Labs", "Midjourney", "Runway", "Pika Labs",
            "Kuaishou", "Luma AI", "MiniMax", "ElevenLabs", "Suno", "Udio",
            "IBM", "LMSYS", "Meta AI", "Community", "Unknown",
        ]

        brands = {}
        for name in brand_names:
            brand, _ = MarkModel.objects.get_or_create(name=name)
            brands[name] = brand

        self.stdout.write(self.style.SUCCESS(f"{len(brands)} marcas mapeadas com sucesso!"))

        # ==================== 2. Dados dos Modelos ====================

        models_data = [
            # ==================== 01.AI ====================
            {"name": "Yi 6B", "level": 1, "mark_model": brands["01.AI"], "gpu_vram": 12, "ram_gb": 24, "storage_gb": 12, "price": Decimal("1600.00"), "base_revenue": Decimal("160.00"), "params": 6000000000},
            {"name": "Yi 1.5 6B", "level": 2, "mark_model": brands["01.AI"], "gpu_vram": 12, "ram_gb": 24, "storage_gb": 12, "price": Decimal("1700.00"), "base_revenue": Decimal("170.00"), "params": 6000000000},
            {"name": "Yi 9B", "level": 3, "mark_model": brands["01.AI"], "gpu_vram": 16, "ram_gb": 32, "storage_gb": 18, "price": Decimal("2400.00"), "base_revenue": Decimal("240.00"), "params": 9000000000},
            {"name": "Yi 1.5 9B", "level": 4, "mark_model": brands["01.AI"], "gpu_vram": 16, "ram_gb": 32, "storage_gb": 18, "price": Decimal("2500.00"), "base_revenue": Decimal("250.00"), "params": 9000000000},
            {"name": "Yi 34B", "level": 5, "mark_model": brands["01.AI"], "gpu_vram": 24, "ram_gb": 48, "storage_gb": 68, "price": Decimal("8500.00"), "base_revenue": Decimal("850.00"), "params": 34000000000},
            {"name": "Yi 1.5 34B", "level": 6, "mark_model": brands["01.AI"], "gpu_vram": 24, "ram_gb": 48, "storage_gb": 68, "price": Decimal("8500.00"), "base_revenue": Decimal("850.00"), "params": 34000000000},

            # ==================== Alibaba ====================
            {"name": "Qwen2 0.5B", "level": 1, "mark_model": brands["Alibaba"], "gpu_vram": 2, "ram_gb": 4, "storage_gb": 2, "price": Decimal("200.00"), "base_revenue": Decimal("20.00"), "params": 500000000},
            {"name": "Qwen2.5 0.5B", "level": 2, "mark_model": brands["Alibaba"], "gpu_vram": 2, "ram_gb": 4, "storage_gb": 2, "price": Decimal("220.00"), "base_revenue": Decimal("22.00"), "params": 500000000},
            {"name": "Qwen3 0.6B", "level": 3, "mark_model": brands["Alibaba"], "gpu_vram": 2, "ram_gb": 4, "storage_gb": 2, "price": Decimal("250.00"), "base_revenue": Decimal("25.00"), "params": 600000000},
            {"name": "Qwen2 1.5B", "level": 4, "mark_model": brands["Alibaba"], "gpu_vram": 4, "ram_gb": 8, "storage_gb": 3, "price": Decimal("450.00"), "base_revenue": Decimal("45.00"), "params": 1500000000},
            {"name": "Qwen2.5 1.5B", "level": 5, "mark_model": brands["Alibaba"], "gpu_vram": 4, "ram_gb": 8, "storage_gb": 3, "price": Decimal("480.00"), "base_revenue": Decimal("48.00"), "params": 1500000000},
            {"name": "Qwen3 1.7B", "level": 6, "mark_model": brands["Alibaba"], "gpu_vram": 4, "ram_gb": 8, "storage_gb": 3, "price": Decimal("500.00"), "base_revenue": Decimal("50.00"), "params": 1700000000},
            {"name": "Qwen2.5 3B", "level": 7, "mark_model": brands["Alibaba"], "gpu_vram": 6, "ram_gb": 12, "storage_gb": 5, "price": Decimal("750.00"), "base_revenue": Decimal("75.00"), "params": 3000000000},
            {"name": "Qwen3 4B", "level": 8, "mark_model": brands["Alibaba"], "gpu_vram": 8, "ram_gb": 16, "storage_gb": 7, "price": Decimal("1100.00"), "base_revenue": Decimal("110.00"), "params": 4000000000},
            {"name": "Qwen2 7B", "level": 9, "mark_model": brands["Alibaba"], "gpu_vram": 16, "ram_gb": 32, "storage_gb": 14, "price": Decimal("2100.00"), "base_revenue": Decimal("210.00"), "params": 7000000000},
            {"name": "Qwen2.5 7B", "level": 10, "mark_model": brands["Alibaba"], "gpu_vram": 16, "ram_gb": 32, "storage_gb": 14, "price": Decimal("2400.00"), "base_revenue": Decimal("240.00"), "params": 7000000000},
            {"name": "Qwen3 8B", "level": 11, "mark_model": brands["Alibaba"], "gpu_vram": 16, "ram_gb": 32, "storage_gb": 16, "price": Decimal("2600.00"), "base_revenue": Decimal("260.00"), "params": 8000000000},
            {"name": "Qwen2.5 14B", "level": 12, "mark_model": brands["Alibaba"], "gpu_vram": 24, "ram_gb": 48, "storage_gb": 28, "price": Decimal("3800.00"), "base_revenue": Decimal("380.00"), "params": 14000000000},
            {"name": "Qwen3 14B", "level": 13, "mark_model": brands["Alibaba"], "gpu_vram": 24, "ram_gb": 48, "storage_gb": 28, "price": Decimal("4000.00"), "base_revenue": Decimal("400.00"), "params": 14000000000},
            {"name": "Qwen3 30B-A3B (MoE)", "level": 14, "mark_model": brands["Alibaba"], "gpu_vram": 24, "ram_gb": 48, "storage_gb": 60, "price": Decimal("7500.00"), "base_revenue": Decimal("750.00"), "params": 30000000000},
            {"name": "Qwen3 32B", "level": 15, "mark_model": brands["Alibaba"], "gpu_vram": 24, "ram_gb": 48, "storage_gb": 64, "price": Decimal("8000.00"), "base_revenue": Decimal("800.00"), "params": 32000000000},
            {"name": "Qwen2 72B", "level": 16, "mark_model": brands["Alibaba"], "gpu_vram": 80, "ram_gb": 128, "storage_gb": 144, "price": Decimal("18000.00"), "base_revenue": Decimal("1800.00"), "params": 72000000000},
            {"name": "Qwen2.5 72B", "level": 17, "mark_model": brands["Alibaba"], "gpu_vram": 80, "ram_gb": 128, "storage_gb": 144, "price": Decimal("19000.00"), "base_revenue": Decimal("1900.00"), "params": 72000000000},
            {"name": "Qwen3 235B-A22B (MoE)", "level": 18, "mark_model": brands["Alibaba"], "gpu_vram": 320, "ram_gb": 512, "storage_gb": 470, "price": Decimal("118000.00"), "base_revenue": Decimal("11800.00"), "params": 235000000000},
            {"name": "Qwen4", "level": 19, "mark_model": brands["Alibaba"], "gpu_vram": 2048, "ram_gb": 4096, "storage_gb": 4800, "price": Decimal("1200000.00"), "base_revenue": Decimal("120000.00"), "params": 2600000000000},
            {"name": "Qwen5", "level": 20, "mark_model": brands["Alibaba"], "gpu_vram": 4096, "ram_gb": 8192, "storage_gb": 11000, "price": Decimal("2750000.00"), "base_revenue": Decimal("275000.00"), "params": 7500000000000},

            # ==================== Anthropic ====================
            {"name": "Claude 3 Haiku", "level": 1, "mark_model": brands["Anthropic"], "gpu_vram": 24, "ram_gb": 48, "storage_gb": 80, "price": Decimal("10000.00"), "base_revenue": Decimal("1000.00"), "params": 50000000000},
            {"name": "Claude 3.5 Haiku", "level": 2, "mark_model": brands["Anthropic"], "gpu_vram": 24, "ram_gb": 48, "storage_gb": 90, "price": Decimal("11250.00"), "base_revenue": Decimal("1125.00"), "params": 60000000000},
            {"name": "Claude 1", "level": 3, "mark_model": brands["Anthropic"], "gpu_vram": 80, "ram_gb": 128, "storage_gb": 200, "price": Decimal("25000.00"), "base_revenue": Decimal("2500.00"), "params": 150000000000},
            {"name": "Claude 1.3", "level": 4, "mark_model": brands["Anthropic"], "gpu_vram": 80, "ram_gb": 128, "storage_gb": 220, "price": Decimal("27500.00"), "base_revenue": Decimal("2750.00"), "params": 160000000000},
            {"name": "Claude 2", "level": 5, "mark_model": brands["Anthropic"], "gpu_vram": 80, "ram_gb": 128, "storage_gb": 240, "price": Decimal("30000.00"), "base_revenue": Decimal("3000.00"), "params": 180000000000},
            {"name": "Claude 2.1", "level": 6, "mark_model": brands["Anthropic"], "gpu_vram": 80, "ram_gb": 128, "storage_gb": 260, "price": Decimal("32500.00"), "base_revenue": Decimal("3250.00"), "params": 200000000000},
            {"name": "Claude 3 Sonnet", "level": 7, "mark_model": brands["Anthropic"], "gpu_vram": 80, "ram_gb": 128, "storage_gb": 280, "price": Decimal("35000.00"), "base_revenue": Decimal("3500.00"), "params": 220000000000},
            {"name": "Claude 3.5 Sonnet", "level": 8, "mark_model": brands["Anthropic"], "gpu_vram": 80, "ram_gb": 128, "storage_gb": 320, "price": Decimal("40000.00"), "base_revenue": Decimal("4000.00"), "params": 280000000000},
            {"name": "Claude 3.5 Sonnet v2", "level": 9, "mark_model": brands["Anthropic"], "gpu_vram": 80, "ram_gb": 128, "storage_gb": 340, "price": Decimal("42500.00"), "base_revenue": Decimal("4250.00"), "params": 300000000000},
            {"name": "Claude 4 Haiku", "level": 10, "mark_model": brands["Anthropic"], "gpu_vram": 80, "ram_gb": 128, "storage_gb": 380, "price": Decimal("47500.00"), "base_revenue": Decimal("4750.00"), "params": 350000000000},
            {"name": "Claude 3 Opus", "level": 11, "mark_model": brands["Anthropic"], "gpu_vram": 320, "ram_gb": 512, "storage_gb": 600, "price": Decimal("75000.00"), "base_revenue": Decimal("7500.00"), "params": 500000000000},
            {"name": "Claude 3.5 Opus", "level": 12, "mark_model": brands["Anthropic"], "gpu_vram": 320, "ram_gb": 512, "storage_gb": 700, "price": Decimal("87500.00"), "base_revenue": Decimal("8750.00"), "params": 600000000000},
            {"name": "Claude 4 Sonnet", "level": 13, "mark_model": brands["Anthropic"], "gpu_vram": 320, "ram_gb": 512, "storage_gb": 800, "price": Decimal("100000.00"), "base_revenue": Decimal("10000.00"), "params": 700000000000},
            {"name": "Claude 5 Haiku", "level": 14, "mark_model": brands["Anthropic"], "gpu_vram": 320, "ram_gb": 512, "storage_gb": 1000, "price": Decimal("125000.00"), "base_revenue": Decimal("12500.00"), "params": 800000000000},
            {"name": "Claude 4 Opus", "level": 15, "mark_model": brands["Anthropic"], "gpu_vram": 640, "ram_gb": 1024, "storage_gb": 1400, "price": Decimal("175000.00"), "base_revenue": Decimal("17500.00"), "params": 1200000000000},
            {"name": "Claude 5 Sonnet", "level": 16, "mark_model": brands["Anthropic"], "gpu_vram": 640, "ram_gb": 1024, "storage_gb": 1800, "price": Decimal("225000.00"), "base_revenue": Decimal("22500.00"), "params": 1500000000000},
            {"name": "Claude 5 Opus", "level": 17, "mark_model": brands["Anthropic"], "gpu_vram": 2048, "ram_gb": 4096, "storage_gb": 4000, "price": Decimal("1000000.00"), "base_revenue": Decimal("100000.00"), "params": 3000000000000},
            {"name": "Claude 6", "level": 18, "mark_model": brands["Anthropic"], "gpu_vram": 4096, "ram_gb": 8192, "storage_gb": 10000, "price": Decimal("2500000.00"), "base_revenue": Decimal("250000.00"), "params": 8000000000000},
            {"name": "Claude 7", "level": 19, "mark_model": brands["Anthropic"], "gpu_vram": 8192, "ram_gb": 16384, "storage_gb": 20000, "price": Decimal("5000000.00"), "base_revenue": Decimal("500000.00"), "params": 15000000000000},
            {"name": "Claude 8", "level": 20, "mark_model": brands["Anthropic"], "gpu_vram": 16384, "ram_gb": 32768, "storage_gb": 40000, "price": Decimal("10000000.00"), "base_revenue": Decimal("1000000.00"), "params": 30000000000000},
            {"name": "Claude 9", "level": 21, "mark_model": brands["Anthropic"], "gpu_vram": 32768, "ram_gb": 65536, "storage_gb": 80000, "price": Decimal("20000000.00"), "base_revenue": Decimal("2000000.00"), "params": 60000000000000},
            {"name": "Claude 10", "level": 22, "mark_model": brands["Anthropic"], "gpu_vram": 65536, "ram_gb": 131072, "storage_gb": 160000, "price": Decimal("40000000.00"), "base_revenue": Decimal("4000000.00"), "params": 120000000000000},

            # ==================== Cohere ====================
            {"name": "Command R7B", "level": 1, "mark_model": brands["Cohere"], "gpu_vram": 16, "ram_gb": 32, "storage_gb": 14, "price": Decimal("1750.00"), "base_revenue": Decimal("175.00"), "params": 7000000000},
            {"name": "Command R 35B", "level": 2, "mark_model": brands["Cohere"], "gpu_vram": 24, "ram_gb": 48, "storage_gb": 70, "price": Decimal("8750.00"), "base_revenue": Decimal("875.00"), "params": 35000000000},
            {"name": "Command R+ 104B", "level": 3, "mark_model": brands["Cohere"], "gpu_vram": 160, "ram_gb": 256, "storage_gb": 208, "price": Decimal("26000.00"), "base_revenue": Decimal("2600.00"), "params": 104000000000},

            # ==================== Community ====================
            {"name": "TinyLlama 1.1B", "level": 1, "mark_model": brands["Community"], "gpu_vram": 4, "ram_gb": 8, "storage_gb": 3, "price": Decimal("400.00"), "base_revenue": Decimal("40.00"), "params": 1100000000},

            # ==================== Databricks ====================
            {"name": "DBRX 132B (MoE 36B ativo)", "level": 1, "mark_model": brands["Databricks"], "gpu_vram": 80, "ram_gb": 128, "storage_gb": 264, "price": Decimal("32000.00"), "base_revenue": Decimal("3200.00"), "params": 132000000000},

            # ==================== DeepSeek ====================
            {"name": "DeepSeek V2 Lite 16B", "level": 1, "mark_model": brands["DeepSeek"], "gpu_vram": 24, "ram_gb": 48, "storage_gb": 32, "price": Decimal("4200.00"), "base_revenue": Decimal("420.00"), "params": 16000000000},
            {"name": "DeepSeek V2 236B (MoE)", "level": 2, "mark_model": brands["DeepSeek"], "gpu_vram": 320, "ram_gb": 512, "storage_gb": 472, "price": Decimal("120000.00"), "base_revenue": Decimal("12000.00"), "params": 236000000000},
            {"name": "DeepSeek V3 671B (MoE)", "level": 3, "mark_model": brands["DeepSeek"], "gpu_vram": 640, "ram_gb": 1024, "storage_gb": 1342, "price": Decimal("335000.00"), "base_revenue": Decimal("33500.00"), "params": 671000000000},
            {"name": "DeepSeek R1 671B (MoE)", "level": 4, "mark_model": brands["DeepSeek"], "gpu_vram": 640, "ram_gb": 1024, "storage_gb": 1342, "price": Decimal("340000.00"), "base_revenue": Decimal("34000.00"), "params": 671000000000},
            {"name": "DeepSeek R1 0528", "level": 5, "mark_model": brands["DeepSeek"], "gpu_vram": 640, "ram_gb": 1024, "storage_gb": 1342, "price": Decimal("345000.00"), "base_revenue": Decimal("34500.00"), "params": 671000000000},
            {"name": "DeepSeek V4", "level": 6, "mark_model": brands["DeepSeek"], "gpu_vram": 2048, "ram_gb": 4096, "storage_gb": 5000, "price": Decimal("1250000.00"), "base_revenue": Decimal("125000.00"), "params": 2800000000000},
            {"name": "DeepSeek R2", "level": 7, "mark_model": brands["DeepSeek"], "gpu_vram": 2560, "ram_gb": 5120, "storage_gb": 6000, "price": Decimal("1500000.00"), "base_revenue": Decimal("150000.00"), "params": 3200000000000},

            # ==================== EleutherAI ====================
            {"name": "Pythia 1B", "level": 1, "mark_model": brands["EleutherAI"], "gpu_vram": 3, "ram_gb": 6, "storage_gb": 2, "price": Decimal("350.00"), "base_revenue": Decimal("35.00"), "params": 1000000000},
            {"name": "GPT-Neo 1.3B", "level": 2, "mark_model": brands["EleutherAI"], "gpu_vram": 4, "ram_gb": 8, "storage_gb": 3, "price": Decimal("420.00"), "base_revenue": Decimal("42.00"), "params": 1300000000},
            {"name": "GPT-Neo 2.7B", "level": 3, "mark_model": brands["EleutherAI"], "gpu_vram": 6, "ram_gb": 12, "storage_gb": 5, "price": Decimal("680.00"), "base_revenue": Decimal("68.00"), "params": 2700000000},
            {"name": "Pythia 2.8B", "level": 4, "mark_model": brands["EleutherAI"], "gpu_vram": 6, "ram_gb": 12, "storage_gb": 5, "price": Decimal("700.00"), "base_revenue": Decimal("70.00"), "params": 2800000000},
            {"name": "GPT-J 6B", "level": 5, "mark_model": brands["EleutherAI"], "gpu_vram": 12, "ram_gb": 24, "storage_gb": 12, "price": Decimal("1500.00"), "base_revenue": Decimal("150.00"), "params": 6000000000},
            {"name": "GPT-NeoX 20B", "level": 6, "mark_model": brands["EleutherAI"], "gpu_vram": 24, "ram_gb": 48, "storage_gb": 40, "price": Decimal("5000.00"), "base_revenue": Decimal("500.00"), "params": 20000000000},

            # ==================== Google ====================
            {"name": "Gemma 3 4B", "level": 1, "mark_model": brands["Google"], "gpu_vram": 8, "ram_gb": 16, "storage_gb": 7, "price": Decimal("1050.00"), "base_revenue": Decimal("105.00"), "params": 4000000000},
            {"name": "Gemini 1.5 Flash 8B", "level": 2, "mark_model": brands["Google"], "gpu_vram": 16, "ram_gb": 32, "storage_gb": 16, "price": Decimal("2000.00"), "base_revenue": Decimal("200.00"), "params": 8000000000},
            {"name": "Gemini 1.5 Flash", "level": 3, "mark_model": brands["Google"], "gpu_vram": 24, "ram_gb": 48, "storage_gb": 100, "price": Decimal("12500.00"), "base_revenue": Decimal("1250.00"), "params": 70000000000},
            {"name": "Gemini 2.0 Flash Lite", "level": 4, "mark_model": brands["Google"], "gpu_vram": 24, "ram_gb": 48, "storage_gb": 120, "price": Decimal("15000.00"), "base_revenue": Decimal("1500.00"), "params": 90000000000},
            {"name": "Gemini 1.0 Pro", "level": 5, "mark_model": brands["Google"], "gpu_vram": 80, "ram_gb": 128, "storage_gb": 250, "price": Decimal("31250.00"), "base_revenue": Decimal("3125.00"), "params": 200000000000},
            {"name": "Gemini 2.0 Flash", "level": 6, "mark_model": brands["Google"], "gpu_vram": 80, "ram_gb": 128, "storage_gb": 400, "price": Decimal("50000.00"), "base_revenue": Decimal("5000.00"), "params": 400000000000},
            {"name": "Gemini 2.5 Flash Lite", "level": 7, "mark_model": brands["Google"], "gpu_vram": 80, "ram_gb": 128, "storage_gb": 450, "price": Decimal("56250.00"), "base_revenue": Decimal("5625.00"), "params": 450000000000},
            {"name": "Gemini 1.0 Ultra", "level": 8, "mark_model": brands["Google"], "gpu_vram": 320, "ram_gb": 512, "storage_gb": 650, "price": Decimal("81250.00"), "base_revenue": Decimal("8125.00"), "params": 550000000000},
            {"name": "Gemini 1.5 Pro", "level": 9, "mark_model": brands["Google"], "gpu_vram": 320, "ram_gb": 512, "storage_gb": 750, "price": Decimal("93750.00"), "base_revenue": Decimal("9375.00"), "params": 600000000000},
            {"name": "Gemini 2.5 Flash", "level": 10, "mark_model": brands["Google"], "gpu_vram": 320, "ram_gb": 512, "storage_gb": 900, "price": Decimal("112500.00"), "base_revenue": Decimal("11250.00"), "params": 700000000000},
            {"name": "Gemini 2.0 Pro", "level": 11, "mark_model": brands["Google"], "gpu_vram": 640, "ram_gb": 1024, "storage_gb": 1500, "price": Decimal("187500.00"), "base_revenue": Decimal("18750.00"), "params": 1300000000000},
            {"name": "Gemini 3.0 Flash", "level": 12, "mark_model": brands["Google"], "gpu_vram": 640, "ram_gb": 1024, "storage_gb": 2000, "price": Decimal("250000.00"), "base_revenue": Decimal("25000.00"), "params": 1800000000000},
            {"name": "Gemini 2.5 Pro", "level": 13, "mark_model": brands["Google"], "gpu_vram": 2048, "ram_gb": 4096, "storage_gb": 4500, "price": Decimal("1125000.00"), "base_revenue": Decimal("112500.00"), "params": 2500000000000},
            {"name": "Gemini 3.0 Pro", "level": 14, "mark_model": brands["Google"], "gpu_vram": 4096, "ram_gb": 8192, "storage_gb": 10000, "price": Decimal("2500000.00"), "base_revenue": Decimal("250000.00"), "params": 7000000000000},
            {"name": "Gemini 4.0", "level": 15, "mark_model": brands["Google"], "gpu_vram": 8192, "ram_gb": 16384, "storage_gb": 24000, "price": Decimal("6000000.00"), "base_revenue": Decimal("600000.00"), "params": 18000000000000},
            {"name": "Gemini 5.0", "level": 16, "mark_model": brands["Google"], "gpu_vram": 32768, "ram_gb": 65536, "storage_gb": 80000, "price": Decimal("20000000.00"), "base_revenue": Decimal("2000000.00"), "params": 60000000000000},
            {"name": "Gemini 6.0", "level": 17, "mark_model": brands["Google"], "gpu_vram": 65536, "ram_gb": 131072, "storage_gb": 160000, "price": Decimal("40000000.00"), "base_revenue": Decimal("4000000.00"), "params": 150000000000000},
            {"name": "Gemini 7.0", "level": 18, "mark_model": brands["Google"], "gpu_vram": 131072, "ram_gb": 262144, "storage_gb": 320000, "price": Decimal("80000000.00"), "base_revenue": Decimal("8000000.00"), "params": 300000000000000},
            {"name": "Gemini 8.0", "level": 19, "mark_model": brands["Google"], "gpu_vram": 262144, "ram_gb": 524288, "storage_gb": 640000, "price": Decimal("160000000.00"), "base_revenue": Decimal("16000000.00"), "params": 600000000000000},

            # ==================== HuggingFace ====================
            {"name": "SmolLM 135M", "level": 1, "mark_model": brands["HuggingFace"], "gpu_vram": 1, "ram_gb": 2, "storage_gb": 1, "price": Decimal("50.00"), "base_revenue": Decimal("5.00"), "params": 135000000},
            {"name": "SmolLM2 135M", "level": 2, "mark_model": brands["HuggingFace"], "gpu_vram": 1, "ram_gb": 2, "storage_gb": 1, "price": Decimal("55.00"), "base_revenue": Decimal("5.50"), "params": 135000000},
            {"name": "SmolLM 360M", "level": 3, "mark_model": brands["HuggingFace"], "gpu_vram": 2, "ram_gb": 4, "storage_gb": 1, "price": Decimal("100.00"), "base_revenue": Decimal("10.00"), "params": 360000000},
            {"name": "SmolLM2 360M", "level": 4, "mark_model": brands["HuggingFace"], "gpu_vram": 2, "ram_gb": 4, "storage_gb": 1, "price": Decimal("110.00"), "base_revenue": Decimal("11.00"), "params": 360000000},
            {"name": "SmolLM 1.7B", "level": 5, "mark_model": brands["HuggingFace"], "gpu_vram": 4, "ram_gb": 8, "storage_gb": 3, "price": Decimal("450.00"), "base_revenue": Decimal("45.00"), "params": 1700000000},
            {"name": "SmolLM2 1.7B", "level": 6, "mark_model": brands["HuggingFace"], "gpu_vram": 4, "ram_gb": 8, "storage_gb": 3, "price": Decimal("470.00"), "base_revenue": Decimal("47.00"), "params": 1700000000},

            # ==================== IBM ====================
            {"name": "Granite Code 3B", "level": 1, "mark_model": brands["IBM"], "gpu_vram": 6, "ram_gb": 12, "storage_gb": 6, "price": Decimal("750.00"), "base_revenue": Decimal("75.00"), "params": 3000000000},
            {"name": "Granite Code 8B", "level": 2, "mark_model": brands["IBM"], "gpu_vram": 16, "ram_gb": 32, "storage_gb": 16, "price": Decimal("2000.00"), "base_revenue": Decimal("200.00"), "params": 8000000000},
            {"name": "Granite Code 20B", "level": 3, "mark_model": brands["IBM"], "gpu_vram": 24, "ram_gb": 48, "storage_gb": 40, "price": Decimal("5000.00"), "base_revenue": Decimal("500.00"), "params": 20000000000},
            {"name": "Granite Code 34B", "level": 4, "mark_model": brands["IBM"], "gpu_vram": 24, "ram_gb": 48, "storage_gb": 68, "price": Decimal("8500.00"), "base_revenue": Decimal("850.00"), "params": 34000000000},

            # ==================== LMSYS ====================
            {"name": "LLaVA 7B", "level": 1, "mark_model": brands["LMSYS"], "gpu_vram": 16, "ram_gb": 32, "storage_gb": 20, "price": Decimal("2500.00"), "base_revenue": Decimal("250.00"), "params": 7000000000},
            {"name": "LLaVA 13B", "level": 2, "mark_model": brands["LMSYS"], "gpu_vram": 24, "ram_gb": 48, "storage_gb": 30, "price": Decimal("3750.00"), "base_revenue": Decimal("375.00"), "params": 13000000000},
            {"name": "LLaVA-NeXT 72B", "level": 3, "mark_model": brands["LMSYS"], "gpu_vram": 80, "ram_gb": 128, "storage_gb": 160, "price": Decimal("20000.00"), "base_revenue": Decimal("2000.00"), "params": 72000000000},

            # ==================== Meta ====================
            {"name": "Llama 2 7B", "level": 1, "mark_model": brands["Meta"], "gpu_vram": 16, "ram_gb": 32, "storage_gb": 14, "price": Decimal("2000.00"), "base_revenue": Decimal("200.00"), "params": 7000000000},
            {"name": "Llama 3 8B", "level": 2, "mark_model": brands["Meta"], "gpu_vram": 16, "ram_gb": 32, "storage_gb": 16, "price": Decimal("2500.00"), "base_revenue": Decimal("250.00"), "params": 8000000000},
            {"name": "Llama 3.1 8B", "level": 3, "mark_model": brands["Meta"], "gpu_vram": 16, "ram_gb": 32, "storage_gb": 16, "price": Decimal("2700.00"), "base_revenue": Decimal("270.00"), "params": 8000000000},
            {"name": "Llama 3.2 8B", "level": 4, "mark_model": brands["Meta"], "gpu_vram": 16, "ram_gb": 32, "storage_gb": 16, "price": Decimal("2800.00"), "base_revenue": Decimal("280.00"), "params": 8000000000},
            {"name": "Llama 3.3 8B", "level": 5, "mark_model": brands["Meta"], "gpu_vram": 16, "ram_gb": 32, "storage_gb": 16, "price": Decimal("2900.00"), "base_revenue": Decimal("290.00"), "params": 8000000000},
            {"name": "Llama 2 13B", "level": 6, "mark_model": brands["Meta"], "gpu_vram": 24, "ram_gb": 48, "storage_gb": 26, "price": Decimal("6500.00"), "base_revenue": Decimal("650.00"), "params": 13000000000},
            {"name": "Llama 4 Scout 17B", "level": 7, "mark_model": brands["Meta"], "gpu_vram": 24, "ram_gb": 48, "storage_gb": 34, "price": Decimal("4500.00"), "base_revenue": Decimal("450.00"), "params": 17000000000},
            {"name": "Llama 2 70B", "level": 8, "mark_model": brands["Meta"], "gpu_vram": 80, "ram_gb": 128, "storage_gb": 140, "price": Decimal("17000.00"), "base_revenue": Decimal("1700.00"), "params": 70000000000},
            {"name": "Llama 3 70B", "level": 9, "mark_model": brands["Meta"], "gpu_vram": 80, "ram_gb": 128, "storage_gb": 140, "price": Decimal("17500.00"), "base_revenue": Decimal("1750.00"), "params": 70000000000},
            {"name": "Llama 3.1 70B", "level": 10, "mark_model": brands["Meta"], "gpu_vram": 80, "ram_gb": 128, "storage_gb": 140, "price": Decimal("18500.00"), "base_revenue": Decimal("1850.00"), "params": 70000000000},
            {"name": "Llama 3.2 70B", "level": 11, "mark_model": brands["Meta"], "gpu_vram": 80, "ram_gb": 128, "storage_gb": 140, "price": Decimal("19000.00"), "base_revenue": Decimal("1900.00"), "params": 70000000000},
            {"name": "Llama 3.3 70B", "level": 12, "mark_model": brands["Meta"], "gpu_vram": 80, "ram_gb": 128, "storage_gb": 140, "price": Decimal("19500.00"), "base_revenue": Decimal("1950.00"), "params": 70000000000},
            {"name": "Llama 4 Maverick 400B", "level": 13, "mark_model": brands["Meta"], "gpu_vram": 640, "ram_gb": 1024, "storage_gb": 800, "price": Decimal("200000.00"), "base_revenue": Decimal("20000.00"), "params": 400000000000},
            {"name": "Llama 4 Behemoth 2T (MoE)", "level": 14, "mark_model": brands["Meta"], "gpu_vram": 2048, "ram_gb": 4096, "storage_gb": 4000, "price": Decimal("1000000.00"), "base_revenue": Decimal("100000.00"), "params": 2000000000000},
            {"name": "Llama 5", "level": 15, "mark_model": brands["Meta"], "gpu_vram": 2048, "ram_gb": 4096, "storage_gb": 5000, "price": Decimal("1250000.00"), "base_revenue": Decimal("125000.00"), "params": 3000000000000},
            {"name": "Llama 6", "level": 16, "mark_model": brands["Meta"], "gpu_vram": 4096, "ram_gb": 8192, "storage_gb": 12000, "price": Decimal("3000000.00"), "base_revenue": Decimal("300000.00"), "params": 8000000000000},
            {"name": "Llama 7", "level": 17, "mark_model": brands["Meta"], "gpu_vram": 8192, "ram_gb": 16384, "storage_gb": 28000, "price": Decimal("7000000.00"), "base_revenue": Decimal("700000.00"), "params": 20000000000000},

            # ==================== Microsoft ====================
            {"name": "Phi-1", "level": 1, "mark_model": brands["Microsoft"], "gpu_vram": 4, "ram_gb": 8, "storage_gb": 3, "price": Decimal("500.00"), "base_revenue": Decimal("50.00"), "params": 1300000000},
            {"name": "Phi-1.5", "level": 2, "mark_model": brands["Microsoft"], "gpu_vram": 4, "ram_gb": 8, "storage_gb": 3, "price": Decimal("600.00"), "base_revenue": Decimal("60.00"), "params": 1300000000},
            {"name": "Phi-2", "level": 3, "mark_model": brands["Microsoft"], "gpu_vram": 6, "ram_gb": 12, "storage_gb": 5, "price": Decimal("800.00"), "base_revenue": Decimal("80.00"), "params": 2700000000},
            {"name": "Phi-3 Mini", "level": 4, "mark_model": brands["Microsoft"], "gpu_vram": 8, "ram_gb": 16, "storage_gb": 7, "price": Decimal("1200.00"), "base_revenue": Decimal("120.00"), "params": 3800000000},
            {"name": "Phi-3.5 Mini", "level": 5, "mark_model": brands["Microsoft"], "gpu_vram": 8, "ram_gb": 16, "storage_gb": 7, "price": Decimal("1400.00"), "base_revenue": Decimal("140.00"), "params": 3800000000},
            {"name": "Phi-4 Mini", "level": 6, "mark_model": brands["Microsoft"], "gpu_vram": 8, "ram_gb": 16, "storage_gb": 8, "price": Decimal("1600.00"), "base_revenue": Decimal("160.00"), "params": 3800000000},

            # ==================== Mistral AI ====================
            {"name": "Mistral 7B", "level": 1, "mark_model": brands["Mistral AI"], "gpu_vram": 16, "ram_gb": 32, "storage_gb": 14, "price": Decimal("2200.00"), "base_revenue": Decimal("220.00"), "params": 7000000000},
            {"name": "Mistral 7B v0.2", "level": 2, "mark_model": brands["Mistral AI"], "gpu_vram": 16, "ram_gb": 32, "storage_gb": 14, "price": Decimal("2300.00"), "base_revenue": Decimal("230.00"), "params": 7000000000},
            {"name": "Mistral 7B v0.3", "level": 3, "mark_model": brands["Mistral AI"], "gpu_vram": 16, "ram_gb": 32, "storage_gb": 14, "price": Decimal("2400.00"), "base_revenue": Decimal("240.00"), "params": 7000000000},
            {"name": "Jamba 1.5 Mini", "level": 4, "mark_model": brands["Mistral AI"], "gpu_vram": 16, "ram_gb": 32, "storage_gb": 16, "price": Decimal("2300.00"), "base_revenue": Decimal("230.00"), "params": 8000000000},
            {"name": "Mistral Nemo 12B", "level": 5, "mark_model": brands["Mistral AI"], "gpu_vram": 24, "ram_gb": 48, "storage_gb": 24, "price": Decimal("3200.00"), "base_revenue": Decimal("320.00"), "params": 12000000000},
            {"name": "Mistral Small 22B", "level": 6, "mark_model": brands["Mistral AI"], "gpu_vram": 24, "ram_gb": 48, "storage_gb": 44, "price": Decimal("5500.00"), "base_revenue": Decimal("550.00"), "params": 22000000000},
            {"name": "Mistral Medium 24B", "level": 7, "mark_model": brands["Mistral AI"], "gpu_vram": 24, "ram_gb": 48, "storage_gb": 48, "price": Decimal("6000.00"), "base_revenue": Decimal("600.00"), "params": 24000000000},
            {"name": "Mixtral 8x7B", "level": 8, "mark_model": brands["Mistral AI"], "gpu_vram": 24, "ram_gb": 48, "storage_gb": 96, "price": Decimal("12000.00"), "base_revenue": Decimal("1200.00"), "params": 46700000000},
            {"name": "Mistral Large 123B", "level": 9, "mark_model": brands["Mistral AI"], "gpu_vram": 160, "ram_gb": 256, "storage_gb": 246, "price": Decimal("30750.00"), "base_revenue": Decimal("3075.00"), "params": 123000000000},
            {"name": "Mistral Large 2 123B", "level": 10, "mark_model": brands["Mistral AI"], "gpu_vram": 160, "ram_gb": 256, "storage_gb": 246, "price": Decimal("31500.00"), "base_revenue": Decimal("3150.00"), "params": 123000000000},
            {"name": "Mixtral 8x22B", "level": 11, "mark_model": brands["Mistral AI"], "gpu_vram": 80, "ram_gb": 128, "storage_gb": 280, "price": Decimal("35000.00"), "base_revenue": Decimal("3500.00"), "params": 141000000000},
            {"name": "Jamba 1.5 Large", "level": 12, "mark_model": brands["Mistral AI"], "gpu_vram": 24, "ram_gb": 48, "storage_gb": 52, "price": Decimal("13000.00"), "base_revenue": Decimal("1300.00"), "params": 398000000000},
            {"name": "Mistral Ultra 1T", "level": 13, "mark_model": brands["Mistral AI"], "gpu_vram": 2048, "ram_gb": 4096, "storage_gb": 4500, "price": Decimal("1125000.00"), "base_revenue": Decimal("112500.00"), "params": 1000000000000},
            {"name": "Mistral Omega 10T", "level": 14, "mark_model": brands["Mistral AI"], "gpu_vram": 8192, "ram_gb": 16384, "storage_gb": 20000, "price": Decimal("5000000.00"), "base_revenue": Decimal("500000.00"), "params": 10000000000000},

            # ==================== OpenAI ====================
            {"name": "GPT-2 117M", "level": 1, "mark_model": brands["OpenAI"], "gpu_vram": 2, "ram_gb": 4, "storage_gb": 1, "price": Decimal("100.00"), "base_revenue": Decimal("10.00"), "params": 117000000},
            {"name": "GPT-2 1.5B", "level": 2, "mark_model": brands["OpenAI"], "gpu_vram": 4, "ram_gb": 8, "storage_gb": 3, "price": Decimal("400.00"), "base_revenue": Decimal("40.00"), "params": 1500000000},
            {"name": "GPT-4.1 nano", "level": 3, "mark_model": brands["OpenAI"], "gpu_vram": 16, "ram_gb": 32, "storage_gb": 60, "price": Decimal("7500.00"), "base_revenue": Decimal("750.00"), "params": 60000000000},
            {"name": "GPT-3 175B", "level": 4, "mark_model": brands["OpenAI"], "gpu_vram": 320, "ram_gb": 512, "storage_gb": 350, "price": Decimal("87500.00"), "base_revenue": Decimal("8750.00"), "params": 175000000000},
            {"name": "GPT-3.5 Turbo", "level": 5, "mark_model": brands["OpenAI"], "gpu_vram": 80, "ram_gb": 128, "storage_gb": 200, "price": Decimal("25000.00"), "base_revenue": Decimal("2500.00"), "params": 200000000000},
            {"name": "GPT-4o mini", "level": 6, "mark_model": brands["OpenAI"], "gpu_vram": 80, "ram_gb": 128, "storage_gb": 200, "price": Decimal("25000.00"), "base_revenue": Decimal("2500.00"), "params": 200000000000},
            {"name": "GPT-4.1 mini", "level": 7, "mark_model": brands["OpenAI"], "gpu_vram": 80, "ram_gb": 128, "storage_gb": 220, "price": Decimal("27500.00"), "base_revenue": Decimal("2750.00"), "params": 220000000000},
            {"name": "GPT-5 mini", "level": 8, "mark_model": brands["OpenAI"], "gpu_vram": 320, "ram_gb": 512, "storage_gb": 1000, "price": Decimal("250000.00"), "base_revenue": Decimal("25000.00"), "params": 1000000000000},
            {"name": "GPT-4 1.8T (MoE estimado)", "level": 9, "mark_model": brands["OpenAI"], "gpu_vram": 2048, "ram_gb": 4096, "storage_gb": 3600, "price": Decimal("900000.00"), "base_revenue": Decimal("90000.00"), "params": 1800000000000},
            {"name": "GPT-4 Turbo", "level": 10, "mark_model": brands["OpenAI"], "gpu_vram": 2048, "ram_gb": 4096, "storage_gb": 3800, "price": Decimal("950000.00"), "base_revenue": Decimal("95000.00"), "params": 1900000000000},
            {"name": "GPT-4o", "level": 11, "mark_model": brands["OpenAI"], "gpu_vram": 2048, "ram_gb": 4096, "storage_gb": 4000, "price": Decimal("1000000.00"), "base_revenue": Decimal("100000.00"), "params": 2000000000000},
            {"name": "GPT-4.1", "level": 12, "mark_model": brands["OpenAI"], "gpu_vram": 2560, "ram_gb": 5120, "storage_gb": 4500, "price": Decimal("1125000.00"), "base_revenue": Decimal("112500.00"), "params": 2200000000000},
            {"name": "GPT-5", "level": 13, "mark_model": brands["OpenAI"], "gpu_vram": 4096, "ram_gb": 8192, "storage_gb": 8000, "price": Decimal("2000000.00"), "base_revenue": Decimal("200000.00"), "params": 5000000000000},
            {"name": "GPT-5 turbo", "level": 14, "mark_model": brands["OpenAI"], "gpu_vram": 5120, "ram_gb": 10240, "storage_gb": 10000, "price": Decimal("2500000.00"), "base_revenue": Decimal("250000.00"), "params": 6000000000000},
            {"name": "GPT-6", "level": 15, "mark_model": brands["OpenAI"], "gpu_vram": 8192, "ram_gb": 16384, "storage_gb": 16000, "price": Decimal("4000000.00"), "base_revenue": Decimal("400000.00"), "params": 10000000000000},
            {"name": "GPT-6 ultra", "level": 16, "mark_model": brands["OpenAI"], "gpu_vram": 16384, "ram_gb": 32768, "storage_gb": 32000, "price": Decimal("8000000.00"), "base_revenue": Decimal("800000.00"), "params": 20000000000000},
            {"name": "GPT-7", "level": 17, "mark_model": brands["OpenAI"], "gpu_vram": 32768, "ram_gb": 65536, "storage_gb": 64000, "price": Decimal("16000000.00"), "base_revenue": Decimal("1600000.00"), "params": 50000000000000},
            {"name": "GPT-8", "level": 18, "mark_model": brands["OpenAI"], "gpu_vram": 65536, "ram_gb": 131072, "storage_gb": 128000, "price": Decimal("32000000.00"), "base_revenue": Decimal("3200000.00"), "params": 100000000000000},
            {"name": "GPT-9", "level": 19, "mark_model": brands["OpenAI"], "gpu_vram": 131072, "ram_gb": 262144, "storage_gb": 256000, "price": Decimal("64000000.00"), "base_revenue": Decimal("6400000.00"), "params": 200000000000000},
            {"name": "GPT-10", "level": 20, "mark_model": brands["OpenAI"], "gpu_vram": 262144, "ram_gb": 524288, "storage_gb": 512000, "price": Decimal("128000000.00"), "base_revenue": Decimal("12800000.00"), "params": 500000000000000},

            # ==================== Stability AI ====================
            {"name": "StableLM 3B", "level": 1, "mark_model": brands["Stability AI"], "gpu_vram": 6, "ram_gb": 12, "storage_gb": 5, "price": Decimal("700.00"), "base_revenue": Decimal("70.00"), "params": 3000000000},

            # ==================== TII ====================
            {"name": "Falcon 3B", "level": 1, "mark_model": brands["TII"], "gpu_vram": 6, "ram_gb": 12, "storage_gb": 5, "price": Decimal("750.00"), "base_revenue": Decimal("75.00"), "params": 3000000000},
            {"name": "Falcon 7B", "level": 2, "mark_model": brands["TII"], "gpu_vram": 16, "ram_gb": 32, "storage_gb": 14, "price": Decimal("1800.00"), "base_revenue": Decimal("180.00"), "params": 7000000000},
            {"name": "Falcon 40B", "level": 3, "mark_model": brands["TII"], "gpu_vram": 24, "ram_gb": 48, "storage_gb": 80, "price": Decimal("10000.00"), "base_revenue": Decimal("1000.00"), "params": 40000000000},
            {"name": "Falcon 180B", "level": 4, "mark_model": brands["TII"], "gpu_vram": 320, "ram_gb": 512, "storage_gb": 360, "price": Decimal("90000.00"), "base_revenue": Decimal("9000.00"), "params": 180000000000},

            # ==================== xAI ====================
            {"name": "Grok-1 314B (MoE)", "level": 1, "mark_model": brands["xAI"], "gpu_vram": 480, "ram_gb": 768, "storage_gb": 628, "price": Decimal("157000.00"), "base_revenue": Decimal("15700.00"), "params": 314000000000},
            {"name": "Grok-2", "level": 2, "mark_model": brands["xAI"], "gpu_vram": 480, "ram_gb": 768, "storage_gb": 800, "price": Decimal("200000.00"), "base_revenue": Decimal("20000.00"), "params": 500000000000},
            {"name": "Grok-3", "level": 3, "mark_model": brands["xAI"], "gpu_vram": 640, "ram_gb": 1024, "storage_gb": 1200, "price": Decimal("300000.00"), "base_revenue": Decimal("30000.00"), "params": 800000000000},
            {"name": "Grok-4", "level": 4, "mark_model": brands["xAI"], "gpu_vram": 800, "ram_gb": 1280, "storage_gb": 1600, "price": Decimal("400000.00"), "base_revenue": Decimal("40000.00"), "params": 1200000000000},
            {"name": "Grok-5", "level": 5, "mark_model": brands["xAI"], "gpu_vram": 2048, "ram_gb": 4096, "storage_gb": 5200, "price": Decimal("1300000.00"), "base_revenue": Decimal("130000.00"), "params": 2900000000000},
            {"name": "Grok-6", "level": 6, "mark_model": brands["xAI"], "gpu_vram": 4096, "ram_gb": 8192, "storage_gb": 12000, "price": Decimal("3000000.00"), "base_revenue": Decimal("300000.00"), "params": 8500000000000},
        ]

        # ==================== 2.1 Filtragem e Ordenação ====================
        # Palavras-chave para remover modelos específicos (vídeo, áudio, foto, domínios muito restritos)
        # Modelos multimodais gerais de texto+visão (como Qwen-VL, LLaVA) foram mantidos por serem "normais" no contexto de LLMs.
        exclude_keywords = [
            # Foto / Geração de Imagem
            "Stable Diffusion",
            "FLUX",
            "DALL-E",
            "Midjourney",
            "Imagen",
            "Ideogram",
            # Vídeo
            "Sora",
            "Runway",
            "Pika",
            "Kling",
            "Veo",
            "Luma",
            "Hailuo",
            # Áudio / Música / Voz
            "Whisper",
            "MusicGen",
            "AudioLDM",
            "Suno",
            "Udio",
            "ElevenLabs",
            "Bark",
            "VALL-E",
            # Domínios muito específicos (Medicina, Biologia, Química, Matemática pura, etc.)
            "Med-PaLM",
            "Med-Gemini",
            "BioMistral",
            "SciPhi",
            "Galactica",
            "ChemLLM",
            "MathLlama",
            # Modelos puramente de visão redundantes (as capacidades multimodais já estão cobertas pelos modelos principais)
            "GPT-4V",
            "GPT-4o Vision",
            "Claude 3 Vision",
            "Gemini 1.5 Pro Vision"
        ]

        # Filtra a lista removendo qualquer modelo que contenha as palavras-chave acima
        filtered_models_data = [
            item for item in models_data 
            if not any(keyword in item["name"] for keyword in exclude_keywords)
        ]
        
        # Ordena a lista filtrada pelo nível (level) de forma crescente
        filtered_models_data.sort(key=lambda x: x["level"])

        # ==================== 3. Insercao e Atualizacao Segura no Banco ====================
        created_count = 0
        updated_count = 0
        
        for item in filtered_models_data:
            obj, created = AIModel.objects.update_or_create(
                name=item["name"],
                defaults=item
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        removed_count = len(models_data) - len(filtered_models_data)

        self.stdout.write(self.style.SUCCESS(
            f"\nBase de dados de marcas e modelos de IA populada com sucesso!\n"
            f"  - Marcas cadastradas: {len(brands)}\n"
            f"  - Modelos filtrados e ordenados por level: {len(filtered_models_data)}\n"
            f"  - Modelos específicos removidos (vídeo, áudio, foto, etc.): {removed_count}\n"
            f"  - Modelos criados no banco: {created_count}\n"
            f"  - Modelos atualizados no banco: {updated_count}"
        ))