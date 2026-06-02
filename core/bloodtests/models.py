"""
Data models for blood test biomarkers
"""

from dataclasses import dataclass, field
from typing import Optional, Callable, List, Dict, Any, Union
from enum import Enum


class Category(Enum):
    """Categories of biomarkers"""
    BLOOD_CHEMISTRY = "blood_chemistry"
    BLOOD_COUNT = "blood_count"
    BONE_HEALTH = "bone_health"
    COAGULATION = "coagulation"
    HORMONES = "hormones"
    IMMUNITY = "immunity"
    IRON_MARKERS = "iron_markers"
    LIPIDS = "lipids"
    PROTEIN_MARKERS = "protein_markers"
    STRESS_INFLAMMATION = "stress_inflammation"
    VITAMINS_MINERALS = "vitamins_minerals"
    TUMOR_MARKERS = "tumor_markers"
    ENZYMES = "enzymes"
    MISC = "misc"


@dataclass
class Quote:
    """A quote with source attribution"""
    text: str
    source: str = ""
    
    def __str__(self):
        return self.text
    
    def __repr__(self):
        return f"Quote({self.text[:50]}..., source={self.source})"


@dataclass 
class RangeCondition:
    """Conditions for when a range applies (e.g., age, gender)"""
    gender: Optional[str] = None  # 'male', 'female', 'both'
    age_min: Optional[float] = None  # in years
    age_max: Optional[float] = None
    pregnant: Optional[bool] = None
    notes: str = ""


@dataclass
class ReferenceRange:
    """
    A reference range for a biomarker
    
    Can be either static values or a function that calculates
    the range based on patient parameters
    """
    label: str  # e.g., 'normal', 'optimal', 'low_risk', 'critical'
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    unit: str = ""
    conditions: Optional[RangeCondition] = None
    # For dynamic ranges based on age/gender:
    range_func: Optional[Callable[[Dict[str, Any]], tuple]] = None
    remarks: List[Quote] = field(default_factory=list)
    
    def get_range(self, patient_data: Optional[Dict[str, Any]] = None) -> tuple:
        """
        Get the range values
        
        Args:
            patient_data: Dict with keys like 'age', 'gender', etc.
            
        Returns:
            Tuple of (min, max) values
        """
        if self.range_func and patient_data:
            return self.range_func(patient_data)
        return (self.min_value, self.max_value)
    
    def check_value(self, value: float, patient_data: Optional[Dict[str, Any]] = None) -> bool:
        """Check if a value is within this range"""
        min_val, max_val = self.get_range(patient_data)
        
        if min_val is not None and value < min_val:
            return False
        if max_val is not None and value > max_val:
            return False
        return True


@dataclass
class Interpretation:
    """Interpretation information for high/low values"""
    low: List[Quote] = field(default_factory=list)
    high: List[Quote] = field(default_factory=list)
    normal: List[Quote] = field(default_factory=list)


@dataclass
class Biomarker:
    """
    A blood test biomarker
    
    Attributes:
        name: Primary name (English preferred)
        name_de: German name
        synonyms: List of alternative names, abbreviations, lab IDs
        categories: List of categories this biomarker belongs to
        ranges: Dict mapping units to lists of reference ranges
        description: List of descriptive quotes
        interpretation: Interpretation object for value meanings
        organs: List of affected organs
        diet: Dietary recommendations as quotes
        wikipedia_url: Wikipedia reference URL
    """
    name: str
    name_de: str = ""
    synonyms: List[str] = field(default_factory=list)
    categories: List[Category] = field(default_factory=list)
    ranges: Dict[str, List[ReferenceRange]] = field(default_factory=dict)
    description: List[Quote] = field(default_factory=list)
    interpretation: Interpretation = field(default_factory=Interpretation)
    organs: List[str] = field(default_factory=list)
    diet: List[Quote] = field(default_factory=list)
    wikipedia_url: str = ""
    
    def __post_init__(self):
        """Ensure categories are Category enum values"""
        if self.categories and isinstance(self.categories[0], str):
            self.categories = [Category(c) for c in self.categories]
    
    def get_all_names(self) -> List[str]:
        """Get all possible names for this biomarker"""
        names = [self.name]
        if self.name_de:
            names.append(self.name_de)
        names.extend(self.synonyms)
        return names
    
    def get_range_for_unit(self, unit: str, patient_data: Optional[Dict[str, Any]] = None) -> Optional[ReferenceRange]:
        """Get the normal range for a specific unit"""
        if unit not in self.ranges:
            return None
        
        ranges = self.ranges[unit]
        # Find the most specific range based on patient data
        if patient_data:
            for r in ranges:
                if r.conditions:
                    # Check if conditions match
                    matches = True
                    if r.conditions.gender and patient_data.get('gender'):
                        if r.conditions.gender != patient_data['gender']:
                            matches = False
                    if r.conditions.age_min and patient_data.get('age'):
                        if patient_data['age'] < r.conditions.age_min:
                            matches = False
                    if r.conditions.age_max and patient_data.get('age'):
                        if patient_data['age'] > r.conditions.age_max:
                            matches = False
                    if matches:
                        return r
        
        # Return first 'normal' range or first range
        for r in ranges:
            if r.label == 'normal':
                return r
        return ranges[0] if ranges else None
    
    def interpret_value(self, value: float, unit: str, patient_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Interpret a value for this biomarker
        
        Returns dict with:
            - status: 'low', 'normal', 'high', 'critical'
            - range: the ReferenceRange that matched
            - interpretation: relevant Quote objects
        """
        range_obj = self.get_range_for_unit(unit, patient_data)
        
        if not range_obj:
            return {'status': 'unknown', 'range': None, 'interpretation': []}
        
        min_val, max_val = range_obj.get_range(patient_data)
        
        if min_val is not None and value < min_val:
            status = 'low'
            interp = self.interpretation.low
        elif max_val is not None and value > max_val:
            status = 'high'
            interp = self.interpretation.high
        else:
            status = 'normal'
            interp = self.interpretation.normal
        
        return {
            'status': status,
            'range': range_obj,
            'interpretation': interp
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            'name': self.name,
            'name_de': self.name_de,
            'synonyms': self.synonyms,
            'categories': [c.value for c in self.categories],
            'ranges': {
                unit: [
                    {
                        'label': r.label,
                        'min': r.min_value,
                        'max': r.max_value,
                        'unit': r.unit,
                        'remarks': [{'text': q.text, 'source': q.source} for q in r.remarks]
                    }
                    for r in ranges
                ]
                for unit, ranges in self.ranges.items()
            },
            'description': [{'text': q.text, 'source': q.source} for q in self.description],
            'organs': self.organs,
            'wikipedia_url': self.wikipedia_url,
        }
