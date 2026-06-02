# ⚠️ ARCHIVED - Legacy Food and Nutrition Tracker

**STATUS: MIGRATED TO NEW SYSTEM**

This code has been migrated to `blutwerte/foods/` and is no longer maintained.

---

## 📦 Archive Contents

**Date Archived:** 2026-02-19  
**Migration Script:** `migrate_legacy_foods.py` (in project root)  
**Total Foods Migrated:** 8,419 → `blutwerte/foods/data/legacy/`  
**New System Location:** `blutwerte/foods/`

---

## ✅ Migration Status

### Fully Migrated to New System

All Python code files have been migrated with improvements:

| Legacy File | New Location | Status |
|-------------|--------------|---------|
| `Food.py` | `blutwerte/foods/models.py` | ✅ Migrated with source tracking |
| `nutriments.py` | `blutwerte/foods/rdi.py` | ✅ Enhanced with sources |
| `food_*.py` (7 files) | `blutwerte/foods/data/legacy/` | ✅ 8,419 foods migrated |
| `importers/*.py` (5 files) | `blutwerte/foods/importers/` | ✅ All importers ported |
| `health.py` | Integrated into models | ✅ Absorbed |
| `activities.py` | `blutwerte/activities/` | ✅ Activities module created |
| `convert_bls_to_python.py` | Migration complete | ✅ One-time use |

### Preserved Source Data

Original data files kept for reference:

- `original data/BLS_4_0_2025_DE.zip` - German BLS database
- `original data/BLS_4_0_Daten_2025_DE.xlsx` - BLS Excel file  
- `original data/naehrwertdaten_ch/` - Swiss database
- `original data/en.openfoodfacts.org.products.csv.zip` - OFF source

---

## 🚀 New System Benefits

### Before (Legacy)
- ❌ No source tracking
- ❌ Limited biomarker effects
- ❌ Mixed architecture patterns

### After (New System)
- ✅ **Source tracking**: Every food has DataSource references
- ✅ **Biomarker effects**: Foods document blood value impacts
- ✅ **Clean architecture**: Consistent dataclass patterns
- ✅ **8,444 total foods**: 25 priority + 8,419 legacy
- ✅ **Activities module**: Top-level exercise tracking
- ✅ **Comprehensive tests**: pytest suite

---

## 📖 Documentation

See new documentation:
- `blutwerte/foods/README.md` - Complete API docs
- `MIGRATION.md` - Migration guide
- `MIGRATION_COMPLETE.md` - Full summary
- `TODO.md` - Future enhancements

---

## 🔧 Using the New System

```python
# Old (this archive - DEPRECATED)
from Food import Food
from food_bls import Hafer_Flocken

# New (RECOMMENDED)
from blutwerte.foods import Food, FoodDatabase
from blutwerte.foods.data.legacy import load_legacy_foods_into_database

db = FoodDatabase()
db.load_all()  # 25 priority foods
count = load_legacy_foods_into_database(db)  # 8,419 legacy foods
print(f"Total: {db.count()} foods")  # 8,444
```

---

## 🗂️ Original Content Below

*The following is the original documentation preserved for reference only:*

---

# Food and Nutrition Tracker

A Python-based nutrition analysis system for tracking food intake, calculating nutritional values, and comparing against recommended daily intake (RDI) based on personal health profiles.

## Features

- **Nutritional Analysis**: Calculate calories, macronutrients, vitamins, and minerals for any food or recipe
- **RDI Comparison**: Compare your intake against age/sex-specific recommended daily values
- **Activity Tracking**: Calculate calorie burn based on activity profiles and metabolic rates
- **Recipe Composition**: Combine ingredients to create composite foods with automatically calculated nutrition
- **Flexible Portions**: Use predefined portions (glasses, slices, cups) or custom amounts
- **Multiple Data Sources**: Import data from Swiss nutrition database, Open Food Facts, Yazio, or manual entry
- **Plugin System**: Extensible importer architecture for easy addition of new food data sources
- **Smart Categorization**: Automatic food categorization with 99.9% coverage across 28 categories
- **Brand Recognition**: Auto-categorizes known brands (Lindt, Gerolsteiner, Flensburger, etc.)
- **Compound Word Parsing**: Understands German compound words (Apfelsaft, Apfelkuchen, etc.)

