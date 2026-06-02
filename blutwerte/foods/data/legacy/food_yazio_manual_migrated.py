"""
Migrated from food_yazio_manual.py

Source: Yazio Food Database
URL: https://www.yazio.com
"""

from blutwerte.foods import Food, DataSource


def create_linsensuppe() -> Food:
    """
    linsensuppe
    
    Source: Yazio Food Database
    """
    return Food(
        name="linsensuppe",
        name_de="linsensuppe",
        category=None,
        nutrition_data={
        "calories": 25.0,
        "fat": 0.1,
        "carbohydrate": 3.3,
        "sugar": 0.4,
        "protein": 1.9,
        "salt": 0.6,
        "fiber": 1.2,
        "sodium": 200.0,
        "water": 92.3,
        "vitamin b3": 0.5,
        "vitamin c": 0.9,
        "vitamin e": 0.1,
        "calcium": 13.0,
        "iron": 0.5,
        "magnesium": 13.0,
        "manganese": 0.2,
        "phospohorus": 0.039,
        "potassium": 71.0,
        "sulfate": 0.018,
        "zinc": 0.3,
        },
        nutrition_sources=[
            DataSource(
                url="https://www.yazio.com",
                title="Yazio Food Database",
                source_type="database"
            )
        ]
    )


def create_rinderrouladen_mit_soße() -> Food:
    """
    rinderrouladen mit soße
    
    Source: Yazio Food Database
    """
    return Food(
        name="rinderrouladen mit soße",
        name_de="rinderrouladen mit soße",
        category=None,
        nutrition_data={
        "calories": 129.0,
        "fat": 7.4,
        "saturated fat": 3.8,
        "monounsaturated fat": 1.6,
        "polyunsaturated fat": 1.2,
        "carbohydrate": 2.6,
        "sugar": 1.2,
        "protein": 11.9,
        "salt": 0.5,
        "alcohol": 0.5,
        "fiber": 0.7,
        "cholesterol": 42.0,
        "sodium": 200.0,
        "water": 75.8,
        "vitamin b2": 0.1,
        "vitamin b3": 4.9,
        "vitamin b5": 0.2,
        "vitamin c": 0.7,
        "vitamin e": 0.3,
        "calcium": 12.0,
        "iron": 1.3,
        "magnesium": 13.0,
        "phospohorus": 0.094,
        "potassium": 149.0,
        "sulfate": 0.122,
        "zinc": 2.6,
        },
        nutrition_sources=[
            DataSource(
                url="https://www.yazio.com",
                title="Yazio Food Database",
                source_type="database"
            )
        ]
    )


def create_gemüsecremesuppe() -> Food:
    """
    gemüsecremesuppe
    
    Source: Yazio Food Database
    """
    return Food(
        name="gemüsecremesuppe",
        name_de="gemüsecremesuppe",
        category=None,
        nutrition_data={
        "calories": 51.0,
        "fat": 2.4,
        "saturated fat": 1.0,
        "carbohydrate": 5.6,
        "sugar": 2.0,
        "protein": 1.6,
        "salt": 0.7,
        "fiber": 1.0,
        },
        nutrition_sources=[
            DataSource(
                url="https://www.yazio.com",
                title="Yazio Food Database",
                source_type="database"
            )
        ]
    )


def create_gemüsesuppe() -> Food:
    """
    gemüsesuppe
    
    Source: Yazio Food Database
    """
    return Food(
        name="gemüsesuppe",
        name_de="gemüsesuppe",
        category=None,
        nutrition_data={
        "calories": 59.0,
        "fat": 2.9,
        "saturated fat": 1.2,
        "monounsaturated fat": 1.1,
        "polyunsaturated fat": 0.5,
        "carbohydrate": 2.4,
        "sugar": 1.1,
        "protein": 4.9,
        "salt": 0.4,
        "fiber": 1.3,
        "cholesterol": 10.0,
        "sodium": 100.0,
        "water": 87.3,
        "vitamin b3": 2.6,
        "vitamin b5": 0.3,
        "vitamin b6": 0.1,
        "vitamin c": 10.8,
        "vitamin e": 0.4,
        "calcium": 15.0,
        "iron": 0.5,
        "magnesium": 13.0,
        "phospohorus": 0.049,
        "potassium": 172.0,
        "sulfate": 0.042,
        "zinc": 0.8,
        },
        nutrition_sources=[
            DataSource(
                url="https://www.yazio.com",
                title="Yazio Food Database",
                source_type="database"
            )
        ]
    )


