#!/usr/bin/env python3
"""
Quick Start: Download FooDB and enrich your first 10 foods.

This is a simplified script to get you started quickly.
Run this to see FooDB enrichment in action on a small sample.
"""

import sys
from pathlib import Path


def main():
    print("=" * 70)
    print("FooDB Quick Start")
    print("=" * 70)
    print()
    
    # Check if FooDB is downloaded
    foodb_path = Path("data/foodb")
    
    # Check for either single file or directory format
    json_file = foodb_path / "FooDB.json"
    has_directory = (foodb_path / "Food.json").exists()
    
    if not (json_file.exists() or has_directory):
        print("FooDB data not found!")
        print()
        print("You have two options:")
        print()
        print("OPTION 1: Automatic Download (Recommended)")
        print("-" * 70)
        print("Run: python download_foodb.py")
        print()
        print("This will:")
        print("  - Download FooDB JSON (~87 MB)")
        print("  - Extract to data/foodb/")
        print("  - Verify the setup")
        print()
        print("OPTION 2: Manual Download")
        print("-" * 70)
        print("1. Visit: https://foodb.ca/downloads")
        print("2. Download: FooDB JSON file (~87 MB)")
        print("3. Extract to: data/foodb/")
        print("   (should have Food.json, Compound.json, Content.json)")
        print()
        return
    
    print(f"✓ FooDB found at: {foodb_path}")
    print()
    
    # Test loading
    print("Testing FooDB import...")
    try:
        from blutwerte.foods.importers import FooDBImporter, FooDBMapper
        print("✓ Imports successful")
        print()
        
        # Load data
        print("Loading FooDB data (this may take a moment)...")
        importer = FooDBImporter()
        importer.load_from_json(json_file)
        
        stats = importer.get_statistics()
        print(f"✓ Loaded {stats['foods']} foods with {stats['compounds']} compounds")
        print()
        
        # Demo: Search for a food
        print("Demo: Searching for 'spinach'...")
        foods = importer.search_food("spinach")
        
        if foods:
            food = foods[0]
            print(f"✓ Found: {food.name}")
            print(f"  Scientific name: {food.name_scientific}")
            print(f"  Group: {food.food_group}")
            print(f"  Compounds: {len(food.compounds)}")
            print()
            
            # Show biomarker mappings
            print("Demo: Biomarker effects for common compound classes...")
            print()
            
            mapper = FooDBMapper()
            
            compound_classes = ["Flavonoids", "Carotenoids", "Phenolic acids"]
            for cls in compound_classes:
                effects = mapper.get_effects_for_compound_class(cls)
                if effects:
                    print(f"{cls}:")
                    print(f"  Affects: {', '.join(effects['biomarkers'])}")
                    print(f"  Direction: {effects['direction']}")
                    print(f"  Evidence: {effects['evidence']}")
                    print()
            
            print("=" * 70)
            print("Ready to Enrich Your Foods!")
            print("=" * 70)
            print()
            print("Next steps:")
            print()
            print("1. Test on a small sample:")
            print("   python enrich_foods_with_foodb.py --limit 10")
            print()
            print("2. Process all foods:")
            print("   python enrich_foods_with_foodb.py")
            print()
            print("3. See detailed documentation:")
            print("   FOODB_INTEGRATION.md")
            print()
            
        else:
            print("✗ Food not found (this is unexpected)")
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