## Quick Start

```python
from Food import *
from food_other_manual import egg, butter
from food_openfoodfacts_manual import golden_toast

# Create a simple breakfast
breakfast = golden_toast * scheibe + butter * gramm(4) + egg * eins

# See total nutrition
print(breakfast)
# Output: Food({'calories': 315.75, 'fat': 18.9, ...}, 59)

# Compare against daily recommendations
print(breakfast.compare_with_rdi())
# Output: {'calories': '12.32%', 'protein': '25.12%', ...}
```

## Project Structure

```
Food-and-Nutrition/
├── Food.py                      # Core classes (Food, Day, Portion, Amount)
├── nutriments.py                # Nutrient definitions and RDI calculations
├── health.py                    # Health metrics (BMI, BMR) and activity profiles
├── activities.py                # Activity database with MET values
├── receipts.py                  # Recipe definitions
├── categorize_foods.py          # Food categorization helper (99.9% coverage)
├── convert_bls_to_python.py     # BLS 4.0 German database converter
├── test_importers.py            # Test suite for importers
├── importers/                   # Plugin-based food data importers
│   ├── __init__.py              # Plugin framework and registry
│   ├── bls.py                   # BLS 4.0 German database importer
│   ├── openfoodfacts.py         # Open Food Facts API importer
│   ├── nutritionix.py           # Nutritionix API importer
│   ├── fddb.py                  # FDDB.info text parser
│   └── yazio.py                 # Yazio.com text parser
├── food_naehrwertdaten_ch.py    # Swiss nutrition database (~1000 foods)
├── food_bls.py                  # Curated BLS German foods (~85 foods) 🆕
├── food_bls_german.py           # Full BLS 4.0 database (7140 foods) 🆕
├── food_openfoodfacts_manual.py # Open Food Facts products
├── food_yazio_manual.py         # Yazio nutrition data
└── food_other_manual.py         # Manual food entries
```

## Core Concepts

### Food Class

The `Food` class represents nutritional data per 100g. All operations maintain nutrition density:

```python
# Base food (nutrition per 100g)
apple = Food({'calories': 52, 'carbohydrate': 14, 'sugar': 10})

# Portion calculation (amounts in grams)
snack = apple * gramm(150)  # 150g of apple

# Division	half_portion = snack / 2

# Addition combines foods with weighted averages
meal = apple * gramm(100) + butter * gramm(10)
```

### Portion System

Use predefined portions or create custom ones:

```python
# Predefined portions
apple * gramm(150)      # 150 grams
milk * ml(200)          # 200 milliliters
beer * flasche          # 500ml (predefined)
bread * scheibe         # 25g slice (predefined)

# Custom portions per food
apple.portion(scheibe, 80)  # Define: 1 slice = 80g for this apple
snack = apple * scheibe     # Uses 80g
```

#### Category-Based Default Portions

Assign foods to categories for automatic portion sizing:

```python
from Food import Food, CategoryPortionDefaults

# Create food with category
beer = Food({'calories': 40, 'alcohol': 4.5}, category='beer')
# beer * flasche automatically uses 500ml (category default)

# Method chaining
bread = Food({'calories': 250}).set_category('bread')
# bread * scheibe automatically uses 25g

# Override category default for specific food
beer.portion(flasche, 330)  # This beer uses 330ml instead
```

**Predefined categories (28 total):**

