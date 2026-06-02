#!/usr/bin/env python3
"""
Enrich your legacy foods with biomarker effects from FooDB.

This script:
1. Loads FooDB data
2. Matches your foods to FooDB foods
3. Extracts bioactive compounds
4. Maps compounds to biomarker effects
5. Adds FoodEffect objects to your foods

Usage:
    python enrich_foods_with_foodb.py --limit 10
"""

import json
import argparse
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def load_foodb_data(foodb_path: Path = None):
    """Load FooDB data from JSON directory."""
    from blutwerte.foods.importers import FooDBImporter
    
    if foodb_path is None:
        foodb_path = Path("data/foodb")
    
    importer = FooDBImporter()
    
    # Check what format we have
    json_file = foodb_path / "FooDB.json"
    has_json_dir = (foodb_path / "Food.json").exists()
    
    if has_json_dir:
        print(f"Loading FooDB from: {foodb_path}")
        importer.load_from_json(foodb_path)
    elif json_file.exists():
        print(f"Loading FooDB from: {json_file}")
        importer.load_from_json(json_file)
    else:
        print(f"ERROR: FooDB data not found at {foodb_path}")
        print("Run: python download_foodb.py")
        return None
    
    stats = importer.get_statistics()
    print(f"Loaded {stats['foods']} foods, {stats['compounds']} compounds")
    
    return importer


def load_legacy_foods():
    """Load your legacy food database and return list of (name, Food) tuples."""
    from blutwerte.foods import FoodDatabase
    from blutwerte.foods.data.legacy import get_all_legacy_foods
    
    print("Loading priority foods...")
    db = FoodDatabase()
    db.load_all()
    
    print("Loading legacy foods...")
    legacy_factories = get_all_legacy_foods()
    legacy_count = 0
    for factory in legacy_factories:
        try:
            food = factory()
            db.add(food)
            legacy_count += 1
        except Exception as e:
            pass
    
    print(f"Loaded {legacy_count} legacy foods")
    
    # Get all food names
    food_names = db.list_all()
    
    # Get Food objects for each
    foods = []
    for name in food_names:
        food_obj = db.get(name)
        if food_obj:
            foods.append((name, food_obj))
    
    print(f"Total foods in database: {len(foods)}")
    
    return foods


def normalize_name(name: str) -> str:
    """Normalize food name for better matching."""
    name = name.lower()
    name = re.sub(r'\s+(roh|cooked|raw|fresh|dried)$', '', name)
    name = ' '.join(name.split())
    return name


# German to English food name translations
GERMAN_TO_ENGLISH = {
    'hafer': 'oat',
    'haferflocken': 'oat',
    'gerste': 'barley',
    'reis': 'rice',
    'vollkornbrot': 'whole grain bread',
    'roggenbrot': 'rye bread',
    'toastbrot': 'toast',
    'milch': 'milk',
    'joghurt': 'yogurt',
    'quark': 'curd',
    'sahne': 'cream',
    'butter': 'butter',
    'käse': 'cheese',
    'gouda': 'gouda',
    'edamer': 'edam',
    'emmentaler': 'swiss cheese',
    'camembert': 'camembert',
    'mozzarella': 'mozzarella',
    'feta': 'feta',
    'parmesan': 'parmesan',
    'Ei': 'egg',
    'eier': 'egg',
    'rindfleisch': 'beef',
    'rind': 'beef',
    'hähnchen': 'chicken',
    'schwein': 'pork',
    'fisch': 'fish',
    'lachs': 'salmon',
    'forelle': 'trout',
    'kartoffel': 'potato',
    'karotte': 'carrot',
    'zwiebel': 'onion',
    'knoblauch': 'garlic',
    'tomate': 'tomato',
    'paprika': 'bell pepper',
    'gurke': 'cucumber',
    'salat': 'lettuce',
    'spinat': 'spinach',
    'brokkoli': 'broccoli',
    'kohl': 'cabbage',
    'blumenkohl': 'cauliflower',
    'gurk': 'cucumber',
    'apfel': 'apple',
    'birne': 'pear',
    'banane': 'banana',
    'orange': 'orange',
    'zitrone': 'lemon',
    'traube': 'grape',
    'erdbeere': 'strawberry',
    'himbeere': 'raspberry',
    'blau Beere': 'blueberry',
    'bohne': 'bean',
    'linse': 'lentil',
    'erbsen': 'pea',
    'tofu': 'tofu',
    'nuss': 'nut',
    'mandel': 'almond',
    'walnuss': 'walnut',
    'hafer': 'oat',
    'weizen': 'wheat',
    'mais': 'corn',
    'quinoa': 'quinoa',
}


