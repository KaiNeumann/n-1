# FooDB Integration Summary

## Overview
We've created a complete FooDB (Food Database) integration system for enriching your food database with bioactive compound data and biomarker effects.

## What's FooDB?
- **Website**: https://foodb.ca/
- **Size**: 797 foods, 70,926 compounds, 5+ million associations
- **License**: Free for academic use (CC BY-NC 4.0), commercial license available
- **Contains**: Bioactive compounds with documented physiological and health effects

## Files Created

### 1. `blutwerte/foods/importers/foodb.py` - Main Importer
**Features:**
- Parse FooDB JSON, CSV, or MySQL dump files
- Query FooDB API (requires API key)
- Data models: `FooDBFood`, `FooDBCompound`, `FooDBContent`, `FooDBNutrient`
- Search foods by name
- Get compounds and nutrients for specific foods

**Usage:**
```python
from blutwerte.foods.importers import FooDBImporter

# Load data
importer = FooDBImporter()
importer.load_from_json("data/foodb/FooDB.json")

# Search
foods = importer.search_food("spinach")
print(f"Found {len(foods)} matching foods")
```

### 2. `blutwerte/foods/importers/foodb_mapping.py` - Biomarker Mapping
**Features:**
- Curated mappings of 15 compound classes to biomarkers
- Specific compound effects (Iron, B12, Folate, Omega-3s, etc.)
- `FooDBMapper` class for mapping compounds to effects
- Evidence levels (strong, moderate, emerging)

**Curated Mappings Include:**
- Flavonoids → CRP, IL-6, TNF-alpha (decrease inflammation)
- Phytosterols → LDL Cholesterol (decrease, 8-10% reduction)
- Catechins → LDL, Blood Pressure (decrease)
- Carotenoids → Vitamin A (increase)
- And 11 more classes...

**Usage:**
```python
from blutwerte.foods.importers import FooDBMapper

mapper = FooDBMapper()

# Get effects for compound class
effects = mapper.get_effects_for_compound_class("Flavonoids")
print(effects['biomarkers'])  # ['CRP', 'IL-6', 'TNF-alpha']

# Map food compounds to biomarkers
compounds = [
    {'name': 'Quercetin', 'klass': 'Flavonoids'},
    {'name': 'Beta-carotene', 'klass': 'Carotenoids'},
]
effects = mapper.map_food_compounds_to_effects(compounds)
```

### 3. `blutwerte/foods/importers/foodb_example.py` - Usage Examples
Complete examples showing:
- Download instructions
- Loading data
- Querying foods
- Mapping to biomarkers
- Enriching your foods with effects

## How to Use

### Step 1: Download FooDB Data
```bash
# Visit https://foodb.ca/downloads
# Download FooDB JSON file (~87 MB recommended)
# Extract to data/foodb/FooDB.json
```

### Step 2: Load and Query
```python
from blutwerte.foods.importers import FooDBImporter, FooDBMapper
from blutwerte.foods.models import FoodEffect

# Load data
importer = FooDBImporter()
importer.load_from_json("data/foodb/FooDB.json")

# Get statistics
stats = importer.get_statistics()
print(f"Loaded {stats['foods']} foods with {stats['compounds']} compounds")

# Search for food
food = importer.get_food("Spinach")
if food:
    print(f"{food.name} has {len(food.compounds)} compounds")
```

### Step 3: Enrich Your Foods
```python
# Map compounds to biomarker effects
mapper = FooDBMapper()

compounds = []
for content in food.compounds:
    compound = importer.compounds.get(content.source_id)
    if compound:
        compounds.append({
            'name': compound.name,
            'klass': compound.compound_class
        })

effects = mapper.map_food_compounds_to_effects(compounds)

# Convert to FoodEffect objects
for effect in effects:
    food_effect = FoodEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name=effect.biomarker_name,
        direction=EffectDirection.INCREASE if effect.effect_direction == "increase" else EffectDirection.DECREASE,
        mechanism=effect.mechanism,
        sources=[create_source(
            url="https://foodb.ca/",
            title=f"FooDB: {effect.compound_name}",
            source_type="database"
        )],
        certainty=EffectCertainty.ESTABLISHED
    )
    your_food.add_effect(food_effect)
```

## Available Compound-Biomarker Mappings

| Compound Class | Affected Biomarkers | Effect | Evidence |
|----------------|-------------------|---------|----------|
| Flavonoids | CRP, IL-6, TNF-alpha | Decrease | Strong |
| Anthocyanins | Blood Pressure, Nitric Oxide | Variable | Strong |
| Catechins | LDL Cholesterol, Oxidative Stress | Decrease | Strong |
| Carotenoids | Vitamin A, Antioxidant Status | Increase | Strong |
| Phenolic acids | Glucose, Insulin | Decrease | Moderate |
| Isoflavonoids | Estrogen, Bone Density | Variable | Moderate |
| Organosulfur compounds | Platelet Aggregation | Decrease | Moderate |
| Phytosterols | LDL Cholesterol (8-10% reduction) | Decrease | Strong |
| Tocopherols | Vitamin E, Oxidative Stress | Increase | Strong |
| Curcuminoids | CRP, Blood Glucose | Decrease | Strong |
| Capsaicinoids | Metabolism, Energy Expenditure | Increase | Moderate |
| Gingerols | Inflammation, Blood Sugar | Decrease | Moderate |
| Resveratrol | Oxidative Stress, Inflammation | Decrease | Moderate |
| Glucosinolates | Detoxification Enzymes | Increase | Moderate |
| Saponins | Cholesterol, Immune Function | Decrease | Emerging |

Plus specific mappings for:
- Iron, Vitamin B12, Folate, Vitamin D, Vitamin K
- Calcium, Magnesium, Zinc, Potassium
- EPA/DHA (Omega-3s), Dietary Fiber

## Next Steps

1. **Download FooDB data** from https://foodb.ca/downloads
2. **Test the importer** with example foods
3. **Enrich your 8,419 legacy foods** by:
   - Matching food names to FooDB
   - Extracting their compounds
   - Mapping to biomarker effects
   - Adding FoodEffect objects

4. **Optional**: Request API key for real-time queries

## API Access (Optional)

FooDB provides a REST API (requires key):
```python
importer = FooDBImporter(api_key="your_key")
result = importer.query_api("foods", {"food_name": "Apple", "page": 1})
```

Request API key: https://foodb.ca/w/contact

## Integration with Your Existing Foods

The importer can be used to automatically enrich your existing 8,419 foods by:
1. Name matching (exact or fuzzy)
2. Category matching
3. Scientific name matching

This would give you biomarker effects for foods based on their actual bioactive compound content!

## Data Quality

- **Strong evidence**: Well-established from multiple studies
- **Moderate evidence**: Good supporting research
- **Emerging evidence**: Promising preliminary research

All mappings include source tracking via FooDB references.
