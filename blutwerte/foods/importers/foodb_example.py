"""
Example usage of FooDB importer for enriching food data.

This script demonstrates how to:
1. Download and load FooDB data
2. Search for foods and their compounds
3. Map compounds to biomarker effects
4. Enrich your food database

FooDB (https://foodb.ca/) contains:
- 797 foods with detailed composition
- 70,926 bioactive compounds
- 5+ million food-compound associations
- Free for academic use (CC BY-NC 4.0)
"""

from pathlib import Path


def example_download_instructions():
    """Show how to download FooDB data."""
    print("=" * 70)
    print("Step 1: Download FooDB Data")
    print("=" * 70)
    print()
    print("1. Visit: https://foodb.ca/downloads")
    print()
    print("2. Download one of these files:")
    print("   - FooDB JSON file (~87 MB) - Recommended")
    print("   - FooDB CSV file (~953 MB)")
    print("   - FooDB MySQL Dump (~173 MB)")
    print()
    print("3. Extract to a directory, e.g.:")
    print("   data/foodb/FooDB.json")
    print("   or")
    print("   data/foodb/Food.csv, Compound.csv, Content.csv")
    print()
    print("4. Optional: Request API key for online queries:")
    print("   https://foodb.ca/w/contact")
    print()


def example_load_and_query():
    """Example: Load data and query foods."""
    print("=" * 70)
    print("Step 2: Load and Query FooDB")
    print("=" * 70)
    print()
    
    code = '''
from blutwerte.foods.importers import FooDBImporter

# Initialize importer
importer = FooDBImporter()

# Load from downloaded JSON file
importer.load_from_json("data/foodb/FooDB.json")

# Or load from CSV files
# importer.load_from_csv("data/foodb/")

# Get statistics
stats = importer.get_statistics()
print(f"Loaded:")
print(f"  - {stats['foods']} foods")
print(f"  - {stats['compounds']} compounds")
print(f"  - {stats['contents']} food-compound associations")

# Search for a food
foods = importer.search_food("spinach")
for food in foods[:3]:  # Show first 3 matches
    print(f"Found: {food.name} ({food.food_group})")
    print(f"  Scientific name: {food.name_scientific}")
    print(f"  Compounds: {len(food.compounds)}")
'''
    
    print(code)
    print()


def example_biomarker_mapping():
    """Example: Map compounds to biomarkers."""
    print("=" * 70)
    print("Step 3: Map Compounds to Biomarkers")
    print("=" * 70)
    print()
    
    code = '''
from blutwerte.foods.importers import FooDBMapper

# Initialize mapper
mapper = FooDBMapper()

# Get effects for a compound class
effects = mapper.get_effects_for_compound_class("Flavonoids")
print(f"Flavonoids affect:")
for biomarker in effects['biomarkers']:
    print(f"  - {biomarker} ({effects['direction']})")
print(f"Mechanism: {effects['mechanism']}")
print(f"Evidence: {effects['evidence']}")

# Map specific food compounds
compounds = [
    {'name': 'Quercetin', 'klass': 'Flavonoids'},
    {'name': 'Beta-carotene', 'klass': 'Carotenoids'},
    {'name': 'Chlorogenic acid', 'klass': 'Phenolic acids'},
]

effects = mapper.map_food_compounds_to_effects(compounds)
for effect in effects:
    print(f"{effect.compound_name} -> {effect.biomarker_name}")
    print(f"  Direction: {effect.effect_direction}")
    print(f"  Evidence: {effect.evidence_level}")
'''
    
    print(code)
    print()