def create_grüne_bohnen_mit_speck() -> Food:
    """
    grüne bohnen mit speck
    
    Source: Yazio Food Database
    """
    return Food(
        name="grüne bohnen mit speck",
        name_de="grüne bohnen mit speck",
        category=None,
        nutrition_data={
        "calories": 72.0,
        "fat": 4.1,
        "saturated fat": 2.6,
        "monounsaturated fat": 3.6,
        "carbohydrate": 4.5,
        "sugar": 3.5,
        "protein": 2.4,
        "salt": 1.0,
        "fiber": 3.6,
        },
        nutrition_sources=[
            DataSource(
                url="https://www.yazio.com",
                title="Yazio Food Database",
                source_type="database"
            )
        ]
    )


def create_mettbrötchen() -> Food:
    """
    mettbrötchen
    
    Source: Yazio Food Database
    """
    return Food(
        name="mettbrötchen",
        name_de="mettbrötchen",
        category=None,
        nutrition_data={
        "calories": 266.0,
        "fat": 12.7,
        "saturated fat": 5.0,
        "monounsaturated fat": 5.6,
        "polyunsaturated fat": 1.1,
        "carbohydrate": 27.2,
        "sugar": 2.5,
        "protein": 8.4,
        "salt": 1.5,
        "fiber": 4.8,
        "cholesterol": 32.0,
        "sodium": 700.0,
        "water": 45.0,
        "vitamin b1": 0.2,
        "vitamin b12": 600.0,
        "vitamin b3": 2.1,
        "vitamin b5": 0.5,
        "vitamin b6": 0.2,
        "vitamin c": 9.7,
        "vitamin e": 0.6,
        "calcium": 20.0,
        "copper": 0.2,
        "iron": 1.6,
        "magnesium": 39.0,
        "manganese": 0.9,
        "phospohorus": 0.146,
        "potassium": 185.0,
        "sulfate": 0.09,
        "zinc": 1.7,
        },
        nutrition_sources=[
            DataSource(
                url="https://www.yazio.com",
                title="Yazio Food Database",
                source_type="database"
            )
        ]
    )


def create_mousse_au_chocolat() -> Food:
    """
    mousse au chocolat
    
    Source: Yazio Food Database
    """
    return Food(
        name="mousse au chocolat",
        name_de="mousse au chocolat",
        category=None,
        nutrition_data={
        "calories": 344.0,
        "fat": 24.5,
        "saturated fat": 14.1,
        "monounsaturated fat": 8.0,
        "polyunsaturated fat": 1.0,
        "carbohydrate": 23.3,
        "sugar": 23.0,
        "protein": 6.6,
        "salt": 0.1,
        "fiber": 3.3,
        "cholesterol": 134.0,
        "water": 40.8,
        "vitamin a": 200.0,
        "vitamin b2": 0.1,
        "vitamin b3": 2.0,
        "vitamin b5": 0.3,
        "vitamin c": 0.3,
        "vitamin e": 1.3,
        "calcium": 63.0,
        "copper": 0.6,
        "iron": 6.5,
        "magnesium": 74.0,
        "manganese": 0.6,
        "phospohorus": 0.163,
        "potassium": 531.0,
        "sulfate": 0.079,
        "zinc": 1.3,
        },
        nutrition_sources=[
            DataSource(
                url="https://www.yazio.com",
                title="Yazio Food Database",
                source_type="database"
            )
        ]
    )


def create_erdbeer_kuchen() -> Food:
    """
    erdbeer kuchen
    
    Source: Yazio Food Database
    """
    return Food(
        name="erdbeer kuchen",
        name_de="erdbeer kuchen",
        category=None,
        nutrition_data={
        "calories": 138.0,
        "fat": 3.0,
        "saturated fat": 0.7,
        "monounsaturated fat": 1.5,
        "polyunsaturated fat": 0.6,
        "carbohydrate": 23.5,
        "sugar": 14.8,
        "protein": 3.0,
        "fiber": 1.3,
        "cholesterol": 30.0,
        "water": 68.3,
        "vitamin b3": 0.9,
        "vitamin b5": 0.3,
        "vitamin c": 16.3,
        "vitamin e": 1.0,
        "calcium": 38.0,
        "iron": 0.6,
        "magnesium": 15.0,
        "manganese": 0.3,
        "phospohorus": 0.074,
        "potassium": 118.0,
        "sulfate": 0.033,
        "zinc": 0.4,
        },
        nutrition_sources=[
            DataSource(
                url="https://www.yazio.com",
                title="Yazio Food Database",
                source_type="database"
            )
        ]
    )


__all__ = [
    "create_linsensuppe",
    "create_rinderrouladen_mit_soße",
    "create_gemüsecremesuppe",
    "create_gemüsesuppe",
    "create_grüne_bohnen_mit_speck",
    "create_mettbrötchen",
    "create_mousse_au_chocolat",
    "create_erdbeer_kuchen",
]
