"""
n-1 - A Python library for personal health analysis (the n-of-1 project)

This is the core package of the n-1 project. It provides structured data
and analysis for the only subject that matters in an n=1 trial: you.

Modules:
- bloodtests : blood biomarker reference ranges and lab data
- medications: medication -> biomarker effects and analysis
- foods      : food -> nutrient / biomarker effects (migrated from
               the original Food-and-Nutrition project)
- activities : exercise -> biomarker effects
- patients   : YAML-based personal health profiles

Example usage:
    >>> from blutwerte import get_biomarker, search_biomarkers
    >>>
    >>> # Get biomarker by name, synonym, or lab ID
    >>> crp = get_biomarker("CRP")
    >>> print(crp.name_de)  # C-reaktives Protein
    >>>
    >>> # Search for biomarkers
    >>> results = search_biomarkers("Cholesterol")
    >>>
    >>> # Load historical blood test data
    >>> from blutwerte import load_blood_tests
    >>> history = load_blood_tests("blutbild.csv")
    >>> timeline = history.get_timeline("Cholesterin")
"""

from .bloodtests import (
    Biomarker, 
    ReferenceRange, 
    Quote, 
    Category, 
    RangeCondition,
    BiomarkerDatabase,
    BloodTestHistory, 
    BloodTestRecord, 
    load_blood_tests
)
from .bloodtests.biomarkers_db import (
    get_biomarker,
    search_biomarkers,
    list_biomarkers
)

__version__ = "0.1.0"
__all__ = [
    "Biomarker",
    "ReferenceRange", 
    "Quote",
    "Category",
    "RangeCondition",
    "BiomarkerDatabase",
    "get_biomarker",
    "search_biomarkers",
    "list_biomarkers",
    "BloodTestHistory",
    "BloodTestRecord",
    "load_blood_tests",
]
