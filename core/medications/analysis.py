"""
Medication effect analysis engine.

Provides functionality to analyze blood test results in the context of
patient medications, determining if observed values are consistent with
expected medication effects.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Tuple, Dict, Any
from enum import Enum

from .models import (
    Medication, 
    MedicationEffect, 
    PatientMedication,
    EffectTargetType,
    EffectDirection
)
from .database import MedicationDatabase


class AnalysisResult(Enum):
    """Possible results of biomarker vs medication analysis"""
    EXPECTED = "expected"           # Value matches medication effect
    EXPLAINED = "explained"         # Value explained by medication
    UNEXPECTED = "unexpected"       # Value contradicts expected effect
    UNRELATED = "unrelated"         # Medication doesn't affect this biomarker
    INSUFFICIENT_DATA = "insufficient_data"  # Can't determine


@dataclass
class EffectAnalysis:
    """
    Result of analyzing a biomarker value against medication effects.
    
    This is the primary output of the analysis engine, containing:
    - Whether the value is consistent with medication
    - Probability of the effect
    - Clinical explanation
    - Monitoring recommendations
    """
    medication: str
    target_name: str
    target_value: Optional[float] = None
    reference_range: Optional[Tuple[float, float]] = None
    unit: Optional[str] = None
    
    is_affected: bool = False
    is_expected: bool = False
    result: AnalysisResult = AnalysisResult.UNRELATED
    
    primary_effect: Optional[MedicationEffect] = None
    all_effects: List[Dict] = field(default_factory=list)
    
    probability: float = 0.0
    patient_probability: Optional[float] = None  # Adjusted for patient factors
    
    requires_monitoring: bool = False
    monitoring_urgency: str = "routine"  # "routine", "soon", "urgent"
    
    explanation: str = ""
    clinical_notes: str = ""
    recommendation: str = ""
    
    sources: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            'medication': self.medication,
            'target': self.target_name,
            'value': self.target_value,
            'unit': self.unit,
            'is_expected': self.is_expected,
            'result': self.result.value,
            'probability': self.probability,
            'patient_probability': self.patient_probability,
            'requires_monitoring': self.requires_monitoring,
            'monitoring_urgency': self.monitoring_urgency,
            'explanation': self.explanation,
            'recommendation': self.recommendation
        }
    
    def to_markdown(self) -> str:
        """Format as markdown for reports"""
        lines = [
            f"### {self.medication}",
            "",
            f"**Result:** {self.result.value.replace('_', ' ').title()}",
        ]
        
        if self.target_value is not None:
            lines.append(f"**Value:** {self.target_value} {self.unit or ''}")
        
        if self.probability > 0:
            lines.append(f"**Expected Effect Probability:** {self.probability:.0f}%")
        
        if self.patient_probability is not None:
            lines.append(f"**Patient-Specific Probability:** {self.patient_probability:.0f}%")
        
        lines.append("")
        
        if self.explanation:
            lines.append(f"**Explanation:** {self.explanation}")
            lines.append("")
        
        if self.requires_monitoring:
            lines.append(f"**Monitoring:** {self.recommendation}")
            lines.append("")
        
        if self.sources:
            lines.append("**Sources:**")
            for source in self.sources[:3]:  # Limit to top 3
                lines.append(f"- {source}")
            lines.append("")
        
        return "\n".join(lines)


class MedicationAnalyzer:
    """
    Analyzes blood test results in the context of patient medications.
    
    This is the core analysis engine that:
    1. Identifies which medications affect each biomarker
    2. Calculates expected effects based on dose and patient factors
    3. Determines if observed values are consistent with medications
    4. Generates clinical recommendations
    
    Usage:
        analyzer = MedicationAnalyzer()
        
        # Analyze single biomarker
        analysis = analyzer.analyze_biomarker(
            biomarker_name="Potassium",
            value=3.31,
            unit="mmol/L",
            reference_range=(3.5, 5.0),
            patient_medications=[xipamid_2_5mg],
            patient_data={'age': 56, 'gender': 'male'}
        )
    """
    
    def __init__(self, database: Optional[MedicationDatabase] = None):
        """
        Initialize analyzer.
        
        Args:
            database: MedicationDatabase to use (creates default if None)
        """
        self.db = database or MedicationDatabase()
    
    def analyze_biomarker(
        self,
        biomarker_name: str,
        value: float,
        unit: str,
        reference_range: Tuple[float, float],
        patient_medications: List[PatientMedication],
        patient_data: Optional[Dict[str, Any]] = None
    ) -> List[EffectAnalysis]:
        """
        Analyze a biomarker value against all patient medications.
        
        Args:
            biomarker_name: Name of biomarker (e.g., "Potassium")
            value: Measured value
            unit: Unit of measurement
            reference_range: (min, max) normal range
            patient_medications: List of patient's current medications
            patient_data: Optional patient attributes for probability adjustment
            
        Returns:
            List of EffectAnalysis objects (one per affecting medication)
        """
        analyses = []
        patient_data = patient_data or {}
        
        for patient_med in patient_medications:
            # Look up medication in database
            med = self.db.get(patient_med.medication_name)
            if not med:
                continue
            
            # Analyze this medication's effect
            analysis = self._analyze_single_medication(
                medication=med,
                patient_medication=patient_med,
                biomarker_name=biomarker_name,
                value=value,
                unit=unit,
                reference_range=reference_range,
                patient_data=patient_data
            )
            
            if analysis:
                analyses.append(analysis)
        
        return analyses
    
    def _analyze_single_medication(
        self,
        medication: Medication,
        patient_medication: PatientMedication,
        biomarker_name: str,
        value: float,
        unit: str,
        reference_range: Tuple[float, float],
        patient_data: Dict[str, Any]
    ) -> Optional[EffectAnalysis]:
        """
        Analyze a single medication's effect on a biomarker.
        """
        # Get all effects on this biomarker
        applicable_effects = medication.get_effects_on_target(
            biomarker_name, 
            EffectTargetType.BIOMARKER
        )
        
        if not applicable_effects:
            return None
        
        ref_min, ref_max = reference_range
        in_normal_range = ref_min <= value <= ref_max
        
        # Analyze each effect
        effect_analyses = []
        for effect in applicable_effects:
            # Calculate probabilities
            base_prob = effect.frequency_percentage
            patient_prob = effect.get_probability_for_patient(
                patient_data, 
                patient_medication.dosage
            )
            
            # Determine if value matches expected direction
            matches_expected = self._check_direction_match(
                effect.direction,
                value,
                reference_range
            )
            
            effect_analyses.append({
                'effect': effect,
                'base_probability': base_prob,
                'patient_probability': patient_prob,
                'matches_expected': matches_expected,
                'in_normal_range': in_normal_range
            })
        
        # Determine primary effect (highest probability match)
        primary = None
        for ea in effect_analyses:
            if ea['matches_expected']:
                if primary is None or ea['patient_probability'] > primary['patient_probability']:
                    primary = ea
        
        # Determine result category
        is_expected = primary is not None
        
        if is_expected:
            result = AnalysisResult.EXPECTED
        elif in_normal_range:
            result = AnalysisResult.EXPLAINED
        else:
            # Value is abnormal but not in expected direction
            result = AnalysisResult.UNEXPECTED
        
        # Generate explanation
        explanation = self._generate_explanation(
            medication,
            patient_medication,
            biomarker_name,
            value,
            reference_range,
            effect_analyses,
            is_expected
        )
        
        # Generate recommendation
        requires_monitoring = any(
            ea['effect'].requires_monitoring for ea in effect_analyses
        )
        
        recommendation = self._generate_recommendation(
            medication,
            effect_analyses,
            is_expected,
            requires_monitoring
        )
        
        # Determine urgency
        urgency = self._determine_urgency(
            effect_analyses,
            is_expected,
            value,
            reference_range
        )
        
        # Collect sources
        sources = []
        for ea in effect_analyses:
            for quote in ea['effect'].evidence[:1]:  # Top source per effect
                if quote.source and quote.source not in sources:
                    sources.append(quote.source)
        
        return EffectAnalysis(
            medication=medication.name,
            target_name=biomarker_name,
            target_value=value,
            reference_range=reference_range,
            unit=unit,
            is_affected=True,
            is_expected=is_expected,
            result=result,
            primary_effect=primary['effect'] if primary else None,
            all_effects=effect_analyses,
            probability=primary['patient_probability'] if primary else 0,
            patient_probability=primary['patient_probability'] if primary else None,
            requires_monitoring=requires_monitoring,
            monitoring_urgency=urgency,
            explanation=explanation,
            recommendation=recommendation,
            sources=sources
        )
    
    def _check_direction_match(
        self,
        direction: EffectDirection,
        value: float,
        reference_range: Tuple[float, float]
    ) -> bool:
        """
        Check if a value matches the expected direction of effect.
        
        Returns True if:
        - Direction is DECREASE and value is below normal
        - Direction is INCREASE and value is above normal
        - Direction is VARIABLE (can't determine)
        """
        ref_min, ref_max = reference_range
        
        if direction == EffectDirection.DECREASE:
            return value < ref_min
        elif direction == EffectDirection.INCREASE:
            return value > ref_max
        elif direction == EffectDirection.VARIABLE:
            return True  # Variable effects can't be directionally matched
        else:
            return False
    
    def _generate_explanation(
        self,
        medication: Medication,
        patient_medication: PatientMedication,
        biomarker_name: str,
        value: float,
        reference_range: Tuple[float, float],
        effect_analyses: List[Dict],
        is_expected: bool
    ) -> str:
        """Generate human-readable explanation"""
        lines = []
        
        # Medication info
        lines.append(f"Patient is taking {medication.name} "
                    f"({patient_medication.dosage}{patient_medication.dosage_unit} "
                    f"{patient_medication.frequency.replace('_', ' ')}).")
        
        # Effect descriptions
        for ea in effect_analyses:
            effect = ea['effect']
            direction = effect.direction.value
            prob = ea['patient_probability']
            
            lines.append(f"\nThis medication {direction}s {biomarker_name}:")
            lines.append(f"- Frequency: {effect.frequency_category.value.replace('_', ' ')} "
                        f"(~{prob:.0f}% probability for this patient)")
            
            if effect.mechanism:
                lines.append(f"- Mechanism: {effect.mechanism}")
        
        # Value assessment
        ref_min, ref_max = reference_range
        if is_expected:
            lines.append(f"\n[OK] The measured value ({value}) is consistent with "
                        f"the expected effect of {medication.name}.")
            # Get direction from primary effect
            primary_effect = effect_analyses[0]['effect'] if effect_analyses else None
            if primary_effect:
                if value < ref_min:
                    lines.append(f"  (Below normal range {ref_min}-{ref_max}, "
                               f"consistent with {primary_effect.direction.value})")
                elif value > ref_max:
                    lines.append(f"  (Above normal range {ref_min}-{ref_max}, "
                               f"consistent with {primary_effect.direction.value})")
        elif ref_min <= value <= ref_max:
            lines.append(f"\n[OK] Value is within normal range despite medication effect. "
                        f"This can occur and does not indicate a problem.")
        else:
            lines.append(f"\n[WARN] The measured value ({value}) is abnormal but not in "
                        f"the expected direction for {medication.name}.")
            lines.append(f"  Consider other causes for this finding.")
        
        return "\n".join(lines)
    
    def _generate_recommendation(
        self,
        medication: Medication,
        effect_analyses: List[Dict],
        is_expected: bool,
        requires_monitoring: bool
    ) -> str:
        """Generate clinical recommendation"""
        if not is_expected:
            return "Continue current monitoring. No specific action required."
        
        # Collect monitoring recommendations
        recs = []
        for ea in effect_analyses:
            effect = ea['effect']
            if effect.monitoring_recommendation:
                recs.append(effect.monitoring_recommendation)
        
        if recs:
            return "; ".join(recs)
        
        if requires_monitoring:
            return f"Continue routine monitoring per {medication.name} protocol."
        
        return "No specific monitoring required for this effect."
    
    def _determine_urgency(
        self,
        effect_analyses: List[Dict],
        is_expected: bool,
        value: float,
        reference_range: Tuple[float, float]
    ) -> str:
        """Determine monitoring urgency"""
        ref_min, ref_max = reference_range
        
        # Check for critical values
        critical_low = ref_min * 0.8 if ref_min > 0 else value - 1
        critical_high = ref_max * 1.2 if ref_max > 0 else value + 1
        
        if value < critical_low or value > critical_high:
            return "urgent"
        
        # Check for concerning but not critical
        concerning_low = ref_min * 0.9
        concerning_high = ref_max * 1.1
        
        if value < concerning_low or value > concerning_high:
            return "soon"
        
        # Expected effects are routine
        if is_expected:
            return "routine"
        
        # Unexpected abnormal values need attention
        if not (ref_min <= value <= ref_max):
            return "soon"
        
        return "routine"
    
    def analyze_blood_test(
        self,
        results: Dict[str, Dict[str, Any]],
        patient_medications: List[PatientMedication],
        patient_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, List[EffectAnalysis]]:
        """
        Analyze a complete blood test panel.
        
        Args:
            results: Dictionary of biomarker results
                    {biomarker_name: {'value': X, 'unit': 'Y', 'reference': (min, max)}}
            patient_medications: List of patient's medications
            patient_data: Optional patient attributes
            
        Returns:
            Dictionary mapping biomarker names to lists of EffectAnalysis
        """
        all_analyses = {}
        
        for biomarker_name, result in results.items():
            analyses = self.analyze_biomarker(
                biomarker_name=biomarker_name,
                value=result['value'],
                unit=result['unit'],
                reference_range=result['reference'],
                patient_medications=patient_medications,
                patient_data=patient_data
            )
            
            if analyses:
                all_analyses[biomarker_name] = analyses
        
        return all_analyses
    
    def generate_medication_summary(
        self,
        patient_medications: List[PatientMedication],
        patient_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate summary of all medication effects for a patient.
        
        Useful for getting overview of what to monitor.
        """
        summary = {
            'total_medications': len(patient_medications),
            'medications_with_effects': 0,
            'biomarkers_affected': set(),
            'requires_monitoring': [],
            'drug_interactions': [],
            'by_medication': {}
        }
        
        for patient_med in patient_medications:
            med = self.db.get(patient_med.medication_name)
            if not med:
                continue
            
            med_summary = {
                'name': med.name,
                'dose': f"{patient_med.dosage}{patient_med.dosage_unit}",
                'biomarker_effects': [],
                'symptom_effects': [],
                'monitoring_required': []
            }
            
            # Collect biomarker effects
            for effect in med.get_biomarker_effects():
                prob = effect.get_probability_for_patient(
                    patient_data or {}, 
                    patient_med.dosage
                )
                
                med_summary['biomarker_effects'].append({
                    'target': effect.target_name,
                    'direction': effect.direction.value,
                    'probability': prob
                })
                summary['biomarkers_affected'].add(effect.target_name)
                
                if effect.requires_monitoring:
                    med_summary['monitoring_required'].append({
                        'target': effect.target_name,
                        'recommendation': effect.monitoring_recommendation
                    })
                    summary['requires_monitoring'].append({
                        'medication': med.name,
                        'biomarker': effect.target_name,
                        'recommendation': effect.monitoring_recommendation
                    })
            
            summary['by_medication'][med.name] = med_summary
            summary['medications_with_effects'] += 1
        
        # Check for drug interactions
        med_names = [pm.medication_name for pm in patient_medications]
        for patient_med in patient_medications:
            med = self.db.get(patient_med.medication_name)
            if med:
                for interaction in med.drug_interactions:
                    if interaction.interacting_drug in med_names:
                        summary['drug_interactions'].append({
                            'drug1': med.name,
                            'drug2': interaction.interacting_drug,
                            'severity': interaction.severity,
                            'description': interaction.effect_description
                        })
        
        summary['biomarkers_affected'] = sorted(list(summary['biomarkers_affected']))
        return summary


# Export public API
__all__ = [
    'AnalysisResult',
    'EffectAnalysis',
    'MedicationAnalyzer'
]
