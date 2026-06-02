# -*- coding: utf-8 -*-
"""
BLS 4.0 to Python Converter

Converts the German Bundeslebensmittelschlüssel (BLS) 4.0 Excel database
to Python format compatible with the Food class.

Source: https://blsdb.de/download
License: CC BY 4.0
Citation: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), 
          Version 4.0 - Deutsche Nährstoffdatenbank. Karlsruhe.

Usage:
    1. Download BLS_4_0_2025_DE.zip from https://blsdb.de/download
    2. Extract to get BLS_4_0_Daten_2025_DE.xlsx
    3. Run: python convert_bls_to_python.py
    4. Output: food_bls_german.py
"""

import pandas as pd
import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional


def sanitize_name(name: str) -> str:
    """Convert German food name to valid Python variable name."""
    if pd.isna(name):
        return None
        
    name = str(name).strip()
    if not name:
        return None
    
    # Replace spaces and special characters
    replacements = {
        ' ': '_', ',': '_', '(': '_', ')': '_', '/': '_', '-': '_',
        '.': '_', ';': '_', ':': '_', '&': '_', '+': '_', '%': '_',
        '"': '', "'": '', '`': '', '´': '', '‚': '', '„': '',
        '(': '_', ')': '_', '[': '_', ']': '_', '{': '_', '}': '_',
    }
    
    for old, new in replacements.items():
        name = name.replace(old, new)
    
    # Replace German umlauts
    umlauts = {
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss',
        'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue',
        'á': 'a', 'à': 'a', 'â': 'a', 'ã': 'a', 'å': 'a', 'æ': 'ae',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'ó': 'o', 'ò': 'o', 'ô': 'o', 'õ': 'o', 'ø': 'o', 'œ': 'oe',
        'ú': 'u', 'ù': 'u', 'û': 'u',
        'ý': 'y', 'ÿ': 'y',
        'ñ': 'n', 'ç': 'c',
    }
    
    for old, new in umlauts.items():
        name = name.replace(old, new)
    
    # Remove any other non-alphanumeric characters except underscore
    name = ''.join(c for c in name if c.isalnum() or c == '_')
    
    # Ensure it starts with a letter
    if name and not name[0].isalpha():
        name = 'Food_' + name
    
    # Remove multiple consecutive underscores
    while '__' in name:
        name = name.replace('__', '_')
    
    # Remove trailing underscore
    name = name.rstrip('_')
    
    # Limit length
    if len(name) > 100:
        name = name[:100]
    
    return name if name else None


def convert_value(value) -> Optional[float]:
    """Convert value to float, return None if not possible."""
    if pd.isna(value):
        return None
    try:
        float_val = float(value)
        # Round to reasonable precision
        if abs(float_val) < 0.001:
            return None
        return round(float_val, 3)
    except (ValueError, TypeError):
        return None


def get_column_mapping(df: pd.DataFrame) -> Dict[str, str]:
    """Map BLS column names to Food class nutrient names."""
    # Based on BLS 4.0 column structure
    mapping = {}
    
    column_patterns = {
        # Energy
        'ENERCJ Energie (Kilojoule)': 'kilojoules',
        'ENERCC Energie (Kilokalorien)': 'calories',
        
        # Macronutrients
        'PROT Protein': 'protein',
        'FAT Fett': 'fat',
        'CHOCDF Kohlenhydrate': 'carbohydrate',
        'FIBTG Ballaststoffe': 'fiber',
        'SUGAR Zucker': 'sugar',
        'STARCH Stärke': 'starch',
        
        # Fats
        'FASAT Fettsäuren gesättigt': 'saturated_fat',
        'FAMS Fettsäuren einfach ungesättigt': 'monounsaturated_fat',
        'FAPU Fettsäuren mehrfach ungesättigt': 'polyunsaturated_fat',
        'CHOLE Cholesterin': 'cholesterol',
        
        # Minerals
        'NA Natrium': 'sodium',
        'K Kalium': 'potassium',
        'CA Calcium': 'calcium',
        'MG Magnesium': 'magnesium',
        'P Phosphor': 'phosphorus',
        'FE Eisen': 'iron',
        'ZN Zink': 'zinc',
        'MN Mangan': 'manganese',
        'CU Kupfer': 'copper',
        'ID Jod': 'iodine',
        'SE Selen': 'selenium',
        'CL Chlorid': 'chloride',
        
        # Vitamins
        'VITA Vitamin A': 'vitamin_a',
        'VITD Vitamin D': 'vitamin_d',
        'VITE Vitamin E': 'vitamin_e',
        'VITK Vitamin K': 'vitamin_k',
        'VITB1 Vitamin B1': 'vitamin_b1',
        'VITB2 Vitamin B2': 'vitamin_b2',
        'VITB6 Vitamin B6': 'vitamin_b6',
        'VITB12 Vitamin B12': 'vitamin_b12',
        'VITC Vitamin C': 'vitamin_c',
        'FOL Folsäure': 'vitamin_b9',
        'NIA Niacin': 'vitamin_b3',
        'PANTAC Pantothensäure': 'vitamin_b5',
        'BIOT Biotin': 'vitamin_b7',
        'VIT Carotinoide': 'provitamin_a',
        
        # Other
        'WATER Wasser': 'water',
        'ALC Alkohol (Ethanol)': 'alcohol',
        'CAFF Koffein': 'caffeine',
        'NACL Natriumchlorid (Salz)': 'salt',
    }
    
    # Find matching columns
    for col in df.columns:
        col_str = str(col)
        for pattern, nutrient in column_patterns.items():
            if pattern in col_str:
                mapping[col_str] = nutrient
                break
    
    return mapping


