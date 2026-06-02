"""
Fish protein definitions.

Sources:
- USDA FoodData Central: https://fdc.nal.usda.gov
- NIH Office of Dietary Supplements: https://ods.od.nih.gov
"""

from blutwerte.foods import (
    Food, FoodEffect, DataSource, EffectTargetType, EffectDirection,
    EffectCertainty
)


def create_salmon() -> Food:
    """
    Salmon - fatty fish rich in omega-3, vitamin D, and B12.
    
    Nutrition per 100g (cooked, dry heat):
    - Omega-3 fatty acids: 2.3 g (EPA + DHA)
    - Vitamin D: 11 mcg (440 IU)
    - Vitamin B12: 2.8 mcg
    - Protein: 25 g
    - Selenium: 37 mcg
    """
    return Food(
        name="Salmon",
        name_de="Lachs",
        category="fish",
        nutrition_data={
            "calories": 206,
            "protein": 25,
            "omega 3": 2.3,
            "vitamin d": 11,
            "vitamin b12": 2.8,
            "selenium": 37,
            "vitamin b3": 8.0,
            "fat": 12,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/175168/nutrients",
                title="USDA FoodData Central - Fish, salmon, Atlantic, farmed, cooked",
                source_type="database"
            )
        ],
        effects=[
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Vitamin D",
                direction=EffectDirection.INCREASE,
                mechanism="One of the few natural food sources of vitamin D (11 mcg/100g). One 100g serving provides 55% of daily value.",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/VitaminD-HealthProfessional/",
                        title="Vitamin D Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    ),
                    DataSource(
                        url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/175168/nutrients",
                        title="USDA FoodData Central - Salmon",
                        source_type="database"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED,
                notes="One of the best dietary sources of vitamin D."
            ),
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Vitamin B12",
                direction=EffectDirection.INCREASE,
                mechanism="Excellent source of vitamin B12 (2.8 mcg/100g). One 100g serving provides 117% of daily value.",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/VitaminB12-HealthProfessional/",
                        title="Vitamin B12 Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED
            )
        ]
    )