def translate_german_name(name: str) -> str:
    """Try to translate German food names to English."""
    name_lower = name.lower()
    
    # Check for known German words
    for german, english in GERMAN_TO_ENGLISH.items():
        if german in name_lower:
            # Replace German word with English
            return english
    
    return name  # Return original if no translation found


def match_food_to_foodb(food_name: str, food_obj, foodb_importer) -> Optional[str]:
    """Match a food name to FooDB using multiple strategies."""
    normalized = normalize_name(food_name)
    
    # Try exact match first (English)
    if foodb_importer.get_food(food_name):
        return food_name
    
    # Try case-insensitive
    for foodb_name in foodb_importer._food_name_map.keys():
        if normalized == foodb_name:
            return foodb_name
    
    # Try partial match with English name
    matches = foodb_importer.search_food(food_name)
    if matches:
        return matches[0].name
    
    # Try German translation
    english_name = translate_german_name(food_name)
    if english_name != food_name:
        if foodb_importer.get_food(english_name):
            return english_name
        
        matches = foodb_importer.search_food(english_name)
        if matches:
            return matches[0].name
        
        # Try partial match with translated name
        for foodb_name in foodb_importer._food_name_map.keys():
            if english_name in foodb_name or foodb_name in english_name:
                return foodb_name
    
    # Try with name_de if available
    if hasattr(food_obj, 'name_de') and food_obj.name_de:
        name_de = food_obj.name_de
        english_name = translate_german_name(name_de)
        
        if foodb_importer.get_food(english_name):
            return english_name
        
        matches = foodb_importer.search_food(english_name)
        if matches:
            return matches[0].name
    
    return None


def get_compound_classes_for_food(food_name: str, foodb_importer) -> set:
    """Get unique compound classes for a food."""
    foodb_food = foodb_importer.get_food(food_name)
    if not foodb_food:
        return set()
    
    classes = set()
    for content in foodb_food.compounds:
        compound = foodb_importer.compounds.get(content.source_id)
        if compound and compound.compound_class:
            classes.add(compound.compound_class)
    
    return classes


def enrich_food(food_name: str, food_obj, foodb_importer, mapper) -> Tuple[int, List[str]]:
    """Enrich a single food with biomarker effects."""
    from blutwerte.foods.models import FoodEffect, EffectCertainty
    from blutwerte.medications.models import EffectTargetType, EffectDirection
    from blutwerte.foods.sources import create_source
    
    # Match to FooDB
    foodb_name = match_food_to_foodb(food_name, food_obj, foodb_importer)
    if not foodb_name:
        return 0, []
    
    # Get compound classes
    compound_classes = get_compound_classes_for_food(foodb_name, foodb_importer)
    if not compound_classes:
        return 0, []
    
    # Map to biomarkers
    biomarkers_added = []
    effects_added = 0
    
    # Track which biomarkers we've already added
    added_biomarkers = set()
    
    for cls in compound_classes:
        effect = mapper.get_effects_for_compound_class(cls)
        if effect:
            for biomarker in effect['biomarkers']:
                if biomarker in added_biomarkers:
                    continue
                added_biomarkers.add(biomarker)
                
                # Determine direction
                direction = (EffectDirection.INCREASE 
                            if effect['direction'] == "increase" 
                            else EffectDirection.DECREASE)
                
                # Determine certainty
                certainty = (EffectCertainty.ESTABLISHED 
                           if effect['evidence'] == "strong" 
                           else EffectCertainty.VARIABLE)
                
                # Create FoodEffect
                food_effect = FoodEffect(
                    target_type=EffectTargetType.BIOMARKER,
                    target_name=biomarker,
                    direction=direction,
                    mechanism=f"{cls}: {effect['mechanism']}",
                    sources=[create_source(
                        url="https://foodb.ca/",
                        title=f"FooDB: Compound class {cls} affects {biomarker}",
                        source_type="database"
                    )],
                    certainty=certainty,
                    notes=f"Compound class: {cls}, Evidence: {effect['evidence']}"
                )
                
                # Add to food
                if hasattr(food_obj, 'add_effect'):
                    food_obj.add_effect(food_effect)
                elif hasattr(food_obj, 'effects'):
                    food_obj.effects.append(food_effect)
                
                effects_added += 1
                biomarkers_added.append(biomarker)
    
    return effects_added, biomarkers_added


