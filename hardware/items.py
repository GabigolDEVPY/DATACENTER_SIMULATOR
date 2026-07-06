
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

pecas = [
    {
        "tipo": "gpu",
        "modelo": "NVIDIA GB200 Grace Blackwell",
        "marca": brands["NVIDIA"],
        "preco_usd": 70000,
        "consumo_w": 2700,
        "score_bottleneck": 3000
    },
    {
        "tipo": "gpu",
        "modelo": "NVIDIA B200",
        "marca": brands["NVIDIA"],
        "preco_usd": 35000,
        "consumo_w": 1000,
        "score_bottleneck": 2500
    },
    {
        "tipo": "gpu",
        "modelo": "NVIDIA H200 SXM",
        "marca": brands["NVIDIA"],
        "preco_usd": 40000,
        "consumo_w": 700,
        "score_bottleneck": 2000
    },
    {
        "tipo": "gpu",
        "modelo": "AMD Instinct MI325X",
        "marca": brands["AMD"],
        "preco_usd": 30000,
        "consumo_w": 750,
        "score_bottleneck": 2000
    },
    {
        "tipo": "gpu",
        "modelo": "AMD Instinct MI300X",
        "marca": brands["AMD"],
        "preco_usd": 25000,
        "consumo_w": 750,
        "score_bottleneck": 1800
    },
    {
        "tipo": "gpu",
        "modelo": "NVIDIA H100 SXM",
        "marca": brands["NVIDIA"],
        "preco_usd": 30000,
        "consumo_w": 700,
        "score_bottleneck": 1800
    },
    {
        "tipo": "gpu",
        "modelo": "NVIDIA H100 PCIe",
        "marca": brands["NVIDIA"],
        "preco_usd": 27000,
        "consumo_w": 350,
        "score_bottleneck": 1600
    },
    {
        "tipo": "gpu",
        "modelo": "NVIDIA A100 80GB",
        "marca": brands["NVIDIA"],
        "preco_usd": 18000,
        "consumo_w": 400,
        "score_bottleneck": 1200
    },
    {
        "tipo": "gpu",
        "modelo": "AMD Instinct MI250X",
        "marca": brands["AMD"],
        "preco_usd": 15000,
        "consumo_w": 560,
        "score_bottleneck": 1200
    },
    {
        "tipo": "gpu",
        "modelo": "NVIDIA L40S",
        "marca": brands["NVIDIA"],
        "preco_usd": 9000,
        "consumo_w": 350,
        "score_bottleneck": 800
    },
    {
        "tipo": "cpu",
        "modelo": "AMD EPYC 9965",
        "marca": brands["AMD"],
        "preco_usd": 15000,
        "consumo_w": 500,
        "score_bottleneck": 3000
    },
    {
        "tipo": "cpu",
        "modelo": "AMD EPYC 9755",
        "marca": brands["AMD"],
        "preco_usd": 13000,
        "consumo_w": 500,
        "score_bottleneck": 2500
    },
    {
        "tipo": "cpu",
        "modelo": "Intel Xeon 6980P",
        "marca": brands["Intel"],
        "preco_usd": 13000,
        "consumo_w": 500,
        "score_bottleneck": 2500
    },
    {
        "tipo": "cpu",
        "modelo": "AMD EPYC 9655",
        "marca": brands["AMD"],
        "preco_usd": 11500,
        "consumo_w": 400,
        "score_bottleneck": 2000
    },
    {
        "tipo": "cpu",
        "modelo": "AMD EPYC 9654",
        "marca": brands["AMD"],
        "preco_usd": 11000,
        "consumo_w": 360,
        "score_bottleneck": 1900
    },
    {
        "tipo": "cpu",
        "modelo": "Intel Xeon Platinum 8592+",
        "marca": brands["Intel"],
        "preco_usd": 10000,
        "consumo_w": 350,
        "score_bottleneck": 1600
    },
    {
        "tipo": "cpu",
        "modelo": "AMD EPYC 9554",
        "marca": brands["AMD"],
        "preco_usd": 8500,
        "consumo_w": 360,
        "score_bottleneck": 1600
    },
    {
        "tipo": "cpu",
        "modelo": "Intel Xeon Platinum 8480+",
        "marca": brands["Intel"],
        "preco_usd": 8000,
        "consumo_w": 350,
        "score_bottleneck": 1400
    },
    {
        "tipo": "cpu",
        "modelo": "AMD EPYC 9454",
        "marca": brands["AMD"],
        "preco_usd": 6000,
        "consumo_w": 290,
        "score_bottleneck": 1200
    },
    {
        "tipo": "cpu",
        "modelo": "Intel Xeon Gold 6548Y+",
        "marca": brands["Intel"],
        "preco_usd": 4200,
        "consumo_w": 250,
        "score_bottleneck": 800
    },
    {
        "tipo": "ram",
        "modelo": "DDR5 ECC RDIMM 512GB",
        "marca": brands["Samsung"],
        "preco_usd": 4500,
        "consumo_w": 18
    },
    {
        "tipo": "ram",
        "modelo": "DDR5 ECC RDIMM 512GB",
        "marca": brands["Micron"],
        "preco_usd": 4400,
        "consumo_w": 18
    },
    {
        "tipo": "ram",
        "modelo": "DDR5 ECC RDIMM 256GB",
        "marca": brands["SK Hynix"],
        "preco_usd": 2400,
        "consumo_w": 15
    },
    {
        "tipo": "ram",
        "modelo": "DDR5 ECC RDIMM 256GB",
        "marca": brands["Samsung"],
        "preco_usd": 2350,
        "consumo_w": 15
    },
    {
        "tipo": "ram",
        "modelo": "DDR5 ECC RDIMM 128GB",
        "marca": brands["Micron"],
        "preco_usd": 1200,
        "consumo_w": 12
    },
    {
        "tipo": "ram",
        "modelo": "DDR5 ECC RDIMM 128GB",
        "marca": brands["Samsung"],
        "preco_usd": 1150,
        "consumo_w": 12
    },
    {
        "tipo": "ram",
        "modelo": "DDR5 ECC RDIMM 96GB",
        "marca": brands["SK Hynix"],
        "preco_usd": 850,
        "consumo_w": 11
    },
    {
        "tipo": "ram",
        "modelo": "DDR5 ECC RDIMM 64GB",
        "marca": brands["Micron"],
        "preco_usd": 450,
        "consumo_w": 10
    },
    {
        "tipo": "ram",
        "modelo": "DDR5 ECC RDIMM 64GB",
        "marca": brands["Samsung"],
        "preco_usd": 430,
        "consumo_w": 10
    },
    {
        "tipo": "ram",
        "modelo": "DDR5 ECC RDIMM 32GB",
        "marca": brands["Kingston Server"],
        "preco_usd": 220,
        "consumo_w": 8
    },
    {
        "tipo": "ssd",
        "modelo": "Solidigm D5-P5336 122TB",
        "marca": brands["Solidigm"],
        "preco_usd": 12000,
        "consumo_w": 25
    },
    {
        "tipo": "ssd",
        "modelo": "Micron 6550 ION 122TB",
        "marca": brands["Micron"],
        "preco_usd": 11500,
        "consumo_w": 25
    },
    {
        "tipo": "ssd",
        "modelo": "Samsung PM1743 30.72TB",
        "marca": brands["Samsung"],
        "preco_usd": 4500,
        "consumo_w": 20
    },
    {
        "tipo": "ssd",
        "modelo": "Kioxia CM7 30.72TB",
        "marca": brands["Kioxia"],
        "preco_usd": 4300,
        "consumo_w": 20
    },
    {
        "tipo": "ssd",
        "modelo": "Micron 7450 PRO 30.72TB",
        "marca": brands["Micron"],
        "preco_usd": 4100,
        "consumo_w": 18
    },
    {
        "tipo": "ssd",
        "modelo": "Samsung PM9A3 15.36TB",
        "marca": brands["Samsung"],
        "preco_usd": 2200,
        "consumo_w": 14
    },
    {
        "tipo": "ssd",
        "modelo": "Solidigm D7-P5520 15.36TB",
        "marca": brands["Solidigm"],
        "preco_usd": 2100,
        "consumo_w": 14
    },
    {
        "tipo": "ssd",
        "modelo": "Micron 7450 PRO 7.68TB",
        "marca": brands["Micron"],
        "preco_usd": 1100,
        "consumo_w": 12
    },
    {
        "tipo": "ssd",
        "modelo": "Samsung PM893 3.84TB",
        "marca": brands["Samsung"],
        "preco_usd": 550,
        "consumo_w": 6
    },
    {
        "tipo": "ssd",
        "modelo": "Kingston DC600M 1.92TB",
        "marca": brands["Kingston"],
        "preco_usd": 280,
        "consumo_w": 4
    }
]


