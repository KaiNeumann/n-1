"""
Vegetable definitions with nutrition data and biomarker effects.

Sources:
- USDA FoodData Central: https://fdc.nal.usda.gov
- NIH Office of Dietary Supplements: https://ods.od.nih.gov
"""

from blutwerte.foods import (
    Food, FoodEffect, DataSource, EffectTargetType, EffectDirection,
    EffectCertainty, EffectModifier
)


def create_spinach() -> Food:
    """
    Spinach - nutrient-dense leafy green vegetable.
    
    Star example with multiple well-documented biomarker effects.
    
    Nutrition per 100g:
    - Vitamin K: 483 mcg (high)
    - Iron: 2.7 mg (moderate, non-heme)
    - Folate: 194 mcg (high)
    - Vitamin C: 28 mg
    - Calcium: 99 mg
    """
    return Food(
        name="Spinach",
        name_de="Spinat",
        category="vegetable",
        nutrition_data={
            "calories": 23,
            "vitamin k": 483,
            "iron": 2.7,
            "folate": 194,
            "vitamin c": 28,
            "calcium": 99,
            "magnesium": 79,
            "potassium": 558,
            "fiber": 2.2,
            "protein": 2.9,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/168462/nutrients",
                title="USDA FoodData Central - Spinach, raw",
                source_type="database"
            )
        ],
        effects=[
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Vitamin K",
                direction=EffectDirection.INCREASE,
                mechanism="Rich in phylloquinone (vitamin K1). One cup cooked (180g) provides 888 mcg (987% of daily value)",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/VitaminK-HealthProfessional/",
                        title="Vitamin K Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED,
                notes="Excellent source of vitamin K. Important for patients on warfarin to maintain consistent intake."
            ),
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Iron",
                direction=EffectDirection.VARIABLE,
                mechanism="Contains non-heme iron (2.7 mg/100g). Absorption is 2-20% depending on enhancers/inhibitors present in the meal.",
                sources=[
                    DataSource(
                        url="https://pubmed.ncbi.nlm.nih.gov/16076240/",
                        title="Iron absorption from spinach: a study in iron absorption",
                        source_type="research"
                    ),
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/",
                        title="Iron Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    )
                ],
                certainty=EffectCertainty.VARIABLE,
                modifiers=[
                    EffectModifier(
                        factor="vitamin_c_present",
                        description="Vitamin C enhances non-heme iron absorption 3-4 fold",
                        impact="3-4x increase",
                        direction="enhances"
                    ),
                    EffectModifier(
                        factor="calcium_high",
                        description="Calcium competes with iron for absorption",
                        impact="50-65% reduction",
                        direction="inhibits"
                    ),
                    EffectModifier(
                        factor="tannins_present",
                        description="Tannins in tea/coffee inhibit iron absorption",
                        impact="Significant reduction",
                        direction="inhibits"
                    )
                ],
                notes="Cooking increases iron bioavailability compared to raw spinach."
            ),
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Folic Acid",
                direction=EffectDirection.INCREASE,
                mechanism="Good source of folate (194 mcg/100g). One cup cooked provides 263 mcg (66% DV).",
                sources=[
                    DataSource(
                        url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/168462/nutrients",
                        title="USDA FoodData Central - Spinach, raw",
                        source_type="database"
                    ),
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/Folate-HealthProfessional/",
                        title="Folate Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED
            )
        ]
    )


def create_tomato() -> Food:
    """
    Tomato - rich in potassium, vitamin C, and lycopene.
    
    Nutrition per 100g:
    - Potassium: 237 mg
    - Vitamin C: 14 mg
    - Lycopene: 2573 mcg (antioxidant)
    """
    return Food(
        name="Tomato",
        name_de="Tomate",
        category="vegetable",
        nutrition_data={
            "calories": 18,
            "potassium": 237,
            "vitamin c": 14,
            "folate": 15,
            "fiber": 1.2,
            "lycopene": 2.573,  # mg
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/170457/nutrients",
                title="USDA FoodData Central - Tomatoes, red, ripe",
                source_type="database"
            )
        ],
        effects=[
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Potassium",
                direction=EffectDirection.INCREASE,
                mechanism="Contains potassium (237 mg/100g). One medium tomato (~123g) provides ~292 mg.",
                sources=[
                    DataSource(
                        url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/170457/nutrients",
                        title="USDA FoodData Central - Tomatoes",
                        source_type="database"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED
            ),
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Vitamin C",
                direction=EffectDirection.INCREASE,
                mechanism="Source of vitamin C (14 mg/100g). One medium tomato provides ~17 mg.",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/VitaminC-HealthProfessional/",
                        title="Vitamin C Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED
            )
        ]
    )


