"""
Migrated from food_openfoodfacts_manual.py

Source: Open Food Facts Database
URL: https://world.openfoodfacts.org
"""

from blutwerte.foods import Food, DataSource


def create_altenmünster_landbier() -> Food:
    """
    altenmünster landbier
    
    Source: Open Food Facts Database
    """
    return Food(
        name="altenmünster landbier",
        name_de="altenmünster landbier",
        category=None,
        nutrition_data={
        "alcohol": 4.9,
        "carbohydrate": 2.9,
        "calories": 44,
        "fat": 0.5,
        "protein": 0.5,
        "salt": 0.01,
        "saturated fat": 0.1,
        "sugar": 0.5,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_becks_pils() -> Food:
    """
    becks pils
    
    Source: Open Food Facts Database
    """
    return Food(
        name="becks pils",
        name_de="becks pils",
        category=None,
        nutrition_data={
        "alcohol": 4.9,
        "carbohydrate": 2.2,
        "calories": 38,
        "fat": 0.01,
        "protein": 0.37,
        "salt": 0.01,
        "saturated fat": 0.01,
        "sodium": 4.0,
        "sugar": 0.1,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_flensburger_gold() -> Food:
    """
    flensburger gold
    
    Source: Open Food Facts Database
    """
    return Food(
        name="flensburger gold",
        name_de="flensburger gold",
        category=None,
        nutrition_data={
        "alcohol": 4.8,
        "carbohydrate": 2.3,
        "calories": 40,
        "salt": 0.01,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_kilkenny_irish_beer() -> Food:
    """
    kilkenny irish beer
    
    Source: Open Food Facts Database
    """
    return Food(
        name="kilkenny irish beer",
        name_de="kilkenny irish beer",
        category=None,
        nutrition_data={
        "alcohol": 4.3,
        "carbohydrate": 3,
        "protein": 0.3,
        "salt": 0.01,
        "sodium": 4.0,
        "sugar": 0.4,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_krombacher_alkoholfrei() -> Food:
    """
    krombacher alkoholfrei
    
    Source: Open Food Facts Database
    """
    return Food(
        name="krombacher alkoholfrei",
        name_de="krombacher alkoholfrei",
        category=None,
        nutrition_data={
        "water": 99.5,
        "calories": 26,
        "carbohydrates": 5.7,
        "sugar": 2.8,
        "alcohol": 0.5,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_krombacher_pils() -> Food:
    """
    krombacher pils
    
    Source: Open Food Facts Database
    """
    return Food(
        name="krombacher pils",
        name_de="krombacher pils",
        category=None,
        nutrition_data={
        "water": 99.5,
        "alcohol": 4.8,
        "carbohydrate": 2.4,
        "calories": 38,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_aioli_jalapeno() -> Food:
    """
    aioli jalapeno
    
    Source: Open Food Facts Database
    """
    return Food(
        name="aioli jalapeno",
        name_de="aioli jalapeno",
        category=None,
        nutrition_data={
        "carbohydrate": 9.9,
        "calories": 284,
        "fat": 25.9,
        "protein": 2.7,
        "salt": 1.02,
        "saturated_fatty_acids": 5,
        "sodium": 408.0,
        "sugar": 6.4,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_amber_mist_mature_cheddar_with_whisky() -> Food:
    """
    what about the 5% whisky?
    
    Source: Open Food Facts Database
    """
    return Food(
        name="what about the 5% whisky?",
        name_de="what about the 5% whisky?",
        category=None,
        nutrition_data={
        "carbohydrate": 4.8,
        "calories": 398,
        "fat": 32.4,
        "protein": 21.7,
        "salt": 1.6,
        "saturated fat": 21.3,
        "sodium": 640.0,
        "sugar": 3.1,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_andechser_bio_rahmjoghurt_vanille() -> Food:
    """
    andechser bio rahmjoghurt vanille
    
    Source: Open Food Facts Database
    """
    return Food(
        name="andechser bio rahmjoghurt vanille",
        name_de="andechser bio rahmjoghurt vanille",
        category=None,
        nutrition_data={
        "carbohydrate": 11.6,
        "calories": 135,
        "fat": 8.6,
        "protein": 2.7,
        "saturated fat": 5.9,
        "sugar": 11.6,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_andechser_bio_rahmjoghurt_heidelbeere() -> Food:
    """
    andechser bio rahmjoghurt heidelbeere
    
    Source: Open Food Facts Database
    """
    return Food(
        name="andechser bio rahmjoghurt heidelbeere",
        name_de="andechser bio rahmjoghurt heidelbeere",
        category=None,
        nutrition_data={
        "carbohydrate": 11.6,
        "calories": 128,
        "fat": 7.8,
        "protein": 2.5,
        "salt": 0.09,
        "saturated fat": 5.3,
        "sugar": 11,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_baguette_kräuterbutter() -> Food:
    """
    baguette kräuterbutter
    
    Source: Open Food Facts Database
    """
    return Food(
        name="baguette kräuterbutter",
        name_de="baguette kräuterbutter",
        category=None,
        nutrition_data={
        "carbohydrate": 40,
        "calories": 283,
        "fat": 10,
        "protein": 7.2,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_bayerischer_meerrettich_alpensahne() -> Food:
    """
    bayerischer meerrettich alpensahne
    
    Source: Open Food Facts Database
    """
    return Food(
        name="bayerischer meerrettich alpensahne",
        name_de="bayerischer meerrettich alpensahne",
        category=None,
        nutrition_data={
        "carbohydrate": 10,
        "calories": 320,
        "fat": 29,
        "fiber": 2.3,
        "protein": 2.4,
        "salt": 0.51,
        "saturated fat": 3.7,
        "sodium": 204.0,
        "sugar": 8,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_bio_feta() -> Food:
    """
    bio feta
    
    Source: Open Food Facts Database
    """
    return Food(
        name="bio feta",
        name_de="bio feta",
        category=None,
        nutrition_data={
        "carbohydrate": 0.7,
        "calories": 276,
        "fat": 23,
        "protein": 16.5,
        "salt": 2.3,
        "saturated fat": 17,
        "sodium": 920.0,
        "sugar": 0.7,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_bio_geschabte_spätzle() -> Food:
    """
    bio geschabte spätzle
    
    Source: Open Food Facts Database
    """
    return Food(
        name="bio geschabte spätzle",
        name_de="bio geschabte spätzle",
        category=None,
        nutrition_data={
        "carbohydrate": 70,
        "calories": 366,
        "fat": 2.6,
        "protein": 14,
        "salt": 0.02,
        "saturated fat": 0.7,
        "sodium": 8.0,
        "sugar": 3,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_bio_streichcreme_paprika_aubergine_zucchini_und_tomate() -> Food:
    """
    bio streichcreme paprika aubergine zucchini und tomate
    
    Source: Open Food Facts Database
    """
    return Food(
        name="bio streichcreme paprika aubergine zucchini und tomate",
        name_de="bio streichcreme paprika aubergine zucchini und tomate",
        category=None,
        nutrition_data={
        "carbohydrate": 7.4,
        "calories": 357,
        "fat": 33.7,
        "protein": 5.2,
        "salt": 1.1,
        "saturated fat": 3.6,
        "sodium": 440.0,
        "sugar": 3.8,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_bio_vollkorn_sandwich() -> Food:
    """
    bio vollkorn sandwich
    
    Source: Open Food Facts Database
    """
    return Food(
        name="bio vollkorn sandwich",
        name_de="bio vollkorn sandwich",
        category=None,
        nutrition_data={
        "carbohydrate": 46.4,
        "calories": 266,
        "fat": 3.7,
        "fiber": 6.4,
        "protein": 8.5,
        "salt": 1.1,
        "saturated fat": 0.4,
        "sodium": 440.0,
        "sugar": 3.9,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_biofix_chicken_kashmir_gewürz() -> Food:
    """
    biofix chicken kashmir gewürz
    
    Source: Open Food Facts Database
    """
    return Food(
        name="biofix chicken kashmir gewürz",
        name_de="biofix chicken kashmir gewürz",
        category=None,
        nutrition_data={
        "carbohydrate": 44.6,
        "calories": 258,
        "fat": 3.7,
        "fiber": 6.1,
        "protein": 7.7,
        "salt": 25,
        "saturated fat": 0.9,
        "sodium": 10000,
        "sugar": 17.9,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_caffe_crema_kaffeepads() -> Food:
    """
    TODO coffein?
    
    Source: Open Food Facts Database
    """
    return Food(
        name="TODO coffein?",
        name_de="TODO coffein?",
        category=None,
        nutrition_data={
        
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_dextro_energy_classic() -> Food:
    """
    dextro energy classic
    
    Source: Open Food Facts Database
    """
    return Food(
        name="dextro energy classic",
        name_de="dextro energy classic",
        category=None,
        nutrition_data={
        "carbohydrate": 91,
        "calories": 368,
        "fat": 1,
        "salt": 0.1,
        "saturated fat": 1,
        "sodium": 40.0,
        "sugar": 82,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_erdnussbutter_peanut_butter_creamy() -> Food:
    """
    erdnussbutter peanut butter creamy
    
    Source: Open Food Facts Database
    """
    return Food(
        name="erdnussbutter peanut butter creamy",
        name_de="erdnussbutter peanut butter creamy",
        category=None,
        nutrition_data={
        "carbohydrate": 18.9,
        "calories": 603,
        "fat": 46.9,
        "fiber": 6.2,
        "protein": 26.2,
        "salt": 0.8,
        "saturated fat": 7.9,
        "sodium": 320.0,
        "sugar": 9.5,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_feta_griechisch() -> Food:
    """
    feta griechisch
    
    Source: Open Food Facts Database
    """
    return Food(
        name="feta griechisch",
        name_de="feta griechisch",
        category=None,
        nutrition_data={
        "carbohydrate": 0.7,
        "calories": 276,
        "fat": 23,
        "protein": 17,
        "salt": 2.2,
        "saturated fat": 17,
        "sodium": 880.0,
        "sugar": 0.7,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_finesse_schinkenaufschnitt_mit_belém_pfeffer() -> Food:
    """
    finesse schinkenaufschnitt mit belém pfeffer
    
    Source: Open Food Facts Database
    """
    return Food(
        name="finesse schinkenaufschnitt mit belém pfeffer",
        name_de="finesse schinkenaufschnitt mit belém pfeffer",
        category=None,
        nutrition_data={
        "carbohydrate": 1,
        "calories": 112,
        "fat": 3,
        "fiber": 0.5,
        "protein": 20,
        "salt": 2.6,
        "saturated fat": 0.9,
        "sodium": 1040.0,
        "sugar": 1,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_gemüse_brotaufstrich_kirschtomate_rucola() -> Food:
    """
    gemüse brotaufstrich kirschtomate rucola
    
    Source: Open Food Facts Database
    """
    return Food(
        name="gemüse brotaufstrich kirschtomate rucola",
        name_de="gemüse brotaufstrich kirschtomate rucola",
        category=None,
        nutrition_data={
        "carbohydrate": 10,
        "calories": 207,
        "fat": 16,
        "fiber": 2.5,
        "protein": 4.4,
        "salt": 1.5,
        "saturated_fatty_acids": 1.8,
        "sodium": 600.0,
        "sugar": 5.3,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_gewürz_ketchup_curry_delikat() -> Food:
    """
    gewürz ketchup curry delikat
    
    Source: Open Food Facts Database
    """
    return Food(
        name="gewürz ketchup curry delikat",
        name_de="gewürz ketchup curry delikat",
        category=None,
        nutrition_data={
        "carbohydrate": 30.6,
        "calories": 135,
        "fat": 0.3,
        "protein": 0.8,
        "salt": 2.2,
        "saturated fat": 0.1,
        "sodium": 880.0,
        "sugar": 29.2,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_golden_toast() -> Food:
    """
    golden toast
    
    Source: Open Food Facts Database
    """
    return Food(
        name="golden toast",
        name_de="golden toast",
        category=None,
        nutrition_data={
        "calories": 265,
        "protein": 8.2,
        "carbohydrates": 48,
        "sugar": 4,
        "fat": 3.8,
        "unsaturated_fatty_acids": 2,
        "salt": 1.1,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_haferflocken() -> Food:
    """
    haferflocken
    
    Source: Open Food Facts Database
    """
    return Food(
        name="haferflocken",
        name_de="haferflocken",
        category=None,
        nutrition_data={
        "calories": 372,
        "protein": 13.5,
        "carbohydrates": 58.7,
        "sugar": 0.7,
        "fat": 7,
        "unsaturated_fatty_acids": 5.7,
        "salt": 0.02,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_handkäse_kümmel() -> Food:
    """
    handkäse kümmel
    
    Source: Open Food Facts Database
    """
    return Food(
        name="handkäse kümmel",
        name_de="handkäse kümmel",
        category=None,
        nutrition_data={
        "calcium": 200.0,
        "carbohydrate": 0.09,
        "calories": 125,
        "fat": 0.5,
        "protein": 30,
        "salt": 4,
        "saturated fat": 0.2,
        "sodium": 1600.0,
        "sugar": 0.09,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_iglo_brokkoli_buchweizen() -> Food:
    """
    iglo brokkoli buchweizen
    
    Source: Open Food Facts Database
    """
    return Food(
        name="iglo brokkoli buchweizen",
        name_de="iglo brokkoli buchweizen",
        category=None,
        nutrition_data={
        "carbohydrate": 13,
        "calories": 92,
        "fat": 2.3,
        "fiber": 3.6,
        "protein": 2.9,
        "salt": 0.73,
        "saturated_fatty_acids": 0.3,
        "sodium": 292.0,
        "sugar": 2.3,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_indische_curry_sauce() -> Food:
    """
    indische curry sauce
    
    Source: Open Food Facts Database
    """
    return Food(
        name="indische curry sauce",
        name_de="indische curry sauce",
        category=None,
        nutrition_data={
        "carbohydrate": 8.3,
        "calories": 95,
        "fat": 5.5,
        "fiber": 2.6,
        "protein": 1.6,
        "salt": 1.4,
        "saturated fat": 3.6,
        "sodium": 560.0,
        "sugar": 5.3,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_jägersauce_feinkörnig() -> Food:
    """
    jägersauce feinkörnig
    
    Source: Open Food Facts Database
    """
    return Food(
        name="jägersauce feinkörnig",
        name_de="jägersauce feinkörnig",
        category=None,
        nutrition_data={
        "carbohydrate": 4.7,
        "calories": 27,
        "fat": 0.2,
        "protein": 1.3,
        "salt": 1.2,
        "sodium": 480.0,
        "sugar": 1.7,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_joghurt_griechische_art() -> Food:
    """
    joghurt griechische art
    
    Source: Open Food Facts Database
    """
    return Food(
        name="joghurt griechische art",
        name_de="joghurt griechische art",
        category=None,
        nutrition_data={
        "carbohydrate": 4,
        "calories": 114,
        "fat": 9.4,
        "fiber": 0.13,
        "protein": 3.3,
        "salt": 0.1,
        "saturated fat": 5.8,
        "sodium": 40.0,
        "sugar": 4,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_k_classic_knuspriger_apfelstrudel() -> Food:
    """
    k classic knuspriger apfelstrudel
    
    Source: Open Food Facts Database
    """
    return Food(
        name="k classic knuspriger apfelstrudel",
        name_de="k classic knuspriger apfelstrudel",
        category=None,
        nutrition_data={
        "carbohydrate": 29,
        "calories": 258,
        "fat": 13,
        "protein": 2.5,
        "salt": 0.24,
        "saturated fat": 6.8,
        "sodium": 96.0,
        "sugar": 13,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_kaufland_bio_vollkorn_spaghetti() -> Food:
    """
    kaufland bio vollkorn spaghetti
    
    Source: Open Food Facts Database
    """
    return Food(
        name="kaufland bio vollkorn spaghetti",
        name_de="kaufland bio vollkorn spaghetti",
        category=None,
        nutrition_data={
        "carbohydrate": 67,
        "calories": 350,
        "fat": 2.2,
        "fiber": 7,
        "protein": 12,
        "salt": 0.01,
        "saturated_fatty_acids": 0.4,
        "sodium": 4.0,
        "sugar": 3.2,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )

def create_kaufland_langkorn_wildreis_mischung() -> Food:
    """
    kaufland langkorn wildreis mischung
    
    Source: Open Food Facts Database
    """
    return Food(
        name="kaufland langkorn wildreis mischung",
        name_de="kaufland langkorn wildreis mischung",
        category=None,
        nutrition_data={
        "carbohydrate": 78.4,
        "calories": 358,
        "fat": 0.96,
        "fiber": 1.44,
        "protein": 8.16,
        "salt": 0.016,
        "saturated fat": 0.48,
        "sodium": 6.4,
        "sugar": 0.8,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_knoblauch_baguette() -> Food:
    """
    knoblauch baguette
    
    Source: Open Food Facts Database
    """
    return Food(
        name="knoblauch baguette",
        name_de="knoblauch baguette",
        category=None,
        nutrition_data={
        "carbohydrate": 38,
        "calories": 305,
        "fat": 13,
        "protein": 7.8,
        "salt": 1.5,
        "saturated fat": 9.5,
        "sodium": 600.0,
        "sugar": 2.2,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_knorr_asia_noodles_huhn_geschmack() -> Food:
    """
    knorr asia noodles huhn geschmack
    
    Source: Open Food Facts Database
    """
    return Food(
        name="knorr asia noodles huhn geschmack",
        name_de="knorr asia noodles huhn geschmack",
        category=None,
        nutrition_data={
        "carbohydrate": 12,
        "calories": 94,
        "fat": 4.3,
        "fiber": 0.5,
        "protein": 1.6,
        "salt": 0.78,
        "saturated fat": 2.1,
        "sodium": 312.0,
        "sugar": 0.5,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_kochhinterschinken() -> Food:
    """
    kochhinterschinken
    
    Source: Open Food Facts Database
    """
    return Food(
        name="kochhinterschinken",
        name_de="kochhinterschinken",
        category=None,
        nutrition_data={
        "carbohydrate": 0.5,
        "calories": 108,
        "fat": 3,
        "protein": 19.5,
        "salt": 2.5,
        "saturated fat": 1.2,
        "sodium": 1000,
        "sugar": 0.5,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_kochschinken_hauchfein() -> Food:
    """
    kochschinken hauchfein
    
    Source: Open Food Facts Database
    """
    return Food(
        name="kochschinken hauchfein",
        name_de="kochschinken hauchfein",
        category=None,
        nutrition_data={
        "carbohydrate": 1,
        "calories": 109,
        "fat": 3,
        "protein": 19.5,
        "salt": 2.3,
        "saturated_fatty_acids": 1,
        "sodium": 920.0,
        "sugar": 1,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_kokos_zwieback() -> Food:
    """
    kokos zwieback
    
    Source: Open Food Facts Database
    """
    return Food(
        name="kokos zwieback",
        name_de="kokos zwieback",
        category=None,
        nutrition_data={
        "calories": 462,
        "protein": 7.5,
        "carbohydrates": 70,
        "sugar": 40,
        "fat": 16,
        "unsaturated_fatty_acids": 3,
        "salt": 0.4,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_lachsfilets_naturbelassen() -> Food:
    """
    lachsfilets naturbelassen
    
    Source: Open Food Facts Database
    """
    return Food(
        name="lachsfilets naturbelassen",
        name_de="lachsfilets naturbelassen",
        category=None,
        nutrition_data={
        "carbohydrate": 0.4,
        "calories": 178,
        "fat": 12,
        "protein": 18,
        "salt": 0.15,
        "saturated fat": 2.5,
        "sodium": 60.0,
        "sugar": 0.4,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_laugenkranz() -> Food:
    """
    laugenkranz
    
    Source: Open Food Facts Database
    """
    return Food(
        name="laugenkranz",
        name_de="laugenkranz",
        category=None,
        nutrition_data={
        "carbohydrate": 47,
        "calories": 287,
        "fat": 7.19,
        "protein": 7.6,
        "salt": 1.38,
        "saturated fat": 0.8,
        "sodium": 552.0,
        "sugar": 1.8,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_naturals_meersalz_und_pfeffer() -> Food:
    """
    naturals meersalz und pfeffer
    
    Source: Open Food Facts Database
    """
    return Food(
        name="naturals meersalz und pfeffer",
        name_de="naturals meersalz und pfeffer",
        category=None,
        nutrition_data={
        "carbohydrate": 54,
        "calories": 517,
        "fat": 30,
        "fiber": 3.6,
        "protein": 5.9,
        "salt": 2,
        "saturated fat": 2.5,
        "sodium": 800.0,
        "sugar": 2.1,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_nutella() -> Food:
    """
    nutella
    
    Source: Open Food Facts Database
    """
    return Food(
        name="nutella",
        name_de="nutella",
        category=None,
        nutrition_data={
        "calories": 539,
        "fat": 30.9,
        "unsaturated_fatty_acids": 11,
        "carbohydrates": 57.5,
        "sugar": 55.9,
        "protein": 6.3,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_ökoland_wok_gemüse_pfanne() -> Food:
    """
    ökoland wok gemüse pfanne
    
    Source: Open Food Facts Database
    """
    return Food(
        name="ökoland wok gemüse pfanne",
        name_de="ökoland wok gemüse pfanne",
        category=None,
        nutrition_data={
        "carbohydrate": 6.6,
        "fat": 5,
        "fiber": 2.2,
        "protein": 1.5,
        "salt": 0.86,
        "saturated fat": 1.5,
        "sodium": 344.0,
        "sugar": 5,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_paradiso_bio_tagliatelle() -> Food:
    """
    paradiso bio tagliatelle
    
    Source: Open Food Facts Database
    """
    return Food(
        name="paradiso bio tagliatelle",
        name_de="paradiso bio tagliatelle",
        category=None,
        nutrition_data={
        "carbohydrate": 72.2,
        "calories": 356,
        "fat": 1.3,
        "protein": 12.6,
        "salt": 0.003,
        "saturated fat": 0.3,
        "sodium": 1.2,
        "sugar": 1,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_patros_feta_aus_griechischer_schafsmilch() -> Food:
    """
    patros feta aus griechischer schafsmilch
    
    Source: Open Food Facts Database
    """
    return Food(
        name="patros feta aus griechischer schafsmilch",
        name_de="patros feta aus griechischer schafsmilch",
        category=None,
        nutrition_data={
        "carbohydrate": 0.5,
        "calories": 287,
        "fat": 24,
        "protein": 18,
        "salt": 2.4,
        "saturated fat": 17,
        "sodium": 960.0,
        "sugar": 0.5,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_pesto_arrabiata_bio_sacla() -> Food:
    """
    pesto arrabiata bio sacla
    
    Source: Open Food Facts Database
    """
    return Food(
        name="pesto arrabiata bio sacla",
        name_de="pesto arrabiata bio sacla",
        category=None,
        nutrition_data={
        "carbohydrate": 6.2,
        "calories": 282,
        "fat": 26.3,
        "protein": 4.2,
        "salt": 1.5,
        "saturated_fatty_acids": 2.8,
        "sodium": 600.0,
        "sugar": 6,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_poussin_lindt_chocolat_au_lait() -> Food:
    """
    poussin lindt chocolat au lait
    
    Source: Open Food Facts Database
    """
    return Food(
        name="poussin lindt chocolat au lait",
        name_de="poussin lindt chocolat au lait",
        category=None,
        nutrition_data={
        "carbohydrate": 56,
        "calories": 545,
        "fat": 32,
        "protein": 7.4,
        "salt": 0.2,
        "saturated fat": 20,
        "sodium": 80.0,
        "sugar": 55,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_raclettekäse() -> Food:
    """
    raclettekäse
    
    Source: Open Food Facts Database
    """
    return Food(
        name="raclettekäse",
        name_de="raclettekäse",
        category=None,
        nutrition_data={
        "carbohydrate": 1,
        "calories": 367,
        "fat": 26,
        "protein": 23,
        "salt": 1.7,
        "saturated fat": 20.5,
        "sodium": 680.0,
        "sugar": 0.5,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_rewe_antipasti_variations() -> Food:
    """
    rewe antipasti variations
    
    Source: Open Food Facts Database
    """
    return Food(
        name="rewe antipasti variations",
        name_de="rewe antipasti variations",
        category=None,
        nutrition_data={
        "carbohydrate": 0.3,
        "calories": 306,
        "fat": 21.5,
        "protein": 27.7,
        "salt": 4.66,
        "saturated fat": 8.6,
        "sodium": 1864.0,
        "sugar": 0.3,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_rewe_bio_beeren_müsli() -> Food:
    """
    rewe bio beeren müsli
    
    Source: Open Food Facts Database
    """
    return Food(
        name="rewe bio beeren müsli",
        name_de="rewe bio beeren müsli",
        category=None,
        nutrition_data={
        "carbohydrate": 62,
        "calories": 354,
        "fat": 5,
        "fiber": 10.6,
        "protein": 10,
        "salt": 0.01,
        "saturated_fatty_acids": 1,
        "sodium": 4.0,
        "sugar": 16,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_rewe_bio_bergkäse() -> Food:
    """
    rewe bio bergkäse
    
    Source: Open Food Facts Database
    """
    return Food(
        name="rewe bio bergkäse",
        name_de="rewe bio bergkäse",
        category=None,
        nutrition_data={
        "kcal": 418,
        "fat": 34,
        "saturated_fatty_acids": 26,
        "protein": 28,
        "salt": 1.6,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_rewe_bio_frischkäse() -> Food:
    """
    rewe bio frischkäse
    
    Source: Open Food Facts Database
    """
    return Food(
        name="rewe bio frischkäse",
        name_de="rewe bio frischkäse",
        category=None,
        nutrition_data={
        "carbohydrate": 3,
        "calories": 268,
        "fat": 26,
        "protein": 5.4,
        "salt": 0.7,
        "saturated fat": 17,
        "sodium": 280.0,
        "sugar": 3,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_rewe_bio_gemüsepfanne_französich() -> Food:
    """
    rewe bio gemüsepfanne französich
    
    Source: Open Food Facts Database
    """
    return Food(
        name="rewe bio gemüsepfanne französich",
        name_de="rewe bio gemüsepfanne französich",
        category=None,
        nutrition_data={
        "carbohydrate": 4.2,
        "calories": 41,
        "fat": 1.5,
        "protein": 1.4,
        "salt": 0.86,
        "saturated fat": 0.2,
        "sodium": 344.0,
        "sugar": 3.1,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_rewe_bio_gemüsepfanne_mediterran() -> Food:
    """
    rewe bio gemüsepfanne mediterran
    
    Source: Open Food Facts Database
    """
    return Food(
        name="rewe bio gemüsepfanne mediterran",
        name_de="rewe bio gemüsepfanne mediterran",
        category=None,
        nutrition_data={
        "carbohydrate": 3.5,
        "calories": 42,
        "fat": 2.1,
        "protein": 1.4,
        "salt": 0.98,
        "saturated fat": 0.8,
        "sodium": 392.0,
        "sugar": 2.9,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_rewe_bio_porridge() -> Food:
    """
    rewe bio porridge
    
    Source: Open Food Facts Database
    """
    return Food(
        name="rewe bio porridge",
        name_de="rewe bio porridge",
        category=None,
        nutrition_data={
        "carbohydrate": 61,
        "calories": 358,
        "fat": 5.6,
        "fiber": 10,
        "protein": 11,
        "salt": 0.02,
        "saturated fat": 1.2,
        "sodium": 8.0,
        "sugar": 8.3,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_rewe_bio_zartbitter_schokocreme() -> Food:
    """
    rewe bio zartbitter schokocreme
    
    Source: Open Food Facts Database
    """
    return Food(
        name="rewe bio zartbitter schokocreme",
        name_de="rewe bio zartbitter schokocreme",
        category=None,
        nutrition_data={
        "carbohydrate": 37,
        "calories": 552,
        "fat": 40,
        "protein": 6.3,
        "saturated fat": 8.5,
        "sugar": 33,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_schwarze_oliven_mit_stein() -> Food:
    """
    schwarze oliven mit stein
    
    Source: Open Food Facts Database
    """
    return Food(
        name="schwarze oliven mit stein",
        name_de="schwarze oliven mit stein",
        category=None,
        nutrition_data={
        "carbohydrate": 5.8,
        "calories": 398,
        "fat": 39.4,
        "protein": 2.4,
        "salt": 8.15,
        "saturated_fatty_acids": 4.4,
        "sodium": 3260.0,
        "sugar": 1.8,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_super_hot_chili_sauce() -> Food:
    """
    super hot chili sauce
    
    Source: Open Food Facts Database
    """
    return Food(
        name="super hot chili sauce",
        name_de="super hot chili sauce",
        category=None,
        nutrition_data={
        "carbohydrate": 34,
        "calories": 168,
        "fat": 1.7,
        "fiber": 4,
        "protein": 1.8,
        "salt": 8.7,
        "saturated fat": 0.3,
        "sodium": 3480.0,
        "sugar": 27,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_swiss_twist() -> Food:
    """
    swiss twist
    
    Source: Open Food Facts Database
    """
    return Food(
        name="swiss twist",
        name_de="swiss twist",
        category=None,
        nutrition_data={
        "carbohydrate": 55,
        "calories": 500,
        "fat": 25,
        "protein": 12,
        "salt": 1.73,
        "saturated fat": 17,
        "sodium": 692.0,
        "sugar": 5,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_tagliatelle_verde() -> Food:
    """
    tagliatelle verde
    
    Source: Open Food Facts Database
    """
    return Food(
        name="tagliatelle verde",
        name_de="tagliatelle verde",
        category=None,
        nutrition_data={
        "calories": 136,
        "carbohydrate": 15,
        "fat": 6.2,
        "fiber": 1.3,
        "protein": 4.3,
        "salt": 0.83,
        "saturated fat": 3.5,
        "sodium": 332.0,
        "sugar": 1.6,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_tegut_bio_haltbare_vollmilch() -> Food:
    """
    tegut bio haltbare vollmilch
    
    Source: Open Food Facts Database
    """
    return Food(
        name="tegut bio haltbare vollmilch",
        name_de="tegut bio haltbare vollmilch",
        category=None,
        nutrition_data={
        "carbohydrate": 4.8,
        "calories": 66,
        "fat": 3.8,
        "protein": 0.13,
        "saturated fat": 2.5,
        "sugar": 3.3,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_tegut_makrelen() -> Food:
    """
    tegut makrelen
    
    Source: Open Food Facts Database
    """
    return Food(
        name="tegut makrelen",
        name_de="tegut makrelen",
        category=None,
        nutrition_data={
        "carbohydrate": 0.5,
        "calories": 299,
        "fat": 25,
        "protein": 19,
        "salt": 2,
        "saturated fat": 8.2,
        "sodium": 800.0,
        "sugar": 0.5,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_veganer_fleischfreisalat() -> Food:
    """
    veganer fleischfreisalat
    
    Source: Open Food Facts Database
    """
    return Food(
        name="veganer fleischfreisalat",
        name_de="veganer fleischfreisalat",
        category=None,
        nutrition_data={
        "carbohydrate": 8.4,
        "calories": 296,
        "fat": 28,
        "protein": 1.7,
        "salt": 1.68,
        "saturated fat": 2.1,
        "sodium": 672.0,
        "sugar": 5.8,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_vollkorn_knäcke_snack_emmentanler_kürbiskern() -> Food:
    """
    vollkorn knäcke snack emmentanler kürbiskern
    
    Source: Open Food Facts Database
    """
    return Food(
        name="vollkorn knäcke snack emmentanler kürbiskern",
        name_de="vollkorn knäcke snack emmentanler kürbiskern",
        category=None,
        nutrition_data={
        "carbohydrate": 46,
        "calories": 439,
        "fat": 18,
        "fiber": 11,
        "protein": 17,
        "salt": 2.3,
        "saturated fat": 4.9,
        "sodium": 920.0,
        "sugar": 3.1,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_wagner_pizza_speciale() -> Food:
    """
    wagner pizza speciale
    
    Source: Open Food Facts Database
    """
    return Food(
        name="wagner pizza speciale",
        name_de="wagner pizza speciale",
        category=None,
        nutrition_data={
        "carbohydrate": 27.7,
        "calories": 204,
        "fat": 5.9,
        "fiber": 4.3,
        "protein": 9.6,
        "salt": 1.2,
        "saturated fat": 2.4,
        "sodium": 480.0,
        "sugar": 3.3,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_weizen_mischbrot() -> Food:
    """
    weizen mischbrot
    
    Source: Open Food Facts Database
    """
    return Food(
        name="weizen mischbrot",
        name_de="weizen mischbrot",
        category=None,
        nutrition_data={
        "carbohydrate": 45,
        "calories": 231,
        "fat": 1.2,
        "fiber": 5,
        "protein": 7.5,
        "salt": 1,
        "saturated_fatty_acids": 1.2,
        "sodium": 400.0,
        "sugar": 2.5,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_wienerle() -> Food:
    """
    wienerle
    
    Source: Open Food Facts Database
    """
    return Food(
        name="wienerle",
        name_de="wienerle",
        category=None,
        nutrition_data={
        "carbohydrate": 1,
        "calories": 236,
        "fat": 20,
        "protein": 13,
        "salt": 2,
        "saturated fat": 8,
        "sodium": 800.0,
        "sugar": 1,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )

def create_yum_yum_chicken_flavour() -> Food:
    """
    yum yum chicken flavour
    
    Source: Open Food Facts Database
    """
    return Food(
        name="yum yum chicken flavour",
        name_de="yum yum chicken flavour",
        category=None,
        nutrition_data={
        "carbohydrate": 10,
        "calories": 76,
        "fat": 3.3,
        "fiber": 0.4,
        "protein": 1.3,
        "salt": 0.8,
        "saturated_fatty_acids": 1.6,
        "sodium": 320.0,
        "sugar": 0.4,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_demeter_bio_zuckermais() -> Food:
    """
    demeter bio zuckermais
    
    Source: Open Food Facts Database
    """
    return Food(
        name="demeter bio zuckermais",
        name_de="demeter bio zuckermais",
        category=None,
        nutrition_data={
        "carbohydrate": 13,
        "calories": 85,
        "fat": 1.6,
        "fiber": 3.3,
        "protein": 3,
        "salt": 0.4,
        "saturated fat": 0.2,
        "sodium": 160.0,
        "sugar": 5.2,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_zwiebel_griebenschmalz() -> Food:
    """
    #####################
    
    Source: Open Food Facts Database
    """
    return Food(
        name="#####################",
        name_de="#####################",
        category=None,
        nutrition_data={
        "carbohydrate": 6,
        "calories": 804,
        "fat": 85,
        "protein": 3.5,
        "salt": 0.8,
        "saturated_fatty_acids": 33,
        "sodium": 320.0,
        "sugar": 3,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_lindt_weiss_feinschmelzend() -> Food:
    """
    lindt weiss feinschmelzend
    
    Source: Open Food Facts Database
    """
    return Food(
        name="lindt weiss feinschmelzend",
        name_de="lindt weiss feinschmelzend",
        category=None,
        nutrition_data={
        "carbohydrate": 55,
        "calories": 567,
        "fat": 35,
        "protein": 6.7,
        "salt": 0.27,
        "saturated_fatty_acids": 22,
        "sodium": 108.0,
        "sugar": 55,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_crunchips_salted() -> Food:
    """
    crunchips salted
    
    Source: Open Food Facts Database
    """
    return Food(
        name="crunchips salted",
        name_de="crunchips salted",
        category=None,
        nutrition_data={
        "carbohydrate": 52,
        "calories": 543,
        "fat": 34,
        "fiber": 3.5,
        "protein": 5.5,
        "salt": 1.6,
        "saturated_fatty_acids": 2.8,
        "sodium": 640.0,
        "sugar": 0.5,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


def create_tuc_original() -> Food:
    """
    tuc original
    
    Source: Open Food Facts Database
    """
    return Food(
        name="tuc original",
        name_de="tuc original",
        category=None,
        nutrition_data={
        "carbohydrate": 67,
        "calories": 479,
        "fat": 19,
        "fiber": 2.4,
        "protein": 8.4,
        "salt": 1.7,
        "saturated_fatty_acids": 1.9,
        "sodium": 680.0,
        "sugar": 7.1,
        },
        nutrition_sources=[
            DataSource(
                url="https://world.openfoodfacts.org",
                title="Open Food Facts Database",
                source_type="database"
            )
        ]
    )


__all__ = [
    "create_altenmünster_landbier",
    "create_becks_pils",
    "create_flensburger_gold",
    "create_kilkenny_irish_beer",
    "create_krombacher_alkoholfrei",
    "create_krombacher_pils",
    "create_aioli_jalapeno",
    "create_amber_mist_mature_cheddar_with_whisky",
    "create_andechser_bio_rahmjoghurt_vanille",
    "create_andechser_bio_rahmjoghurt_heidelbeere",
    "create_baguette_kräuterbutter",
    "create_bayerischer_meerrettich_alpensahne",
    "create_bio_feta",
    "create_bio_geschabte_spätzle",
    "create_bio_streichcreme_paprika_aubergine_zucchini_und_tomate",
    "create_bio_vollkorn_sandwich",
    "create_biofix_chicken_kashmir_gewürz",
    "create_caffe_crema_kaffeepads",
    "create_dextro_energy_classic",
    "create_erdnussbutter_peanut_butter_creamy",
    "create_feta_griechisch",
    "create_finesse_schinkenaufschnitt_mit_belém_pfeffer",
    "create_gemüse_brotaufstrich_kirschtomate_rucola",
    "create_gewürz_ketchup_curry_delikat",
    "create_golden_toast",
    "create_haferflocken",
    "create_handkäse_kümmel",
    "create_iglo_brokkoli_buchweizen",
    "create_indische_curry_sauce",
    "create_jägersauce_feinkörnig",
    "create_joghurt_griechische_art",
    "create_k_classic_knuspriger_apfelstrudel",
    "create_kaufland_bio_vollkorn_spaghetti",
    "create_kaufland_langkorn_wildreis_mischung",
    "create_knoblauch_baguette",
    "create_knorr_asia_noodles_huhn_geschmack",
    "create_kochhinterschinken",
    "create_kochschinken_hauchfein",
    "create_kokos_zwieback",
    "create_lachsfilets_naturbelassen",
    "create_laugenkranz",
    "create_naturals_meersalz_und_pfeffer",
    "create_nutella",
    "create_ökoland_wok_gemüse_pfanne",
    "create_paradiso_bio_tagliatelle",
    "create_patros_feta_aus_griechischer_schafsmilch",
    "create_pesto_arrabiata_bio_sacla",
    "create_poussin_lindt_chocolat_au_lait",
    "create_raclettekäse",
    "create_rewe_antipasti_variations",
    "create_rewe_bio_beeren_müsli",
    "create_rewe_bio_bergkäse",
    "create_rewe_bio_frischkäse",
    "create_rewe_bio_gemüsepfanne_französich",
    "create_rewe_bio_gemüsepfanne_mediterran",
    "create_rewe_bio_porridge",
    "create_rewe_bio_zartbitter_schokocreme",
    "create_schwarze_oliven_mit_stein",
    "create_super_hot_chili_sauce",
    "create_swiss_twist",
    "create_tagliatelle_verde",
    "create_tegut_bio_haltbare_vollmilch",
    "create_tegut_makrelen",
    "create_veganer_fleischfreisalat",
    "create_vollkorn_knäcke_snack_emmentanler_kürbiskern",
    "create_wagner_pizza_speciale",
    "create_weizen_mischbrot",
    "create_wienerle",
    "create_yum_yum_chicken_flavour",
    "create_demeter_bio_zuckermais",
    "create_zwiebel_griebenschmalz",
    "create_lindt_weiss_feinschmelzend",
    "create_crunchips_salted",
    "create_tuc_original",
]
