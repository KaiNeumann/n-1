"""
Test script for the food importers plugin system.

Run this to verify all importers are properly registered and working.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from importers import list_importers, get_importer, get_importer_info


def test_importers():
    """Test that all importers are registered and accessible."""
    print("Testing Food Importers Plugin System")
    print("=" * 50)
    
    # List all importers
    importers = list_importers()
    print(f"\nRegistered importers ({len(importers)}):")
    for name in importers:
        print(f"  - {name}")
    
    # Test each importer
    print("\nTesting each importer:")
    print("-" * 50)
    
    for name in importers:
        try:
            importer = get_importer(name)
            info = get_importer_info(name)
            
            print(f"\n[OK] {info['display_name']} ({name})")
            print(f"  Supports lookup: {info['supports_lookup']}")
            print(f"  Supports search: {info['supports_search']}")
            print(f"  Supports parse: {info['supports_parse']}")
            
        except Exception as e:
            print(f"\n[ERR] {name}: ERROR - {e}")
    
    print("\n" + "=" * 50)
    print("Test complete!")


def test_parsers():
    """Test the text parsers with example data."""
    print("\n\nTesting Text Parsers")
    print("=" * 50)
    
    # Test FDDB parser
    print("\n1. Testing FDDB Parser:")
    fddb_text = """
Brennwert
108 kJ
Kalorien
26 kcal
Protein
1,3 g
Kohlenhydrate
3,2 g
davon Zucker
0 g
Fett
0,4 g
Ballaststoffe
0 g
"""
    
    try:
        fddb = get_importer("fddb")
        food = fddb.parse(fddb_text)
        if food:
            print(f"[OK] Parsed successfully: {len(food.nutrition_data)} nutrients")
            print(f"  Calories: {food.nutrition_data.get('calories', 'N/A')}")
        else:
            print("[ERR] Parsing returned None")
    except Exception as e:
        print(f"[ERR] Error: {e}")
    
    # Test Yazio parser
    print("\n2. Testing Yazio Parser:")
    yazio_text = """
Nährwerte
pro Portion
Brennwert
266 kcal
1.114 kJ
Fett
12,7 g
gesättigte Fettsäuren
5,0 g
Kohlenhydrate
27,2 g
Zucker
2,5 g
Eiweiß
8,4 g
Salz
1,5 g
"""
    
    try:
        yazio = get_importer("yazio")
        food = yazio.parse(yazio_text)
        if food:
            print(f"[OK] Parsed successfully: {len(food.nutrition_data)} nutrients")
            print(f"  Calories: {food.nutrition_data.get('calories', 'N/A')}")
        else:
            print("[ERR] Parsing returned None")
    except Exception as e:
        print(f"[ERR] Error: {e}")
    
    print("\n" + "=" * 50)


def print_examples():
    """Print usage examples."""
    print("\n\nExample usage:")
    print("-" * 50)
    print("from importers import get_importer")
    print("")
    print("# Lookup by barcode via Open Food Facts")
    print('off = get_importer("openfoodfacts")')
    print('food = off.lookup("4053400205298")')
    print("")
    print("# Search for products")
    print('results = off.search("apple", limit=5)')
    print("")
    print("# Parse text from FDDB")
    print('fddb = get_importer("fddb")')
    print('food = fddb.parse("Kalorien\\n52 kcal\\nProtein\\n0,3 g")')
    print("")
    print("# Use Nutritionix natural language")
    print('nix = get_importer("nutritionix")')
    print('nix.app_id = "your_app_id"')
    print('nix.app_key = "your_app_key"')
    print('food = nix.lookup("1 large apple")')


if __name__ == "__main__":
    test_importers()
    test_parsers()
    print_examples()
