"""
Dairy definitions with nutrition data and biomarker effects.

Sources:
- USDA FoodData Central: https://fdc.nal.usda.gov
- NIH Office of Dietary Supplements: https://ods.od.nih.gov
"""

from blutwerte.foods import (
    Food, FoodEffect, DataSource, EffectTargetType, EffectDirection,
    EffectCertainty
)


def create_milk() -> Food:
    """
    Milk - calcium and B12 source, vitamin D if fortified.
    
    Nutrition per 100g (whole milk):
    - Calcium: 113 mg
    - Vitamin B12: 0.4 mcg
    - Protein: 3.2 g
    - Vitamin D: 0.5 mcg (if fortified)
    - Riboflavin (B2): 0.2 mg
    """
    return Food(
        name="Milk",
        name_de="Milch",
        category="dairy",
        nutrition_data={
            "calories": 61,
            "calcium": 113,
            "vitamin b12": 0.4,
            "protein": 3.2,
            "vitamin d": 0.5,
            "vitamin b2": 0.2,
            "phosphorus": 91,
            "potassium": 132,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/171265/nutrients",
                title="USDA FoodData Central - Milk, whole, 3.25% milkfat",
                source_type="database"
            )
        ],
        effects=[
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Calcium",
                direction=EffectDirection.INCREASE,
                mechanism="Good source of calcium (113 mg/100g). One cup (244g) provides 276 mg (21% DV).",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/Calcium-HealthProfessional/",
                        title="Calcium Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    ),
                    DataSource(
                        url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/171265/nutrients",
                        title="USDA FoodData Central - Milk",
                        source_type="database"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED
            ),
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Vitamin B12",
                direction=EffectDirection.INCREASE,
                mechanism="Contains vitamin B12 (0.4 mcg/100g). One cup provides 1.1 mcg (46% DV).",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/VitaminB12-HealthProfessional/",
                        title="Vitamin B12 Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED,
                notes="Milk and dairy are important B12 sources, especially for vegetarians."
            ),
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Vitamin D",
                direction=EffectDirection.INCREASE,
                mechanism="Fortified milk contains vitamin D (0.5 mcg/100g). One cup provides 2.4 mcg (12% DV). Note: Only applies to fortified milk.",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/VitaminD-HealthProfessional/",
                        title="Vitamin D Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED,
                notes="Vitamin D content varies by fortification. Check product label."
            )
        ]
    )


def create_yogurt() -> Food:
    """
    Yogurt - calcium and protein with probiotics.
    
    Nutrition per 100g (plain, whole milk):
    - Calcium: 121 mg
    - Protein: 3.5 g
    - Vitamin B12: 0.4 mcg
    - Phosphorus: 95 mg
    """
    return Food(
        name="Yogurt",
        name_de="Joghurt",
        category="dairy",
        nutrition_data={
            "calories": 61,
            "calcium": 121,
            "protein": 3.5,
            "vitamin b12": 0.4,
            "phosphorus": 95,
            "potassium": 155,
            "vitamin b2": 0.1,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/171283/nutrients",
                title="USDA FoodData Central - Yogurt, plain, whole milk",
                source_type="database"
            )
        ],
        effects=[
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Calcium",
                direction=EffectDirection.INCREASE,
                mechanism="Good calcium source (121 mg/100g). One cup (245g) provides 296 mg (23% DV).",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/Calcium-HealthProfessional/",
                        title="Calcium Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED
            ),
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Vitamin B12",
                direction=EffectDirection.INCREASE,
                mechanism="Contains vitamin B12 (0.4 mcg/100g). One cup provides 1.0 mcg (42% DV).",
                sources=[
                    DataSource(
                        url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/171283/nutrients",
                        title="USDA FoodData Central - Yogurt",
                        source_type="database"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED
            )
        ]
    )


def create_cheddar() -> Food:
    """
    Cheddar cheese - concentrated calcium and protein.
    
    Nutrition per 100g:
    - Calcium: 721 mg (very high)
    - Protein: 25 g
    - Vitamin B12: 0.8 mcg
    - Phosphorus: 512 mg
    - Zinc: 3.1 mg
    """
    return Food(
        name="Cheddar Cheese",
        name_de="Cheddar Käse",
        category="dairy",
        nutrition_data={
            "calories": 403,
            "calcium": 721,
            "protein": 25,
            "vitamin b12": 0.8,
            "phosphorus": 512,
            "zinc": 3.1,
            "vitamin a": 100,
            "fat": 33,
        },
        nutrition_sources=[
            DataSource(
                url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/168917/nutrients",
                title="USDA FoodData Central - Cheese, cheddar",
                source_type="database"
            )
        ],
        effects=[
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Calcium",
                direction=EffectDirection.INCREASE,
                mechanism="Excellent calcium source (721 mg/100g). One slice (28g) provides 202 mg (16% DV).",
                sources=[
                    DataSource(
                        url="https://ods.od.nih.gov/factsheets/Calcium-HealthProfessional/",
                        title="Calcium Fact Sheet for Health Professionals - NIH",
                        source_type="guideline"
                    ),
                    DataSource(
                        url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/168917/nutrients",
                        title="USDA FoodData Central - Cheddar Cheese",
                        source_type="database"
                    )
                ],
                certainty=EffectCertainty.ESTABLISHED,
                notes="Cheese is one of the most calcium-dense foods."
            ),
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Vitamin B12",
                direction=EffectDirection.INCREASE,
                mechanism="Good B12 source (0.8 mcg/100g). One slice provides 0.2 mcg (8% DV).",
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
