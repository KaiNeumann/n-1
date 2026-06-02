"""
Migration script to convert legacy food files to new blutwerte.foods format.

This script parses legacy food_legacy/*.py files and converts them to the new
Food dataclass format with proper source tracking.

Usage:
    python migrate_legacy_foods.py
"""

import re
import ast
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Nutrient name mapping (old -> new)
NUTRIENT_MAP = {
    'calories': 'calories',
    'water': 'water',
    'protein': 'protein',
    'fat': 'fat',
    'carbohydrate': 'carbohydrate',
    'sugar': 'sugar',
    'starch': 'starch',
    'fiber': 'fiber',
    'sodium': 'sodium',
    'potassium': 'potassium',
    'calcium': 'calcium',
    'magnesium': 'magnesium',
    'phosphorus': 'phosphorus',
    'iron': 'iron',
    'zinc': 'zinc',
    'manganese': 'manganese',
    'copper': 'copper',
    'selenium': 'selenium',
    'iodine': 'iodine',
    'vitamin_a': 'vitamin a',
    'provitamin_a': 'provitamin a',
    'vitamin_b1': 'vitamin b1',
    'vitamin_b2': 'vitamin b2',
    'vitamin_b3': 'vitamin b3',
    'vitamin_b5': 'vitamin b5',
    'vitamin_b6': 'vitamin b6',
    'vitamin_b7': 'vitamin b7',
    'vitamin_b9': 'vitamin b9',
    'folate': 'folate',
    'vitamin_b12': 'vitamin b12',
    'vitamin_c': 'vitamin c',
    'vitamin_d': 'vitamin d',
    'vitamin_e': 'vitamin e',
    'vitamin_k': 'vitamin k',
    'cholesterol': 'cholesterol',
    'salt': 'salt',
    'alcohol': 'alcohol',
    'saturated_fat': 'saturated fat',
    'monounsaturated_fat': 'monounsaturated fat',
    'polyunsaturated_fat': 'polyunsaturated fat',
    'omega_3': 'omega 3',
    'omega_6': 'omega 6',
}

# Unit conversions (legacy values -> standard units)
# Legacy uses grams for everything, need to convert vitamins/minerals to mg/mcg
UNIT_CONVERSIONS = {
    'vitamin a': (1000000, 'mcg'),  # g -> mcg
    'provitamin a': (1000000, 'mcg'),
    'vitamin b1': (1000, 'mg'),
    'vitamin b2': (1000, 'mg'),
    'vitamin b3': (1000, 'mg'),
    'vitamin b5': (1000, 'mg'),
    'vitamin b6': (1000, 'mg'),
    'vitamin b7': (1000, 'mg'),
    'vitamin b9': (1000, 'mg'),
    'folate': (1000, 'mcg'),
    'vitamin b12': (1000000, 'mcg'),
    'vitamin c': (1000, 'mg'),
    'vitamin d': (1000000, 'mcg'),
    'vitamin e': (1000, 'mg'),
    'vitamin k': (1000, 'mcg'),
    'sodium': (1000, 'mg'),
    'potassium': (1000, 'mg'),
    'calcium': (1000, 'mg'),
    'magnesium': (1000, 'mg'),
    'phosphorus': (1000, 'mg'),
    'iron': (1000, 'mg'),
    'zinc': (1000, 'mg'),
    'manganese': (1000, 'mg'),
    'copper': (1000, 'mg'),
    'selenium': (1000000, 'mcg'),
    'iodine': (1000000, 'mcg'),
    'cholesterol': (1000, 'mg'),
}

