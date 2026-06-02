"""
Medication database container with search and retrieval capabilities.

Provides centralized storage and lookup for all medications in the system.
Supports multi-field search, class-based retrieval, and biomarker reverse lookup.
"""

from typing import Dict, List, Optional, Any
import importlib
import pkgutil

from .models import Medication, EffectTargetType


class MedicationDatabase:
    """
    Central database for all medications.
    
    Features:
    - Multi-field search (generic name, brand, German name, ATC code)
    - Class-based retrieval
    - Biomarker reverse lookup ("what affects potassium?")
    - Lazy loading of medication modules
    
    Usage:
        db = MedicationDatabase()
        
        # Look up by name
        xipamid = db.get("Xipamid")
        
        # Search by partial match
        results = db.search("thiazide")
        
        # Get all medications affecting a biomarker
        potassium_drugs = db.get_affecting_biomarker("Potassium")
    """
    
    def __init__(self, auto_load: bool = True):
        """
        Initialize the medication database.
        
        Args:
            auto_load: If True, automatically load all medication modules on init
        """
        self._medications: Dict[str, Medication] = {}
        self._by_synonym: Dict[str, str] = {}
        self._by_brand: Dict[str, str] = {}
        self._by_atc: Dict[str, str] = {}
        
        if auto_load:
            self._load_all_medications()
    
    def _load_all_medications(self):
        """Load all medications. Prefers JSONL under knowledge/, falls back to Python."""
        from .jsonl_loader import load_medications_from_jsonl, load_medications_from_python

        loaded = load_medications_from_jsonl()
        if not loaded:
            loaded = load_medications_from_python()
        for med in loaded.values():
            self._add(med)

    def _load_all_medications_python(self):
        """Legacy Python-authored medication loader. Only used as fallback."""
        from . import data

        for importer, modname, ispkg in pkgutil.iter_modules(data.__path__, data.__name__ + "."):
            if not ispkg:
                try:
                    module = importlib.import_module(modname)
                    self._load_module_medications(module)
                except Exception as e:
                    print(f"Warning: Could not load module {modname}: {e}")

        try:
            from .data import vitamins
            for importer, modname, ispkg in pkgutil.iter_modules(vitamins.__path__, vitamins.__name__ + "."):
                if not ispkg:
                    try:
                        module = importlib.import_module(modname)
                        self._load_module_medications(module)
                    except Exception as e:
                        print(f"Warning: Could not load vitamin module {modname}: {e}")
        except ImportError:
            pass

    def _load_module_medications(self, module):
        """Load medication definitions from a module"""
        # Look for medication creation functions (convention: create_<medication_name>())
        for attr_name in dir(module):
            if attr_name.startswith('create_'):
                try:
                    func = getattr(module, attr_name)
                    if callable(func):
                        medication = func()
                        if isinstance(medication, Medication):
                            self._add(medication)
                except Exception as e:
                    print(f"Warning: Could not create medication from {attr_name}: {e}")
    
    def _add(self, med: Medication):
        """
        Add a medication to the database with full indexing.
        
        Creates multiple indexes for flexible lookup:
        - Primary name (lowercase)
        - German name
        - Synonyms (ATC codes, abbreviations)
        - Brand names
        """
        primary_key = med.name.lower()
        self._medications[primary_key] = med
        
        # Index synonyms (ATC codes, abbreviations)
        for syn in med.synonyms:
            if syn:
                self._by_synonym[syn.lower()] = primary_key
        
        # Index brand names
        for brand in med.brand_names:
            if brand:
                self._by_brand[brand.lower()] = primary_key
        
        # Index German name
        if med.name_de:
            self._by_synonym[med.name_de.lower()] = primary_key
        
        # Index ATC codes (typically in format "ATC:XXXXXX")
        for syn in med.synonyms:
            if syn and syn.upper().startswith('ATC:'):
                self._by_atc[syn.upper()] = primary_key
    
    def get(self, name: str) -> Optional[Medication]:
        """
        Look up medication by any identifier.
        
        Searches through:
        1. Primary generic name
        2. Synonyms (ATC codes, abbreviations)
        3. Brand/trade names
        4. German name
        
        Args:
            name: Medication name or identifier
            
        Returns:
            Medication object if found, None otherwise
            
        Example:
            db.get("Xipamid")  # By brand name
            db.get("Bendroflumethiazide")  # By generic name
            db.get("ATC:C03AA01")  # By ATC code
        """
        name_lower = name.lower()
        name_upper = name.upper()
        
        # Direct lookup by primary name
        if name_lower in self._medications:
            return self._medications[name_lower]
        
        # Lookup by synonym
        if name_lower in self._by_synonym:
            primary = self._by_synonym[name_lower]
            return self._medications.get(primary)
        
        # Lookup by brand name
        if name_lower in self._by_brand:
            primary = self._by_brand[name_lower]
            return self._medications.get(primary)
        
        # Lookup by ATC code
        if name_upper in self._by_atc:
            primary = self._by_atc[name_upper]
            return self._medications.get(primary)
        
        return None
    
    def search(self, query: str) -> List[Medication]:
        """
        Search medications by partial match.
        
        Searches across all name fields:
        - Generic name
        - German name
        - Synonyms
        - Brand names
        
        Args:
            query: Search string (case-insensitive)
            
        Returns:
            List of matching Medication objects
            
        Example:
            db.search("thiazide")  # Finds all thiazide diuretics
            db.search("potassium")  # Finds all meds affecting potassium
        """
        query_lower = query.lower()
        results = []
        seen = set()
        
        for med in self._medications.values():
            # Build searchable text
            searchable = [
                med.name,
                med.name_de,
                med.drug_class,
                med.drug_subclass
            ]
            searchable.extend(med.synonyms)
            searchable.extend(med.brand_names)
            
            # Check for match
            for text in searchable:
                if text and query_lower in text.lower():
                    if med.name not in seen:
                        results.append(med)
                        seen.add(med.name)
                    break
        
        return results
    
    def by_class(self, drug_class: str) -> List[Medication]:
        """
        Get all medications in a specific drug class.
        
        Args:
            drug_class: Drug class name (e.g., "Diuretic", "Statin")
            
        Returns:
            List of medications in that class
        """
        return [
            m for m in self._medications.values()
            if m.drug_class.lower() == drug_class.lower() or
               m.drug_subclass.lower() == drug_class.lower()
        ]
    
    def get_affecting_biomarker(self, biomarker_name: str) -> List[Medication]:
        """
        Find all medications that affect a specific biomarker.
        
        This is a reverse lookup - instead of "what does this drug do?",
        it answers "what drugs cause this effect?"
        
        Args:
            biomarker_name: Name of biomarker (e.g., "Potassium", "LDL")
            
        Returns:
            List of medications with effects on that biomarker
            
        Example:
            # Find all drugs that lower potassium
            hypokalemia_drugs = db.get_affecting_biomarker("Potassium")
        """
        affecting = []
        search_name = biomarker_name.lower()
        
        for med in self._medications.values():
            for effect in med.effects:
                if effect.target_type == EffectTargetType.BIOMARKER:
                    if effect.matches_target(search_name):
                        affecting.append(med)
                        break
        
        return affecting
    
    def get_affecting_target(self, target_name: str, target_type: Optional[EffectTargetType] = None) -> List[Medication]:
        """
        Find medications affecting any type of target.
        
        More general version of get_affecting_biomarker that works
        with any target type.
        
        Args:
            target_name: Name of target
            target_type: Optional filter by target type
            
        Returns:
            List of affecting medications
        """
        affecting = []
        search_name = target_name.lower()
        
        for med in self._medications.values():
            for effect in med.effects:
                if target_type is None or effect.target_type == target_type:
                    if effect.matches_target(search_name):
                        affecting.append(med)
                        break
        
        return affecting
    
    def list_all(self) -> List[str]:
        """Get list of all medication primary names"""
        return list(self._medications.keys())
    
    def list_by_class(self) -> Dict[str, List[str]]:
        """
        Group all medications by drug class.
        
        Returns:
            Dictionary mapping drug class to list of medication names
        """
        by_class: Dict[str, List[str]] = {}
        
        for med in self._medications.values():
            class_key = med.drug_class if med.drug_class else "Uncategorized"
            if class_key not in by_class:
                by_class[class_key] = []
            by_class[class_key].append(med.name)
        
        return by_class
    
    def count(self) -> int:
        """Get total number of medications in database"""
        return len(self._medications)
    
    def summary(self) -> Dict[str, Any]:
        """
        Get database summary statistics.
        
        Returns:
            Dictionary with database statistics
        """
        total_effects = sum(len(med.effects) for med in self._medications.values())
        biomarker_effects = sum(
            len([e for e in med.effects if e.target_type == EffectTargetType.BIOMARKER])
            for med in self._medications.values()
        )
        
        return {
            'total_medications': len(self._medications),
            'total_effects': total_effects,
            'biomarker_effects': biomarker_effects,
            'drug_classes': len(self.list_by_class()),
            'indexed_synonyms': len(self._by_synonym),
            'indexed_brands': len(self._by_brand),
            'indexed_atc': len(self._by_atc)
        }


# Singleton instance for global access
_db_instance: Optional[MedicationDatabase] = None


def get_database() -> MedicationDatabase:
    """
    Get the global medication database instance.
    
    Returns a singleton instance to avoid reloading medications multiple times.
    
    Returns:
        MedicationDatabase instance
    """
    global _db_instance
    if _db_instance is None:
        _db_instance = MedicationDatabase()
    return _db_instance


def reset_database():
    """Reset the global database instance (useful for testing)"""
    global _db_instance
    _db_instance = None


# Export public API
__all__ = [
    'MedicationDatabase',
    'get_database',
    'reset_database'
]
