"""
Core data models for the medication database system.

This module defines the complete data structures for medications, their effects,
dosage relationships, and analysis capabilities.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Tuple, Any, Dict
from datetime import date
from enum import Enum


class EffectTargetType(Enum):
    """Types of targets that medications can affect"""
    BIOMARKER = "biomarker"
    VITAL_SIGN = "vital_sign"
    SYMPTOM = "symptom"
    CLINICAL_OUTCOME = "clinical_outcome"


class EffectDirection(Enum):
    """Direction of medication effect"""
    INCREASE = "increase"
    DECREASE = "decrease"
    VARIABLE = "variable"
    NONE = "none"


class FrequencyCategory(Enum):
    """Frequency categories for adverse effects (ICH guidelines)"""
    VERY_COMMON = "very_common"      # >10%
    COMMON = "common"                 # 1-10%
    UNCOMMON = "uncommon"             # 0.1-1%
    RARE = "rare"                     # 0.01-0.1%
    VERY_RARE = "very_rare"           # <0.01%


class DoseEffectModelType(Enum):
    """Types of dose-effect relationships"""
    PRECISE = "precise"               # Known dose-response curve
    APPROXIMATE = "approximate"       # Low/medium/high brackets
    THRESHOLD = "threshold"           # Effect above certain dose


@dataclass
class Quote:
    """
    Source attribution for clinical information.
    
    Attributes:
        text: The clinical information or statement
        source: URL, DOI, or citation
        source_type: Type of source for categorization
    """
    text: str
    source: str = ""
    source_type: str = "research"  # "research", "guideline", "fda_label", "clinical"
    
    def __str__(self):
        return f"{self.text} [{self.source}]"


@dataclass
class DoseEffectRange:
    """
    Effect at a specific dose level.
    
    Used within APPROXIMATE dose models to define effects at 
    low, medium, and high dose ranges.
    """
    min_dose: float
    max_dose: float
    dose_unit: str
    frequency_percentage: float  # 0-100
    magnitude: str               # "mild", "moderate", "severe"
    description: str
    
    def __post_init__(self):
        """Validate frequency percentage"""
        if not 0 <= self.frequency_percentage <= 100:
            raise ValueError(f"Frequency must be 0-100, got {self.frequency_percentage}")


@dataclass  
class RiskFactor:
    """
    Patient factors that modify the probability of medication effects.
    
    Examples:
        - Age > 65 increases thiazide-induced hyponatremia risk
        - Baseline K+ < 3.8 increases hypokalemia risk
        - Concurrent loop diuretics increase potassium wasting
    """
    factor_type: str             # "age", "gender", "condition", "biomarker", "concurrent_med"
    description: str             # Human-readable description
    multiplier: float = 1.0      # How much this increases probability (e.g., 1.5 = 50% increase)
    
    # Specific check parameters
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    gender: Optional[str] = None
    condition: Optional[str] = None
    biomarker_name: Optional[str] = None
    biomarker_range: Optional[Tuple[float, float]] = None  # (min, max) values
    concurrent_med: Optional[str] = None
    
    def applies_to(self, patient_data: Dict) -> bool:
        """
        Check if this risk factor applies to a specific patient.
        
        Args:
            patient_data: Dictionary with patient attributes
            
        Returns:
            True if risk factor applies to this patient
        """
        # Age check
        if self.age_min is not None:
            if patient_data.get('age', 0) < self.age_min:
                return False
        if self.age_max is not None:
            if patient_data.get('age', 0) > self.age_max:
                return False
        
        # Gender check
        if self.gender is not None:
            if patient_data.get('gender') != self.gender:
                return False
        
        # Medical condition check
        if self.condition is not None:
            conditions = patient_data.get('conditions', [])
            if isinstance(conditions, str):
                conditions = [conditions]
            if self.condition not in conditions:
                return False
        
        # Current medication check
        if self.concurrent_med is not None:
            current_meds = patient_data.get('medications', [])
            med_names = [m.name if hasattr(m, 'name') else m for m in current_meds]
            if self.concurrent_med not in med_names:
                return False
        
        return True


@dataclass
class MedicationEffect:
    """
    Defines how a medication affects a specific target.
    
    This is the core class that links medications to their effects on:
    - Biomarkers (e.g., potassium decrease)
    - Vital signs (e.g., blood pressure decrease)
    - Symptoms (e.g., dizziness)
    - Clinical outcomes (e.g., cardiovascular risk reduction)
    
    Includes dose-dependent modeling, risk factors, and evidence sources.
    """
    
    # Required fields (no defaults)
    target_type: EffectTargetType
    target_name: str
    direction: EffectDirection
    typical_magnitude: str                       # "mild", "moderate", "severe"
    frequency_category: FrequencyCategory
    
    # Fields with defaults
    target_synonyms: List[str] = field(default_factory=list)
    dose_dependent: bool = False
    dose_model: Optional[Any] = None             # Will be DoseEffectModel, set via post_init
    frequency_percentage: Optional[float] = None # Exact percentage if known
    time_to_onset: str = "days"                  # "immediate", "hours", "days", "weeks", "months"
    duration: str = "persistent"                 # "transient", "persistent", "dose_dependent"
    administration_time_relevant: bool = False   # True for diuretics, statins
    mechanism: str = ""
    clinical_significance: str = "expected"      # "expected", "monitor", "concerning", "emergency"
    requires_monitoring: bool = False
    monitoring_recommendation: str = ""
    risk_factors: List[RiskFactor] = field(default_factory=list)
    protective_factors: List[str] = field(default_factory=list)
    evidence: List[Quote] = field(default_factory=list)
    likelihood_score: str = ""                   # "A"=well-established, "B"=documented, "C"=suspected
    symptom_description: str = ""                # If target_type == SYMPTOM
    outcome_metric: str = ""                     # If target_type == CLINICAL_OUTCOME
    outcome_timeframe: str = ""                  # "3_months", "1_year", etc.
    
    def __post_init__(self):
        """Set default frequency percentage from category if not provided"""
        if self.frequency_percentage is None:
            self.frequency_percentage = self._category_to_percentage()
    
    def _category_to_percentage(self) -> float:
        """Convert frequency category to approximate percentage"""
        mapping = {
            FrequencyCategory.VERY_COMMON: 25.0,
            FrequencyCategory.COMMON: 5.5,
            FrequencyCategory.UNCOMMON: 0.5,
            FrequencyCategory.RARE: 0.05,
            FrequencyCategory.VERY_RARE: 0.005
        }
        return mapping.get(self.frequency_category, 5.0)
    
    def get_probability_for_patient(self, patient_data: Dict, dose: Optional[float] = None) -> float:
        """
        Calculate patient-specific effect probability.
        
        Args:
            patient_data: Patient attributes dictionary
            dose: Current dose in mg (optional, for dose-dependent effects)
            
        Returns:
            Adjusted probability percentage (0-100)
        """
        base_prob = self.frequency_percentage or self._category_to_percentage()
        
        # Adjust for risk factors
        for risk in self.risk_factors:
            if risk.applies_to(patient_data):
                base_prob *= risk.multiplier
        
        # Adjust for dose if applicable
        if self.dose_dependent and dose is not None and self.dose_model is not None:
            dose_effect = self.dose_model.get_effect_for_dose(dose, "mg")
            if dose_effect:
                base_prob = dose_effect.frequency_percentage
        
        return min(base_prob, 100.0) if base_prob is not None else 0.0
    
    def matches_target(self, target_name: str) -> bool:
        """Check if this effect applies to a named target"""
        search_name = target_name.lower()
        all_names = [self.target_name.lower()] + [s.lower() for s in self.target_synonyms]
        return search_name in all_names


@dataclass
class DrugInteraction:
    """
    Interaction between this medication and another drug.
    
    Includes severity classification and management recommendations.
    """
    interacting_drug: str
    severity: str                                # "contraindicated", "major", "moderate", "minor"
    effect_description: str
    mechanism: str = ""
    management: str = ""
    evidence: List[Quote] = field(default_factory=list)


@dataclass
class MonitoringRequirement:
    """
    Defines what should be monitored when taking this medication.
    """
    target_type: EffectTargetType
    target_name: str
    baseline_required: bool = True
    frequency: str = ""                          # "weekly", "monthly", "quarterly", "annually"
    condition: str = ""                          # "if elderly", "if dose > X", etc.


@dataclass
class Medication:
    """
    Complete medication profile with all effects and clinical information.
    
    This is the primary data container for a medication in the database.
    Includes identification, classification, effects, interactions, and monitoring.
    """
    
    # Identification
    name: str                                    # Generic name
    name_de: str = ""                           # German name
    brand_names: List[str] = field(default_factory=list)
    synonyms: List[str] = field(default_factory=list)  # ATC codes, abbreviations
    
    # Classification
    drug_class: str = ""                         # e.g., "Diuretic"
    drug_subclass: str = ""                      # e.g., "Thiazide"
    
    # Dosage information
    available_doses: List[Tuple[float, str]] = field(default_factory=list)  # [(5, "mg"), (10, "mg")]
    typical_dose_range: Optional[Tuple[float, float]] = None  # (min, max) mg
    
    # Core effects data
    effects: List[MedicationEffect] = field(default_factory=list)
    
    # Clinical use
    indications: List[Quote] = field(default_factory=list)
    contraindications: List[Quote] = field(default_factory=list)
    black_box_warnings: List[Quote] = field(default_factory=list)
    
    # Safety information
    drug_interactions: List[DrugInteraction] = field(default_factory=list)
    monitoring_protocol: List[MonitoringRequirement] = field(default_factory=list)
    
    # Regulatory
    pregnancy_category: str = ""                 # "A", "B", "C", "D", "X"
    requires_prescription: bool = True
    controlled_substance: bool = False
    
    # Sources
    primary_sources: List[Quote] = field(default_factory=list)
    fda_label_url: str = ""
    ema_label_url: str = ""
    
    # Metadata
    last_updated: str = ""
    
    def get_effects_on_target(self, target_name: str, 
                             target_type: Optional[EffectTargetType] = None) -> List[MedicationEffect]:
        """
        Get all effects on a specific target.
        
        Args:
            target_name: Name of target (e.g., "Potassium")
            target_type: Optional filter by target type
            
        Returns:
            List of matching MedicationEffect objects
        """
        matching = []
        for effect in self.effects:
            if effect.matches_target(target_name):
                if target_type is None or effect.target_type == target_type:
                    matching.append(effect)
        return matching
    
    def get_biomarker_effects(self) -> List[MedicationEffect]:
        """Get all biomarker effects for this medication"""
        return [e for e in self.effects if e.target_type == EffectTargetType.BIOMARKER]
    
    def get_symptom_effects(self) -> List[MedicationEffect]:
        """Get all symptom effects for this medication"""
        return [e for e in self.effects if e.target_type == EffectTargetType.SYMPTOM]
    
    def get_vital_effects(self) -> List[MedicationEffect]:
        """Get all vital sign effects for this medication"""
        return [e for e in self.effects if e.target_type == EffectTargetType.VITAL_SIGN]
    
    def affects_biomarker(self, biomarker_name: str) -> bool:
        """Quick check if medication affects a biomarker"""
        return len(self.get_effects_on_target(biomarker_name, EffectTargetType.BIOMARKER)) > 0
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            'name': self.name,
            'name_de': self.name_de,
            'drug_class': self.drug_class,
            'effects_count': len(self.effects),
            'requires_prescription': self.requires_prescription
        }


@dataclass 
class PatientMedication:
    """
    A medication actually being taken by a patient.
    
    Links to the Medication database entry with patient-specific details
    like dose, timing, and duration.
    """
    medication_name: str                         # Links to Medication.name
    dosage: float
    dosage_unit: str
    frequency: str                               # "once_daily", "BID", "TID", "as_needed"
    administration_time: str = "morning"         # "morning", "midday", "evening", "bedtime"
    start_date: Optional[date] = None
    end_date: Optional[date] = None              # None = currently taking
    prescribed_for: str = ""                     # Indication
    notes: str = ""
    
    def is_active_on(self, query_date: date) -> bool:
        """Check if medication was active on a specific date"""
        if self.start_date and query_date < self.start_date:
            return False
        if self.end_date and query_date > self.end_date:
            return False
        return True
    
    def is_current(self) -> bool:
        """Check if currently active"""
        return self.is_active_on(date.today())


@dataclass
class VitalsSnapshot:
    """Snapshot of vital signs at a specific time"""
    timestamp: date
    blood_pressure_systolic: Optional[int] = None
    blood_pressure_diastolic: Optional[int] = None
    heart_rate: Optional[int] = None
    weight: Optional[float] = None
    temperature: Optional[float] = None
    notes: str = ""


@dataclass
class TemporalValue:
    """
    Wrapper for any value that changes over time.
    
    Used to track medications, conditions, weight, etc. with start/end dates.
    """
    value: Any
    start_date: date
    end_date: Optional[date] = None
    notes: str = ""
    
    def is_active_on(self, query_date: date) -> bool:
        """Check if value was active on a specific date"""
        if query_date < self.start_date:
            return False
        if self.end_date and query_date > self.end_date:
            return False
        return True


@dataclass
class PatientProfile:
    """
    Complete patient profile with full temporal history.
    
    Supports querying patient state at any point in time,
    tracking medication changes, and analyzing trends.
    """
    # Required fields (no defaults)
    patient_id: str
    gender: str
    birth_date: date
    
    # Optional fields (with defaults)
    name: str = ""
    medications: List[TemporalValue] = field(default_factory=list)  # TemporalValue[PatientMedication]
    conditions: List[TemporalValue] = field(default_factory=list)   # TemporalValue[str]
    weight_history: List[TemporalValue] = field(default_factory=list)  # TemporalValue[float]
    vitals: List[VitalsSnapshot] = field(default_factory=list)
    lifestyle: List[TemporalValue] = field(default_factory=list)
    lab_files: List[Dict] = field(default_factory=list)
    lab_files: List[Dict] = field(default_factory=list)
    
    def get_age_on_date(self, query_date: date) -> int:
        """Calculate age on a specific date"""
        age = query_date.year - self.birth_date.year
        if query_date.month < self.birth_date.month or \
           (query_date.month == self.birth_date.month and query_date.day < self.birth_date.day):
            age -= 1
        return age
    
    def get_current_age(self) -> int:
        """Get current age"""
        return self.get_age_on_date(date.today())
    
    def get_medications_on_date(self, query_date: date) -> List[PatientMedication]:
        """Get all active medications on a specific date"""
        active = []
        for temp_med in self.medications:
            if temp_med.is_active_on(query_date):
                active.append(temp_med.value)
        return active
    
    def get_current_medications(self) -> List[PatientMedication]:
        """Get currently active medications"""
        return self.get_medications_on_date(date.today())
    
    def get_medication_history(self, medication_name: str) -> List[TemporalValue]:
        """Get complete history of a specific medication"""
        return [tm for tm in self.medications 
                if tm.value.medication_name == medication_name]
    
    def get_conditions_on_date(self, query_date: date) -> List[str]:
        """Get all active conditions on a specific date"""
        active = []
        for temp_cond in self.conditions:
            if temp_cond.is_active_on(query_date):
                active.append(temp_cond.value)
        return active
    
    def get_weight_on_date(self, query_date: date) -> Optional[float]:
        """Get weight on or before a specific date (most recent)"""
        valid_weights = [tw for tw in self.weight_history 
                        if tw.start_date <= query_date]
        if valid_weights:
            return sorted(valid_weights, key=lambda x: x.start_date)[-1].value
        return None
    
    def get_patient_data_for_date(self, query_date: date) -> Dict:
        """
        Compile all patient data as of a specific date.
        
        Returns dictionary suitable for medication effect probability calculation.
        """
        return {
            'patient_id': self.patient_id,
            'gender': self.gender,
            'age': self.get_age_on_date(query_date),
            'medications': self.get_medications_on_date(query_date),
            'conditions': self.get_conditions_on_date(query_date),
            'weight': self.get_weight_on_date(query_date)
        }


# Export all public classes
__all__ = [
    'EffectTargetType',
    'EffectDirection', 
    'FrequencyCategory',
    'DoseEffectModelType',
    'Quote',
    'DoseEffectRange',
    'RiskFactor',
    'MedicationEffect',
    'DrugInteraction',
    'MonitoringRequirement',
    'Medication',
    'PatientMedication',
    'VitalsSnapshot',
    'TemporalValue',
    'PatientProfile'
]
