"""
Fruit definitions with nutrition data and biomarker effects.

Sources:
- USDA FoodData Central: https://fdc.nal.usda.gov
- NIH Office of Dietary Supplements: https://ods.od.nih.gov
"""

from blutwerte.foods import (
    Food, FoodEffect, DataSource, EffectTargetType, EffectDirection,
    EffectCertainty
)


def create_banana() -> Food:
    """
    Banana - excellent source of potassium.
    
    Nutrition per 100g:
    - Potassium: 358 mg (high)
    - Vitamin C: 8.7 mg
    - Vitamin B6: 0.4 mg
    - Fiber: 2.6 g
    """
    return Food(
        name="Banana",
        name_de="Banane",
        category="fruit",
        nutrition_data={
            "calories": 89,
            "potassium": 358,
            "vitamin c": 8.7,
            "vitamin b6": 0.4,
            "fiber": 2.6,
            "magnesium": 27,
            "folate": 20,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/173944/nutrients",
                title="USDA FoodData Central - Bananas, raw",
                source_type="database"
            )
        ],
        effects=[
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Potassium",
                direction=EffectDirection.INCREASE,
                mechanism="Excellent source of potassium (358 mg/100g). One medium banana (118g) provides ~422 mg (9% DV).",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/Potassium-HealthProfessional/",
                        title="Potassium Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    ),
                    DataSource(
                        url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/173944/nutrients",
                        title="USDA FoodData Central - Banana",
                        source_type="database"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED,
                notes="One of the best natural sources of potassium."
            )
        ]
    )


def create_orange() -> Food:
    """
    Orange - well-known vitamin C source.
    
    Nutrition per 100g:
    - Vitamin C: 53 mg (high)
    - Folate: 30 mcg
    - Potassium: 181 mg
    """
    return Food(
        name="Orange",
        name_de="Orange",
        category="fruit",
        nutrition_data={
            "calories": 47,
            "vitamin c": 53,
            "folate": 30,
            "potassium": 181,
            "calcium": 40,
            "fiber": 2.4,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/169097/nutrients",
                title="USDA FoodData Central - Oranges, raw, all commercial varieties",
                source_type="database"
            )
        ],
        effects=[
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Vitamin C",
                direction=EffectDirection.INCREASE,
                mechanism="Rich in vitamin C (53 mg/100g). One medium orange (131g) provides ~70 mg (78% DV).",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/VitaminC-HealthProfessional/",
                        title="Vitamin C Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED
            ),
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Folic Acid",
                direction=EffectDirection.INCREASE,
                mechanism="Contains folate (30 mcg/100g). One medium orange provides ~39 mcg.",
                sources=[
                    DataSource(
                        url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/169097/nutrients",
                        title="USDA FoodData Central - Orange",
                        source_type="database"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED
            )
        ]
    )


def create_avocado() -> Food:
    """
    Avocado - unique fruit rich in healthy fats and potassium.
    
    Nutrition per 100g:
    - Potassium: 485 mg (very high for fruit)
    - Fiber: 6.7 g (high)
    - Monounsaturated fat: 9.8 g
    - Folate: 81 mcg
    """
    return Food(
        name="Avocado",
        name_de="Avocado",
        category="fruit",
        nutrition_data={
            "calories": 160,
            "potassium": 485,
            "fiber": 6.7,
            "monounsaturated fat": 9.8,
            "folate": 81,
            "vitamin k": 21,
            "vitamin c": 10,
            "vitamin b6": 0.3,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/171705/nutrients",
                title="USDA FoodData Central - Avocados, raw, all commercial varieties",
                source_type="database"
            )
        ],
        effects=[
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Potassium",
                direction=EffectDirection.INCREASE,
                mechanism="Very high in potassium for a fruit (485 mg/100g). One-half avocado (100g) provides 485 mg (10% DV).",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/Potassium-HealthProfessional/",
                        title="Potassium Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED,
                notes="Higher potassium content than bananas by weight."
            )
        ]
    )


def create_strawberry() -> Food:
    """
    Strawberry - excellent vitamin C source.
    
    Nutrition per 100g:
    - Vitamin C: 59 mg (high)
    - Folate: 24 mcg
    - Fiber: 2 g
    - Manganese: 0.4 mg
    """
    return Food(
        name="Strawberry",
        name_de="Erdbeere",
        category="fruit",
        nutrition_data={
            "calories": 32,
            "vitamin c": 59,
            "folate": 24,
            "fiber": 2.0,
            "manganese": 0.4,
            "potassium": 153,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/167762/nutrients",
                title="USDA FoodData Central - Strawberries, raw",
                source_type="database"
            )
        ],
        effects=[
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Vitamin C",
                direction=EffectDirection.INCREASE,
                mechanism="Excellent source of vitamin C (59 mg/100g). One cup halves (152g) provides ~90 mg (100% DV).",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/VitaminC-HealthProfessional/",
                        title="Vitamin C Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    ),
                    DataSource(
                        url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/167762/nutrients",
                        title="USDA FoodData Central - Strawberries",
                        source_type="database"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED,
                notes="One serving (1 cup) provides 100% of daily vitamin C needs."
            )
        ]
    )