def generate_python_file(df: pd.DataFrame, output_file: str = 'food_bls_german.py'):
    """Generate Python file from BLS DataFrame."""
    
    # Get column mappings
    column_mapping = get_column_mapping(df)
    print(f"Found {len(column_mapping)} nutrient columns")
    
    # Find name columns
    name_col = None
    for col in df.columns:
        col_str = str(col).lower()
        if 'lebensmittelbezeichnung' in col_str or 'food name' in col_str:
            name_col = col
            break
    
    if name_col is None:
        raise ValueError("Could not find food name column")
    
    print(f"Using name column: {name_col}")
    
    # Generate Python code
    lines = [
        '# -*- coding: utf-8 -*-',
        '"""',
        'German Food Database (BLS 4.0)',
        '',
        'Bundeslebensmittelschlüssel Version 4.0',
        'Source: https://blsdb.de/download',
        '',
        'License: CC BY 4.0 (Creative Commons Attribution 4.0 International)',
        '',
        'Citation:',
        '  Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS),',
        '  Version 4.0 - Deutsche Nährstoffdatenbank. Karlsruhe.',
        '  DOI: 10.25826/Data20251217-134202-0',
        '',
        f'Total foods: {len(df)}',
        'Auto-generated: 2025',
        '"""',
        '',
        'from Food import Food',
        '',
    ]
    
    foods_generated = 0
    foods_skipped = 0
    name_collisions = {}
    
    for idx, row in df.iterrows():
        # Get food name
        food_name = row[name_col]
        if pd.isna(food_name):
            foods_skipped += 1
            continue
        
        # Sanitize name
        var_name = sanitize_name(food_name)
        if not var_name:
            foods_skipped += 1
            continue
        
        # Handle name collisions
        if var_name in name_collisions:
            name_collisions[var_name] += 1
            var_name = f"{var_name}_{name_collisions[var_name]}"
        else:
            name_collisions[var_name] = 1
        
        # Build nutrient dictionary
        nutrients = {}
        for bls_col, food_key in column_mapping.items():
            if bls_col in df.columns:
                value = convert_value(row[bls_col])
                if value is not None:
                    nutrients[food_key] = value
        
        if not nutrients:
            foods_skipped += 1
            continue
        
        # Build Python line
        nutrient_items = [f"'{k}': {v}" for k, v in sorted(nutrients.items())]
        nutrient_str = ', '.join(nutrient_items)
        
        # Escape any special characters in food name for comment
        safe_name = str(food_name).replace('\\', '\\\\').replace("'", "\\'")
        
        line = f"{var_name} = Food({{{nutrient_str}}})  # {safe_name}"
        lines.append(line)
        foods_generated += 1
        
        # Progress
        if foods_generated % 1000 == 0:
            print(f"  Processed {foods_generated} foods...")
    
    # Add summary
    lines.append('')
    lines.append(f'# Summary:')
    lines.append(f'# - Total foods in database: {len(df)}')
    lines.append(f'# - Successfully converted: {foods_generated}')
    lines.append(f'# - Skipped (no data): {foods_skipped}')
    lines.append('')
    
    # Write file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"\n[OK] Generated {output_file}")
    print(f"  Foods converted: {foods_generated}")
    print(f"  Foods skipped: {foods_skipped}")


def main():
    """Main conversion function."""
    # Find input file
    input_paths = [
        Path('BLS_4_0_Daten_2025_DE.xlsx'),
        Path('BLS_4_0_2025_DE/BLS_4_0_Daten_2025_DE.xlsx'),
        Path('/tmp/BLS_4_0_2025_DE/BLS_4_0_Daten_2025_DE.xlsx'),
        Path('original data/BLS_4_0_Daten_2025_DE.xlsx'),
        Path('../original data/BLS_4_0_Daten_2025_DE.xlsx'),
    ]
    
    input_file = None
    for path in input_paths:
        if path.exists():
            input_file = path
            break
    
    if not input_file:
        print("Error: Could not find BLS_4_0_Daten_2025_DE.xlsx")
        print("Please download from https://blsdb.de/download and extract.")
        sys.exit(1)
    
    print(f"Converting BLS database: {input_file}")
    print()
    
    # Read Excel
    try:
        print("Reading Excel file...")
        df = pd.read_excel(input_file, sheet_name=0)
        print(f"[OK] Loaded {len(df)} foods")
    except Exception as e:
        print(f"Error reading Excel: {e}")
        sys.exit(1)
    
    # Show sample
    print("\nSample entries:")
    for col in df.columns:
        if 'name' in str(col).lower() or 'bezeichnung' in str(col).lower():
            for i in range(min(3, len(df))):
                print(f"  - {df[col].iloc[i]}")
            break
    
    # Generate Python file
    print("\nGenerating Python code...")
    generate_python_file(df)
    
    print("\n[OK] Done! Import with: from food_bls_german import *")


if __name__ == '__main__':
    main()
