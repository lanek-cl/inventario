import os


class Config:

    familia_insumos = {
        "Resina UV": "Estandar Blanco 0.5kg, Estandar Negro 0.5kg, Estandar Azul 0.5kg, Estandar Transparente 0.5kg, ABS Negro 0.5kg, ABS Gris 1kg".split(
            ","
        ),
        "Filamento PLA": "Blanco 1kg, Negro 1kg".strip().split(","),
        "Silicona": "  2comp. Transparente 1kg, Adhesiva Transparente 110ml, Adhesiva Negro 110ml, Caliente 10 barras".strip().split(
            ","
        ),
        "Tinte Silicona": "Negro 22gr".strip().split(","),
        "Alcohol Isopropílico": "5Lt".strip().split(","),
        "Guantes Nitrilo": "100-200U".strip().split(","),
        "Toalla de Papel": ["500mts"],
        "Flux": ["Líquido 1 jeringa"],
        "Estaño": ["Carrete 250g", "Tarrito 50g"],
        "Termoretráctil": ["Mix 500U"],
        "Cable Enmallado": ["3 Hilos"],
    }

    familia_componentes = {
        "Antena": ["2.4GHz"],
        "Batería": ["3.7V"],
        "Cable": ["TAG-Connect", "Tres Conductores"],
        "Condensador": [
            " 0.1UF",
            "0.8PF",
            "1.2PF",
            "1000PF",
            "100PF",
            "10PF",
            "10UF",
            "12PF",
            "18PF",
            "1UF",
            "22UF",
        ],
        "Conector": [
            "USB TYPE C",
            "USB TYPE B",
            "Jack",
            "Male SlimStack",
            "Female SlimStack",
            "Pitch microSD",
        ],
        "Cristal": ["32Mhz", "12.288Mhz"],
        "IC": [
            "Codec",
            "MCU",
            "PMIC",
            "REG LINEAR 1.8V",
            "REG LINEAR 3V",
            "Bluetooth",
            "TVS",
        ],
        "Inductor": ["100NH", "10UH", "15NH", "2.7NH", "3.3NH", "3.9NH", "6.8UH"],
        "LED": ["RGB", "Orange", "Green"],
        "Micro SD": ["32GB"],
        "PCB": ["Flex", "Rigid"],
        "Resistencia": [
            "100K",
            "10K",
            "150R",
            "1K",
            "2K2",
            "2K7",
            "1M",
            "2M05",
            "1K87",
            "1M5",
            "20K",
            "220R",
            "2M",
            "47R",
            "50R",
            "649K",
        ],
        "Sensor": ["Acelerometro", "Microfono"],
        "Switch": ["Tactile"],
    }
