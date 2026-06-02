"""
Migrated from food_bls.py

Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
URL: https://blsdb.de/download
"""

from blutwerte.foods import Food, DataSource
from blutwerte.foods.models import FoodEffect, EffectCertainty
from blutwerte.medications.models import EffectTargetType, EffectDirection


def create_hafer_ganzes_korn_roh() -> Food:
    """
    Hafer ganzes Korn roh
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Hafer ganzes Korn roh",
        name_de="Hafer ganzes Korn roh",
        category="cereal",
        nutrition_data={
        "calories": 343.0,
        "water": 11.45,
        "protein": 11.5,
        "fat": 7.09,
        "carbohydrate": 57.8,
        "sugar": 1.08,
        "starch": 52.6,
        "fiber": 9.8,
        "sodium": 8.0,
        "potassium": 412.0,
        "calcium": 56.0,
        "magnesium": 116.0,
        "phosphorus": 342.0,
        "iron": 5.0,
        "zinc": 4.0,
        "manganese": 6160.0,
        "copper": 484.0,
        "selenium": 8.0,
        "vitamin e": 1.342,
        "vitamin b1": 0.7,
        "vitamin b3": 2.37,
        "vitamin b5": 0.71,
        "vitamin b6": 0.96,
        "vitamin b7": 0.013,
        "vitamin k": 0.0021,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_hafer_flocken() -> Food:
    """
    Hafer Flocken
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Hafer Flocken",
        name_de="Hafer Flocken",
        category="cereal",
        nutrition_data={
        "calories": 348.0,
        "water": 10.07,
        "protein": 11.2,
        "fat": 6.65,
        "carbohydrate": 58.9,
        "sugar": 0.74,
        "starch": 52.6,
        "fiber": 8.3,
        "sodium": 2.0,
        "potassium": 382.0,
        "calcium": 44.0,
        "magnesium": 121.0,
        "phosphorus": 325.0,
        "iron": 4.0,
        "zinc": 4.0,
        "manganese": 4934.0,
        "copper": 410.0,
        "selenium": 9.0,
        "vitamin e": 0.8,
        "vitamin b1": 0.65,
        "vitamin b3": 1.0,
        "vitamin b5": 1.09,
        "vitamin b6": 0.098,
        "vitamin b7": 0.02,
        "vitamin k": 0.0021,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_gerste_ganzes_korn_roh() -> Food:
    """
    Gerste ganzes Korn roh
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Gerste ganzes Korn roh",
        name_de="Gerste ganzes Korn roh",
        category="cereal",
        nutrition_data={
        "calories": 332.0,
        "water": 12.7,
        "protein": 10.5,
        "fat": 2.1,
        "carbohydrate": 67.2,
        "sugar": 1.71,
        "starch": 60.9,
        "fiber": 14.5,
        "sodium": 18.0,
        "potassium": 510.0,
        "calcium": 35.0,
        "magnesium": 114.0,
        "phosphorus": 342.0,
        "iron": 6.0,
        "zinc": 3.0,
        "manganese": 1680.0,
        "copper": 524.0,
        "vitamin e": 0.31,
        "vitamin b1": 0.4,
        "vitamin b3": 4.8,
        "vitamin b5": 0.68,
        "vitamin b6": 0.56,
        "vitamin b7": 0.009,
        "vitamin k": 0.0022,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_reis_poliert_roh() -> Food:
    """
    Reis poliert roh
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Reis poliert roh",
        name_de="Reis poliert roh",
        category="cereal",
        nutrition_data={
        "calories": 351.0,
        "water": 11.88,
        "protein": 7.0,
        "fat": 0.62,
        "carbohydrate": 77.0,
        "sugar": 0.28,
        "starch": 76.8,
        "fiber": 1.3,
        "sodium": 16.0,
        "potassium": 107.0,
        "calcium": 5.0,
        "magnesium": 40.0,
        "phosphorus": 114.0,
        "iron": 0.3,
        "zinc": 3.0,
        "manganese": 702.0,
        "copper": 251.0,
        "vitamin b3": 1.3,
        "vitamin b5": 0.63,
        "vitamin b6": 0.048,
        "vitamin b7": 0.003,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_vollkornbrot() -> Food:
    """
    Vollkornbrot
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Vollkornbrot",
        name_de="Vollkornbrot",
        category="bread",
        nutrition_data={
        "calories": 209.0,
        "water": 41.3,
        "protein": 7.0,
        "fat": 1.4,
        "carbohydrate": 39.7,
        "sugar": 2.1,
        "starch": 33.6,
        "fiber": 6.3,
        "sodium": 460.0,
        "potassium": 240.0,
        "calcium": 41.0,
        "magnesium": 45.0,
        "phosphorus": 110.0,
        "iron": 1.7,
        "zinc": 1.0,
        "vitamin e": 0.36,
        "vitamin b1": 0.18,
        "vitamin b2": 0.07,
        "vitamin b3": 1.44,
        "vitamin b6": 0.085,
        "vitamin b9": 0.025,
        "vitamin b5": 0.4,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_roggenbrot() -> Food:
    """
    Roggenbrot
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Roggenbrot",
        name_de="Roggenbrot",
        category="bread",
        nutrition_data={
        "calories": 204.0,
        "water": 42.4,
        "protein": 6.1,
        "fat": 1.3,
        "carbohydrate": 39.0,
        "sugar": 2.2,
        "starch": 33.6,
        "fiber": 5.5,
        "sodium": 530.0,
        "potassium": 230.0,
        "calcium": 37.0,
        "magnesium": 44.0,
        "phosphorus": 95.0,
        "iron": 1.6,
        "zinc": 1.0,
        "vitamin b1": 0.21,
        "vitamin b2": 0.07,
        "vitamin b3": 1.0,
        "vitamin b6": 0.09,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_toastbrot_weiss() -> Food:
    """
    Toastbrot weiss
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Toastbrot weiss",
        name_de="Toastbrot weiss",
        category="bread",
        nutrition_data={
        "calories": 265.0,
        "water": 33.0,
        "protein": 8.2,
        "fat": 3.8,
        "carbohydrate": 48.0,
        "sugar": 4.0,
        "starch": 43.0,
        "fiber": 2.8,
        "sodium": 450.0,
        "potassium": 100.0,
        "calcium": 26.0,
        "magnesium": 21.0,
        "phosphorus": 77.0,
        "iron": 1.0,
        "zinc": 0.6,
        "vitamin b1": 0.23,
        "vitamin b2": 0.08,
        "vitamin b3": 1.78,
        "vitamin b9": 0.027,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_milch_voll() -> Food:
    """
    Milch voll
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Milch voll",
        name_de="Milch voll",
        category="milk",
        nutrition_data={
        "calories": 64.0,
        "water": 87.8,
        "protein": 3.3,
        "fat": 3.5,
        "carbohydrate": 4.8,
        "sugar": 4.8,
        "sodium": 50.0,
        "potassium": 150.0,
        "calcium": 120.0,
        "magnesium": 11.0,
        "phosphorus": 95.0,
        "iron": 0.03,
        "zinc": 0.4,
        "iodine": 11.0,
        "vitamin a": 52.0,
        "vitamin d": 1.0,
        "vitamin e": 0.1,
        "vitamin b1": 0.038,
        "vitamin b2": 0.18,
        "vitamin b12": 0.38,
        "vitamin b3": 0.1,
        "vitamin b5": 0.32,
        "cholesterol": 14.0,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_milch_fettarm() -> Food:
    """
    Milch fettarm
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Milch fettarm",
        name_de="Milch fettarm",
        category="milk",
        nutrition_data={
        "calories": 48.0,
        "water": 89.0,
        "protein": 3.4,
        "fat": 1.5,
        "carbohydrate": 4.9,
        "sugar": 4.9,
        "sodium": 50.0,
        "potassium": 160.0,
        "calcium": 120.0,
        "magnesium": 11.0,
        "phosphorus": 100.0,
        "iron": 0.03,
        "zinc": 0.4,
        "iodine": 11.0,
        "vitamin a": 24.0,
        "vitamin d": 1.0,
        "vitamin e": 0.05,
        "vitamin b1": 0.04,
        "vitamin b2": 0.18,
        "vitamin b12": 0.44,
        "vitamin b3": 0.1,
        "vitamin b5": 0.35,
        "cholesterol": 7.0,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_joghurt_natur() -> Food:
    """
    Joghurt natur
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Joghurt natur",
        name_de="Joghurt natur",
        category="yogurt",
        nutrition_data={
        "calories": 62.0,
        "water": 85.5,
        "protein": 3.5,
        "fat": 3.0,
        "carbohydrate": 4.7,
        "sugar": 4.7,
        "sodium": 60.0,
        "potassium": 170.0,
        "calcium": 120.0,
        "magnesium": 12.0,
        "phosphorus": 100.0,
        "iron": 0.05,
        "zinc": 0.4,
        "iodine": 11.0,
        "vitamin a": 32.0,
        "vitamin d": 0.8,
        "vitamin e": 0.09,
        "vitamin b1": 0.03,
        "vitamin b2": 0.14,
        "vitamin b12": 0.24,
        "vitamin b3": 0.08,
        "vitamin b5": 0.35,
        "cholesterol": 9.0,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_joghurt_griechisch() -> Food:
    """
    Joghurt griechisch
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Joghurt griechisch",
        name_de="Joghurt griechisch",
        category="yogurt",
        nutrition_data={
        "calories": 114.0,
        "water": 77.8,
        "protein": 3.3,
        "fat": 9.4,
        "carbohydrate": 4.0,
        "sugar": 4.0,
        "fiber": 0.13,
        "sodium": 40.0,
        "potassium": 140.0,
        "calcium": 110.0,
        "magnesium": 11.0,
        "phosphorus": 91.0,
        "iron": 0.03,
        "zinc": 0.4,
        "vitamin a": 89.0,
        "vitamin e": 0.15,
        "vitamin b1": 0.03,
        "vitamin b2": 0.13,
        "vitamin b12": 0.18,
        "vitamin b3": 0.09,
        "cholesterol": 36.0,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_quark_mager() -> Food:
    """
    Quark mager
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Quark mager",
        name_de="Quark mager",
        category="yogurt",
        nutrition_data={
        "calories": 67.0,
        "water": 82.5,
        "protein": 12.0,
        "fat": 0.3,
        "carbohydrate": 3.8,
        "sugar": 3.8,
        "sodium": 50.0,
        "potassium": 130.0,
        "calcium": 90.0,
        "magnesium": 9.0,
        "phosphorus": 140.0,
        "iron": 0.1,
        "zinc": 0.4,
        "vitamin a": 9.0,
        "vitamin b1": 0.04,
        "vitamin b2": 0.28,
        "vitamin b12": 0.7,
        "vitamin b3": 0.12,
        "cholesterol": 3.0,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_quark_20() -> Food:
    """
    Quark 20
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Quark 20",
        name_de="Quark 20",
        category="yogurt",
        nutrition_data={
        "calories": 107.0,
        "water": 76.0,
        "protein": 10.0,
        "fat": 6.0,
        "carbohydrate": 3.5,
        "sugar": 3.5,
        "sodium": 70.0,
        "potassium": 140.0,
        "calcium": 100.0,
        "magnesium": 9.0,
        "phosphorus": 150.0,
        "iron": 0.05,
        "zinc": 0.4,
        "vitamin a": 70.0,
        "vitamin b1": 0.03,
        "vitamin b2": 0.24,
        "vitamin b12": 0.65,
        "vitamin b3": 0.1,
        "cholesterol": 20.0,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_butter() -> Food:
    """
    Butter
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Butter",
        name_de="Butter",
        category="spread",
        nutrition_data={
        "calories": 741.0,
        "water": 15.3,
        "protein": 0.7,
        "fat": 83.2,
        "carbohydrate": 0.6,
        "sugar": 0.6,
        "sodium": 10.0,
        "potassium": 24.0,
        "calcium": 15.0,
        "magnesium": 2.0,
        "phosphorus": 24.0,
        "iron": 0.02,
        "vitamin a": 683.0,
        "vitamin d": 1.5,
        "vitamin e": 2.0,
        "vitamin k": 0.007,
        "vitamin b2": 0.04,
        "cholesterol": 215.0,
        "saturated fat": 53.8,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )

def create_sahne() -> Food:
    """
    Sahne
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Sahne",
        name_de="Sahne",
        category="milk",
        nutrition_data={
        "calories": 204.0,
        "water": 72.0,
        "protein": 2.1,
        "fat": 19.3,
        "carbohydrate": 3.2,
        "sugar": 3.2,
        "sodium": 40.0,
        "potassium": 77.0,
        "calcium": 65.0,
        "magnesium": 4.0,
        "phosphorus": 60.0,
        "iron": 0.02,
        "vitamin a": 155.0,
        "vitamin d": 0.6,
        "vitamin e": 0.4,
        "vitamin b2": 0.09,
        "cholesterol": 65.0,
        "saturated fat": 12.3,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_gouda() -> Food:
    """
    Gouda
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Gouda",
        name_de="Gouda",
        category="cheese",
        nutrition_data={
        "calories": 356.0,
        "water": 38.2,
        "protein": 25.0,
        "fat": 27.4,
        "carbohydrate": 2.2,
        "sodium": 820.0,
        "potassium": 120.0,
        "calcium": 700.0,
        "magnesium": 27.0,
        "phosphorus": 550.0,
        "iron": 0.1,
        "zinc": 3.7,
        "vitamin a": 270.0,
        "vitamin b2": 0.34,
        "vitamin b12": 1.6,
        "cholesterol": 115.0,
        "saturated fat": 17.6,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_edamer() -> Food:
    """
    Edamer
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Edamer",
        name_de="Edamer",
        category="cheese",
        nutrition_data={
        "calories": 327.0,
        "water": 43.0,
        "protein": 25.0,
        "fat": 24.3,
        "carbohydrate": 1.4,
        "sodium": 960.0,
        "potassium": 120.0,
        "calcium": 730.0,
        "magnesium": 29.0,
        "phosphorus": 540.0,
        "iron": 0.1,
        "zinc": 3.9,
        "vitamin a": 260.0,
        "vitamin b2": 0.38,
        "vitamin b12": 1.7,
        "cholesterol": 100.0,
        "saturated fat": 15.6,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_emmentaler() -> Food:
    """
    Emmentaler
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Emmentaler",
        name_de="Emmentaler",
        category="cheese",
        nutrition_data={
        "calories": 382.0,
        "water": 35.0,
        "protein": 28.5,
        "fat": 29.2,
        "sodium": 400.0,
        "potassium": 90.0,
        "calcium": 1040.0,
        "magnesium": 35.0,
        "phosphorus": 760.0,
        "iron": 0.2,
        "zinc": 4.8,
        "vitamin a": 300.0,
        "vitamin b2": 0.3,
        "vitamin b12": 2.0,
        "cholesterol": 110.0,
        "saturated fat": 19.2,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_camembert() -> Food:
    """
    Camembert
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Camembert",
        name_de="Camembert",
        category="cheese",
        nutrition_data={
        "calories": 297.0,
        "water": 51.0,
        "protein": 19.8,
        "fat": 24.3,
        "carbohydrate": 0.5,
        "sodium": 800.0,
        "potassium": 100.0,
        "calcium": 350.0,
        "magnesium": 20.0,
        "phosphorus": 380.0,
        "iron": 0.2,
        "zinc": 2.7,
        "vitamin a": 240.0,
        "vitamin b2": 0.5,
        "vitamin b12": 1.5,
        "cholesterol": 90.0,
        "saturated fat": 15.5,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_frischkäse() -> Food:
    """
    Frischkäse
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Frischkäse",
        name_de="Frischkäse",
        category="cheese",
        nutrition_data={
        "calories": 264.0,
        "water": 57.8,
        "protein": 6.5,
        "fat": 25.0,
        "carbohydrate": 3.2,
        "sugar": 3.2,
        "sodium": 400.0,
        "potassium": 130.0,
        "calcium": 65.0,
        "magnesium": 5.0,
        "phosphorus": 100.0,
        "iron": 0.1,
        "zinc": 0.4,
        "vitamin a": 250.0,
        "vitamin b2": 0.22,
        "vitamin b12": 0.5,
        "cholesterol": 85.0,
        "saturated fat": 16.2,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_mozzarella() -> Food:
    """
    Mozzarella
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Mozzarella",
        name_de="Mozzarella",
        category="cheese",
        nutrition_data={
        "calories": 256.0,
        "water": 58.8,
        "protein": 19.5,
        "fat": 19.5,
        "carbohydrate": 0.7,
        "sugar": 0.7,
        "sodium": 140.0,
        "potassium": 8.0,
        "calcium": 340.0,
        "magnesium": 10.0,
        "phosphorus": 350.0,
        "iron": 0.1,
        "zinc": 2.6,
        "vitamin a": 183.0,
        "vitamin d": 0.3,
        "vitamin b2": 0.27,
        "vitamin b12": 1.4,
        "cholesterol": 46.0,
        "saturated fat": 11.4,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_feta() -> Food:
    """
    Feta
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Feta",
        name_de="Feta",
        category="cheese",
        nutrition_data={
        "calories": 264.0,
        "water": 55.2,
        "protein": 14.2,
        "fat": 21.3,
        "carbohydrate": 4.1,
        "sugar": 4.1,
        "sodium": 1110.0,
        "potassium": 60.0,
        "calcium": 490.0,
        "magnesium": 19.0,
        "phosphorus": 340.0,
        "iron": 0.2,
        "zinc": 2.2,
        "vitamin a": 130.0,
        "vitamin b2": 0.24,
        "vitamin b12": 1.0,
        "cholesterol": 89.0,
        "saturated fat": 13.3,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_rindfleisch_roh() -> Food:
    """
    Rindfleisch roh
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Rindfleisch roh",
        name_de="Rindfleisch roh",
        category="meat",
        nutrition_data={
        "calories": 113.0,
        "water": 75.0,
        "protein": 22.0,
        "fat": 2.5,
        "sodium": 60.0,
        "potassium": 320.0,
        "calcium": 5.0,
        "magnesium": 22.0,
        "phosphorus": 200.0,
        "iron": 2.3,
        "zinc": 4.2,
        "vitamin b1": 0.09,
        "vitamin b2": 0.22,
        "vitamin b3": 5.0,
        "vitamin b6": 0.35,
        "vitamin b12": 2.0,
        "cholesterol": 55.0,
        "saturated fat": 1.0,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_schweinefleisch_roh() -> Food:
    """
    Schweinefleisch roh
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Schweinefleisch roh",
        name_de="Schweinefleisch roh",
        category="meat",
        nutrition_data={
        "calories": 143.0,
        "water": 72.0,
        "protein": 20.5,
        "fat": 6.3,
        "sodium": 60.0,
        "potassium": 350.0,
        "calcium": 6.0,
        "magnesium": 23.0,
        "phosphorus": 210.0,
        "iron": 1.0,
        "zinc": 2.0,
        "vitamin b1": 0.9,
        "vitamin b2": 0.19,
        "vitamin b3": 4.5,
        "vitamin b6": 0.4,
        "vitamin b12": 0.7,
        "cholesterol": 60.0,
        "saturated fat": 2.3,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_hähnchenbrust_roh() -> Food:
    """
    Hähnchenbrust roh
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Hähnchenbrust roh",
        name_de="Hähnchenbrust roh",
        category="meat",
        nutrition_data={
        "calories": 114.0,
        "water": 75.5,
        "protein": 21.2,
        "fat": 2.6,
        "sodium": 70.0,
        "potassium": 250.0,
        "calcium": 6.0,
        "magnesium": 27.0,
        "phosphorus": 210.0,
        "iron": 0.5,
        "zinc": 0.9,
        "vitamin b3": 7.0,
        "vitamin b6": 0.55,
        "vitamin b12": 0.4,
        "cholesterol": 65.0,
        "saturated fat": 0.7,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_wiener_würstchen() -> Food:
    """
    Wiener Würstchen
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Wiener Würstchen",
        name_de="Wiener Würstchen",
        category="sausage",
        nutrition_data={
        "calories": 296.0,
        "water": 56.0,
        "protein": 11.5,
        "fat": 27.0,
        "carbohydrate": 1.0,
        "sodium": 1000.0,
        "potassium": 150.0,
        "calcium": 10.0,
        "magnesium": 15.0,
        "phosphorus": 100.0,
        "iron": 1.5,
        "zinc": 2.0,
        "vitamin b1": 0.25,
        "vitamin b2": 0.12,
        "vitamin b3": 3.0,
        "vitamin b12": 1.0,
        "cholesterol": 55.0,
        "saturated fat": 10.0,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_bratwurst() -> Food:
    """
    Bratwurst
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Bratwurst",
        name_de="Bratwurst",
        category="sausage",
        nutrition_data={
        "calories": 313.0,
        "water": 53.0,
        "protein": 13.5,
        "fat": 28.0,
        "carbohydrate": 1.0,
        "sodium": 900.0,
        "potassium": 220.0,
        "calcium": 9.0,
        "magnesium": 18.0,
        "phosphorus": 130.0,
        "iron": 1.3,
        "zinc": 2.5,
        "vitamin b1": 0.35,
        "vitamin b2": 0.18,
        "vitamin b3": 3.5,
        "vitamin b12": 1.0,
        "cholesterol": 70.0,
        "saturated fat": 10.5,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_schinken_gekocht() -> Food:
    """
    Schinken gekocht
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Schinken gekocht",
        name_de="Schinken gekocht",
        category="sausage",
        nutrition_data={
        "calories": 122.0,
        "water": 72.0,
        "protein": 20.0,
        "fat": 4.5,
        "carbohydrate": 0.5,
        "sodium": 1200.0,
        "potassium": 300.0,
        "calcium": 6.0,
        "magnesium": 20.0,
        "phosphorus": 200.0,
        "iron": 0.9,
        "zinc": 1.8,
        "vitamin b1": 0.6,
        "vitamin b2": 0.15,
        "vitamin b3": 4.5,
        "vitamin b6": 0.35,
        "vitamin b12": 0.8,
        "cholesterol": 40.0,
        "saturated fat": 1.5,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_lachs_roh() -> Food:
    """
    Lachs roh
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Lachs roh",
        name_de="Lachs roh",
        category="fish",
        nutrition_data={
        "calories": 208.0,
        "water": 67.0,
        "protein": 20.0,
        "fat": 14.0,
        "sodium": 50.0,
        "potassium": 360.0,
        "calcium": 9.0,
        "magnesium": 27.0,
        "phosphorus": 240.0,
        "iron": 0.3,
        "zinc": 0.4,
        "iodine": 12.0,
        "vitamin d": 8.0,
        "vitamin e": 3.0,
        "vitamin b3": 7.0,
        "vitamin b6": 0.6,
        "vitamin b12": 3.0,
        "cholesterol": 55.0,
        "saturated fat": 3.0,
        "omega 3": 2.3,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_thunfisch_dose() -> Food:
    """
    Thunfisch Dose
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Thunfisch Dose",
        name_de="Thunfisch Dose",
        category="fish",
        nutrition_data={
        "calories": 116.0,
        "water": 70.0,
        "protein": 26.0,
        "fat": 1.0,
        "sodium": 400.0,
        "potassium": 300.0,
        "calcium": 10.0,
        "magnesium": 35.0,
        "phosphorus": 220.0,
        "iron": 0.8,
        "zinc": 0.5,
        "iodine": 15.0,
        "vitamin d": 1.0,
        "vitamin b3": 12.0,
        "vitamin b6": 0.4,
        "vitamin b12": 2.0,
        "cholesterol": 40.0,
        "saturated fat": 0.3,
        "omega 3": 0.3,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_kartoffel_roh() -> Food:
    """
    Kartoffel roh
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Kartoffel roh",
        name_de="Kartoffel roh",
        category="vegetable",
        nutrition_data={
        "calories": 71.0,
        "water": 79.0,
        "protein": 1.8,
        "fat": 0.1,
        "carbohydrate": 15.2,
        "sugar": 0.8,
        "starch": 13.5,
        "fiber": 1.7,
        "sodium": 8.0,
        "potassium": 410.0,
        "calcium": 9.0,
        "magnesium": 22.0,
        "phosphorus": 55.0,
        "iron": 0.5,
        "zinc": 0.3,
        "vitamin c": 11.0,
        "vitamin b3": 1.4,
        "vitamin b6": 0.24,
        "vitamin b9": 0.018,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_möhre_roh() -> Food:
    """
    Möhre roh
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Möhre roh",
        name_de="Möhre roh",
        category="vegetable",
        nutrition_data={
        "calories": 35.0,
        "water": 88.0,
        "protein": 0.9,
        "fat": 0.2,
        "carbohydrate": 6.8,
        "sugar": 4.7,
        "fiber": 2.4,
        "sodium": 60.0,
        "potassium": 320.0,
        "calcium": 33.0,
        "magnesium": 12.0,
        "phosphorus": 35.0,
        "iron": 0.4,
        "zinc": 0.2,
        "provitamin a": 8350.0,
        "vitamin c": 4.0,
        "vitamin b3": 0.6,
        "vitamin b6": 0.12,
        "vitamin b9": 0.024,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_broccoli_roh() -> Food:
    """
    Broccoli roh
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Broccoli roh",
        name_de="Broccoli roh",
        category="vegetable",
        nutrition_data={
        "calories": 35.0,
        "water": 89.0,
        "protein": 2.8,
        "fat": 0.4,
        "carbohydrate": 3.0,
        "sugar": 1.7,
        "fiber": 2.6,
        "sodium": 30.0,
        "potassium": 380.0,
        "calcium": 47.0,
        "magnesium": 21.0,
        "phosphorus": 66.0,
        "iron": 0.7,
        "zinc": 0.4,
        "provitamin a": 361.0,
        "vitamin c": 89.0,
        "vitamin b3": 0.64,
        "vitamin b5": 0.57,
        "vitamin b6": 0.2,
        "vitamin b9": 0.063,
        "vitamin e": 0.78,
        "vitamin k": 0.102,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_tomate_roh() -> Food:
    """
    Tomate roh
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Tomate roh",
        name_de="Tomate roh",
        category="vegetable",
        nutrition_data={
        "calories": 18.0,
        "water": 94.0,
        "protein": 0.9,
        "fat": 0.2,
        "carbohydrate": 2.8,
        "sugar": 2.6,
        "fiber": 1.2,
        "sodium": 5.0,
        "potassium": 240.0,
        "calcium": 10.0,
        "magnesium": 11.0,
        "phosphorus": 24.0,
        "iron": 0.3,
        "zinc": 0.1,
        "provitamin a": 450.0,
        "vitamin c": 14.0,
        "vitamin b3": 0.6,
        "vitamin b5": 0.2,
        "vitamin b6": 0.06,
        "vitamin b9": 0.015,
        "vitamin e": 0.54,
        "vitamin k": 0.079,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_gurke_roh() -> Food:
    """
    Gurke roh
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Gurke roh",
        name_de="Gurke roh",
        category="vegetable",
        nutrition_data={
        "calories": 13.0,
        "water": 96.0,
        "protein": 0.6,
        "fat": 0.1,
        "carbohydrate": 2.2,
        "sugar": 1.7,
        "fiber": 0.8,
        "sodium": 2.0,
        "potassium": 150.0,
        "calcium": 16.0,
        "magnesium": 13.0,
        "phosphorus": 24.0,
        "iron": 0.3,
        "zinc": 0.2,
        "vitamin c": 4.0,
        "vitamin b3": 0.1,
        "vitamin b5": 0.26,
        "vitamin b9": 0.007,
        "vitamin k": 0.016,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_paprika_rot_roh() -> Food:
    """
    Paprika rot roh
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Paprika rot roh",
        name_de="Paprika rot roh",
        category="vegetable",
        nutrition_data={
        "calories": 26.0,
        "water": 92.0,
        "protein": 1.0,
        "fat": 0.3,
        "carbohydrate": 4.6,
        "sugar": 4.2,
        "fiber": 1.9,
        "sodium": 3.0,
        "potassium": 210.0,
        "calcium": 10.0,
        "magnesium": 12.0,
        "phosphorus": 26.0,
        "iron": 0.4,
        "zinc": 0.2,
        "provitamin a": 1620.0,
        "vitamin c": 128.0,
        "vitamin b3": 0.5,
        "vitamin b5": 0.3,
        "vitamin b6": 0.29,
        "vitamin b9": 0.046,
        "vitamin e": 1.4,
        "vitamin k": 0.043,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_zwiebel_roh() -> Food:
    """
    Zwiebel roh
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Zwiebel roh",
        name_de="Zwiebel roh",
        category="vegetable",
        nutrition_data={
        "calories": 38.0,
        "water": 89.0,
        "protein": 1.1,
        "fat": 0.1,
        "carbohydrate": 7.9,
        "sugar": 4.2,
        "fiber": 1.5,
        "sodium": 4.0,
        "potassium": 150.0,
        "calcium": 23.0,
        "magnesium": 10.0,
        "phosphorus": 30.0,
        "iron": 0.2,
        "zinc": 0.2,
        "vitamin c": 7.0,
        "vitamin b3": 0.12,
        "vitamin b5": 0.12,
        "vitamin b6": 0.12,
        "vitamin b9": 0.016,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_knoblauch_roh() -> Food:
    """
    Knoblauch roh
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Knoblauch roh",
        name_de="Knoblauch roh",
        category="vegetable",
        nutrition_data={
        "calories": 141.0,
        "water": 60.0,
        "protein": 6.4,
        "fat": 0.5,
        "carbohydrate": 28.2,
        "sugar": 1.0,
        "fiber": 1.9,
        "sodium": 17.0,
        "potassium": 400.0,
        "calcium": 181.0,
        "magnesium": 25.0,
        "phosphorus": 153.0,
        "iron": 1.7,
        "zinc": 1.6,
        "manganese": 167.0,
        "vitamin c": 31.0,
        "vitamin b3": 0.6,
        "vitamin b5": 0.3,
        "vitamin b6": 1.2,
        "vitamin b9": 0.003,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_salat_grün_roh() -> Food:
    """
    Salat grün roh
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Salat grün roh",
        name_de="Salat grün roh",
        category="vegetable",
        nutrition_data={
        "calories": 14.0,
        "water": 95.0,
        "protein": 1.3,
        "fat": 0.2,
        "carbohydrate": 1.4,
        "sugar": 0.8,
        "fiber": 1.3,
        "sodium": 30.0,
        "potassium": 250.0,
        "calcium": 36.0,
        "magnesium": 13.0,
        "phosphorus": 29.0,
        "iron": 0.9,
        "zinc": 0.2,
        "provitamin a": 1880.0,
        "vitamin c": 9.0,
        "vitamin b3": 0.3,
        "vitamin b5": 0.15,
        "vitamin b6": 0.07,
        "vitamin b9": 0.073,
        "vitamin e": 0.18,
        "vitamin k": 0.126,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_apfel_roh() -> Food:
    """
    Apfel roh
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Apfel roh",
        name_de="Apfel roh",
        category="fruit",
        nutrition_data={
        "calories": 52.0,
        "water": 85.0,
        "protein": 0.3,
        "fat": 0.2,
        "carbohydrate": 11.8,
        "sugar": 10.4,
        "fiber": 2.0,
        "sodium": 1.0,
        "potassium": 120.0,
        "calcium": 7.0,
        "magnesium": 5.0,
        "phosphorus": 12.0,
        "iron": 0.2,
        "zinc": 0.05,
        "vitamin c": 5.0,
        "vitamin b3": 0.1,
        "vitamin b5": 0.06,
        "vitamin b6": 0.04,
        "vitamin b9": 0.003,
        "vitamin e": 0.18,
        "vitamin k": 0.002,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_banane_roh() -> Food:
    """
    Banane roh
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Banane roh",
        name_de="Banane roh",
        category="fruit",
        nutrition_data={
        "calories": 89.0,
        "water": 75.0,
        "protein": 1.1,
        "fat": 0.3,
        "carbohydrate": 20.2,
        "sugar": 12.0,
        "starch": 6.0,
        "fiber": 2.1,
        "sodium": 1.0,
        "potassium": 360.0,
        "calcium": 5.0,
        "magnesium": 27.0,
        "phosphorus": 22.0,
        "iron": 0.3,
        "zinc": 0.15,
        "provitamin a": 26.0,
        "vitamin c": 9.0,
        "vitamin b3": 0.7,
        "vitamin b5": 0.33,
        "vitamin b6": 0.37,
        "vitamin b9": 0.02,
        "vitamin e": 0.1,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_orange_roh() -> Food:
    """
    Orange roh
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Orange roh",
        name_de="Orange roh",
        category="fruit",
        nutrition_data={
        "calories": 47.0,
        "water": 87.0,
        "protein": 0.9,
        "fat": 0.1,
        "carbohydrate": 9.6,
        "sugar": 8.5,
        "fiber": 2.0,
        "sodium": 1.0,
        "potassium": 180.0,
        "calcium": 40.0,
        "magnesium": 10.0,
        "phosphorus": 18.0,
        "iron": 0.1,
        "zinc": 0.05,
        "provitamin a": 71.0,
        "vitamin c": 53.0,
        "vitamin b1": 0.09,
        "vitamin b3": 0.3,
        "vitamin b5": 0.25,
        "vitamin b9": 0.03,
        "vitamin b6": 0.06,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_birne_roh() -> Food:
    """
    Birne roh
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Birne roh",
        name_de="Birne roh",
        category="fruit",
        nutrition_data={
        "calories": 57.0,
        "water": 84.0,
        "protein": 0.4,
        "fat": 0.1,
        "carbohydrate": 13.5,
        "sugar": 10.0,
        "fiber": 2.6,
        "sodium": 1.0,
        "potassium": 120.0,
        "calcium": 9.0,
        "magnesium": 6.0,
        "phosphorus": 12.0,
        "iron": 0.2,
        "zinc": 0.07,
        "provitamin a": 12.0,
        "vitamin c": 4.0,
        "vitamin b3": 0.1,
        "vitamin b5": 0.05,
        "vitamin b9": 0.007,
        "vitamin e": 0.12,
        "vitamin k": 0.004,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_trauben_roh() -> Food:
    """
    Trauben roh
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Trauben roh",
        name_de="Trauben roh",
        category="fruit",
        nutrition_data={
        "calories": 69.0,
        "water": 81.0,
        "protein": 0.7,
        "fat": 0.2,
        "carbohydrate": 16.5,
        "sugar": 15.5,
        "fiber": 1.0,
        "sodium": 2.0,
        "potassium": 190.0,
        "calcium": 10.0,
        "magnesium": 7.0,
        "phosphorus": 20.0,
        "iron": 0.4,
        "zinc": 0.07,
        "vitamin c": 4.0,
        "vitamin b3": 0.2,
        "vitamin b5": 0.05,
        "vitamin b6": 0.09,
        "vitamin b9": 0.002,
        "vitamin k": 0.015,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_erdbeeren_roh() -> Food:
    """
    Erdbeeren roh
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Erdbeeren roh",
        name_de="Erdbeeren roh",
        category="fruit",
        nutrition_data={
        "calories": 32.0,
        "water": 91.0,
        "protein": 0.7,
        "fat": 0.3,
        "carbohydrate": 5.7,
        "sugar": 4.9,
        "fiber": 2.0,
        "sodium": 1.0,
        "potassium": 150.0,
        "calcium": 16.0,
        "magnesium": 13.0,
        "phosphorus": 24.0,
        "iron": 0.4,
        "zinc": 0.1,
        "provitamin a": 8.0,
        "vitamin c": 59.0,
        "vitamin b3": 0.4,
        "vitamin b5": 0.13,
        "vitamin b6": 0.05,
        "vitamin b9": 0.024,
        "vitamin e": 0.29,
        "vitamin k": 0.003,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_bohnen_weiss_gekocht() -> Food:
    """
    Bohnen weiss gekocht
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Bohnen weiss gekocht",
        name_de="Bohnen weiss gekocht",
        category="legume",
        nutrition_data={
        "calories": 114.0,
        "water": 69.0,
        "protein": 7.0,
        "fat": 0.5,
        "carbohydrate": 17.0,
        "sugar": 0.3,
        "starch": 14.0,
        "fiber": 7.0,
        "sodium": 20.0,
        "potassium": 400.0,
        "calcium": 50.0,
        "magnesium": 40.0,
        "phosphorus": 120.0,
        "iron": 2.0,
        "zinc": 1.0,
        "vitamin b1": 0.1,
        "vitamin b3": 0.5,
        "vitamin b5": 0.2,
        "vitamin b6": 0.1,
        "vitamin b9": 0.035,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_linsen_gekocht() -> Food:
    """
    Linsen gekocht
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Linsen gekocht",
        name_de="Linsen gekocht",
        category="legume",
        nutrition_data={
        "calories": 116.0,
        "water": 69.0,
        "protein": 9.0,
        "fat": 0.4,
        "carbohydrate": 16.0,
        "sugar": 0.5,
        "starch": 13.0,
        "fiber": 8.0,
        "sodium": 20.0,
        "potassium": 370.0,
        "calcium": 19.0,
        "magnesium": 36.0,
        "phosphorus": 180.0,
        "iron": 3.3,
        "zinc": 1.3,
        "vitamin b1": 0.17,
        "vitamin b3": 1.0,
        "vitamin b5": 0.4,
        "vitamin b6": 0.18,
        "vitamin b9": 0.181,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_mandeln() -> Food:
    """
    Mandeln
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Mandeln",
        name_de="Mandeln",
        category="snack",
        nutrition_data={
        "calories": 579.0,
        "water": 4.4,
        "protein": 21.2,
        "fat": 49.9,
        "carbohydrate": 6.0,
        "sugar": 4.4,
        "fiber": 12.5,
        "sodium": 1.0,
        "potassium": 730.0,
        "calcium": 269.0,
        "magnesium": 270.0,
        "phosphorus": 481.0,
        "iron": 3.7,
        "zinc": 3.1,
        "manganese": 2.17,
        "vitamin e": 25.6,
        "vitamin b2": 1.0,
        "vitamin b3": 3.5,
        "vitamin b5": 0.3,
        "vitamin b6": 0.14,
        "vitamin b9": 0.044,
        "saturated fat": 3.8,
        "omega 6": 12.3,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_walnüsse() -> Food:
    """
    Walnüsse
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Walnüsse",
        name_de="Walnüsse",
        category="snack",
        nutrition_data={
        "calories": 654.0,
        "water": 3.0,
        "protein": 15.2,
        "fat": 65.2,
        "carbohydrate": 6.0,
        "sugar": 2.6,
        "fiber": 6.7,
        "sodium": 2.0,
        "potassium": 440.0,
        "calcium": 98.0,
        "magnesium": 158.0,
        "phosphorus": 346.0,
        "iron": 2.9,
        "zinc": 3.1,
        "vitamin b6": 0.54,
        "vitamin b9": 0.098,
        "vitamin e": 0.7,
        "saturated fat": 6.1,
        "omega 3": 9.1,
        "omega 6": 38.1,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_olivenöl() -> Food:
    """
    Olivenöl
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Olivenöl",
        name_de="Olivenöl",
        category="oil",
        nutrition_data={
        "calories": 884.0,
        "fat": 100.0,
        "vitamin e": 14.4,
        "vitamin k": 0.06,
        "saturated fat": 13.8,
        "monounsaturated fat": 73.0,
        "polyunsaturated fat": 10.5,
        "omega 3": 0.8,
        "omega 6": 9.8,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_rapsöl() -> Food:
    """
    Rapsöl
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Rapsöl",
        name_de="Rapsöl",
        category="oil",
        nutrition_data={
        "calories": 884.0,
        "fat": 100.0,
        "vitamin e": 17.3,
        "vitamin k": 0.071,
        "saturated fat": 7.4,
        "monounsaturated fat": 63.3,
        "polyunsaturated fat": 28.1,
        "omega 3": 9.1,
        "omega 6": 19.0,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_sonnenblumenöl() -> Food:
    """
    Sonnenblumenöl
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Sonnenblumenöl",
        name_de="Sonnenblumenöl",
        category="oil",
        nutrition_data={
        "calories": 884.0,
        "fat": 100.0,
        "vitamin e": 41.1,
        "vitamin k": 0.005,
        "saturated fat": 10.3,
        "monounsaturated fat": 19.5,
        "polyunsaturated fat": 65.7,
        "omega 6": 65.7,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_butterschmalz() -> Food:
    """
    Butterschmalz
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Butterschmalz",
        name_de="Butterschmalz",
        category="oil",
        nutrition_data={
        "calories": 900.0,
        "fat": 100.0,
        "vitamin a": 840.0,
        "vitamin d": 1.0,
        "vitamin e": 3.0,
        "vitamin k": 0.009,
        "cholesterol": 285.0,
        "saturated fat": 65.0,
        "omega 3": 1.0,
        "omega 6": 3.0,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_schokolade_vollmilch() -> Food:
    """
    Schokolade vollmilch
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Schokolade vollmilch",
        name_de="Schokolade vollmilch",
        category="sweet",
        nutrition_data={
        "calories": 546.0,
        "water": 1.0,
        "protein": 7.3,
        "fat": 31.0,
        "carbohydrate": 56.0,
        "sugar": 55.0,
        "fiber": 3.4,
        "sodium": 90.0,
        "potassium": 370.0,
        "calcium": 190.0,
        "magnesium": 63.0,
        "phosphorus": 210.0,
        "iron": 1.0,
        "zinc": 1.2,
        "vitamin a": 200.0,
        "vitamin b2": 0.3,
        "vitamin b12": 0.5,
        "vitamin d": 2.0,
        "vitamin e": 1.0,
        "cholesterol": 23.0,
        "saturated fat": 19.0,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_schokolade_zartbitter() -> Food:
    """
    Schokolade zartbitter
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Schokolade zartbitter",
        name_de="Schokolade zartbitter",
        category="sweet",
        nutrition_data={
        "calories": 598.0,
        "water": 1.0,
        "protein": 7.8,
        "fat": 42.6,
        "carbohydrate": 45.4,
        "sugar": 24.0,
        "fiber": 10.9,
        "sodium": 20.0,
        "potassium": 720.0,
        "calcium": 31.0,
        "magnesium": 230.0,
        "phosphorus": 310.0,
        "iron": 17.0,
        "zinc": 3.0,
        "manganese": 19.0,
        "copper": 1.4,
        "vitamin b3": 1.2,
        "vitamin b6": 0.04,
        "vitamin b12": 0.3,
        "vitamin e": 1.0,
        "saturated fat": 24.5,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_honig() -> Food:
    """
    Honig
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Honig",
        name_de="Honig",
        category="spread",
        nutrition_data={
        "calories": 304.0,
        "water": 17.0,
        "protein": 0.3,
        "carbohydrate": 82.4,
        "sugar": 82.1,
        "fiber": 0.2,
        "sodium": 4.0,
        "potassium": 52.0,
        "calcium": 6.0,
        "magnesium": 2.0,
        "phosphorus": 4.0,
        "iron": 0.4,
        "zinc": 0.2,
        "vitamin b2": 0.04,
        "vitamin b3": 0.1,
        "vitamin b5": 0.06,
        "vitamin b6": 0.01,
        "vitamin b9": 0.002,
        "vitamin c": 0.5,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_zucker_weiss() -> Food:
    """
    Zucker weiss
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Zucker weiss",
        name_de="Zucker weiss",
        category="spices",
        nutrition_data={
        "calories": 400.0,
        "carbohydrate": 100.0,
        "sugar": 100.0,
        "potassium": 2.0,
        "calcium": 1.0,
        "iron": 0.1,
        "zinc": 0.01,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_marmelade() -> Food:
    """
    Marmelade
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Marmelade",
        name_de="Marmelade",
        category="spread",
        nutrition_data={
        "calories": 250.0,
        "water": 30.0,
        "protein": 0.3,
        "fat": 0.1,
        "carbohydrate": 62.0,
        "sugar": 59.0,
        "fiber": 1.0,
        "sodium": 30.0,
        "potassium": 80.0,
        "calcium": 20.0,
        "magnesium": 3.0,
        "phosphorus": 10.0,
        "iron": 0.4,
        "zinc": 0.1,
        "vitamin b3": 0.1,
        "vitamin b9": 0.002,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_keks_butter() -> Food:
    """
    Keks Butter
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Keks Butter",
        name_de="Keks Butter",
        category="sweet",
        nutrition_data={
        "calories": 502.0,
        "water": 2.0,
        "protein": 5.8,
        "fat": 25.0,
        "carbohydrate": 64.0,
        "sugar": 20.0,
        "fiber": 2.0,
        "sodium": 380.0,
        "potassium": 80.0,
        "calcium": 20.0,
        "magnesium": 10.0,
        "phosphorus": 80.0,
        "iron": 1.0,
        "zinc": 0.4,
        "vitamin b1": 0.08,
        "vitamin b2": 0.04,
        "vitamin b3": 0.3,
        "vitamin b6": 0.04,
        "vitamin b9": 0.015,
        "saturated fat": 15.0,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_salz() -> Food:
    """
    Salz
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Salz",
        name_de="Salz",
        category="spices",
        nutrition_data={
        "water": 0.2,
        "sodium": 38760.0,
        "chloride": 59.66,
        "iodine": 200.0,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_pfeffer_schwarz() -> Food:
    """
    Pfeffer schwarz
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Pfeffer schwarz",
        name_de="Pfeffer schwarz",
        category="spices",
        nutrition_data={
        "calories": 255.0,
        "water": 12.0,
        "protein": 10.0,
        "fat": 3.3,
        "carbohydrate": 64.0,
        "sugar": 0.6,
        "fiber": 25.3,
        "sodium": 44.0,
        "potassium": 1330.0,
        "calcium": 443.0,
        "magnesium": 194.0,
        "phosphorus": 158.0,
        "iron": 28.6,
        "zinc": 1.3,
        "manganese": 5.9,
        "copper": 1.0,
        "vitamin b3": 1.1,
        "vitamin b5": 0.3,
        "vitamin b6": 0.3,
        "vitamin b9": 0.017,
        "vitamin a": 27.0,
        "vitamin e": 1.0,
        "vitamin k": 0.163,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_zimt() -> Food:
    """
    Zimt
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Zimt",
        name_de="Zimt",
        category="spices",
        nutrition_data={
        "calories": 247.0,
        "water": 10.0,
        "protein": 4.0,
        "fat": 1.2,
        "carbohydrate": 81.0,
        "sugar": 2.2,
        "fiber": 53.1,
        "sodium": 10.0,
        "potassium": 430.0,
        "calcium": 1002.0,
        "magnesium": 60.0,
        "phosphorus": 64.0,
        "iron": 8.3,
        "zinc": 1.8,
        "manganese": 17470.0,
        "copper": 0.4,
        "vitamin c": 4.0,
        "vitamin b3": 1.3,
        "vitamin b6": 0.2,
        "vitamin b9": 0.006,
        "vitamin a": 29.0,
        "vitamin e": 2.3,
        "vitamin k": 0.031,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_basilikum_frisch() -> Food:
    """
    Basilikum frisch
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Basilikum frisch",
        name_de="Basilikum frisch",
        category="vegetable",
        nutrition_data={
        "calories": 23.0,
        "water": 92.0,
        "protein": 3.2,
        "fat": 0.6,
        "carbohydrate": 2.7,
        "sugar": 0.3,
        "fiber": 1.8,
        "sodium": 4.0,
        "potassium": 295.0,
        "calcium": 177.0,
        "magnesium": 64.0,
        "phosphorus": 56.0,
        "iron": 3.2,
        "zinc": 0.8,
        "manganese": 1.15,
        "vitamin c": 18.0,
        "vitamin b3": 0.9,
        "vitamin b5": 0.3,
        "vitamin b6": 0.16,
        "vitamin b9": 0.068,
        "vitamin a": 528.0,
        "vitamin e": 0.8,
        "vitamin k": 0.415,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_petersilie_frisch() -> Food:
    """
    Petersilie frisch
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Petersilie frisch",
        name_de="Petersilie frisch",
        category="vegetable",
        nutrition_data={
        "calories": 36.0,
        "water": 88.0,
        "protein": 3.0,
        "fat": 0.8,
        "carbohydrate": 6.3,
        "sugar": 0.9,
        "fiber": 3.3,
        "sodium": 56.0,
        "potassium": 554.0,
        "calcium": 138.0,
        "magnesium": 50.0,
        "phosphorus": 58.0,
        "iron": 6.2,
        "zinc": 1.1,
        "manganese": 0.16,
        "copper": 0.15,
        "vitamin c": 133.0,
        "vitamin b3": 0.3,
        "vitamin b5": 0.4,
        "vitamin b6": 0.09,
        "vitamin b9": 0.152,
        "vitamin a": 842.0,
        "vitamin e": 0.75,
        "vitamin k": 1.64,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_bier_pils() -> Food:
    """
    Bier Pils
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Bier Pils",
        name_de="Bier Pils",
        category="beer",
        nutrition_data={
        "calories": 43.0,
        "water": 91.0,
        "protein": 0.4,
        "carbohydrate": 3.6,
        "sugar": 0.1,
        "sodium": 3.0,
        "potassium": 50.0,
        "calcium": 5.0,
        "magnesium": 6.0,
        "phosphorus": 14.0,
        "iron": 0.1,
        "zinc": 0.04,
        "vitamin b3": 0.4,
        "vitamin b6": 0.04,
        "vitamin b9": 0.006,
        "alcohol": 4.9,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_weissbier() -> Food:
    """
    Weissbier
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Weissbier",
        name_de="Weissbier",
        category="beer",
        nutrition_data={
        "calories": 44.0,
        "water": 90.0,
        "protein": 0.5,
        "carbohydrate": 4.0,
        "sugar": 0.1,
        "sodium": 3.0,
        "potassium": 40.0,
        "calcium": 6.0,
        "magnesium": 8.0,
        "phosphorus": 15.0,
        "iron": 0.1,
        "zinc": 0.05,
        "vitamin b3": 0.5,
        "vitamin b6": 0.05,
        "vitamin b9": 0.008,
        "alcohol": 5.3,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_rotwein() -> Food:
    """
    Rotwein
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Rotwein",
        name_de="Rotwein",
        category="alcohol",
        nutrition_data={
        "calories": 85.0,
        "water": 87.0,
        "protein": 0.1,
        "carbohydrate": 2.6,
        "sugar": 0.6,
        "sodium": 4.0,
        "potassium": 120.0,
        "calcium": 8.0,
        "magnesium": 12.0,
        "phosphorus": 20.0,
        "iron": 0.5,
        "zinc": 0.1,
        "manganese": 0.15,
        "vitamin b3": 0.1,
        "vitamin b6": 0.03,
        "alcohol": 12.0,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_weisswein() -> Food:
    """
    Weisswein
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Weisswein",
        name_de="Weisswein",
        category="alcohol",
        nutrition_data={
        "calories": 82.0,
        "water": 87.5,
        "protein": 0.1,
        "carbohydrate": 2.6,
        "sugar": 1.2,
        "sodium": 5.0,
        "potassium": 90.0,
        "calcium": 9.0,
        "magnesium": 10.0,
        "phosphorus": 18.0,
        "iron": 0.3,
        "zinc": 0.1,
        "vitamin b3": 0.1,
        "alcohol": 11.5,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_weizenbrötchen() -> Food:
    """
    Weizenbrötchen
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Weizenbrötchen",
        name_de="Weizenbrötchen",
        category="bread",
        nutrition_data={
        "calories": 261.0,
        "water": 34.0,
        "protein": 8.3,
        "fat": 3.2,
        "carbohydrate": 48.0,
        "sugar": 2.6,
        "starch": 43.0,
        "fiber": 3.0,
        "sodium": 470.0,
        "potassium": 120.0,
        "calcium": 29.0,
        "magnesium": 23.0,
        "phosphorus": 90.0,
        "iron": 1.0,
        "zinc": 0.7,
        "vitamin b1": 0.38,
        "vitamin b2": 0.07,
        "vitamin b3": 2.0,
        "vitamin b6": 0.05,
        "vitamin b9": 0.037,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_roggenbrötchen() -> Food:
    """
    Roggenbrötchen
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Roggenbrötchen",
        name_de="Roggenbrötchen",
        category="bread",
        nutrition_data={
        "calories": 249.0,
        "water": 36.0,
        "protein": 7.5,
        "fat": 2.3,
        "carbohydrate": 47.0,
        "sugar": 3.5,
        "starch": 41.0,
        "fiber": 5.5,
        "sodium": 520.0,
        "potassium": 180.0,
        "calcium": 35.0,
        "magnesium": 38.0,
        "phosphorus": 100.0,
        "iron": 1.5,
        "zinc": 1.0,
        "vitamin b1": 0.23,
        "vitamin b2": 0.09,
        "vitamin b3": 1.2,
        "vitamin b6": 0.12,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_baguette() -> Food:
    """
    Baguette
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Baguette",
        name_de="Baguette",
        category="bread",
        nutrition_data={
        "calories": 261.0,
        "water": 33.0,
        "protein": 8.5,
        "fat": 3.2,
        "carbohydrate": 48.0,
        "sugar": 2.5,
        "starch": 43.0,
        "fiber": 2.8,
        "sodium": 580.0,
        "potassium": 100.0,
        "calcium": 30.0,
        "magnesium": 20.0,
        "phosphorus": 80.0,
        "iron": 1.0,
        "zinc": 0.6,
        "vitamin b1": 0.4,
        "vitamin b2": 0.07,
        "vitamin b3": 2.0,
        "vitamin b6": 0.05,
        "vitamin b9": 0.032,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


def create_spaghetti_roh() -> Food:
    """
    Spaghetti roh
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Spaghetti roh",
        name_de="Spaghetti roh",
        category="pasta",
        nutrition_data={
        "calories": 357.0,
        "water": 10.0,
        "protein": 12.0,
        "fat": 1.8,
        "carbohydrate": 73.0,
        "sugar": 2.5,
        "starch": 67.0,
        "fiber": 3.6,
        "sodium": 5.0,
        "potassium": 200.0,
        "calcium": 25.0,
        "magnesium": 45.0,
        "phosphorus": 150.0,
        "iron": 1.4,
        "zinc": 1.0,
        "manganese": 540.0,
        "selenium": 26.0,
        "vitamin b1": 0.25,
        "vitamin b2": 0.06,
        "vitamin b3": 2.0,
        "vitamin b6": 0.15,
        "vitamin b9": 0.022,
        "vitamin e": 0.2,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )

def create_nudeln_ei_roh() -> Food:
    """
    Nudeln Ei roh
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Nudeln Ei roh",
        name_de="Nudeln Ei roh",
        category="pasta",
        nutrition_data={
        "calories": 384.0,
        "water": 9.0,
        "protein": 13.0,
        "fat": 5.5,
        "carbohydrate": 71.0,
        "sugar": 1.8,
        "starch": 67.0,
        "fiber": 3.0,
        "sodium": 40.0,
        "potassium": 150.0,
        "calcium": 25.0,
        "magnesium": 30.0,
        "phosphorus": 160.0,
        "iron": 1.3,
        "zinc": 1.0,
        "vitamin b1": 0.25,
        "vitamin b2": 0.12,
        "vitamin b3": 1.8,
        "vitamin b6": 0.1,
        "vitamin b9": 0.04,
        "vitamin e": 0.6,
        "cholesterol": 70.0,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )

def create_pizza_margherita() -> Food:
    """
    Pizza Margherita
    
    Source: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0
    """
    return Food(
        name="Pizza Margherita",
        name_de="Pizza Margherita",
        category="prepared",
        nutrition_data={
        "calories": 222.0,
        "water": 51.0,
        "protein": 9.5,
        "fat": 7.8,
        "carbohydrate": 28.0,
        "sugar": 2.5,
        "fiber": 2.0,
        "sodium": 500.0,
        "potassium": 180.0,
        "calcium": 140.0,
        "magnesium": 20.0,
        "phosphorus": 160.0,
        "iron": 1.2,
        "zinc": 1.0,
        "vitamin a": 60.0,
        "vitamin b1": 0.1,
        "vitamin b2": 0.1,
        "vitamin b3": 1.0,
        "vitamin b12": 0.3,
        "cholesterol": 15.0,
        "saturated fat": 3.5,
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    )


__all__ = [
    "create_hafer_ganzes_korn_roh",
    "create_hafer_flocken",
    "create_gerste_ganzes_korn_roh",
    "create_reis_poliert_roh",
    "create_vollkornbrot",
    "create_roggenbrot",
    "create_toastbrot_weiss",
    "create_milch_voll",
    "create_milch_fettarm",
    "create_joghurt_natur",
    "create_joghurt_griechisch",
    "create_quark_mager",
    "create_quark_20",
    "create_butter",
    "create_sahne",
    "create_gouda",
    "create_edamer",
    "create_emmentaler",
    "create_camembert",
    "create_frischkäse",
    "create_mozzarella",
    "create_feta",
    "create_rindfleisch_roh",
    "create_schweinefleisch_roh",
    "create_hähnchenbrust_roh",
    "create_wiener_würstchen",
    "create_bratwurst",
    "create_schinken_gekocht",
    "create_lachs_roh",
    "create_thunfisch_dose",
    "create_kartoffel_roh",
    "create_möhre_roh",
    "create_broccoli_roh",
    "create_tomate_roh",
    "create_gurke_roh",
    "create_paprika_rot_roh",
    "create_zwiebel_roh",
    "create_knoblauch_roh",
    "create_salat_grün_roh",
    "create_apfel_roh",
    "create_banane_roh",
    "create_orange_roh",
    "create_birne_roh",
    "create_trauben_roh",
    "create_erdbeeren_roh",
    "create_bohnen_weiss_gekocht",
    "create_linsen_gekocht",
    "create_mandeln",
    "create_walnüsse",
    "create_olivenöl",
    "create_rapsöl",
    "create_sonnenblumenöl",
    "create_butterschmalz",
    "create_schokolade_vollmilch",
    "create_schokolade_zartbitter",
    "create_honig",
    "create_zucker_weiss",
    "create_marmelade",
    "create_keks_butter",
    "create_salz",
    "create_pfeffer_schwarz",
    "create_zimt",
    "create_basilikum_frisch",
    "create_petersilie_frisch",
    "create_bier_pils",
    "create_weissbier",
    "create_rotwein",
    "create_weisswein",
    "create_weizenbrötchen",
    "create_roggenbrötchen",
    "create_baguette",
    "create_spaghetti_roh",
    "create_nudeln_ei_roh",
    "create_pizza_margherita",
]