def example_enrich_food():
    """Example: Enrich a food with biomarker effects."""
    print("=" * 70)
    print("Step 4: Enrich Your Foods")
    print("=" * 70)
    print()
    
    code = '''
from blutwerte.foods.importers import FooDBImporter, FooDBMapper
from blutwerte.foods.models import FoodEffect, EffectCertainty
from blutwerte.medications.models import EffectTargetType, EffectDirection
from blutwerte.foods.sources import create_source

# Load FooDB
importer = FooDBImporter()
importer.load_from_json("data/foodb/FooDB.json")

mapper = FooDBMapper()

# Enrich your food
def enrich_food_with_foodb(your_food_name: str):
    """Add biomarker effects from FooDB to your food."""
    
    # Find matching food in FooDB
    foodb_food = importer.get_food(your_food_name)
    if not foodb_food:
        return None
    
    # Get compounds
    compounds = []
    for content in foodb_food.compounds:
        # Get compound details
        compound = importer.compounds.get(content.source_id)
        if compound:
            compounds.append({
                'name': compound.name,
                'klass': compound.compound_class
            })
    
    # Map to biomarker effects
    effects = mapper.map_food_compounds_to_effects(compounds)
    
    # Convert to FoodEffect objects
    food_effects = []
    for effect in effects:
        food_effects.append(FoodEffect(
            target_type=EffectTargetType.BIOMARKER,
            target_name=effect.biomarker_name,
            direction=EffectDirection.INCREASE 
                if effect.effect_direction == "increase" 
                else EffectDirection.DECREASE,
            mechanism=effect.mechanism,
            sources=[create_source(
                url="https://foodb.ca/",
                title=f"FooDB: {effect.compound_name} biomarker effects",
                source_type="database"
            )],
            certainty=EffectCertainty.ESTABLISHED 
                if effect.evidence_level == "strong" 
                else EffectCertainty.VARIABLE
        ))
    
    return food_effects

# Example usage
effects = enrich_food_with_foodb("Spinach")
print(f"Found {len(effects)} biomarker effects")
'''
    
    print(code)
    print()


def example_available_mappings():
    """Show available compound-biomarker mappings."""
    print("=" * 70)
    print("Available Compound-Biomarker Mappings")
    print("=" * 70)
    print()
    
    from blutwerte.foods.importers import COMPOUND_CLASS_TO_BIOMARKERS
    
    print("Curated mappings include:\n")
    
    for compound_class, data in COMPOUND_CLASS_TO_BIOMARKERS.items():
        print(f"{compound_class}:")
        print(f"  Biomarkers: {', '.join(data['biomarkers'])}")
        print(f"  Effect: {data['direction']}")
        print(f"  Evidence: {data['evidence']}")
        if 'magnitude' in data:
            print(f"  Magnitude: {data['magnitude']}")
        print()


def example_api_usage():
    """Example: Query FooDB API."""
    print("=" * 70)
    print("Optional: Query FooDB API (requires API key)")
    print("=" * 70)
    print()
    
    code = '''
from blutwerte.foods.importers import FooDBImporter

# Initialize with API key (request at https://foodb.ca/w/contact)
importer = FooDBImporter(api_key="your_api_key_here")

# Search foods via API
result = importer.query_api("foods", {
    "food_name": "Apple",
    "page": 1
})

for food in result.get('value', []):
    print(f"Found: {food['food_name']}")
    print(f"  ID: {food['public_id']}")
    print(f"  Group: {food['food_group']}")

# Search compounds via API
result = importer.query_api("compounds", {
    "compound_name": "Quercetin",
    "page": 1
})
'''
    
    print(code)
    print()


if __name__ == "__main__":
    print()
    print("FooDB Importer Examples")
    print("=" * 70)
    print()
    
    example_download_instructions()
    example_load_and_query()
    example_biomarker_mapping()
    example_enrich_food()
    example_available_mappings()
    example_api_usage()
    
    print("=" * 70)
    print("Next Steps")
    print("=" * 70)
    print()
    print("1. Download FooDB data from https://foodb.ca/downloads")
    print("2. Extract to data/foodb/ directory")
    print("3. Use the examples above to enrich your foods")
    print("4. Consider requesting an API key for real-time queries")
    print()
    print("Note: Academic use is free (CC BY-NC 4.0)")
    print("      Commercial use requires a license")
    print()
