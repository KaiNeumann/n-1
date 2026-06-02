# core Food System

Comprehensive food data system with nutrition information, biomarker effects, and source tracking for the core blood test analysis platform.

## Quick Start

```python
from core.foods import Food, FoodDatabase, gramm, scheibe
from core.foods.data import create_spinach, create_banana

# Load foods from database
db = FoodDatabase()
db.load_all()

# Get food by name
spinach = db.get("Spinach")

# Use portions
portion = spinach * gramm(100)  # 100g of spinach
portion = spinach * scheibe(2)   # 2 portions

# Check biomarker effects
effects = spinach.affects_biomarker("Vitamin K")
for effect in effects:
    print(f"{effect.target_name}: {effect.direction.value}")
    print(f"  Mechanism: {effect.mechanism}")
    print(f"  Sources: {len(effect.sources)} references")
```

## Features

- **25 Priority Foods**: Complete nutrition data and biomarker effects
- **Source Tracking**: All data includes references (USDA, NIH, research papers)
- **Biomarker Effects**: Documented effects on blood values (Vitamin K, Iron, etc.)
- **German Localization**: All foods have German names for patient-facing features
- **Portion System**: 28 portion types (scheibe, glas, portion, etc.)
- **Analysis Engine**: Analyze how food intake affects biomarkers
- **Flexible Importers**: Support for external data sources (Open Food Facts, BLS)

## Installation

The food system is included in core. No additional installation required.

```bash
# Optional: For Open Food Facts importer
pip install requests

# Optional: For testing
pip install pytest
```

## Core Concepts

### Food Model

```python
from core.foods import Food, DataSource, FoodEffect
from core.medications.models import EffectTargetType, EffectDirection

food = Food(
    name="Spinach",
    name_de="Spinat",
    category="vegetable",
    nutrition_data={
        "calories": 23,
        "vitamin k": 483,  # mcg per 100g
        "iron": 2.7,       # mg per 100g
    },
    nutrition_sources=[
        DataSource(
            url="https://fdc.nal.usda.gov/fdc_app.html#/food-details/168462/nutrients",
            title="USDA FoodData Central - Spinach",
            source_type="database"
        )
    ],
    effects=[
        FoodEffect(
            target_type=EffectTargetType.BIOMARKER,
            target_name="Vitamin K",
            direction=EffectDirection.INCREASE,
            mechanism="Rich in phylloquinone (vitamin K1)",
            sources=[...]
        )
    ]
)
```

### Food Effects

Effects document how foods influence biomarkers:

```python
# Simple established effect
FoodEffect(
    target_type=EffectTargetType.BIOMARKER,
    target_name="Vitamin K",
    direction=EffectDirection.INCREASE,
    mechanism="Rich in vitamin K1",
    sources=[...],
    certainty=EffectCertainty.ESTABLISHED
)

# Variable effect with modifiers
FoodEffect(
    target_type=EffectTargetType.BIOMARKER,
    target_name="Iron",
    direction=EffectDirection.VARIABLE,
    mechanism="Non-heme iron, absorption 2-20%",
    sources=[...],
    certainty=EffectCertainty.VARIABLE,
    modifiers=[
        EffectModifier(
            factor="vitamin_c_present",
            description="Enhances absorption 3-4x",
            impact="3-4x increase",
            direction="enhances"
        )
    ]
)
```

### Portion System

```python
from core.foods import gramm, scheibe, glas, portion

# Amount-based portions (weight in grams)
apple = apple * gramm(150)      # 150g
meat = meat * gramm(200)        # 200g

# Named portions
bread = bread * scheibe(2)      # 2 slices (2 x 25g = 50g)
juice = juice * glas(1)         # 1 glass (200ml)
steak = steak * portion(1)      # 1 portion (100g for meat category)

# Custom portion sizes
cheese.set_portion(scheibe, 30)  # Custom: 30g per slice for this cheese
cheese_portion = cheese * scheibe(1)  # Uses 30g, not default 20g
```

## Available Foods

### Vegetables (6)
- Spinach (Spinat) - Vitamin K↑, Iron↔, Folate↑
- Tomato (Tomate) - Potassium↑, Vitamin C↑
- Potato (Kartoffel) - Potassium↑, Vitamin C↑
- Bell Pepper (Paprika) - Vitamin C↑
- Kale (Grünkohl) - Vitamin K↑, Vitamin C↑, Calcium↑
- Broccoli (Brokkoli) - Vitamin C↑, Folate↑

### Fruits (4)
- Banana (Banane) - Potassium↑
- Orange (Orange) - Vitamin C↑, Folate↑
- Avocado (Avocado) - Potassium↑
- Strawberry (Erdbeere) - Vitamin C↑

### Proteins (6)
- Beef (Rindfleisch) - Iron↑, Vitamin B12↑
- Chicken Breast (Hähnchenbrust) - Vitamin B3↑, Vitamin B6↑
- Salmon (Lachs) - Vitamin D↑, Vitamin B12↑
- Egg (Ei) - Vitamin B12↑, Choline↑
- Lentils (Linsen) - Iron↔, Folate↑
- Tofu - Iron↔, Calcium↑

### Dairy (3)
- Milk (Milch) - Calcium↑, Vitamin B12↑, Vitamin D↑ (if fortified)
- Yogurt (Joghurt) - Calcium↑
- Cheddar Cheese (Cheddar Käse) - Calcium↑, Vitamin B12↑

