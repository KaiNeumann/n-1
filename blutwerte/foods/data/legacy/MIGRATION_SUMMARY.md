# Legacy Food Migration Summary

## Migration Complete ✓

Successfully migrated **1,279 foods** from `food_legacy/` to the new `blutwerte.foods` system with full source tracking.

## Migration Statistics

| Source File | Foods Migrated | Data Source |
|-------------|----------------|-------------|
| food_bls.py | 74 | Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key |
| food_naehrwertdaten_ch.py | 1,092 | Swiss Food Composition Database |
| food_openfoodfacts_manual.py | 74 | Open Food Facts |
| food_other_manual.py | 31 | Various sources (USDA, etc.) |
| food_yazio_manual.py | 8 | Yazio Food Database |
| **TOTAL** | **1,279** | |

## What Was Converted

### Format Changes
- ✅ Legacy `Food({...})` → New `Food(...)` dataclass
- ✅ Legacy nutrient names (`vitamin_b1`) → Standard names (`vitamin b1`)
- ✅ Legacy units (all in grams) → Standard units (mg, mcg where appropriate)
- ✅ German food names preserved in `name_de` field
- ✅ Categories preserved (`set_category('...')`)
- ✅ Custom portions preserved (`portion(name, amount)`)
- ✅ **Source references added** with URLs, titles, and source types

### Example Conversion

**Legacy:**
```python
Hafer_Flocken = Food({'calories': 348.0, 'vitamin_b1': 0.00065, ...})
Hafer_Flocken.set_category('cereal')
Hafer_Flocken.portion(becher, 50)
```

**New:**
```python
def create_hafer_flocken() -> Food:
    return Food(
        name="Hafer Flocken",
        name_de="Hafer Flocken",
        category="cereal",
        nutrition_data={
            "calories": 348.0,
            "vitamin b1": 0.65,  # converted mg
            ...
        },
        nutrition_sources=[
            DataSource(
                url="https://blsdb.de/download",
                title="BLS 4.0 - German Federal Food Key",
                source_type="government"
            )
        ]
    ).set_portion(becher, 50)
```

## Usage

### Load All Legacy Foods

```python
from blutwerte.foods import FoodDatabase
from blutwerte.foods.data.legacy import load_legacy_foods_into_database

db = FoodDatabase()

# Load all 1,279 legacy foods
count = load_legacy_foods_into_database(db)
print(f"Loaded {count} foods")  # Loaded 1279 foods

# Now use normally
food = db.get("Hafer Flocken")
```

### Load Specific Legacy Sources

```python
from blutwerte.foods.data.legacy import food_bls_migrated

# Get BLS factory functions
factories = food_bls_migrated.__all__

# Create a specific food
oats = food_bls_migrated.create_hafer_flocken()
```

## Files Location

```
blutwerte/foods/data/legacy/
├── __init__.py                        # Package exports
├── food_bls_migrated.py              # 74 German foods
├── food_naehrwertdaten_ch_migrated.py # 1,092 Swiss foods
├── food_openfoodfacts_manual_migrated.py # 74 OFF foods
├── food_other_manual_migrated.py     # 31 other foods
├── food_yazio_migrated.py            # 8 Yazio foods
└── MIGRATION_SUMMARY.md              # This file
```

## Known Limitations

1. **Arithmetic Expressions**: Some legacy foods had calculations (e.g., `56.0/1000`) which couldn't be parsed automatically (19 foods skipped)
2. **No Biomarker Effects**: Legacy foods don't have biomarker effects - these would need to be added manually for high-priority foods
3. **German Names**: German food names are used for both `name` and `name_de` - English translations could be added later

## Next Steps

1. ✅ **Migrate complete** - All parseable foods migrated
2. 🔄 **Port importers** - Next: fddb, nutritionix, yazio importers
3. 🔄 **Add biomarker effects** - Manually add effects to high-priority legacy foods
4. 🔄 **Activities module** - Design as top-level entity alongside foods/medications

## Source References

All migrated foods include proper source attribution:

- **BLS**: `https://blsdb.de/download` - German Federal Food Key
- **Swiss**: `https://naehrwertdaten.ch` - Swiss Federal Food Safety Office
- **Open Food Facts**: `https://world.openfoodfacts.org` - Crowdsourced database
- **Yazio**: `https://www.yazio.com` - Nutrition tracking app
- **Other**: Mixed sources including USDA

## Data Quality

- ✅ All foods have complete nutrition data
- ✅ All foods have source references
- ✅ All foods have German names
- ✅ Unit conversions applied correctly
- ✅ Categories and portions preserved
- ⚠️ Some foods skipped due to arithmetic expressions (fixable)

---

*Migration completed: 2026-02-19*
*Total foods: 1,279*
*Migration script: `migrate_legacy_foods.py`*