| Category | Default Portion | Size | Description |
|----------|----------------|------|-------------|
| **beer** | flasche | 500ml | Alcoholic beers and beer-like beverages |
| **bread** | scheibe | 25g | Sliced bread, toast, baguettes, rolls |
| **cheese** | scheibe | 20g | All types of cheese (sliced portions) |
| **yogurt** | becher | 150g | Yogurt, quark, dairy desserts |
| **soup** | teller | 250g | Liquid soups and stews |
| **pasta** | teller | 210g | Spaghetti, noodles, pasta dishes |
| **water** | flasche | 750ml | Mineral water, sparkling water |
| **milk** | glas | 200ml | Dairy milk and plant-based milk alternatives |
| **meat** | portion | 100g | Chicken, beef, pork, game meats |
| **sausage** | stück | 50g | Sausages, wurst, cold cuts |
| **beverage** | flasche | 500ml | Soft drinks, juices, sodas (non-alcoholic) |
| **snack** | packung | 100g | Chips, crackers, nuts, chocolate bars |
| **spread** | esslöffel | 15g | Peanut butter, nutella, jams, cream cheese |
| **supplement** | tablette | 1g | Vitamins, probiotics, pills, powders |
| **fruit** | portion | 150g | Apples, bananas, berries, fresh fruit |
| **vegetable** | portion | 100g | Carrots, broccoli, salad, vegetables |
| **fish** | portion | 120g | Salmon, tuna, white fish |
| **cereal** | becher | 50g | Oats, muesli, breakfast cereals |
| **rice** | teller | 180g | Rice dishes and grains |
| **oil** | esslöffel | 10g | Cooking oils and fats |
| **sweet** | stück | 80g | Cakes, pastries, cookies, chocolate |
| **prepared** | packung | 400g | Ready meals, frozen dishes, mixed foods |
| **alcohol** | glas | 40ml | Wine, spirits, liquor (by the glass) |
| **legume** | becher | 80g | Beans, lentils, peas, chickpeas |
| **seafood** | portion | 100g | Shrimp, squid, mussels, crustaceans |
| **spices** | teelöffel | 5g | Salt, pepper, herbs, spices, seasonings |

Add custom category defaults:

```python
from Food import CategoryPortionDefaults, flasche

CategoryPortionDefaults.set("wine", flasche, 750)
# Now all wines with category='wine' will use 750ml for flasche
```

### RDI Comparison

Compare intake against personalized recommendations:

```python
# Get RDI for specific category
print(food.compare_with_rdi(category='main'))      # Main nutrients
print(food.compare_with_rdi(category='vitamins'))  # Vitamins only

# Compare over multiple days
print(food.compare_with_rdi(days=7))  # Weekly intake
```

### Activity Profiles

Calculate calorie burn based on daily activities:

```python
from health import Activity_profile

# Define daily activities
profile = Activity_profile({
    'sleeping': 7,
    'desk work (sitting)': 8,
    'walking (brisk pace)': 1,
    'cycling (moderate)': 0.5
})

# Calculate daily burn
daily_burn = profile.get_kcal({'age': 35, 'sex': 'male', 'weight': 80})

# Compare with food intake
food.compare_with_activity_profile(profile)
```

### Day Tracking

Track full days with food and activities:

```python
from Food import Day

# Create a day
day = Day('2024-01-15',
    breakfast,
    lunch,
    dinner,
    Activity_profile({...})
)

# Get calorie balance
print(day.calorie_balance())

# Check RDI compliance
print(day.compare_with_rdi())
```

## Creating Recipes

Define composite foods in `receipts.py`:

```python
# receipts.py
from Food import *
from food_naehrwertdaten_ch import *

ofenkartoffeln = Food().add(
    Kartoffel_geschält_roh * gramm(1000),
    Olivenöl * ml(50),
    Paprika_Gewürz * gramm(2),
    Food({'salt': 100}) * gramm(1)
)
ofenkartoffeln.portion(stück, 50)  # 1 piece = 50g
```

## Plugin System: Food Importers

The system includes an extensible plugin architecture for importing food data from various sources.

### Using Importers

```python
from importers import get_importer, list_importers

# List available importers
print(list_importers())  # ['openfoodfacts', 'nutritionix', 'fddb', 'yazio']

# Lookup by barcode (Open Food Facts)
off = get_importer("openfoodfacts")
food = off.lookup("4053400205298")

# Search products
results = off.search("apple", limit=5)

# Parse text from FDDB
fddb = get_importer("fddb")
food = fddb.parse("""
Kalorien
52 kcal
Protein
0,3 g
""")

# Search German BLS database (7,140 foods)
bls = get_importer("bls")
results = bls.search("Apfel", limit=5)  # Search for apple
for food_info in results:
    print(f"{food_info['name']} ({food_info['id']})")

# Lookup specific food from BLS by code
food = bls.lookup("BLS_0")  # Get first food (Hafer)
print(f"Calories: {food.nutrition_data.get('calories')} kcal")

# Natural language lookup (Nutritionix - requires API key)
nix = get_importer("nutritionix")
nix.app_id = "your_app_id"
nix.app_key = "your_app_key"
food = nix.lookup("1 large grilled chicken breast")
```

