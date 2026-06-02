# Food System Migration Guide

## Overview

This guide documents the migration from `food_legacy/` to the new `blutwerte/foods/` system. The new system provides improved architecture, source tracking, biomarker effects, and integration with the existing Blutwerte medication analysis.

## What's New

### Key Improvements

1. **Source Tracking**: All food effects and nutrition data now include source references (URLs, DOIs)
2. **Biomarker Effects**: Foods now document how they affect blood values (Vitamin K, Iron, etc.)
3. **Effect Modifiers**: Variable effects (like iron absorption) include detailed modifiers
4. **Unified Naming**: Consistent Title Case for biomarkers ("Vitamin K", "Iron", "Folic Acid")
5. **Internal UUIDs**: All foods have internal UUIDs for reliable identification
6. **German Localization**: All foods have German names (name_de) for patient-facing features
7. **Flexible Importers**: Importer system supports both Food objects and raw dict format
8. **Comprehensive Testing**: Full test suite with pytest

## Migration Status

### Phase 1: Infrastructure ✓ COMPLETE
- [x] Created `foods/` directory structure
- [x] Ported portion system (28 portion types)
- [x] Created base models with source tracking
- [x] Implemented RDI calculations with DGE/WHO/FDA sources
- [x] Created FoodDatabase with indexing

### Phase 2: Core Foods ✓ COMPLETE
- [x] Defined 25 priority foods with complete nutrition data
- [x] Added biomarker effects to all relevant foods
- [x] All foods have German names
- [x] All foods have source references

### Phase 3: Analysis Engine ✓ COMPLETE
- [x] Basic FoodAnalyzer implementation
- [x] Impact level estimation
- [x] Net effect calculation
- [x] Recommendation generation

### Phase 4: Importers ✓ COMPLETE (Basic Implementation)
- [x] Base importer interface
- [x] Open Food Facts importer (functional)
- [x] BLS importer (placeholder - requires database)

### Phase 5: Documentation ✓ COMPLETE
- [x] API documentation (README.md)
- [x] Migration guide (this file)
- [x] Comprehensive test suite

### Future Enhancements (Post-MVP)
- [ ] Add remaining 100 high-impact foods
- [ ] Unified medication+food analysis
- [ ] Port BLS importer with full database
- [ ] Comprehensive migration of 8,000+ foods
- [ ] Delete food_legacy/ directory

## API Changes

### Import Changes

**Old:**
```python
from Food import Food
from nutriments import get_rdi
```

**New:**
```python
from blutwerte.foods import Food, FoodDatabase, get_rdi
from blutwerte.foods.data import create_spinach, create_banana
```

### Food Creation

**Old:**
```python
apple = Food({'calories': 52, 'sugar': 10})
apple.set_category('fruit')
```

**New:**
```python
# Using factory functions (recommended)
from blutwerte.foods.data.fruits import create_apple
apple = create_apple()

# Or manual creation
from blutwerte.foods import Food, DataSource
apple = Food(
    name="Apple",
    name_de="Apfel",
    category="fruit",
    nutrition_data={'calories': 52, 'sugar': 10},
    nutrition_sources=[
        DataSource(
            url="https://fdc.nal.usda.gov/...",
            title="USDA FoodData Central",
            source_type="database"
        )
    ]
)
```

### Portion System

**Old:**
```python
from Food import gramm, scheibe, Food
apple = Food({'calories': 52})
apple = apple * gramm(100)
```

**New:**
```python
from blutwerte.foods import Food, gramm, scheibe
apple = Food(name="Apple", name_de="Apfel", nutrition_data={'calories': 52})
apple = apple * gramm(100)  # Same interface!
```

### Mathematical Operations

**Old:**
```python
meal = apple + banana
calories = meal.nutrition_data.get('calories', 0) * meal.weight / 100
```

**New:**
```python
meal = apple + banana  # Same interface!
nutrients = meal.get_all_nutrients()
calories = nutrients.get('calories', 0)
```

## Biomarker Effects

### New Feature: Effect Tracking

Foods can now document how they affect biomarkers:

