"""
Food data module.

This module provides factory functions for creating Food objects
with complete nutrition data and biomarker effects.
"""

from .vegetables import (
    create_spinach,
    create_tomato,
    create_potato,
    create_bell_pepper,
    create_kale,
    create_broccoli,
)

from .fruits import (
    create_banana,
    create_orange,
    create_avocado,
    create_strawberry,
)

from .proteins import (
    create_beef,
    create_chicken,
    create_salmon,
    create_egg,
    create_lentils,
    create_tofu,
)

from .dairy import (
    create_milk,
    create_yogurt,
    create_cheddar,
)

from .grains import (
    create_oats,
    create_quinoa,
    create_brown_rice,
)

# Convenience function to get all foods
def get_all_foods():
    """Get list of all 25 priority food factory functions."""
    return [
        # Vegetables (6)
        create_spinach,
        create_tomato,
        create_potato,
        create_bell_pepper,
        create_kale,
        create_broccoli,
        # Fruits (4)
        create_banana,
        create_orange,
        create_avocado,
        create_strawberry,
        # Proteins (6)
        create_beef,
        create_chicken,
        create_salmon,
        create_egg,
        create_lentils,
        create_tofu,
        # Dairy (3)
        create_milk,
        create_yogurt,
        create_cheddar,
        # Grains (3)
        create_oats,
        create_quinoa,
        create_brown_rice,
    ]

__all__ = [
    # Vegetables
    "create_spinach",
    "create_tomato",
    "create_potato",
    "create_bell_pepper",
    "create_kale",
    "create_broccoli",
    # Fruits
    "create_banana",
    "create_orange",
    "create_avocado",
    "create_strawberry",
    # Proteins
    "create_beef",
    "create_chicken",
    "create_salmon",
    "create_egg",
    "create_lentils",
    "create_tofu",
    # Dairy
    "create_milk",
    "create_yogurt",
    "create_cheddar",
    # Grains
    "create_oats",
    "create_quinoa",
    "create_brown_rice",
    # Utility
    "get_all_foods",
]