### Available Importers

| Importer | Type | Lookup | Search | Parse | Credentials |
|----------|------|--------|--------|-------|-------------|
| **openfoodfacts** | API | ✓ | ✓ | ✗ | None |
| **nutritionix** | API | ✓ (natural language) | ✗ | ✗ | App ID + Key |
| **fddb** | Parser | ✗ | ✗ | ✓ | None |
| **yazio** | Parser | ✗ | ✗ | ✓ | None |
| **bls** | Database | ✓ | ✓ | ✗ | None (Excel file) |

### Creating Custom Importers

Add new data sources by creating a module in `importers/`:

```python
# importers/my_source.py
from importers import FoodImporter, register_importer
from Food import Food

@register_importer
class MySourceImporter(FoodImporter):
    @property
    def name(self):
        return "my_source"
    
    @property
    def display_name(self):
        return "My Data Source"
    
    @property
    def supports_lookup(self):
        return True
    
    def lookup(self, identifier):
        # Fetch data from your source
        nutrition_data = {...}  # Dict of nutrients per 100g
        return Food(nutrition_data, 100)
```

The importer auto-registers and becomes available immediately:

```python
from importers import get_importer
source = get_importer("my_source")
food = source.lookup("item_id")
```

## Adding New Foods

### Option 1: Manual Entry

Add to `food_other_manual.py`:

```python
my_food = Food({
    'calories': 120,
    'protein': 5,
    'fat': 3,
    'carbohydrate': 18,
    'fiber': 2
})
my_food.portion(packung, 250)  # Define package size
```

### Option 2: Import BLS 4.0 (German Database)

The German Bundeslebensmittelschlüssel (BLS) 4.0 with 7,140 foods is included:

```python
# Import German BLS database
from food_bls_german import *

# Use German foods
breakfast = Hafer_Flocken * gramm(50) + Milch * ml(200)
```

**To update from latest BLS release:**
```bash
# 1. Download from https://blsdb.de/download
# 2. Extract BLS_4_0_Daten_2025_DE.xlsx
# 3. Run converter
python convert_bls_to_python.py
```

### Option 3: Import from CSV

Convert CSV data to Python (see `convert_csv_to_python.ipynb` for examples).

## Food Categorization Helper

The system includes an intelligent categorization helper that automatically suggests categories for foods based on their names.

### Coverage Statistics

- **1,226 foods** analyzed across all databases
- **99.9% auto-categorized** (1,225 foods)
- **Only 1 food** requires manual review

### How It Works

The categorization system uses multiple strategies:

1. **Brand Recognition** - Identifies 17+ major brands (Lindt, Gerolsteiner, Flensburger, etc.)
2. **Keyword Matching** - 300+ food-specific keywords with UTF-8 support for German umlauts
3. **Compound Word Decomposition** - Parses German compound words:
   - `Apfelsaft` → fruit + beverage = **beverage**
   - `Apfelkuchen` → fruit + cake = **sweet**
   - `Gemüsegratin` → vegetable + gratin = **prepared**
4. **Preparation Method Detection** - Recognizes suffixes:
   - `_roh` (raw), `_gedämpft` (steamed), `_gekocht` (cooked)
   - `_zubereitet` (prepared), `_konserve` (canned)
5. **Exclusion Patterns** - Prevents false positives (e.g., "wein" in "Schwein" ≠ alcohol)

### Using the Helper

```bash
# Analyze all food files and suggest categories
python categorize_foods.py

# Show categorization statistics
python categorize_foods.py --stats

# Check specific files
python categorize_foods.py food_naehrwertdaten_ch.py
```

### Example Output

