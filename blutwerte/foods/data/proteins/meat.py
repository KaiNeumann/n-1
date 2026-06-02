"""
Meat protein definitions.

Sources:
- USDA FoodData Central: https://fdc.nal.usda.gov
- NIH Office of Dietary Supplements: https://ods.od.nih.gov
"""

from blutwerte.foods import (
    Food, FoodEffect, DataSource, EffectTargetType, EffectDirection,
    EffectCertainty
)


def create_beef() -> Food:
    """
    Beef - rich in highly bioavailable heme iron and vitamin B12.
    
    Nutrition per 100g (cooked, lean):
    - Protein: 26 g
    - Iron: 2.6 mg (heme iron - highly bioavailable)
    - Vitamin B12: 2.6 mcg
    - Zinc: 6.3 mg
    - Vitamin B3: 4.8 mg
    """
    return Food(
        name="Beef",
        name_de="Rindfleisch",
        category="meat",
        nutrition_data={
            "calories": 250,
            "protein": 26,
            "iron": 2.6,
            "vitamin b12": 2.6,
            "zinc": 6.3,
            "vitamin b3": 4.8,
            "vitamin b6": 0.3,
            "fat": 15,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/171781/nutrients",
                title="USDA FoodData Central - Beef, ground, 85% lean meat",
                source_type="database"
            )
        ],
        effects=[
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Iron",
                direction=EffectDirection.INCREASE,
                mechanism="Contains highly bioavailable heme iron (2.6 mg/100g). Heme iron absorption is 15-35%, much higher than non-heme iron (2-20%).",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/",
                        title="Iron Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    ),
                    DataSource(
                        url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/171781/nutrients",
                        title="USDA FoodData Central - Beef",
                        source_type="database"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED,
                notes="Best dietary source of highly bioavailable iron."
            ),
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Vitamin B12",
                direction=EffectDirection.INCREASE,
                mechanism="Richest dietary source of vitamin B12 (2.6 mcg/100g). One 100g serving provides 108% of daily value.",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/VitaminB12-HealthProfessional/",
                        title="Vitamin B12 Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED,
                notes="Only naturally occurs in animal products."
            )
        ]
    )


def create_chicken() -> Food:
    """
    Chicken breast - lean protein with B vitamins.
    
    Nutrition per 100g (cooked, roasted):
    - Protein: 31 g
    - Vitamin B3: 13.4 mg
    - Vitamin B6: 0.6 mg
    - Selenium: 24 mcg
    - Phosphorus: 228 mg
    """
    return Food(
        name="Chicken Breast",
        name_de="Hähnchenbrust",
        category="meat",
        nutrition_data={
            "calories": 165,
            "protein": 31,
            "vitamin b3": 13.4,
            "vitamin b6": 0.6,
            "selenium": 24,
            "phosphorus": 228,
            "fat": 3.6,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/171444/nutrients",
                title="USDA FoodData Central - Chicken breast, grilled",
                source_type="database"
            )
        ],
        effects=[
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Vitamin B3",
                direction=EffectDirection.INCREASE,
                mechanism="Excellent source of niacin (13.4 mg/100g). One 100g serving provides 84% of daily value.",
                sources=[
                    DataSource(
                        url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/171444/nutrients",
                        title="USDA FoodData Central - Chicken Breast",
                        source_type="database"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED
            ),
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Vitamin B6",
                direction=EffectDirection.INCREASE,
                mechanism="Good source of vitamin B6 (0.6 mg/100g). One 100g serving provides 35% of daily value.",
                sources=[
                    DataSource(
                        url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/171444/nutrients",
                        title="USDA FoodData Central - Chicken Breast",
                        source_type="database"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED
            )
        ]
    )
