"""
Plant protein definitions.

Sources:
- USDA FoodData Central: https://fdc.nal.usda.gov
- NIH Office of Dietary Supplements: https://ods.od.nih.gov
"""

from blutwerte.foods import (
    Food, FoodEffect, DataSource, EffectTargetType, EffectDirection,
    EffectCertainty, EffectModifier
)


def create_tofu() -> Food:
    """
    Tofu - soy-based protein with iron and calcium.
    
    Nutrition per 100g (firm, prepared with calcium sulfate):
    - Protein: 8 g
    - Iron: 2 mg (non-heme)
    - Calcium: 350 mg (if calcium-set)
    - Manganese: 0.6 mg
    - Selenium: 9 mcg
    """
    return Food(
        name="Tofu",
        name_de="Tofu",
        category="protein",
        nutrition_data={
            "calories": 70,
            "protein": 8,
            "iron": 2.0,
            "calcium": 350,
            "manganese": 0.6,
            "selenium": 9,
            "magnesium": 37,
            "fat": 4.2,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/172475/nutrients",
                title="USDA FoodData Central - Tofu, firm, prepared with calcium sulfate",
                source_type="database"
            )
        ],
        effects=[
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Iron",
                direction=EffectDirection.VARIABLE,
                mechanism="Contains non-heme iron (2 mg/100g). One-half cup (126g) provides 2.5 mg iron. Absorption depends on enhancers/inhibitors.",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/",
                        title="Iron Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    ),
                    DataSource(
                        url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/172475/nutrients",
                        title="USDA FoodData Central - Tofu",
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
                    )
                ],
                notes="Good plant-based iron source. Calcium-set tofu also provides significant calcium."
            ),
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Calcium",
                direction=EffectDirection.INCREASE,
                mechanism="Calcium-set tofu is an excellent calcium source (350 mg/100g). One-half cup provides 441 mg (34% DV). Note: Not all tofu is calcium-set.",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/Calcium-HealthProfessional/",
                        title="Calcium Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    ),
                    DataSource(
                        url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/172475/nutrients",
                        title="USDA FoodData Central - Tofu (calcium-set)",
                        source_type="database"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED,
                notes="Check label for 'calcium sulfate' or 'calcium chloride' in ingredients."
            )
        ]
    )