```
CATEGORIZATION STATISTICS
======================================================================
Total foods analyzed: 1226
Categorized: 1225 (99.9%)
Uncategorized: 1 (0.1%)

Breakdown by category:
  meat: 175 (14.3%)
  vegetable: 142 (11.6%)
  prepared: 166 (13.5%)
  ...
```

The helper suggests exact code to add:
```python
# For each uncategorized food, it shows:
Schwein_Filet.set_category('meat')
Lindt_Schokolade.set_category('sweet')
Gerolsteiner_Wasser.set_category('water')
```

### Adding New Categories

Extend the system by editing `categorize_foods.py`:

```python
# Add new keywords to existing categories
CATEGORY_KEYWORDS['fruit'].extend(['exotic_fruit', 'dragonfruit'])

# Add a new category
CATEGORY_KEYWORDS['superfood'] = ['chia', 'quinoa', 'kale', 'acai']
CategoryPortionDefaults.set("superfood", becher, 50)

# Add brand mappings
BRAND_CATEGORIES['new_brand'] = 'category_name'

# Add compound word suffixes
COMPOUND_SUFFIXES['smoothie'] = 'beverage'
```

## Available Nutrients

The system tracks 80+ nutrients including:

**Macronutrients:** calories, protein, carbohydrate, fat, fiber, sugar, starch

**Fats:** saturated fat, monounsaturated fat, polyunsaturated fat, omega-3, omega-6, trans fat

**Vitamins:** A, B1, B2, B3, B5, B6, B7, B9, B12, C, D, E, K

**Minerals:** calcium, iron, magnesium, phosphorus, potassium, sodium, zinc, iodine, selenium

**Other:** cholesterol, caffeine, alcohol, water

## Health Profile Options

Customize RDI calculations with body parameters:

```python
options = {
    'age': 35,              # years
    'sex': 'male',          # 'male' or 'female'
    'height': 180,          # cm
    'weight': 80,           # kg
    'is_pregnant': False,
    'is_lactating': False,
    'is_smoker': False,
    'hypertension': False,
    'lifestyle': 'moderately active',  # sedentary, moderately active, vigorously active
    'diet': 'balanced'       # meat centric, balanced, vegan or vegetarian
}
```

## Data Sources

### Integrated Databases (Manual)
- **[naehrwertdaten.ch](https://naehrwertdaten.ch)**: Swiss Federal Food Safety and Veterinary Office (~1000 foods)
- **[BLS 4.0](https://blsdb.de)**: German Federal Food Key (Bundeslebensmittelschlüssel) - **7,140 foods** 🆕
  - Curated selection: `food_bls.py` (~85 popular German foods with categories)
  - Full database: Use importer plugin or `food_bls_german.py` (7,140 foods)
- **Manual entries**: `food_openfoodfacts_manual.py`, `food_yazio_manual.py`, `food_other_manual.py`
- **Total foods**: 8,300+ foods across all databases, 99.9% auto-categorized

### Dynamic Importers (Plugin System)
- **[BLS 4.0](https://blsdb.de)**: German Federal Food Key - 7,140 foods via plugin (search + lookup)
- **[Open Food Facts](https://world.openfoodfacts.org)**: Crowd-sourced global food database (barcode lookup + search)
- **[Nutritionix](https://developer.nutritionix.com)**: Natural language food lookup (requires free API key)
- **[FDDB.info](https://fddb.info)**: German nutrition database (text parser)
- **[Yazio](https://www.yazio.com)**: Nutrition tracking platform (text parser)

Add new sources via the plugin system (see [Plugin System](#plugin-system-food-importers) section).

## Requirements

- Python 3.7+
- Core functionality: No external dependencies (stdlib only)
- API importers: `requests` library (optional, for Open Food Facts and Nutritionix)

Install optional dependencies:
```bash
pip install requests
```

## Testing

Run the test suite to verify all components are working:

```bash
# Test the importer plugin system
python test_importers.py

# Test food categorization coverage
python categorize_foods.py --stats
```

This will:
- List all registered importers
- Test text parsers with example data
- Show categorization coverage across all food databases
- Display category distribution statistics

## License

Personal project for nutritional analysis and meal planning.
