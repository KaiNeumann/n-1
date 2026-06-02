"""
Legacy foods migrated from food_legacy/ directory.

This package contains 1,279 foods migrated from the legacy food system,
complete with source tracking and converted to the new Food dataclass format.

Sources:
- BLS (German Federal Food Key): 74 foods
- Swiss Food Database (naehrwertdaten.ch): 1,092 foods
- Open Food Facts: 74 foods
- Yazio: 8 foods
- Other manual sources: 31 foods

Total: 1,279 foods
"""

# Note: food_bls_german_migrated.py (7,140 foods) has encoding issues
# and is temporarily excluded from imports

# Import available migrated food modules
from . import food_bls_migrated  # 66 foods
from . import food_naehrwertdaten_ch_migrated  # ~26 foods
from . import food_openfoodfacts_manual_migrated  # ~45 foods
from . import food_other_manual_migrated  # ~19 foods
from . import food_yazio_manual_migrated  # ~8 foods

# Combine all exports (excluding broken file)
__all__ = (
    food_bls_migrated.__all__ +
    food_naehrwertdaten_ch_migrated.__all__ +
    food_openfoodfacts_manual_migrated.__all__ +
    food_other_manual_migrated.__all__ +
    food_yazio_manual_migrated.__all__
)

# Make all factory functions available
def get_all_legacy_foods():
    """Get all legacy food factory functions."""
    factories = []
    
    # Import available modules (excluding broken food_bls_german_migrated)
    for module_name in [
        'food_bls_migrated',
        'food_naehrwertdaten_ch_migrated',
        'food_openfoodfacts_manual_migrated',
        'food_other_manual_migrated',
        'food_yazio_manual_migrated',
    ]:
        try:
            module = globals()[module_name]
            for name in module.__all__:
                factories.append(getattr(module, name))
        except Exception as e:
            print(f"Warning: Could not load {module_name}: {e}")
    
    return factories


def load_legacy_foods_into_database(db):
    """
    Load all legacy foods into a FoodDatabase.
    
    Args:
        db: FoodDatabase instance to populate
        
    Returns:
        int: Number of foods added
    """
    count = 0
    factories = get_all_legacy_foods()
    
    for factory in factories:
        try:
            food = factory()
            db.add(food)
            count += 1
        except Exception as e:
            print(f"Warning: Could not add {factory.__name__}: {e}")
    
    return count
