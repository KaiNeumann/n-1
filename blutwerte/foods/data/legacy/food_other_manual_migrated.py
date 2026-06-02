"""
Migrated from food_other_manual.py

Source: USDA FoodData Central & Various Sources
URL: https://fdc.nal.usda.gov
"""

from blutwerte.foods import Food, DataSource


def create_wasser() -> Food:
    """
    wasser
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="wasser",
        name_de="wasser",
        category=None,
        nutrition_data={
        "water": 100,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_kaffee() -> Food:
    """
    kaffee
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="kaffee",
        name_de="kaffee",
        category=None,
        nutrition_data={
        "calories": 2,
        "carbohydrates": 0.3,
        "protein": 0.2,
        "water": 99.4,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_altenmünster_landbier() -> Food:
    """
    altenmünster landbier
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="altenmünster landbier",
        name_de="altenmünster landbier",
        category=None,
        nutrition_data={
        "calories": 43,
        "carbohydrates": 2.9,
        "sugar": 0.5,
        "protein": 0.5,
        "fat": 0.5,
        "saturated fat": 0.1,
        "water": 97,
        "alcohol": 4.9,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_schmucker_bio_bier_alkoholfrei() -> Food:
    """
    schmucker bio bier alkoholfrei
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="schmucker bio bier alkoholfrei",
        name_de="schmucker bio bier alkoholfrei",
        category=None,
        nutrition_data={
        "calories": 12,
        "carbohydrates": 2.3,
        "sugar": 0.5,
        "protein": 0.5,
        "water": 97,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_schmucker_bio_landbier() -> Food:
    """
    schmucker bio landbier
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="schmucker bio landbier",
        name_de="schmucker bio landbier",
        category=None,
        nutrition_data={
        "carbohydrate": 3.2,
        "calories": 42,
        "protein": 0.5,
        "sugar": 0.5,
        "alcohol": 5,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_dennree_bio_hartweizen_linguine() -> Food:
    """
    https://www.dennree.de/dennree-produkte/uebersicht/hartweizen-vollkorn/vollkorn-hartweizen-linguine
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="https://www.dennree.de/dennree-produkte/uebersicht/hartweizen-vollkorn/vollkorn-hartweizen-linguine",
        name_de="https://www.dennree.de/dennree-produkte/uebersicht/hartweizen-vollkorn/vollkorn-hartweizen-linguine",
        category=None,
        nutrition_data={
        "carbohydrate": 62,
        "calories": 335,
        "fat": 2.1,
        "protein": 12.5,
        "salt": 0.01,
        "saturated fat": 0.4,
        "sugar": 3,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_kulturchampignion_braun() -> Food:
    """
    kulturchampignion braun
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="kulturchampignion braun",
        name_de="kulturchampignion braun",
        category=None,
        nutrition_data={
        "calories": 26,
        "fat": 0.3,
        "carbohydrates": 2.7,
        "sugar": 2.3,
        "protein": 1.9,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_baguette() -> Food:
    """
    https://fddb.info/db/de/lebensmittel/baecker_baguette/index.html
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="https://fddb.info/db/de/lebensmittel/baecker_baguette/index.html",
        name_de="https://fddb.info/db/de/lebensmittel/baecker_baguette/index.html",
        category=None,
        nutrition_data={
        "calories": 242.0,
        "protein": 7.9,
        "carbohydrate": 55.4,
        "sugar": 1.0,
        "fat": 0.7,
        "fiber": 3.2,
        "water": 30.0,
        "vitamin e": 0.3,
        "vitamin b1": 0.06,
        "vitamin b2": 0.05,
        "vitamin b6": 0.09,
        "salt": 1.3716,
        "iron": 1.2,
        "zinc": 0.7,
        "magnesium": 19.0,
        "manganese": 0.6,
        "potassium": 130.0,
        "calcium": 18.0,
        "phospohorus": 0.105,
        "copper": 0.2,
        "iodine": 7.0,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_baguettebrötchen() -> Food:
    """
    baguettebrötchen
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="baguettebrötchen",
        name_de="baguettebrötchen",
        category=None,
        nutrition_data={
        "calories": 305,
        "fat": 1.8,
        "carbohydrates": 60.2,
        "sugar": 1.1,
        "protein": 9.7,
        "fiber": 3.5,
        "salt": 1.7,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_bio_hackfleisch() -> Food:
    """
    bio hackfleisch
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="bio hackfleisch",
        name_de="bio hackfleisch",
        category=None,
        nutrition_data={
        "calories": 243,
        "fat": 19,
        "saturated_fatty_acids": 6.4,
        "protein": 18,
        "salt": 0.1,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_bio_inside_ratatouille_mix() -> Food:
    """
    bio inside ratatouille mix
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="bio inside ratatouille mix",
        name_de="bio inside ratatouille mix",
        category=None,
        nutrition_data={
        "calories": 26.0,
        "protein": 1.3,
        "carbohydrate": 3.2,
        "fat": 0.4,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_bratwurst_mit_senf_und_brötchen() -> Food:
    """
    https://fddb.info/db/de/lebensmittel/imbiss_bratwurst_mit_senf_und_broetchen/index.html
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="https://fddb.info/db/de/lebensmittel/imbiss_bratwurst_mit_senf_und_broetchen/index.html",
        name_de="https://fddb.info/db/de/lebensmittel/imbiss_bratwurst_mit_senf_und_broetchen/index.html",
        category=None,
        nutrition_data={
        "calories": 250,
        "fat": 18.2,
        "carbohydrates": 9.2,
        "sugar": 0.2,
        "protein": 12.6,
        "fiber": 0.5,
        "water": 41,
        "salt": 0.365,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_calvados() -> Food:
    """
    calvados
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="calvados",
        name_de="calvados",
        category=None,
        nutrition_data={
        "calories": 248,
        "alcohol": 32,
        "water": 68,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_hähnchenbrustfilet() -> Food:
    """
    hähnchenbrustfilet
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="hähnchenbrustfilet",
        name_de="hähnchenbrustfilet",
        category=None,
        nutrition_data={
        "calories": 107,
        "protein": 23,
        "carbohydrate": 0.5,
        "fat": 1.7,
        "salt": 0.13,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_honig() -> Food:
    """
    honig
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="honig",
        name_de="honig",
        category=None,
        nutrition_data={
        "calories": 306.0,
        "carbohydrates": 76.0,
        "sugar": 76.0,
        "protein": 0.4,
        "water": 20.0,
        "vitamin b2": 0.05,
        "vitamin b6": 0.3,
        "vitamin b3": 0.2,
        "provitamin_b5": 0.0001,
        "vitamin c": 1.7,
        "potassium": 47.0,
        "sodium": 7.0,
        "chloride": 0.018,
        "calcium": 5.0,
        "magnesium": 3.0,
        "phosphorus": 17.0,
        "iron": 0.5,
        "iodine": 0.5,
        "zinc": 0.4,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_cholula_hot_sauce() -> Food:
    """
    water estimated. https://www.scovilla.com/de/hot-sauces/111/cholula-hot-sauce-mexico-148ml
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="water estimated. https://www.scovilla.com/de/hot-sauces/111/cholula-hot-sauce-mexico-148ml",
        name_de="water estimated. https://www.scovilla.com/de/hot-sauces/111/cholula-hot-sauce-mexico-148ml",
        category=None,
        nutrition_data={
        "kcal": 19,
        "fat": 1,
        "protein": 1,
        "salt": 5,
        "water": 90,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_creme_fraiche() -> Food:
    """
    creme fraiche
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="creme fraiche",
        name_de="creme fraiche",
        category=None,
        nutrition_data={
        "calories": 294,
        "protein": 2.4,
        "carbohydrate": 3,
        "sugar": 3,
        "fat": 30,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_tabasco_habanero() -> Food:
    """
    https://shop.rewe.de/p/tabasco-habanero-60ml/2235797?source=mc
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="https://shop.rewe.de/p/tabasco-habanero-60ml/2235797?source=mc",
        name_de="https://shop.rewe.de/p/tabasco-habanero-60ml/2235797?source=mc",
        category=None,
        nutrition_data={
        "kcal": 121,
        "carbohydrate": 21,
        "sugar": 21,
        "protein": 1.5,
        "salt": 6.1,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_landprimus_pfefferbeisser() -> Food:
    """
    https://www.tegut.com/angebote-produkte/produkte/eigenmarken/produkt/pfefferbeisser.html
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="https://www.tegut.com/angebote-produkte/produkte/eigenmarken/produkt/pfefferbeisser.html",
        name_de="https://www.tegut.com/angebote-produkte/produkte/eigenmarken/produkt/pfefferbeisser.html",
        category=None,
        nutrition_data={
        "calories": 300,
        "fat": 25,
        "saturated_fatty_acids": 10,
        "carbohydrates": 0.5,
        "sugar": 0.5,
        "protein": 19,
        "salt": 2.1,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )

def create_ökostern_bio_dijon_senf() -> Food:
    """
    ökostern bio dijon senf
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="ökostern bio dijon senf",
        name_de="ökostern bio dijon senf",
        category=None,
        nutrition_data={
        "calories": 220,
        "fat": 13.3,
        "saturated_fatty_acids": 0.4,
        "carbohydrates": 8.9,
        "sugar": 1,
        "protein": 14.6,
        "salt": 7.1,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_walnüsse() -> Food:
    """
    walnüsse
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="walnüsse",
        name_de="walnüsse",
        category=None,
        nutrition_data={
        "calories": 687,
        "fat": 63.8,
        "carbohydrates": 10.5,
        "sugar": 3.4,
        "protein": 14.5,
        "fiber": 6.4,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_schnitzel() -> Food:
    """
    schnitzel
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="schnitzel",
        name_de="schnitzel",
        category=None,
        nutrition_data={
        "protein": 21.5547,
        "fat": 14.6839,
        "carbohydrate": 6.9475,
        "calories": 251.5474,
        "starch": 5.6529,
        "glucose": 0.2159,
        "fructose": 0.2332,
        "maltose": 0.1819,
        "water": 55.2782,
        "sugar": 0.6312,
        "fiber": 0.4434,
        "calcium": 41904.3141,
        "iron": 1251.4037,
        "magnesium": 23961.9596,
        "potassium": 288343.8611,
        "sodium": 264291.5029,
        "zinc": 1861.501,
        "copper": 90.8666,
        "manganese": 105.8862,
        "selenium": 38011791.1286,
        "vitamin a": 20185523.1144,
        "beta carotene": 0.2085,
        "alpha carotene": 0.0081,
        "vitamin e": 667.0878,
        "vitamin d": 31630544.6378,
        "vitamin d3": 0.8216,
        "vitamin b1": 536.4028,
        "vitamin b2": 263.6627,
        "vitamin b3": 6623.0114,
        "vitamin b5": 715.9367,
        "vitamin b6": 523.0208,
        "vitamin b12": 570699.9813,
        "vitamin k": 10536.4964,
        "vitamin b9": 7769.6051,
        "glutamate": 3.5911,
        "cholesterol": 105223.0021,
        "trans fat": 0.2104,
        "saturated fat": 3.4321,
        "monounsaturated fat": 4.7488,
        "polyunsaturated fat": 4.637,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_zigeuner_schnitzel() -> Food:
    """
    zigeuner schnitzel
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="zigeuner schnitzel",
        name_de="zigeuner schnitzel",
        category=None,
        nutrition_data={
        "carbohydrate": 16.2,
        "calories": 165,
        "fat": 2.2,
        "fiber": 4.1,
        "protein": 18,
        "salt": 1.5,
        "saturated fat": 0.3,
        "sodium": 600.0,
        "sugar": 1.3,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_haselnusskerne_gehackt() -> Food:
    """
    haselnusskerne gehackt
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="haselnusskerne gehackt",
        name_de="haselnusskerne gehackt",
        category=None,
        nutrition_data={
        "carbohydrate": 5.4,
        "calories": 695,
        "sugar": 5.4,
        "fat": 67,
        "fiber": 8.2,
        "protein": 15,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_leicht_und_cross_goldweizen() -> Food:
    """
    leicht und cross goldweizen
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="leicht und cross goldweizen",
        name_de="leicht und cross goldweizen",
        category=None,
        nutrition_data={
        "carbohydrate": 73,
        "calories": 391,
        "fat": 4,
        "fiber": 5.4,
        "protein": 13,
        "saturated fat": 0.5,
        "salt": 1.2,
        "sugar": 3.5,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_palatum_grüne_oliven_mit_frischkäse_creme() -> Food:
    """
    palatum grüne oliven mit frischkäse creme
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="palatum grüne oliven mit frischkäse creme",
        name_de="palatum grüne oliven mit frischkäse creme",
        category=None,
        nutrition_data={
        "carbohydrate": 4,
        "calories": 217,
        "fat": 19.4,
        "fiber": 1.9,
        "protein": 4.6,
        "saturated fat": 5.2,
        "salt": 2.1,
        "sugar": 0.4,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_palatum_naturschwarze_kalamata_oliven() -> Food:
    """
    palatum naturschwarze kalamata oliven
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="palatum naturschwarze kalamata oliven",
        name_de="palatum naturschwarze kalamata oliven",
        category=None,
        nutrition_data={
        "carbohydrate": 1.1,
        "calories": 224,
        "fat": 22.5,
        "fiber": 6.4,
        "protein": 1.1,
        "salt": 1.94,
        "saturated fat": 2.5,
        "sodium": 776.0,
        "sugar": 0.1,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_spinat_dinkel_pfannkuchen() -> Food:
    """
    spinat dinkel pfannkuchen
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="spinat dinkel pfannkuchen",
        name_de="spinat dinkel pfannkuchen",
        category=None,
        nutrition_data={
        "calories": 123,
        "protein": 12.5,
        "carbohydrate": 12.7,
        "fat": 2.4,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_omni_biotic_10() -> Food:
    """
    omni biotic 10
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="omni biotic 10",
        name_de="omni biotic 10",
        category=None,
        nutrition_data={
        "kcal": 371,
        "fat": 0.1,
        "unsaturated fat": 0.02,
        "carbohydrate": 90.4,
        "sugar": 3.78,
        "proteine": 2.2,
        "salt": 0.66,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_cheeseburger() -> Food:
    """
    cheeseburger
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="cheeseburger",
        name_de="cheeseburger",
        category=None,
        nutrition_data={
        "kcal": 261,
        "fat": 11,
        "carbohydrate": 27,
        "sugar": 4.3,
        "proteine": 12,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


def create_börek_mit_käse() -> Food:
    """
    börek mit käse
    
    Source: USDA FoodData Central & Various Sources
    """
    return Food(
        name="börek mit käse",
        name_de="börek mit käse",
        category=None,
        nutrition_data={
        "kcal": 300,
        "fat": 13,
        "carbohydrate": 39,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov",
                title="USDA FoodData Central & Various Sources",
                source_type="database"
            )
        ]
    )


__all__ = [
    "create_wasser",
    "create_kaffee",
    "create_altenmünster_landbier",
    "create_schmucker_bio_bier_alkoholfrei",
    "create_schmucker_bio_landbier",
    "create_dennree_bio_hartweizen_linguine",
    "create_kulturchampignion_braun",
    "create_baguette",
    "create_baguettebrötchen",
    "create_bio_hackfleisch",
    "create_bio_inside_ratatouille_mix",
    "create_bratwurst_mit_senf_und_brötchen",
    "create_calvados",
    "create_hähnchenbrustfilet",
    "create_honig",
    "create_cholula_hot_sauce",
    "create_creme_fraiche",
    "create_tabasco_habanero",
    "create_landprimus_pfefferbeisser",
    "create_ökostern_bio_dijon_senf",
    "create_walnüsse",
    "create_schnitzel",
    "create_zigeuner_schnitzel",
    "create_haselnusskerne_gehackt",
    "create_leicht_und_cross_goldweizen",
    "create_palatum_grüne_oliven_mit_frischkäse_creme",
    "create_palatum_naturschwarze_kalamata_oliven",
    "create_spinat_dinkel_pfannkuchen",
    "create_omni_biotic_10",
    "create_cheeseburger",
    "create_börek_mit_käse",
]