def enrich_all_foods(foodb_path: Path, output_dir: Path, limit: Optional[int] = None):
    """Main enrichment function."""
    from blutwerte.foods.importers import FooDBMapper
    
    print("=" * 70)
    print("Enriching Foods with FooDB Biomarker Effects")
    print("=" * 70)
    print()
    
    # Load FooDB
    foodb_importer = load_foodb_data(foodb_path)
    if foodb_importer is None:
        return
    
    mapper = FooDBMapper()
    
    # Load legacy foods
    legacy_foods = load_legacy_foods()
    
    if limit:
        legacy_foods = legacy_foods[:limit]
        print(f"Processing first {limit} foods")
    
    print()
    print("Enriching foods...")
    print()
    
    # Process each food
    enriched_count = 0
    total_effects = 0
    unmatched_foods = []
    biomarker_coverage = {}
    enriched_foods = []
    
    for i, (food_name, food_obj) in enumerate(legacy_foods):
        if limit and i >= limit:
            break
            
        if i % 10 == 0:
            print(f"  Progress: {i}/{len(legacy_foods)}...", end="\r")
        
        try:
            num_effects, biomarkers = enrich_food(food_name, food_obj, foodb_importer, mapper)
            
            if num_effects > 0:
                enriched_count += 1
                total_effects += num_effects
                enriched_foods.append((food_name, food_obj, biomarkers))
                
                for biomarker in biomarkers:
                    biomarker_coverage[biomarker] = biomarker_coverage.get(biomarker, 0) + 1
            else:
                unmatched_foods.append(food_name)
                
        except Exception as e:
            print(f"\nError: {food_name}: {e}")
            unmatched_foods.append(food_name)
    
    print(f"  Progress: {len(legacy_foods)}/{len(legacy_foods)}")
    print()
    
    # Save results
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save enriched foods summary
    summary_file = output_dir / "enriched_summary.txt"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("FooDB Enrichment Results\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total foods processed: {len(legacy_foods)}\n")
        f.write(f"Foods enriched: {enriched_count}\n")
        f.write(f"Total effects: {total_effects}\n\n")
        
        f.write("Enriched foods:\n")
        f.write("-" * 30 + "\n")
        for name, food, biomarkers in enriched_foods:
            f.write(f"{name}: {len(biomarkers)} biomarkers\n")
        
        if unmatched_foods:
            f.write(f"\nUnmatched foods ({len(unmatched_foods)}):\n")
            for name in unmatched_foods[:20]:
                f.write(f"  - {name}\n")
    
    # Save JSON stats
    stats_file = output_dir / "enrichment_stats.json"
    stats = {
        "total_foods": len(legacy_foods),
        "enriched_foods": enriched_count,
        "total_effects": total_effects,
        "enrichment_rate": round(enriched_count / len(legacy_foods) * 100, 1) if legacy_foods else 0,
        "biomarker_coverage": biomarker_coverage,
        "unmatched_count": len(unmatched_foods),
        "unmatched_sample": unmatched_foods[:50],
        "foodb_foods_available": foodb_importer.get_statistics()['foods']
    }
    
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2)
    
    # Print summary
    print("=" * 70)
    print("Enrichment Complete!")
    print("=" * 70)
    print()
    print(f"Total foods processed: {len(legacy_foods)}")
    print(f"Foods enriched: {enriched_count} ({stats['enrichment_rate']}%)")
    print(f"Total biomarker effects: {total_effects}")
    print()
    print("Biomarker coverage:")
    for biomarker, count in sorted(biomarker_coverage.items(), key=lambda x: -x[1])[:10]:
        print(f"  {biomarker}: {count} foods")
    print()
    print(f"Unmatched: {len(unmatched_foods)} foods")
    print()
    print(f"Output saved to: {output_dir}")
    print(f"  - Summary: {summary_file}")
    print(f"  - Stats: {stats_file}")


def main():
    parser = argparse.ArgumentParser(description="Enrich foods with FooDB biomarker effects")
    parser.add_argument("--limit", "-l", type=int, default=None, help="Limit number of foods")
    parser.add_argument("--output", "-o", type=str, default="enriched_foods", help="Output directory")
    parser.add_argument("--food-db", "-f", type=str, default="data/foodb", help="FooDB directory")
    
    args = parser.parse_args()
    
    foodb_path = Path(args.food_db)
    output_dir = Path(args.output)
    
    if not foodb_path.exists():
        print(f"ERROR: FooDB directory not found: {foodb_path}")
        print("Download from: https://foodb.ca/downloads")
        return
    
    enrich_all_foods(foodb_path, output_dir, args.limit)


if __name__ == "__main__":
    main()
