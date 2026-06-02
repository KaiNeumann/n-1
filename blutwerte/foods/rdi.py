"""
Recommended Daily Intake (RDI) calculations with source tracking.

The RDI values themselves live in
``knowledge/nutrients/nutrients.jsonl`` (10 entries: vitamin K, iron,
folate, potassium, vitamin C, calcium, B12, D, magnesium, zinc).
This module is a thin consumer: it loads the JSONL, holds the
RDI dataclass, and exposes the public API (``get_rdi``,
``get_all_rdis``, ``register_rdi``, ``compare_to_rdi``).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union, Any

from .sources import DataSource


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


def _load_rdi_registry() -> Dict[str, RDI]:
    """Load RDI values from knowledge/nutrients/nutrients.jsonl."""
    from .jsonl_rdi_loader import load_rdis
    return load_rdis()


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
