"""
Legume protein definitions.

Sources:
- USDA FoodData Central: https://fdc.nal.usda.gov
- NIH Office of Dietary Supplements: https://ods.od.nih.gov
"""

from blutwerte.foods import (
    Food, FoodEffect, DataSource, EffectTargetType, EffectDirection,
    EffectCertainty, EffectModifier
)


def create_lentils() -> Food:
    """
    Lentils - plant-based protein with iron and folate.
    
    Nutrition per 100g (cooked, boiled, without salt):
    - Protein: 9 g
    - Iron: 3.3 mg (non-heme)
    - Folate: 181 mcg
    - Fiber: 8 g
    - Potassium: 369 mg
    """
    return Food(
        name="Lentils",
        name_de="Linsen",
        category="legume",
        nutrition_data={
            "calories": 116,
            "protein": 9,
            "iron": 3.3,
            "folate": 181,
            "fiber": 8,
            "potassium": 369,
            "magnesium": 36,
            "zinc": 1.3,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/172421/nutrients",
                title="USDA FoodData Central - Lentils, mature seeds, cooked, boiled, without salt",
                source_type="database"
            )
        ],
        effects=[
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Iron",
                direction=EffectDirection.VARIABLE,
                mechanism="Contains non-heme iron (3.3 mg/100g). Absorption is 2-20% depending on meal composition. One cup cooked (198g) provides 6.6 mg iron.",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/",
                        title="Iron Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    ),
                    DataSource(
                        url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/172421/nutrients",
                        title="USDA FoodData Central - Lentils",
                        source_type="database"
                    )
                ],
                certainty=EffectCertainty.VARIABLE,
                modifiers=[
                    EffectModifier(
                        factor="vitamin_c_present",
                        description="Vitamin C enhances non-heme iron absorption",
                        impact="3-4x increase",
                        direction="enhances"
                    ),
                    EffectModifier(
                        factor="phytates_present",
                        description="Phytates in legumes can inhibit iron absorption",
                        impact="Partial inhibition",
                        direction="inhibits"
                    )
                ],
                notes="Good plant-based iron source, but absorption is lower than heme iron from meat."
            ),
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Folic Acid",
                direction=EffectDirection.INCREASE,
                mechanism="Excellent source of folate (181 mcg/100g). One cup cooked provides 358 mcg (90% DV).",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/Folate-HealthProfessional/",
                        title="Folate Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED,
                notes="One of the best plant-based folate sources."
            )
        ]
    )
