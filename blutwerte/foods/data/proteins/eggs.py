"""
Egg protein definitions.

Sources:
- USDA FoodData Central: https://fdc.nal.usda.gov
- NIH Office of Dietary Supplements: https://ods.od.nih.gov
"""

from blutwerte.foods import (
    Food, FoodEffect, DataSource, EffectTargetType, EffectDirection,
    EffectCertainty
)


def create_egg() -> Food:
    """
    Egg - complete protein with B12 and choline.
    
    Nutrition per 100g (whole, cooked, hard-boiled):
    - Protein: 13 g
    - Vitamin B12: 1.1 mcg
    - Choline: 294 mg
    - Selenium: 27 mcg
    - Vitamin A: 149 mcg RAE
    """
    return Food(
        name="Egg",
        name_de="Ei",
        category="protein",
        nutrition_data={
            "calories": 155,
            "protein": 13,
            "vitamin b12": 1.1,
            "choline": 294,
            "selenium": 27,
            "vitamin a": 149,
            "vitamin d": 2.2,
            "fat": 11,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/171287/nutrients",
                title="USDA FoodData Central - Egg, whole, cooked, hard-boiled",
                source_type="database"
            )
        ],
        effects=[
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Vitamin B12",
                direction=EffectDirection.INCREASE,
                mechanism="Good source of vitamin B12 (1.1 mcg/100g). One large egg (50g) provides 0.6 mcg (25% DV).",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/VitaminB12-HealthProfessional/",
                        title="Vitamin B12 Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    ),
                    DataSource(
                        url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/171287/nutrients",
                        title="USDA FoodData Central - Egg",
                        source_type="database"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED
            ),
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Choline",
                direction=EffectDirection.INCREASE,
                mechanism="Excellent source of choline (294 mg/100g). One large egg provides ~147 mg (27% DV). Eggs are the primary source of choline in the diet.",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/Choline-HealthProfessional/",
                        title="Choline Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED,
                notes="Eggs are the best dietary source of choline."
            )
        ]
    )