# Source configurations per file
FILE_SOURCES = {
    'food_bls.py': {
        'url': 'https://blsdb.de/download',
        'title': 'Bundeslebensmittelschlüssel (BLS) 4.0 - German Federal Food Key',
        'source_type': 'government',
        'citation': 'Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0',
    },
    'food_bls_german.py': {
        'url': 'https://blsdb.de/download',
        'title': 'Bundeslebensmittelschlüssel (BLS) 4.0 - Complete Database (7,140 foods)',
        'source_type': 'government',
        'citation': 'Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0 - Complete Database',
    },
    'food_naehrwertdaten_ch.py': {
        'url': 'https://naehrwertdaten.ch',
        'title': 'Swiss Food Composition Database',
        'source_type': 'government',
        'citation': 'Federal Food Safety and Veterinary Office (FSVO), Switzerland',
    },
    'food_openfoodfacts_manual.py': {
        'url': 'https://world.openfoodfacts.org',
        'title': 'Open Food Facts Database',
        'source_type': 'database',
    },
    'food_yazio_manual.py': {
        'url': 'https://www.yazio.com',
        'title': 'Yazio Food Database',
        'source_type': 'database',
    },
    'food_other_manual.py': {
        'url': 'https://fdc.nal.usda.gov',
        'title': 'USDA FoodData Central & Various Sources',
        'source_type': 'database',
    },
}


def convert_name_to_readable(name: str) -> Tuple[str, str]:
    """
    Convert Python variable name to readable English and German names.
    
    Examples:
        Hafer_Flocken -> ("Hafer Flocken", "Hafer Flocken")
        Milch_voll -> ("Vollmilch", "Vollmilch")
    """
    # Replace underscores with spaces
    readable = name.replace('_', ' ')
    
    # German food names are typically the same or very similar
    # For now, use the same name for both (can be refined later)
    name_de = readable
    
    return readable, name_de


def convert_nutrients(nutrition_data: Dict[str, float]) -> Dict[str, float]:
    """Convert nutrient names and units from legacy format."""
    converted = {}
    
    for old_name, value in nutrition_data.items():
        # Map nutrient name
        new_name = NUTRIENT_MAP.get(old_name, old_name)
        
        # Apply unit conversion if needed
        if new_name in UNIT_CONVERSIONS:
            multiplier, unit = UNIT_CONVERSIONS[new_name]
            value = value * multiplier
        
        converted[new_name] = round(value, 4)  # Round to avoid floating point issues
    
    return converted


def parse_food_legacy_file(filepath: Path) -> List[Dict[str, Any]]:
    """
    Parse a legacy food file and extract food definitions.
    
    Returns list of dicts with:
        - name: Variable name
        - name_de: German name
        - nutrition_data: Dict of nutrients
        - category: Food category
        - portions: List of (portion_name, amount) tuples
    """
    foods = []
    content = filepath.read_text(encoding='utf-8')
    
    # Find all Food(...) assignments
    # Pattern: VarName = Food({...})  # optional comment with food name
    food_pattern = r'^(\w+)\s*=\s*Food\((\{[^}]+\})\)(?:\s*#\s*(.+))?$'
    
    for match in re.finditer(food_pattern, content, re.MULTILINE):
        var_name = match.group(1)
        dict_str = match.group(2)
        comment = match.group(3)  # Optional comment with actual food name
        
        try:
            # Parse the nutrition dict
            nutrition_data = ast.literal_eval(dict_str)
            
            # Use comment as food name if available, otherwise use variable name
            food_name = comment.strip() if comment else var_name.replace('_', ' ')
            
            food_info = {
                'var_name': var_name,
                'name_en': food_name,
                'name_de': food_name,
                'nutrition_data': nutrition_data,
                'category': None,
                'portions': [],
            }
            
            # Look for .set_category() call after this food
            category_pattern = rf'{var_name}\.set_category\([\'"](\w+)[\'"]\)'
            cat_match = re.search(category_pattern, content[match.end():match.end()+500])
            if cat_match:
                food_info['category'] = cat_match.group(1)
            
            # Look for .portion() calls
            portion_pattern = rf'{var_name}\.portion\((\w+),\s*(\d+)\)'
            for portion_match in re.finditer(portion_pattern, content):
                portion_name = portion_match.group(1)
                amount = int(portion_match.group(2))
                food_info['portions'].append((portion_name, amount))
            
            foods.append(food_info)
            
        except Exception as e:
            print(f"Warning: Could not parse {var_name}: {e}")
            continue
    
    return foods


