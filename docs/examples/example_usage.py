"""
Example usage of the core library

This file demonstrates how to use the blood test biomarker library.
"""

from core import (
    get_biomarker, 
    search_biomarkers, 
    list_biomarkers,
    Category,
    load_blood_tests
)
from datetime import datetime


def example_basic_lookup():
    """Example: Look up biomarkers by name, synonym, or lab ID"""
    print("=" * 60)
    print("Example 1: Basic Biomarker Lookup")
    print("=" * 60)
    
    # Look up by German name
    crp = get_biomarker("C-reaktives Protein")
    print(f"\nFound by German name: {crp.name} ({crp.name_de})")
    print(f"Categories: {[c.value for c in crp.categories]}")
    
    # Look up by abbreviation
    crp2 = get_biomarker("CRP")
    print(f"\nFound by abbreviation: {crp2.name}")
    
    # Look up by lab ID
    crp3 = get_biomarker("A-CRPQ")
    print(f"\nFound by lab ID: {crp3.name}")
    
    # Show all names and synonyms
    print(f"\nAll names for this biomarker:")
    for name in crp.get_all_names():
        print(f"  - {name}")


def example_ranges_and_units():
    """Example: Working with reference ranges"""
    print("\n" + "=" * 60)
    print("Example 2: Reference Ranges and Units")
    print("=" * 60)
    
    # Get hemoglobin (has gender-specific ranges)
    hb = get_biomarker("Hemoglobin")
    print(f"\n{hb.name} ({hb.name_de})")
    print(f"Affected organs: {hb.organs}")
    
    # Show ranges for different units
    for unit, ranges in hb.ranges.items():
        print(f"\nUnit: {unit}")
        for r in ranges:
            if r.conditions and r.conditions.gender:
                print(f"  {r.label}: {r.min_value} - {r.max_value} "
                      f"(for {r.conditions.gender})")
            else:
                print(f"  {r.label}: {r.min_value} - {r.max_value}")


def example_interpret_value():
    """Example: Interpret a blood test value"""
    print("\n" + "=" * 60)
    print("Example 3: Interpret Blood Test Values")
    print("=" * 60)
    
    # Interpret a CRP value
    crp = get_biomarker("CRP")
    test_value = 3.5  # mg/l
    
    result = crp.interpret_value(test_value, "mg/l")
    print(f"\nCRP value: {test_value} mg/l")
    print(f"Status: {result['status']}")
    
    # Interpret with patient data
    patient = {"gender": "male", "age": 45}
    hb = get_biomarker("Hemoglobin")
    result = hb.interpret_value(15.0, "g/dl", patient)
    print(f"\nHemoglobin for 45-year-old male: 15.0 g/dl")
    print(f"Status: {result['status']}")
    
    # Check if value is in range
    range_obj = crp.get_range_for_unit("mg/l")
    if range_obj:
        in_range = range_obj.check_value(test_value)
        print(f"\nIs {test_value} in normal range? {in_range}")


def example_search():
    """Example: Search for biomarkers"""
    print("\n" + "=" * 60)
    print("Example 4: Search Biomarkers")
    print("=" * 60)
    
    # Search for cholesterol-related biomarkers
    results = search_biomarkers("Cholesterol")
    print(f"\nFound {len(results)} biomarkers matching 'Cholesterol':")
    for b in results:
        print(f"  - {b.name} ({b.name_de})")
    
    # Search for German terms
    results = search_biomarkers("Blutzucker")
    print(f"\nFound {len(results)} biomarkers matching 'Blutzucker':")
    for b in results:
        print(f"  - {b.name} ({b.name_de})")


def example_categories():
    """Example: Browse by category"""
    print("\n" + "=" * 60)
    print("Example 5: Browse by Category")
    print("=" * 60)
    
    # Get all enzymes
    from core.biomarkers_db import _db
    enzymes = _db.by_category(Category.ENZYMES)
    print(f"\nEnzymes ({len(enzymes)} total):")
    for e in enzymes[:5]:  # Show first 5
        print(f"  - {e.name}")
    print(f"  ... and {len(enzymes) - 5} more")


def example_csv_loading():
    """Example: Load and analyze historical blood test data"""
    print("\n" + "=" * 60)
    print("Example 6: Load Historical Blood Test Data")
    print("=" * 60)
    
    try:
        # Load the CSV file
        history = load_blood_tests("blutbild.csv")
        
        print(f"\nLoaded {len(history.records)} measurements")
        print(f"Number of unique biomarkers: {len(history.list_biomarkers())}")
        print(f"Date range: {min(history.dates).date()} to {max(history.dates).date()}")
        
        # Get latest cholesterol value
        latest_chol = history.get_latest_value("Cholesterin")
        if latest_chol:
            print(f"\nLatest cholesterol: {latest_chol.value} {latest_chol.unit}")
            print(f"  Measured on: {latest_chol.date.date()}")
        
        # Get timeline for a biomarker
        timeline = history.get_timeline("HbA1c")
        print(f"\nHbA1c timeline ({len(timeline)} measurements):")
        for date, value in timeline[-5:]:  # Show last 5
            print(f"  {date.date()}: {value}%")
        
        # Get all values on a specific date
        date = datetime(2024, 4, 4)
        records = history.get_records_for_date(date)
        print(f"\nAll measurements on {date.date()}:")
        for r in records[:10]:  # Show first 10
            print(f"  {r.biomarker_name}: {r.value} {r.unit}")
            
    except FileNotFoundError:
        print("\nCSV file not found. Run from the project directory.")


def example_export():
    """Example: Export biomarker data"""
    print("\n" + "=" * 60)
    print("Example 7: Export Biomarker Data")
    print("=" * 60)
    
    crp = get_biomarker("CRP")
    data = crp.to_dict()
    
    print(f"\nJSON representation of CRP:")
    import json
    print(json.dumps(data, indent=2, ensure_ascii=False))


def example_list_all():
    """Example: List all available biomarkers"""
    print("\n" + "=" * 60)
    print("Example 8: List All Biomarkers")
    print("=" * 60)
    
    all_names = list_biomarkers()
    print(f"\nTotal biomarkers in database: {len(all_names)}")
    print("\nFirst 20 biomarkers:")
    for name in all_names[:20]:
        b = get_biomarker(name)
        print(f"  - {name} ({b.name_de})")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("core Library - Usage Examples")
    print("=" * 60)
    
    # Run all examples
    example_basic_lookup()
    example_ranges_and_units()
    example_interpret_value()
    example_search()
    example_categories()
    example_csv_loading()
    example_export()
    example_list_all()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)