```python
from blutwerte.foods import Food, FoodEffect, DataSource
from blutwerte.medications.models import EffectTargetType, EffectDirection

spinach = Food(
    name="Spinach",
    effects=[
        FoodEffect(
            target_type=EffectTargetType.BIOMARKER,
            target_name="Vitamin K",  # Use Title Case
            direction=EffectDirection.INCREASE,
            mechanism="Rich in phylloquinone (vitamin K1)",
            sources=[
                DataSource(
                    url="https://ods.od.nih.gov/factsheets/VitaminK-HealthProfessional/",
                    title="Vitamin K Fact Sheet",
                    source_type="guideline"
                )
            ]
        )
    ]
)

# Check effects
vitamin_k_effects = spinach.affects_biomarker("Vitamin K")
```

### Variable Effects with Modifiers

For effects that depend on context (like iron absorption):

```python
from blutwerte.foods import EffectModifier, EffectCertainty

FoodEffect(
    target_type=EffectTargetType.BIOMARKER,
    target_name="Iron",
    direction=EffectDirection.VARIABLE,  # Not just INCREASE
    mechanism="Contains non-heme iron. Absorption: 2-20%",
    sources=[...],
    certainty=EffectCertainty.VARIABLE,
    modifiers=[
        EffectModifier(
            factor="vitamin_c_present",
            description="Vitamin C enhances absorption 3-4 fold",
            impact="3-4x increase",
            direction="enhances"
        ),
        EffectModifier(
            factor="tannins_present",
            description="Tannins inhibit absorption",
            impact="Significant reduction",
            direction="inhibits"
        )
    ]
)
```

## Food Database

### Using the Database

```python
from blutwerte.foods import FoodDatabase

db = FoodDatabase()

# Load all 25 priority foods
db.load_all()

# Get food by name
spinach = db.get("Spinach")
spinach = db.get("Spinat")  # Also works with German names

# Search
results = db.search("vitamin k")

# Get by category
vegetables = db.by_category("vegetable")

# Get foods affecting a biomarker
vitamin_k_foods = db.get_affecting_biomarker("Vitamin K")
```

## Analysis Engine

### Analyzing Food Effects

```python
from blutwerte.foods import FoodAnalyzer, FoodIntake
from datetime import datetime

analyzer = FoodAnalyzer()

# Create daily intake
intakes = [
    FoodIntake(spinach, 100, datetime.now()),
    FoodIntake(banana, 150, datetime.now()),
]

# Analyze single biomarker
result = analyzer.analyze_biomarker("Vitamin K", intakes)
print(result.net_effect)  # "increase", "decrease", "mixed", or "neutral"

# Analyze all biomarkers from intake
results = analyzer.analyze_daily_intake(intakes)
for biomarker, analysis in results.items():
    print(f"{biomarker}: {analysis.net_effect}")
```

## Importers

### Open Food Facts

```python
from blutwerte.foods.importers import OpenFoodFactsImporter

importer = OpenFoodFactsImporter()

# Look up by barcode
food = importer.lookup("3017620422003")  # Nutella

# Search by name
results = importer.search("chocolate", limit=5)
```

### BLS (German Federal Food Key)

```python
from blutwerte.foods.importers import BLSImporter, setup_bls_importer

# Requires local BLS database
importer = setup_bls_importer("/path/to/bls.db")
food = importer.lookup("B1001")
```

## Testing

### Running Tests

```bash
# Run all food tests
pytest blutwerte/foods/tests/ -v

# Run specific test file
pytest blutwerte/foods/tests/test_models.py -v

# Run with coverage
pytest blutwerte/foods/tests/ --cov=blutwerte.foods -v
```

## Backward Compatibility

### Portion System
The portion system maintains full backward compatibility:
- All 28 portions from food_legacy are available
- Same API: `food * gramm(100)`
- Category defaults preserved

### Food Operations
- `food * quantity` - Same
- `food + other` - Same (nutrition weighted average)
- `food / divisor` - Same

### Migration Path
1. Use new import paths
2. Add source references to existing foods
3. Gradually migrate to factory functions
4. Add biomarker effects where applicable

## Known Limitations

1. **BLS Importer**: Requires local database setup
2. **Open Food Facts**: Requires internet connection and `requests` package
3. **25 Foods Only**: Full migration of 8,000+ foods pending
4. **Analysis**: Recommendation engine is basic (will be enhanced)

## Getting Help

- **API Reference**: See `blutwerte/foods/README.md`
- **Test Examples**: See `blutwerte/foods/tests/`
- **Food Definitions**: See `blutwerte/foods/data/`

## Changelog

### v1.0.0 (Current)
- Initial release
- 25 priority foods with complete data
- Source tracking for all effects
- Biomarker effect documentation
- Analysis engine
- Importer framework
- Comprehensive test suite