def generate_food_factory(food: Dict[str, Any], source_config: Dict[str, str]) -> str:
    """Generate a factory function for a food."""
    
    name_en = food['name_en']
    name_de = food['name_de']
    var_name = food['var_name']
    
    # Convert nutrients
    nutrition_data = convert_nutrients(food['nutrition_data'])
    
    # Format nutrition data
    nutrition_str = '\n        '.join([
            f'"{k}": {v},'
        for k, v in nutrition_data.items() if v > 0  # Skip zero values
    ])
    
    # Format portions
    portions_str = ''
    if food['portions']:
        portions_str = '\n        '.join([
            f'.set_portion({name}, {amount})'
        for name, amount in food['portions']
        ])
        portions_str = '\n        ' + portions_str
    
    # Format category
    category_str = f'"{food["category"]}"' if food['category'] else 'None'
    
    factory = f'''\ndef create_{var_name.lower()}() -> Food:
    """
    {name_en}
    
    Source: {source_config.get('citation', source_config['title'])}
    """
    return Food(
        name="{name_en}",
        name_de="{name_de}",
        category={category_str},
        nutrition_data={{
        {nutrition_str}
        }},
        nutrition_sources=[
            DataSource(
                url="{source_config['url']}",
                title="{source_config['title']}",
                source_type="{source_config['source_type']}"
            )
        ]
    ){portions_str}
'''
    
    return factory


def migrate_file(input_path: Path, output_path: Path, source_config: Dict[str, str]):
    """Migrate a single legacy food file."""
    print(f"Migrating {input_path.name}...")
    
    foods = parse_food_legacy_file(input_path)
    print(f"  Found {len(foods)} foods")
    
    # Generate output
    output_lines = [
        '"""',
        f'Migrated from {input_path.name}',
        '',
        f'Source: {source_config.get("citation", source_config["title"])}',
        f'URL: {source_config["url"]}',
        '"""',
        '',
        'from blutwerte.foods import Food, DataSource',
        '',
    ]
    
    for food in foods:
        factory = generate_food_factory(food, source_config)
        output_lines.append(factory)
    
    # Write exports
    output_lines.append('\n__all__ = [')
    for food in foods:
        output_lines.append(f'    "create_{food["var_name"].lower()}",')
    output_lines.append(']\n')
    
    output_path.write_text('\n'.join(output_lines), encoding='utf-8')
    print(f"  Written to {output_path}")


def main():
    """Main migration function."""
    # Get the project root directory
    base_dir = Path(__file__).parent  # D:\Personal Data\Kai Uwe\Documents\Kai\projects\Blutwerte
    food_legacy_dir = base_dir / 'food_legacy'
    output_dir = base_dir / 'blutwerte' / 'foods' / 'data' / 'legacy'
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Files to migrate
    files_to_migrate = [
        'food_bls.py',
        'food_bls_german.py',  # Full BLS database (7,140 foods)
        'food_naehrwertdaten_ch.py',
        'food_openfoodfacts_manual.py',
        'food_other_manual.py',
        'food_yazio_manual.py',
    ]
    
    total_foods = 0
    
    for filename in files_to_migrate:
        input_path = food_legacy_dir / filename
        if not input_path.exists():
            print(f"Warning: {filename} not found, skipping")
            continue
        
        source_config = FILE_SOURCES.get(filename, {
            'url': 'https://unknown.source',
            'title': 'Unknown Source',
            'source_type': 'database',
        })
        
        output_path = output_dir / filename.replace('.py', '_migrated.py')
        
        try:
            migrate_file(input_path, output_path, source_config)
            # Count foods for reporting
            foods = parse_food_legacy_file(input_path)
            total_foods += len(foods)
        except Exception as e:
            print(f"Error migrating {filename}: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*60}")
    print(f"Migration complete!")
    print(f"Total foods migrated: {total_foods}")
    print(f"Output directory: {output_dir}")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