### Grains (3)
- Oats (Hafer) - Iron↑
- Quinoa - Iron↑, Magnesium↑
- Brown Rice (Vollkornreis)

## Analysis

### FoodAnalyzer

```python
from core.foods import FoodAnalyzer, FoodIntake
from datetime import datetime

analyzer = FoodAnalyzer()

# Daily intake
intakes = [
    FoodIntake(spinach, 100, datetime.now()),
    FoodIntake(banana, 150, datetime.now()),
    FoodIntake(salmon, 120, datetime.now()),
]

# Analyze single biomarker
result = analyzer.analyze_biomarker("Vitamin K", intakes)
print(f"Net effect: {result.net_effect}")  # "increase", "decrease", "mixed", "neutral"
print(f"Contributions:")
for contrib in result.food_contributions:
    print(f"  - {contrib.food_name}: {contrib.estimated_impact.value}")

# Analyze all biomarkers
results = analyzer.analyze_daily_intake(intakes)
for biomarker, analysis in results.items():
    print(f"{biomarker}: {analysis.net_effect}")
```

### Comparing to RDI

```python
from core.foods import compare_to_rdi

# Check if intake meets RDI
intake_mg = 150  # mg of vitamin C
result = compare_to_rdi(intake_mg, "vitamin c")
print(f"Status: {result['status']}")  # "adequate", "below_minimum", "exceeds_maximum"
print(f"Percentage: {result.get('ref_percentage', 0):.1f}%")
```

## Importers

### Open Food Facts

```python
from core.foods.importers import OpenFoodFactsImporter

importer = OpenFoodFactsImporter()

# Look up by barcode
food = importer.lookup("3017620422003")
if food:
    print(f"Found: {food.name}")
    print(f"Nutrition: {food.nutrition_data}")

# Search by name
results = importer.search("chocolate", limit=5)
for food in results:
    print(f"- {food.name}")
```

### BLS (German Federal Food Key)

```python
from core.foods.importers import setup_bls_importer

# Requires local BLS database
importer = setup_bls_importer("/path/to/bls.db")

# Look up by BLS code
food = importer.lookup("B1001")
```

## Database

```python
from core.foods import FoodDatabase

db = FoodDatabase()

# Load all 25 priority foods
db.load_all()

# Or load specific modules
db.load_from_module("core.foods.data.vegetables")

# Query
food = db.get("Spinach")
food = db.get("Spinat")  # German name also works

# Search
results = db.search("vitamin")

# By category
vegetables = db.by_category("vegetable")
meats = db.by_category("meat")

# By biomarker effect
vitamin_k_foods = db.get_affecting_biomarker("Vitamin K")
iron_foods = db.get_affecting_biomarker("Iron")

# Rich in nutrient
iron_rich = db.get_rich_in_nutrient("iron", min_amount=2.0)
```

## Testing

```bash
# Run all food tests
pytest core/foods/tests/ -v

# Run specific test file
pytest core/foods/tests/test_models.py -v
pytest core/foods/tests/test_food_data.py -v

# Run with coverage
pytest core/foods/tests/ --cov=core.foods
```

## Architecture

```
core/foods/
├── __init__.py              # Public API exports
├── models.py                # Food, FoodEffect, FoodIntake
├── portions.py              # Portion system (28 portions)
├── rdi.py                   # RDI calculations with sources
├── database.py              # FoodDatabase with indexing
├── analysis.py              # FoodAnalyzer
├── sources.py               # DataSource tracking
├── data/                    # Food definitions
│   ├── __init__.py
│   ├── vegetables.py        # 6 vegetables
│   ├── fruits.py            # 4 fruits
│   ├── proteins/            # 6 proteins
│   ├── dairy.py             # 3 dairy
│   └── grains.py            # 3 grains
├── importers/               # External data importers
│   ├── __init__.py
│   ├── openfoodfacts.py
│   └── bls.py
└── tests/                   # Test suite
    ├── __init__.py
    ├── test_models.py
    ├── test_portions.py
    ├── test_database.py
    └── test_food_data.py
```

## Contributing

When adding new foods:

1. Use factory functions in appropriate data module
2. Include complete nutrition data per 100g
3. Add German name (name_de)
4. Add biomarker effects with sources
5. Use Title Case for biomarker names ("Vitamin K", "Iron")
6. Add tests for the new food

Example:

```python
def create_new_food() -> Food:
    return Food(
        name="Food Name",
        name_de="German Name",
        category="category",
        nutrition_data={
            "calories": 100,
            "nutrient": 50,
        },
        nutrition_sources=[
            DataSource(
                url="https://source.url",
                title="Source Title",
                source_type="database"
            )
        ],
        effects=[
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Biomarker Name",
                direction=EffectDirection.INCREASE,
                mechanism="How it works",
                sources=[...]
            )
        ]
    )
```

## Sources

All food data includes references to:
- **USDA FoodData Central**: https://fdc.nal.usda.gov
- **NIH Office of Dietary Supplements**: https://ods.od.nih.gov
- **DGE Referenzwerte**: https://www.dge.de/wissenschaft/referenzwerte/
- Research papers (PubMed)

## License

Part of the core project. See main project license.

## Migration from food_legacy

See `MIGRATION.md` for detailed migration guide from the legacy food system.
