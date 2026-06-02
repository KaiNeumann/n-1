"""
Biomarker database with all blood test measurements
"""

from typing import Dict, List, Optional, Any
from .models import Biomarker, ReferenceRange, Quote, Interpretation, Category, RangeCondition


class BiomarkerDatabase:
    """Database of all biomarkers with search functionality"""
    
    def __init__(self):
        self._biomarkers: Dict[str, Biomarker] = {}
        self._by_synonym: Dict[str, str] = {}  # Maps synonyms to primary name
        self._by_lab_id: Dict[str, str] = {}   # Maps lab IDs to primary name
        self._initialize_biomarkers()
    
    def _add(self, biomarker: Biomarker):
        """Add a biomarker to the database"""
        self._biomarkers[biomarker.name] = biomarker
        
        # Index by all names and synonyms
        for name in biomarker.get_all_names():
            self._by_synonym[name.lower()] = biomarker.name
        
        # Index lab IDs (uppercase abbreviations like A-AMYS, ALBELK, etc.)
        for syn in biomarker.synonyms:
            if syn and len(syn) <= 10 and any(c.isupper() for c in syn):
                self._by_lab_id[syn.upper()] = biomarker.name
    
    def get(self, name: str) -> Optional[Biomarker]:
        """Get a biomarker by any of its names"""
        name_lower = name.lower()
        
        # Direct lookup
        if name in self._biomarkers:
            return self._biomarkers[name]
        
        # Lookup by synonym
        if name_lower in self._by_synonym:
            primary = self._by_synonym[name_lower]
            return self._biomarkers.get(primary)
        
        # Lookup by lab ID
        if name.upper() in self._by_lab_id:
            primary = self._by_lab_id[name.upper()]
            return self._biomarkers.get(primary)
        
        return None
    
    def search(self, query: str) -> List[Biomarker]:
        """Search for biomarkers by partial name match"""
        query_lower = query.lower()
        results = []
        
        for biomarker in self._biomarkers.values():
            if any(query_lower in name.lower() for name in biomarker.get_all_names()):
                results.append(biomarker)
        
        return results
    
    def by_category(self, category: Category) -> List[Biomarker]:
        """Get all biomarkers in a category"""
        return [b for b in self._biomarkers.values() if category in b.categories]
    
    def list_all(self) -> List[str]:
        """List all primary biomarker names"""
        return list(self._biomarkers.keys())
    
    def _initialize_biomarkers(self):
        """Initialize all biomarkers. Prefers JSONL under knowledge/, falls back to Python."""
        from .jsonl_loader import load_biomarkers_from_jsonl, load_biomarkers_from_python

        loaded = load_biomarkers_from_jsonl()
        if not loaded:
            loaded = load_biomarkers_from_python()
        for name, biomarker in loaded.items():
            self._add(biomarker)

_db = BiomarkerDatabase()


def get_biomarker(name: str) -> Optional[Biomarker]:
    """Get a biomarker by name, synonym, or lab ID"""
    return _db.get(name)


def search_biomarkers(query: str) -> List[Biomarker]:
    """Search for biomarkers by partial name match"""
    return _db.search(query)


def list_biomarkers() -> List[str]:
    """List all primary biomarker names"""
    return _db.list_all()