def create_potato() -> Food:
    """
    Potato - starchy vegetable rich in potassium.
    
    Nutrition per 100g (boiled, without skin):
    - Potassium: 379 mg (high)
    - Vitamin C: 10 mg
    - Fiber: 1.8 g
    """
    return Food(
        name="Potato",
        name_de="Kartoffel",
        category="vegetable",
        nutrition_data={
            "calories": 87,
            "potassium": 379,
            "vitamin c": 10,
            "fiber": 1.8,
            "vitamin b6": 0.3,
            "magnesium": 20,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/170026/nutrients",
                title="USDA FoodData Central - Potatoes, boiled, cooked without skin",
                source_type="database"
            )
        ],
        effects=[
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Potassium",
                direction=EffectDirection.INCREASE,
                mechanism="Rich in potassium (379 mg/100g). One medium potato (167g) provides ~633 mg.",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/Potassium-HealthProfessional/",
                        title="Potassium Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED,
                notes="One of the best dietary sources of potassium."
            )
        ]
    )


def create_bell_pepper() -> Food:
    """
    Bell Pepper - excellent source of vitamin C.
    
    Nutrition per 100g (red, raw):
    - Vitamin C: 128 mg (very high)
    - Vitamin A: 157 mcg RAE
    - Folate: 46 mcg
    """
    return Food(
        name="Bell Pepper",
        name_de="Paprika",
        category="vegetable",
        nutrition_data={
            "calories": 31,
            "vitamin c": 128,
            "vitamin a": 157,
            "folate": 46,
            "vitamin b6": 0.3,
            "fiber": 2.1,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/170493/nutrients",
                title="USDA FoodData Central - Peppers, sweet, red, raw",
                source_type="database"
            )
        ],
        effects=[
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Vitamin C",
                direction=EffectDirection.INCREASE,
                mechanism="Excellent source of vitamin C (128 mg/100g). One medium pepper (~119g) provides ~152 mg (169% DV).",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/VitaminC-HealthProfessional/",
                        title="Vitamin C Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    ),
                    DataSource(
                        url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/170493/nutrients",
                        title="USDA FoodData Central - Red Bell Pepper",
                        source_type="database"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED,
                notes="One medium red bell pepper provides more vitamin C than an orange."
            )
        ]
    )


def create_kale() -> Food:
    """
    Kale - nutrient-dense leafy green.
    
    Nutrition per 100g (raw):
    - Vitamin K: 705 mcg (very high)
    - Vitamin C: 93 mg (high)
    - Calcium: 150 mg
    """
    return Food(
        name="Kale",
        name_de="Grünkohl",
        category="vegetable",
        nutrition_data={
            "calories": 35,
            "vitamin k": 705,
            "vitamin c": 93,
            "calcium": 150,
            "vitamin a": 241,
            "folate": 62,
            "fiber": 4.1,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/168421/nutrients",
                title="USDA FoodData Central - Kale, raw",
                source_type="database"
            )
        ],
        effects=[
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Vitamin K",
                direction=EffectDirection.INCREASE,
                mechanism="Extremely rich in vitamin K (705 mcg/100g). One cup chopped (67g) provides 472 mcg (525% DV).",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/VitaminK-HealthProfessional/",
                        title="Vitamin K Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED,
                notes="One of the highest vitamin K foods. Important for warfarin patients."
            ),
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Vitamin C",
                direction=EffectDirection.INCREASE,
                mechanism="Rich in vitamin C (93 mg/100g). One cup provides 62 mg.",
                sources=[
                    DataSource(
                        url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/168421/nutrients",
                        title="USDA FoodData Central - Kale",
                        source_type="database"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED
            ),
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Calcium",
                direction=EffectDirection.INCREASE,
                mechanism="Good source of calcium for a vegetable (150 mg/100g). One cup provides 100 mg.",
                sources=[
                    DataSource(
                        url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/168421/nutrients",
                        title="USDA FoodData Central - Kale",
                        source_type="database"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED
            )
        ]
    )


def create_broccoli() -> Food:
    """
    Broccoli - cruciferous vegetable rich in vitamin C and folate.
    
    Nutrition per 100g (raw):
    - Vitamin C: 89 mg (high)
    - Folate: 63 mcg
    - Vitamin K: 102 mcg
    - Fiber: 2.6 g
    """
    return Food(
        name="Broccoli",
        name_de="Brokkoli",
        category="vegetable",
        nutrition_data={
            "calories": 34,
            "vitamin c": 89,
            "folate": 63,
            "vitamin k": 102,
            "fiber": 2.6,
            "vitamin a": 31,
            "potassium": 316,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/170379/nutrients",
                title="USDA FoodData Central - Broccoli, raw",
                source_type="database"
            )
        ],
        effects=[
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Vitamin C",
                direction=EffectDirection.INCREASE,
                mechanism="Rich in vitamin C (89 mg/100g). One cup chopped (91g) provides 81 mg (90% DV).",
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
                mechanism="Good source of folate (63 mcg/100g). One cup provides 57 mcg.",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/Folate-HealthProfessional/",
                        title="Folate Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED
            )
        ]
    )
