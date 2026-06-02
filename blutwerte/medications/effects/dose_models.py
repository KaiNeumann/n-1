"""
Dose-response modeling for medication effects.

This module provides flexible dose-effect relationship modeling
supporting precise curves, approximate brackets, and threshold models.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Tuple
import math


@dataclass
class DoseEffectRange:
    """
    Effect at a specific dose level.
    
    Attributes:
        min_dose: Minimum dose in this range
        max_dose: Maximum dose in this range
        dose_unit: Unit of measurement (mg, mcg, IU, etc.)
        frequency_percentage: Probability of effect (0-100)
        magnitude: Severity of effect ("mild", "moderate", "severe")
        description: Clinical description of effect at this dose
    """
    min_dose: float
    max_dose: float
    dose_unit: str
    frequency_percentage: float
    magnitude: str
    description: str
    
    def __post_init__(self):
        """Validate inputs"""
        if not 0 <= self.frequency_percentage <= 100:
            raise ValueError(
                f"Frequency percentage must be 0-100, got {self.frequency_percentage}"
            )
        if self.min_dose > self.max_dose:
            raise ValueError(
                f"min_dose ({self.min_dose}) cannot exceed max_dose ({self.max_dose})"
            )
    
    def contains_dose(self, dose: float) -> bool:
        """Check if a specific dose falls within this range"""
        return self.min_dose <= dose <= self.max_dose
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'min_dose': self.min_dose,
            'max_dose': self.max_dose,
            'unit': self.dose_unit,
            'frequency': self.frequency_percentage,
            'magnitude': self.magnitude,
            'description': self.description
        }


@dataclass
class DoseEffectModel:
    """
    Models how medication effect varies with dosage.
    
    Supports three model types:
    1. PRECISE: Known dose-response curve with interpolation
    2. APPROXIMATE: Low/medium/high dose brackets (most clinically realistic)
    3. THRESHOLD: Effect only above/below a specific dose
    
    Example usage:
        # Thiazide diuretic hypokalemia (APPROXIMATE)
        model = DoseEffectModel(
            model_type=DoseEffectModelType.APPROXIMATE,
            typical_max_dose=5.0,  # mg
            low_dose=DoseEffectRange(2.5, 2.5, "mg", 10.0, "mild", "10% risk"),
            medium_dose=DoseEffectRange(5.0, 5.0, "mg", 20.0, "mild", "20% risk"),
            high_dose=DoseEffectRange(10.0, 10.0, "mg", 40.0, "moderate", "40% risk")
        )
        
        effect = model.get_effect_for_dose(5.0, "mg")
        # Returns medium_dose range
    """
    
    model_type: str  # "precise", "approximate", "threshold"
    
    # For APPROXIMATE models
    typical_max_dose: Optional[float] = None  # Typical maximum therapeutic dose
    low_dose: Optional[DoseEffectRange] = None       # <50% of typical max
    medium_dose: Optional[DoseEffectRange] = None    # 50-100% of typical max
    high_dose: Optional[DoseEffectRange] = None      # >100% of typical max
    
    # For PRECISE models
    dose_response_points: Optional[List[Tuple[float, float]]] = None  # [(dose, freq%), ...]
    
    # For THRESHOLD models
    threshold_dose: Optional[float] = None
    threshold_unit: Optional[str] = None
    above_threshold_effect: Optional[str] = None
    above_threshold_frequency: Optional[float] = None
    
    def __post_init__(self):
        """Validate model configuration"""
        if self.model_type == "approximate":
            if self.typical_max_dose is None:
                raise ValueError("APPROXIMATE model requires typical_max_dose")
        elif self.model_type == "precise":
            if not self.dose_response_points or len(self.dose_response_points) < 2:
                raise ValueError("PRECISE model requires at least 2 dose-response points")
        elif self.model_type == "threshold":
            if self.threshold_dose is None:
                raise ValueError("THRESHOLD model requires threshold_dose")
    
    def get_effect_for_dose(self, dose: float, unit: str) -> Optional[DoseEffectRange]:
        """
        Get expected effect for a specific patient dose.
        
        Args:
            dose: The dose amount
            unit: Unit of measurement
            
        Returns:
            DoseEffectRange describing the effect, or None if no model applies
        """
        if self.model_type == "precise":
            return self._interpolate_precise(dose, unit)
        elif self.model_type == "approximate":
            return self._get_approximate_bracket(dose, unit)
        elif self.model_type == "threshold":
            return self._evaluate_threshold(dose, unit)
        
        return None
    
    def _interpolate_precise(self, dose: float, unit: str) -> Optional[DoseEffectRange]:
        """
        Interpolate effect from known dose-response points.
        
        Uses linear interpolation between known data points.
        """
        if not self.dose_response_points:
            return None
        
        # Sort points by dose
        points = sorted(self.dose_response_points, key=lambda x: x[0])
        
        # Below first point - extrapolate down
        if dose <= points[0][0]:
            return DoseEffectRange(
                min_dose=0,
                max_dose=points[0][0],
                dose_unit=unit,
                frequency_percentage=points[0][1],
                magnitude="extrapolated_low",
                description=f"Effect extrapolated below lowest known dose"
            )
        
        # Above last point - extrapolate up
        if dose >= points[-1][0]:
            return DoseEffectRange(
                min_dose=points[-1][0],
                max_dose=float('inf'),
                dose_unit=unit,
                frequency_percentage=points[-1][1],
                magnitude="extrapolated_high",
                description=f"Effect extrapolated above highest known dose"
            )
        
        # Find bracketing points and interpolate
        for i in range(len(points) - 1):
            d1, f1 = points[i]
            d2, f2 = points[i + 1]
            
            if d1 <= dose <= d2:
                # Linear interpolation
                if d2 == d1:  # Avoid division by zero
                    fraction = 0
                else:
                    fraction = (dose - d1) / (d2 - d1)
                
                freq = f1 + fraction * (f2 - f1)
                
                # Determine magnitude based on frequency
                if freq < 10:
                    magnitude = "mild"
                elif freq < 30:
                    magnitude = "moderate"
                else:
                    magnitude = "severe"
                
                return DoseEffectRange(
                    min_dose=dose,
                    max_dose=dose,
                    dose_unit=unit,
                    frequency_percentage=freq,
                    magnitude=magnitude,
                    description=f"Interpolated effect: {freq:.1f}% at {dose}{unit}"
                )
        
        return None
    
    def _get_approximate_bracket(self, dose: float, unit: str) -> Optional[DoseEffectRange]:
        """
        Get dose bracket for APPROXIMATE models.
        
        Classifies dose as low, medium, or high based on typical_max_dose.
        """
        if self.typical_max_dose is None:
            return None
        
        # Determine dose category
        low_threshold = self.typical_max_dose * 0.5
        high_threshold = self.typical_max_dose
        
        if dose < low_threshold:
            # Low dose category
            if self.low_dose:
                return self._adapt_range(self.low_dose, dose, unit)
            elif self.medium_dose:
                # Scale down from medium dose
                scaled_freq = self.medium_dose.frequency_percentage * (dose / low_threshold)
                return DoseEffectRange(
                    min_dose=dose,
                    max_dose=dose,
                    dose_unit=unit,
                    frequency_percentage=scaled_freq,
                    magnitude="mild",
                    description=f"Low dose effect (scaled from medium): ~{scaled_freq:.1f}%"
                )
        
        elif dose <= high_threshold:
            # Medium dose category
            if self.medium_dose:
                return self._adapt_range(self.medium_dose, dose, unit)
            elif self.low_dose and self.high_dose:
                # Interpolate between low and high
                fraction = (dose - low_threshold) / (high_threshold - low_threshold)
                low_freq = self.low_dose.frequency_percentage
                high_freq = self.high_dose.frequency_percentage
                freq = low_freq + fraction * (high_freq - low_freq)
                return DoseEffectRange(
                    min_dose=dose,
                    max_dose=dose,
                    dose_unit=unit,
                    frequency_percentage=freq,
                    magnitude="moderate",
                    description=f"Medium dose effect (interpolated): ~{freq:.1f}%"
                )
        
        else:
            # High dose category
            if self.high_dose:
                return self._adapt_range(self.high_dose, dose, unit)
            elif self.medium_dose:
                # Scale up from medium dose (diminishing returns)
                scale_factor = 1 + 0.5 * ((dose / high_threshold) - 1)
                scaled_freq = min(self.medium_dose.frequency_percentage * scale_factor, 95)
                return DoseEffectRange(
                    min_dose=dose,
                    max_dose=dose,
                    dose_unit=unit,
                    frequency_percentage=scaled_freq,
                    magnitude="severe" if scale_factor > 1.3 else "moderate",
                    description=f"High dose effect (scaled): ~{scaled_freq:.1f}%"
                )
        
        return None
    
    def _adapt_range(self, template: DoseEffectRange, actual_dose: float, unit: str) -> DoseEffectRange:
        """
        Adapt a template dose range to an actual patient dose.
        
        Keeps the frequency and magnitude but updates the dose values.
        """
        return DoseEffectRange(
            min_dose=actual_dose,
            max_dose=actual_dose,
            dose_unit=unit,
            frequency_percentage=template.frequency_percentage,
            magnitude=template.magnitude,
            description=f"{template.description} (at patient's dose of {actual_dose}{unit})"
        )
    
    def _evaluate_threshold(self, dose: float, unit: str) -> Optional[DoseEffectRange]:
        """
        Evaluate THRESHOLD models.
        
        Returns effect only if dose is above/below threshold.
        """
        if self.threshold_dose is None:
            return None
        
        if dose >= self.threshold_dose:
            return DoseEffectRange(
                min_dose=self.threshold_dose,
                max_dose=float('inf'),
                dose_unit=unit if self.threshold_unit is None else self.threshold_unit,
                frequency_percentage=self.above_threshold_frequency or 90.0,
                magnitude="moderate",
                description=self.above_threshold_effect or f"Effect above {self.threshold_dose}{unit}"
            )
        else:
            # Below threshold - minimal effect
            return DoseEffectRange(
                min_dose=0,
                max_dose=self.threshold_dose,
                dose_unit=unit,
                frequency_percentage=5.0,
                magnitude="none",
                description=f"Below threshold dose ({self.threshold_dose}{unit})"
            )
    
    def get_all_defined_ranges(self) -> List[DoseEffectRange]:
        """Get all dose ranges defined in this model"""
        ranges = []
        if self.low_dose:
            ranges.append(self.low_dose)
        if self.medium_dose:
            ranges.append(self.medium_dose)
        if self.high_dose:
            ranges.append(self.high_dose)
        return ranges
    
    def to_dict(self) -> dict:
        """Convert model to dictionary representation"""
        return {
            'model_type': self.model_type,
            'typical_max_dose': self.typical_max_dose,
            'low_dose': self.low_dose.to_dict() if self.low_dose else None,
            'medium_dose': self.medium_dose.to_dict() if self.medium_dose else None,
            'high_dose': self.high_dose.to_dict() if self.high_dose else None,
            'dose_response_points': self.dose_response_points,
            'threshold_dose': self.threshold_dose
        }


# Convenience factory functions

def create_precise_model(points: List[Tuple[float, float]]) -> DoseEffectModel:
    """
    Create a PRECISE dose model from known dose-response points.
    
    Args:
        points: List of (dose, frequency_percentage) tuples
        
    Example:
        model = create_precise_model([
            (2.5, 10),   # 2.5mg → 10% effect
            (5.0, 20),   # 5mg → 20% effect
            (10.0, 40)   # 10mg → 40% effect
        ])
    """
    return DoseEffectModel(
        model_type="precise",
        dose_response_points=points
    )


def create_approximate_model(
    typical_max_dose: float,
    low: Optional[Tuple[float, str]] = None,      # (frequency%, description)
    medium: Optional[Tuple[float, str]] = None,
    high: Optional[Tuple[float, str]] = None,
    low_magnitude: str = "mild",
    medium_magnitude: str = "moderate",
    high_magnitude: str = "severe"
) -> DoseEffectModel:
    """
    Create an APPROXIMATE dose model with low/medium/high brackets.
    
    This is the most clinically realistic model for most medications.
    
    Args:
        typical_max_dose: Standard maximum therapeutic dose
        low: (frequency%, description) for low dose effects
        medium: (frequency%, description) for medium dose effects
        high: (frequency%, description) for high dose effects
        
    Example:
        model = create_approximate_model(
            typical_max_dose=5.0,
            low=(10.0, "Mild hypokalemia risk"),
            medium=(20.0, "Moderate hypokalemia risk"),
            high=(40.0, "Significant hypokalemia risk")
        )
    """
    low_range = None
    medium_range = None
    high_range = None
    
    if low:
        low_range = DoseEffectRange(
            min_dose=typical_max_dose * 0.25,
            max_dose=typical_max_dose * 0.5,
            dose_unit="mg",
            frequency_percentage=low[0],
            magnitude=low_magnitude,
            description=low[1]
        )
    
    if medium:
        medium_range = DoseEffectRange(
            min_dose=typical_max_dose * 0.5,
            max_dose=typical_max_dose,
            dose_unit="mg",
            frequency_percentage=medium[0],
            magnitude=medium_magnitude,
            description=medium[1]
        )
    
    if high:
        high_range = DoseEffectRange(
            min_dose=typical_max_dose,
            max_dose=typical_max_dose * 2,
            dose_unit="mg",
            frequency_percentage=high[0],
            magnitude=high_magnitude,
            description=high[1]
        )
    
    return DoseEffectModel(
        model_type="approximate",
        typical_max_dose=typical_max_dose,
        low_dose=low_range,
        medium_dose=medium_range,
        high_dose=high_range
    )


def create_threshold_model(
    threshold: float,
    unit: str,
    effect_description: str,
    frequency: float = 90.0
) -> DoseEffectModel:
    """
    Create a THRESHOLD dose model.
    
    Effect only manifests above a specific dose (e.g., toxicity).
    
    Args:
        threshold: Dose threshold
        unit: Unit of measurement
        effect_description: Description of effect above threshold
        frequency: Probability of effect above threshold (default 90%)
        
    Example:
        # Vitamin B6 neurotoxicity above 100mg
        model = create_threshold_model(
            threshold=100.0,
            unit="mg",
            effect_description="Risk of sensory neuropathy",
            frequency=85.0
        )
    """
    return DoseEffectModel(
        model_type="threshold",
        threshold_dose=threshold,
        threshold_unit=unit,
        above_threshold_effect=effect_description,
        above_threshold_frequency=frequency
    )


# Export public API
__all__ = [
    'DoseEffectRange',
    'DoseEffectModel',
    'create_precise_model',
    'create_approximate_model',
    'create_threshold_model'
]
