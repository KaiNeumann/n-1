"""
Grain definitions with nutrition data and biomarker effects.

Sources:
- USDA FoodData Central: https://fdc.nal.usda.gov
- NIH Office of Dietary Supplements: https://ods.od.nih.gov
"""

from blutwerte.foods import (
    Food, FoodEffect, DataSource, EffectTargetType, EffectDirection,
    EffectCertainty
)


def create_oats() -> Food:
    """
    Oats - whole grain with beta-glucan fiber and iron.
    
    Nutrition per 100g (raw):
    - Iron: 4.7 mg
    - Fiber: 10.6 g
    - Protein: 13.2 g
    - Magnesium: 177 mg
    - Zinc: 4 mg
    """
    return Food(
        name="Oats",
        name_de="Hafer",
        category="cereal",
        nutrition_data={
            "calories": 389,
            "iron": 4.7,
            "fiber": 10.6,
            "protein": 13.2,
            "magnesium": 177,
            "zinc": 4.0,
            "phosphorus": 523,
            "manganese": 4.9,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/173904/nutrients",
                title="USDA FoodData Central - Oats",
                source_type="database"
            )
        ],
        effects=[
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Iron",
                direction=EffectDirection.INCREASE,
                mechanism="Contains iron (4.7 mg/100g dry). One cup dry oats (81g) provides 3.8 mg iron (21% DV).",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/",
                        title="Iron Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    ),
                    DataSource(
                        url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/173904/nutrients",
                        title="USDA FoodData Central - Oats",
                        source_type="database"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED,
                notes="Good plant-based iron source, especially when paired with vitamin C."
            )
        ]
    )


def create_quinoa() -> Food:
    """
    Quinoa - complete protein grain with iron and magnesium.
    
    Nutrition per 100g (cooked):
    - Protein: 4.4 g (complete protein)
    - Iron: 2.8 mg
    - Magnesium: 64 mg
    - Fiber: 2.8 g
    - Folate: 42 mcg
    """
    return Food(
        name="Quinoa",
        name_de="Quinoa",
        category="cereal",
        nutrition_data={
            "calories": 120,
            "protein": 4.4,
            "iron": 2.8,
            "magnesium": 64,
            "fiber": 2.8,
            "folate": 42,
            "manganese": 0.6,
            "phosphorus": 152,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/168917/nutrients",
                title="USDA FoodData Central - Quinoa, cooked",
                source_type="database"
            )
        ],
        effects=[
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Iron",
                direction=EffectDirection.INCREASE,
                mechanism="Good iron source for a grain (2.8 mg/100g cooked). One cup cooked (185g) provides 5.2 mg iron (29% DV).",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/",
                        title="Iron Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    ),
                    DataSource(
                        url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/168917/nutrients",
                        title="USDA FoodData Central - Quinoa",
                        source_type="database"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED
            ),
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Magnesium",
                direction=EffectDirection.INCREASE,
                mechanism="Good magnesium source (64 mg/100g cooked). One cup provides 118 mg (28% DV).",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/Magnesium-HealthProfessional/",
                        title="Magnesium Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED
            )
        ]
    )


def create_brown_rice() -> Food:
    """
    Brown rice - whole grain with fiber and B vitamins.
    
    Nutrition per 100g (cooked, long-grain):
    - Fiber: 1.8 g
    - Magnesium: 44 mg
    - Vitamin B1: 0.1 mg
    - Manganese: 0.9 mg
    - Selenium: 10 mcg
    """
    return Food(
        name="Brown Rice",
        name_de="Vollkornreis",
        category="cereal",
        nutrition_data={
            "calories": 111,
            "fiber": 1.8,
            "magnesium": 44,
            "vitamin b1": 0.1,
            "manganese": 0.9,
            "selenium": 10,
            "phosphorus": 77,
            "protein": 2.6,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/168892/nutrients",
                title="USDA FoodData Central - Rice, brown, long-grain, cooked",
                source_type="database"
            )
        ],
        effects=[]  # No direct biomarker effects at typical serving sizes
    )
