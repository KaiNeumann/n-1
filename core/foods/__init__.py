"""
Food system public API.

This module exports the main classes and functions for working with foods,
nutrition data, and biomarker effects.

Example:
    >>> from core.foods import Food, FoodDatabase, gramm, scheibe
    >>> 
    >>> # Create a food
    >>> spinach = Food(
    ...     name="Spinach",
    ...     name_de="Spinat",
    ...     category="vegetable",
    ...     nutrition_data={"vitamin k": 483, "iron": 2.7}
    ... )
    >>> 
    >>> # Use portions
    >>> portion = spinach * gramm(100)  # 100g
    >>> portion = spinach * scheibe(2)  # 2 portions
    >>> 
    >>> # Search database
    >>> db = FoodDatabase()
    >>> db.load_all()
    >>> foods = db.get_affecting_biomarker("Vitamin K")
"""

# Core models
from .models import (
    Food,
    FoodEffect,
    FoodIntake,
    EffectModifier,
    EffectCertainty,
)

# Source tracking
from .sources import (
    DataSource,
    SourcedValue,
    create_source,
    validate_source,
)

# Portions and measurements
from .portions import (
    Amount,
    Portion,
    CategoryPortionDefaults,
    PortionRegistry,
    Registry,
    # Base units
    gramm,
    kilo,
    ml,
    liter,
    # Predefined portions
    becher,
    beutel,
    dose,
    eins,
    esslöffel,
    flasche,
    glas,
    handvoll,
    kleine_flasche,
    kugel,
    packung,
    pad,
    portion,
    pott,
    prise,
    scheibe,
    schnapsglas,
    schüssel,
    stück,
    tablette,
    tafel,
    tasse,
    teelöffel,
    teller,
    topf,
    tüte,
    zehe,
)

# Database
from .database import (
    FoodDatabase,
    db as default_db,
)

# RDI
from .rdi import (
    RDI,
    get_rdi,
    get_all_rdis,
    register_rdi,
    compare_to_rdi,
)

# Import enums from medications for convenience
from core.medications.models import (
    EffectTargetType,
    EffectDirection,
)

__all__ = [
    # Models
    "Food",
    "FoodEffect",
    "FoodIntake",
    "EffectModifier",
    "EffectCertainty",
    # Sources
    "DataSource",
    "SourcedValue",
    "create_source",
    "validate_source",
    # Enums
    "EffectTargetType",
    "EffectDirection",
    # Portions
    "Amount",
    "Portion",
    "CategoryPortionDefaults",
    "PortionRegistry",
    "Registry",
    "gramm",
    "kilo",
    "ml",
    "liter",
    "becher",
    "beutel",
    "dose",
    "eins",
    "esslöffel",
    "flasche",
    "glas",
    "handvoll",
    "kleine_flasche",
    "kugel",
    "packung",
    "pad",
    "portion",
    "pott",
    "prise",
    "scheibe",
    "schnapsglas",
    "schüssel",
    "stück",
    "tablette",
    "tafel",
    "tasse",
    "teelöffel",
    "teller",
    "topf",
    "tüte",
    "zehe",
    # Database
    "FoodDatabase",
    "default_db",
    # RDI
    "RDI",
    "get_rdi",
    "get_all_rdis",
    "register_rdi",
    "compare_to_rdi",
]
