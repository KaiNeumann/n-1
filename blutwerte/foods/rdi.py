"""
Recommended Daily Intake (RDI) calculations with source tracking.

This module provides RDI values for nutrients with references to
authoritative sources (DGE, WHO, FDA, etc.).

Based on the legacy _RDI class from food_legacy/nutriments.py.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union, Callable, Any

from .sources import DataSource, create_source


@dataclass
class RDI:
    """
    Recommended Daily Intake for a nutrient.
    
    Attributes:
        minimum: Minimum recommended amount
        reference: Reference/optimal amount
        maximum: Maximum safe amount (if applicable)
        unit: Unit of measurement (e.g., "mcg/day", "mg/day")
        comments: Additional notes about the RDI
        sources: List of sources for this RDI value
    """
    minimum: Optional[Union[int, float]] = None
    reference: Optional[Union[int, float]] = None
    maximum: Optional[Union[int, float]] = None
    unit: str = "g/day"
    comments: List[str] = field(default_factory=list)
    sources: List[DataSource] = field(default_factory=list)
    
    def __post_init__(self):
        """Ensure sources is a list"""
        if self.sources is None:
            self.sources = []
    
    def __str__(self) -> str:
        """String representation of RDI values"""
        values = {}
        if self.minimum is not None:
            values['minimum'] = self.minimum
        if self.reference is not None:
            values['reference'] = self.reference
        if self.maximum is not None:
            values['maximum'] = self.maximum
        return str(values)
    
    def __truediv__(self, divisor: Union[int, float]) -> 'RDI':
        """Divide RDI values by a number (useful for conversions)"""
        return RDI(
            minimum=self.minimum / divisor if self.minimum else None,
            maximum=self.maximum / divisor if self.maximum else None,
            reference=self.reference / divisor if self.reference else None,
            unit=self.unit,
            comments=self.comments.copy(),
            sources=self.sources.copy()
        )
    
    def __mul__(self, value: Union[int, float]) -> 'RDI':
        """Multiply RDI values by a number"""
        return RDI(
            minimum=self.minimum * value if self.minimum else None,
            maximum=self.maximum * value if self.maximum else None,
            reference=self.reference * value if self.reference else None,
            unit=self.unit,
            comments=self.comments.copy(),
            sources=self.sources.copy()
        )
    
    def set_unit(self, unit: str) -> 'RDI':
        """Set the unit (for method chaining)"""
        self.unit = unit
        return self
    
    def add_comment(self, comment: str) -> 'RDI':
        """Add a comment (for method chaining)"""
        self.comments.append(comment)
        return self
    
    def add_source(self, source: DataSource) -> 'RDI':
        """Add a source (for method chaining)"""
        self.sources.append(source)
        return self


# Default source for DGE (German Nutrition Society)
DGE_SOURCE = create_source(
    url="https://www.dge.de/wissenschaft/referenzwerte/",
    title="DGE Referenzwerte für die Nährstoffzufuhr",
    source_type="government"
)

# Default source for WHO
WHO_SOURCE = create_source(
    url="https://www.who.int/publications/i/item/9789240045164",
    title="WHO Guidelines on Nutrition",
    source_type="guideline"
)

# Default source for NIH/FDA
NIH_SOURCE = create_source(
    url="https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx",
    title="NIH Office of Dietary Supplements - Nutrient Recommendations",
    source_type="guideline"
)


# RDI definitions for common nutrients
# Values are for adults unless otherwise specified

RDI_VITAMIN_K = RDI(
    reference=70,  # mcg/day for adults
    unit="mcg/day",
    sources=[
        create_source(
            url="https://ods.od.nih.gov/factsheets/VitaminK-HealthProfessional/",
            title="Vitamin K Fact Sheet for Health Professionals - NIH",
            source_type="guideline"
        ),
        DGE_SOURCE
    ]
)

RDI_IRON = RDI(
    minimum=8,  # mg/day for adult men
    reference=8,
    maximum=45,  # UL for adults
    unit="mg/day",
    sources=[
        create_source(
            url="https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/",
            title="Iron Fact Sheet for Health Professionals - NIH",
            source_type="guideline"
        ),
        DGE_SOURCE
    ]
).add_comment("Women 19-50 years: 18 mg/day (menstruation)")

RDI_FOLATE = RDI(
    reference=400,  # mcg DFE/day
    unit="mcg DFE/day",
    sources=[
        create_source(
            url="https://ods.od.nih.gov/factsheets/Folate-HealthProfessional/",
            title="Folate Fact Sheet for Health Professionals - NIH",
            source_type="guideline"
        ),
        DGE_SOURCE
    ]
).add_comment("Pregnancy: 600 mcg/day")

RDI_POTASSIUM = RDI(
    reference=3500,  # mg/day (DGE) / 3400-2600 mg (NIH)
    unit="mg/day",
    sources=[
        create_source(
            url="https://ods.od.nih.gov/factsheets/Potassium-HealthProfessional/",
            title="Potassium Fact Sheet for Health Professionals - NIH",
            source_type="guideline"
        ),
        DGE_SOURCE
    ]
)

RDI_VITAMIN_C = RDI(
    reference=95,  # mg/day (DGE) / 75-90 mg (NIH)
    unit="mg/day",
    sources=[
        create_source(
            url="https://ods.od.nih.gov/factsheets/VitaminC-HealthProfessional/",
            title="Vitamin C Fact Sheet for Health Professionals - NIH",
            source_type="guideline"
        ),
        DGE_SOURCE
    ]
)

RDI_CALCIUM = RDI(
    reference=1000,  # mg/day for adults
    unit="mg/day",
    sources=[
        create_source(
            url="https://ods.od.nih.gov/factsheets/Calcium-HealthProfessional/",
            title="Calcium Fact Sheet for Health Professionals - NIH",
            source_type="guideline"
        ),
        DGE_SOURCE
    ]
).add_comment("Ages 51-70: 1200 mg/day (women), 1000 mg/day (men)")

RDI_VITAMIN_B12 = RDI(
    reference=4,  # mcg/day (DGE) / 2.4 mcg (NIH)
    unit="mcg/day",
    sources=[
        create_source(
            url="https://ods.od.nih.gov/factsheets/VitaminB12-HealthProfessional/",
            title="Vitamin B12 Fact Sheet for Health Professionals - NIH",
            source_type="guideline"
        ),
        DGE_SOURCE
    ]
)

RDI_VITAMIN_D = RDI(
    reference=20,  # mcg/day (800 IU)
    unit="mcg/day",
    sources=[
        create_source(
            url="https://ods.od.nih.gov/factsheets/VitaminD-HealthProfessional/",
            title="Vitamin D Fact Sheet for Health Professionals - NIH",
            source_type="guideline"
        ),
        DGE_SOURCE
    ]
)

RDI_MAGNESIUM = RDI(
    reference=350,  # mg/day for men (310-320 for women)
    unit="mg/day",
    sources=[
        create_source(
            url="https://ods.od.nih.gov/factsheets/Magnesium-HealthProfessional/",
            title="Magnesium Fact Sheet for Health Professionals - NIH",
            source_type="guideline"
        ),
        DGE_SOURCE
    ]
)

RDI_ZINC = RDI(
    reference=10,  # mg/day (DGE) / 8-11 mg (NIH)
    unit="mg/day",
    sources=[
        create_source(
            url="https://ods.od.nih.gov/factsheets/Zinc-HealthProfessional/",
            title="Zinc Fact Sheet for Health Professionals - NIH",
            source_type="guideline"
        ),
        DGE_SOURCE
    ]
)


# RDI registry
def _load_rdi_registry() -> Dict[str, RDI]:
    """Prefer JSONL under knowledge/nutrients/, fall back to Python definitions."""
    from .jsonl_rdi_loader import load_rdis
    loaded = load_rdis()
    if loaded:
        return loaded
    return {
        "vitamin k": RDI_VITAMIN_K,
        "iron": RDI_IRON,
        "folate": RDI_FOLATE,
        "potassium": RDI_POTASSIUM,
        "vitamin c": RDI_VITAMIN_C,
        "calcium": RDI_CALCIUM,
        "vitamin b12": RDI_VITAMIN_B12,
        "vitamin d": RDI_VITAMIN_D,
        "magnesium": RDI_MAGNESIUM,
        "zinc": RDI_ZINC,
    }


_rdi_registry: Dict[str, RDI] = _load_rdi_registry()


def get_rdi(nutrient_name: str) -> Optional[RDI]:
    """
    Get RDI for a nutrient.
    
    Args:
        nutrient_name: Name of the nutrient (lowercase, e.g., "vitamin k", "iron")
        
    Returns:
        RDI object or None if not found
    """
    return _rdi_registry.get(nutrient_name.lower())


def get_all_rdis() -> Dict[str, RDI]:
    """
    Get all RDI definitions.
    
    Returns:
        Dict of nutrient name -> RDI
    """
    return dict(_rdi_registry)


def register_rdi(nutrient_name: str, rdi: RDI) -> None:
    """
    Register a new RDI definition.
    
    Args:
        nutrient_name: Name of the nutrient
        rdi: RDI object
    """
    _rdi_registry[nutrient_name.lower()] = rdi


def compare_to_rdi(nutrient_value: float, nutrient_name: str, 
                   days: float = 1) -> Dict[str, Any]:
    """
    Compare a nutrient value to its RDI.
    
    Args:
        nutrient_value: Amount of nutrient (in RDI units)
        nutrient_name: Name of the nutrient
        days: Number of days the value represents (default 1)
        
    Returns:
        Dict with status and percentage of RDI
    """
    rdi = get_rdi(nutrient_name)
    if not rdi:
        return {"status": "unknown", "percentage": None}
    
    result = {"nutrient": nutrient_name, "value": nutrient_value, "unit": rdi.unit}
    
    # Calculate percentages
    if rdi.minimum:
        min_target = rdi.minimum * days
        result["min_percentage"] = (nutrient_value / min_target) * 100
        
        if nutrient_value < min_target:
            result["status"] = "below_minimum"
            result["message"] = f"Below minimum ({result['min_percentage']:.1f}% of minimum)"
            return result
    
    if rdi.maximum:
        max_target = rdi.maximum * days
        if nutrient_value > max_target:
            result["status"] = "exceeds_maximum"
            result["max_percentage"] = (nutrient_value / max_target) * 100
            result["message"] = f"Exceeds maximum ({result['max_percentage']:.1f}% of max)"
            return result
    
    if rdi.reference:
        ref_target = rdi.reference * days
        result["ref_percentage"] = (nutrient_value / ref_target) * 100
        result["status"] = "adequate"
        result["message"] = f"{result['ref_percentage']:.1f}% of reference value"
    else:
        result["status"] = "adequate"
        result["message"] = "Within acceptable range"
    
    return result
