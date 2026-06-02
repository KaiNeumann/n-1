"""
Correlation Engine Module

Connects diary data (food, medications, activities, vitals) with blood test
biomarkers to explain changes and generate insights.

Example Usage:
    >>> from blutwerte.correlation import CorrelationEngine
    >>> from blutwerte.diary import Diary
    >>> from blutwerte.bloodtests import BloodTestResult
    >>>
    >>> engine = CorrelationEngine(diary=diary, blood_tests=blood_tests)
    >>> result = engine.analyze_change("ldl", start_date, end_date)
    >>> print(result)
    >>> insights = engine.generate_insights()
"""

from datetime import datetime, date, timedelta
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import math


class EvidenceStrength(Enum):
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"
    ANECDOTAL = "anecdotal"


@dataclass
class FactorContribution:
    """How much a specific factor contributed to a biomarker change."""
    source: str          # "food", "medication", "activity", "vital"
    factor: str           # "oatmeal", "statin", "running", "sleep"
    estimated_impact: float  # e.g., -15 (mg/dL or %)
    impact_percent: float   # What % of total change this explains
    evidence_strength: EvidenceStrength
    description: str = ""


@dataclass
class CorrelationResult:
    """Result of analyzing a biomarker's change."""
    biomarker: str
    start_value: float
    end_value: float
    change: float
    change_percent: float
    
    time_period_days: int
    start_date: date
    end_date: date
    
    contributing_factors: List[FactorContribution] = field(default_factory=list)
    
    confidence: float = 0.0        # 0-1
    p_value: float = 1.0
    correlation_found: bool = False
    
    explanation: str = ""
    recommendations: List[str] = field(default_factory=list)


@dataclass
class Insight:
    """Actionable health insight generated from correlations."""
    id: str
    title: str
    message: str
    
    insight_type: str      # "food", "medication", "activity", "vital", "pattern"
    priority: str           # "high", "medium", "low"
    
    biomarker: Optional[str] = None
    related_metrics: List[str] = field(default_factory=list)
    action_items: List[str] = field(default_factory=list)
    estimated_impact: Optional[str] = None


@dataclass
class TimeAlignedData:
    """Diary data aligned to blood test periods."""
    period_start: date
    period_end: date
    biomarker_value: Optional[float] = None
    
    # Aggregated diary data
    food_frequency: Dict[str, int] = field(default_factory=dict)      # food_name: count
    medications: Dict[str, int] = field(default_factory=dict)           # med_name: doses_taken
    activities: Dict[str, int] = field(default_factory=dict)            # activity: minutes
    vitals: Dict[str, List[float]] = field(default_factory=dict)        # metric: [values]
    sleep: Dict[str, float] = field(default_factory=dict)               # avg values


class KnownEffect:
    """A known effect of food/medication/activity on a biomarker."""
    def __init__(
        self,
        source: str,
        factor: str,
        biomarker: str,
        effect_type: str,    # "increase", "decrease", "no_effect"
        effect_magnitude: float,  # % change expected
        evidence: EvidenceStrength,
        timeframe_days: int = 30,   # How long to see effect
        mechanism: str = "",
    ):
        self.source = source
        self.factor = factor
        self.biomarker = biomarker
        self.effect_type = effect_type
        self.effect_magnitude = effect_magnitude
        self.evidence = evidence
        self.timeframe_days = timeframe_days
        self.mechanism = mechanism


class CorrelationEngine:
    """
    Engine for correlating diary data with blood test biomarkers.
    
    Connects:
    - Food intake → Biomarker effects
    - Medications → Biomarker effects  
    - Activities → Biomarker effects
    - Vitals/Sleep → Biomarker correlations
    """
    
    def __init__(
        self,
        diary: Any = None,
        blood_tests: List[Any] = None,
        medication_diary: Any = None,
    ):
        self.diary = diary
        self.blood_tests = blood_tests or []
        self.medication_diary = medication_diary
        
        # Load known effects from existing modules
        self.known_effects: List[KnownEffect] = []
        self._load_known_effects()
    
    def _load_known_effects(self):
        """Load known effects from existing blutwerte databases."""
        
        # Food effects (from food analysis module)
        self._load_food_effects()
        
        # Medication effects (from medications module)
        self._load_medication_effects()
        
        # Activity effects
        self._load_activity_effects()
        
        # Vital correlations
        self._load_vital_correlations()
    
    def _load_food_effects(self):
        """Load known food → biomarker effects."""
        
        # Core LDL-lowering foods (evidence-based)
        food_effects = [
            ("oatmeal", "ldl", "decrease", 5, EvidenceStrength.STRONG, "beta-glucan fiber"),
            ("salmon", "ldl", "decrease", 3, EvidenceStrength.STRONG, "omega-3 fatty acids"),
            ("nuts", "ldl", "decrease", 4, EvidenceStrength.STRONG, "plant sterols"),
            ("olive_oil", "ldl", "decrease", 2, EvidenceStrength.MODERATE, "monounsaturated fats"),
            ("avocado", "ldl", "decrease", 2, EvidenceStrength.MODERATE, "fiber and plant sterols"),
            ("beans", "ldl", "decrease", 3, EvidenceStrength.MODERATE, "soluble fiber"),
            ("apples", "ldl", "decrease", 2, EvidenceStrength.MODERATE, "pectin fiber"),
            ("eggplant", "ldl", "decrease", 2, EvidenceStrength.WEAK, "soluble fiber"),
            ("okra", "ldl", "decrease", 2, EvidenceStrength.WEAK, "soluble fiber"),
            
            # HDL-increasing foods
            ("salmon", "hdl", "increase", 3, EvidenceStrength.STRONG, "omega-3"),
            ("olive_oil", "hdl", "increase", 2, EvidenceStrength.MODERATE, "healthy fats"),
            ("nuts", "hdl", "increase", 2, EvidenceStrength.MODERATE, "healthy fats"),
            ("avocado", "hdl", "increase", 1, EvidenceStrength.WEAK, "healthy fats"),
            
            # Triglyceride-lowering
            ("salmon", "triglycerides", "decrease", 5, EvidenceStrength.STRONG, "omega-3"),
            ("fish", "triglycerides", "decrease", 4, EvidenceStrength.STRONG, "omega-3"),
            ("oatmeal", "triglycerides", "decrease", 2, EvidenceStrength.MODERATE, "fiber"),
            
            # Anti-inflammatory (CRP)
            ("salmon", "crp", "decrease", 3, EvidenceStrength.MODERATE, "omega-3"),
            ("blueberries", "crp", "decrease", 2, EvidenceStrength.WEAK, "antioxidants"),
            ("spinach", "crp", "decrease", 1, EvidenceStrength.WEAK, "antioxidants"),
            
            # Iron/ferritin
            ("beef", "ferritin", "increase", 5, EvidenceStrength.STRONG, "heme iron"),
            ("lentils", "ferritin", "increase", 3, EvidenceStrength.MODERATE, "non-heme iron"),
            ("spinach", "ferritin", "increase", 1, EvidenceStrength.WEAK, "non-heme iron (low bioavail)"),
            ("coffee", "ferritin", "decrease", 2, EvidenceStrength.MODERATE, "tannins inhibit absorption"),
            ("tea", "ferritin", "decrease", 2, EvidenceStrength.MODERATE, "tannins"),
            
            # Vitamin D
            ("salmon", "vitamin_d", "increase", 2, EvidenceStrength.STRONG, "naturally contains D3"),
            ("egg_yolk", "vitamin_d", "increase", 1, EvidenceStrength.MODERATE, "contains D3"),
            ("mushrooms", "vitamin_d", "increase", 1, EvidenceStrength.WEAK, "contains D2"),
            
            # Blood pressure
            ("beets", "blood_pressure", "decrease", 2, EvidenceStrength.MODERATE, "nitric oxide"),
            ("banana", "blood_pressure", "decrease", 1, EvidenceStrength.WEAK, "potassium"),
            ("spinach", "blood_pressure", "decrease", 1, EvidenceStrength.WEAK, "magnesium"),
            
            # Blood sugar
            ("cinnamon", "glucose", "decrease", 2, EvidenceStrength.MODERATE, "insulin sensitivity"),
            ("berries", "glucose", "decrease", 1, EvidenceStrength.WEAK, "fiber"),
            ("oatmeal", "glucose", "decrease", 2, EvidenceStrength.MODERATE, "low glycemic"),
        ]
        
        for factor, biomarker, effect_type, magnitude, evidence, mechanism in food_effects:
            self.known_effects.append(KnownEffect(
                source="food",
                factor=factor,
                biomarker=biomarker,
                effect_type=effect_type,
                effect_magnitude=magnitude,
                evidence=evidence,
                mechanism=mechanism,
            ))
    
    def _load_medication_effects(self):
        """Load known medication → biomarker effects."""
        
        med_effects = [
            # Statins
            ("statin", "ldl", "decrease", 30, EvidenceStrength.STRONG, "HMG-CoA reductase inhibition"),
            ("statin", "hdl", "increase", 5, EvidenceStrength.MODERATE, "improved lipid metabolism"),
            ("statin", "triglycerides", "decrease", 15, EvidenceStrength.STRONG, "VLDL reduction"),
            ("statin", "coq10", "decrease", 30, EvidenceStrength.STRONG, "blocks CoQ10 synthesis"),
            
            # Metformin
            ("metformin", "glucose", "decrease", 15, EvidenceStrength.STRONG, "reduces glucose production"),
            ("metformin", "hba1c", "decrease", 10, EvidenceStrength.STRONG, "improves insulin sensitivity"),
            ("metformin", "b12", "decrease", 20, EvidenceStrength.MODERATE, "B12 malabsorption"),
            
            # Blood pressure medications
            ("ace_inhibitor", "blood_pressure", "decrease", 15, EvidenceStrength.STRONG, "vasodilation"),
            ("beta_blocker", "blood_pressure", "decrease", 15, EvidenceStrength.STRONG, "reduces heart rate"),
            ("diuretic", "potassium", "decrease", 10, EvidenceStrength.STRONG, "potassium loss"),
            ("diuretic", "sodium", "decrease", 5, EvidenceStrength.MODERATE, "sodium excretion"),
            
            # Vitamin D supplementation
            ("vitamin_d_supplement", "vitamin_d", "increase", 20, EvidenceStrength.STRONG, "direct supplementation"),
            ("vitamin_d_supplement", "calcium", "increase", 5, EvidenceStrength.MODERATE, "enhanced absorption"),
            
            # Iron supplementation
            ("iron_supplement", "ferritin", "increase", 15, EvidenceStrength.STRONG, "direct supplementation"),
            ("iron_supplement", "hemoglobin", "increase", 5, EvidenceStrength.STRONG, "hemoglobin synthesis"),
            
            # Fish oil / Omega-3
            ("fish_oil", "triglycerides", "decrease", 20, EvidenceStrength.STRONG, "VLDL reduction"),
            ("fish_oil", "ldl", "increase", 5, EvidenceStrength.WEAK, "may slightly raise LDL"),
            ("fish_oil", "hdl", "increase", 3, EvidenceStrength.MODERATE, "HDL enhancement"),
            
            # B12 supplementation
            ("b12_supplement", "b12", "increase", 25, EvidenceStrength.STRONG, "direct supplementation"),
            
            # Magnesium supplementation
            ("magnesium_supplement", "magnesium", "increase", 10, EvidenceStrength.STRONG, "direct supplementation"),
            ("magnesium_supplement", "blood_pressure", "decrease", 3, EvidenceStrength.MODERATE, "vasodilation"),
        ]
        
        for factor, biomarker, effect_type, magnitude, evidence, mechanism in med_effects:
            self.known_effects.append(KnownEffect(
                source="medication",
                factor=factor,
                biomarker=biomarker,
                effect_type=effect_type,
                effect_magnitude=magnitude,
                evidence=evidence,
                mechanism=mechanism,
            ))
    
    def _load_activity_effects(self):
        """Load known activity → biomarker effects."""
        
        activity_effects = [
            # Running/Cardio
            ("running", "hdl", "increase", 5, EvidenceStrength.STRONG, "HDL elevation"),
            ("running", "triglycerides", "decrease", 10, EvidenceStrength.STRONG, "fat burning"),
            ("running", "ldl", "decrease", 3, EvidenceStrength.MODERATE, "weight management"),
            ("running", "blood_pressure", "decrease", 3, EvidenceStrength.MODERATE, "vasodilation"),
            ("running", "resting_heart_rate", "decrease", 5, EvidenceStrength.STRONG, "cardio fitness"),
            
            # Walking
            ("walking", "hdl", "increase", 2, EvidenceStrength.MODERATE, "moderate exercise"),
            ("walking", "triglycerides", "decrease", 3, EvidenceStrength.MODERATE, "fat burning"),
            
            # Strength training
            ("strength_training", "hdl", "increase", 3, EvidenceStrength.MODERATE, "muscle building"),
            ("strength_training", "ldl", "decrease", 2, EvidenceStrength.WEAK, "metabolic health"),
            ("strength_training", "creatine_kinase", "increase", 20, EvidenceStrength.STRONG, "muscle damage"),
            
            # Cycling
            ("cycling", "hdl", "increase", 4, EvidenceStrength.MODERATE, "endurance"),
            ("cycling", "triglycerides", "decrease", 8, EvidenceStrength.STRONG, "fat oxidation"),
            
            # Swimming
            ("swimming", "hdl", "increase", 3, EvidenceStrength.MODERATE, "aerobic exercise"),
            ("swimming", "blood_pressure", "decrease", 2, EvidenceStrength.WEAK, "cardio"),
            
            # HIIT
            ("hiit", "hdl", "increase", 4, EvidenceStrength.STRONG, "intense exercise"),
            ("hiit", "triglycerides", "decrease", 10, EvidenceStrength.STRONG, "fat burning"),
            ("hiit", "insulin_sensitivity", "increase", 10, EvidenceStrength.STRONG, "glucose metabolism"),
            
            # Yoga
            ("yoga", "cortisol", "decrease", 5, EvidenceStrength.MODERATE, "stress reduction"),
            ("yoga", "blood_pressure", "decrease", 2, EvidenceStrength.WEAK, "relaxation"),
            
            # Sleep impact on biomarkers
            ("sleep_poor", "crp", "increase", 10, EvidenceStrength.MODERATE, "inflammation"),
            ("sleep_poor", "cortisol", "increase", 15, EvidenceStrength.STRONG, "stress response"),
            ("sleep_poor", "ghrelin", "increase", 5, EvidenceStrength.MODERATE, "appetite hormone"),
            ("sleep_poor", "leptin", "decrease", 5, EvidenceStrength.MODERATE, "satiety hormone"),
            
            # Steps
            ("steps_low", "triglycerides", "increase", 5, EvidenceStrength.WEAK, "sedentary"),
            ("steps_high", "hdl", "increase", 2, EvidenceStrength.MODERATE, "movement"),
        ]
        
        for factor, biomarker, effect_type, magnitude, evidence, mechanism in activity_effects:
            self.known_effects.append(KnownEffect(
                source="activity",
                factor=factor,
                biomarker=biomarker,
                effect_type=effect_type,
                effect_magnitude=magnitude,
                evidence=evidence,
                timeframe_days=30,
                mechanism=mechanism,
            ))
    
    def _load_vital_correlations(self):
        """Load known vital sign → biomarker correlations."""
        
        vital_correlations = [
            # Weight
            ("weight", "ldl", "increase", 2, EvidenceStrength.MODERATE, "body fat"),
            ("weight", "hdl", "decrease", 1, EvidenceStrength.WEAK, "adipose tissue"),
            ("weight", "triglycerides", "increase", 3, EvidenceStrength.MODERATE, "visceral fat"),
            ("weight", "blood_pressure", "increase", 3, EvidenceStrength.STRONG, "cardiac workload"),
            ("weight", "glucose", "increase", 2, EvidenceStrength.MODERATE, "insulin resistance"),
            
            # Blood pressure correlations
            ("blood_pressure", "ldl", "increase", 2, EvidenceStrength.WEAK, "vascular health"),
            ("blood_pressure", "cardiovascular_risk", "increase", 5, EvidenceStrength.STRONG, "risk factor"),
            
            # Sleep
            ("sleep_hours", "cortisol", "decrease", 3, EvidenceStrength.MODERATE, "restoration"),
            ("sleep_hours", "crp", "decrease", 2, EvidenceStrength.WEAK, "inflammation reduction"),
            ("sleep_hours", "testosterone", "increase", 2, EvidenceStrength.WEAK, "hormone balance"),
            
            # Stress
            ("stress_level", "cortisol", "increase", 10, EvidenceStrength.STRONG, "stress response"),
            ("stress_level", "crp", "increase", 5, EvidenceStrength.MODERATE, "inflammation"),
            ("stress_level", "blood_pressure", "increase", 3, EvidenceStrength.MODERATE, "vasoconstriction"),
        ]
        
        for factor, biomarker, effect_type, magnitude, evidence, mechanism in vital_correlations:
            self.known_effects.append(KnownEffect(
                source="vital",
                factor=factor,
                biomarker=biomarker,
                effect_type=effect_type,
                effect_magnitude=magnitude,
                evidence=evidence,
                timeframe_days=14,
                mechanism=mechanism,
            ))
    
    def get_effects_for_biomarker(self, biomarker: str) -> List[KnownEffect]:
        """Get all known effects for a specific biomarker."""
        return [e for e in self.known_effects if e.biomarker == biomarker]
    
    def analyze_change(
        self,
        biomarker: str,
        start_date: date,
        end_date: date,
        start_value: Optional[float] = None,
        end_value: Optional[float] = None,
    ) -> CorrelationResult:
        """
        Analyze why a biomarker changed between two blood tests.
        
        Args:
            biomarker: The biomarker to analyze (e.g., "ldl", "ferritin")
            start_date: Date of first blood test
            end_date: Date of second blood test
            start_value: Known value at start (optional)
            end_value: Known value at end (optional)
            
        Returns:
            CorrelationResult with explanation
        """
        # Get values if not provided
        if start_value is None or end_value is None:
            values = self._get_biomarker_values(biomarker, start_date, end_date)
            if start_value is None:
                start_value = values.get("start")
            if end_value is None:
                end_value = values.get("end")
        
        # Calculate change
        if start_value is None or end_value is None:
            return CorrelationResult(
                biomarker=biomarker,
                start_value=start_value or 0,
                end_value=end_value or 0,
                change=0,
                change_percent=0,
                time_period_days=(end_date - start_date).days,
                start_date=start_date,
                end_date=end_date,
                explanation="Insufficient blood test data to analyze change.",
                correlation_found=False,
            )
        
        change = end_value - start_value
        change_percent = (change / start_value * 100) if start_value != 0 else 0
        
        # Get aligned diary data for the period
        aligned_data = self._get_aligned_diary_data(start_date, end_date)
        
        # Find contributing factors
        factors = self._attribute_change(
            biomarker=biomarker,
            change=change,
            change_percent=change_percent,
            diary_data=aligned_data,
            period_days=(end_date - start_date).days,
        )
        
        # Calculate confidence based on evidence
        confidence = self._calculate_confidence(factors)
        
        # Generate explanation
        explanation = self._generate_explanation(
            biomarker, start_value, end_value, change, change_percent, factors
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(biomarker, factors, change)
        
        return CorrelationResult(
            biomarker=biomarker,
            start_value=start_value,
            end_value=end_value,
            change=change,
            change_percent=change_percent,
            time_period_days=(end_date - start_date).days,
            start_date=start_date,
            end_date=end_date,
            contributing_factors=factors,
            confidence=confidence,
            correlation_found=len(factors) > 0,
            explanation=explanation,
            recommendations=recommendations,
        )
    
    def _get_biomarker_values(
        self,
        biomarker: str,
        start_date: date,
        end_date: date,
    ) -> Dict[str, float]:
        """Extract biomarker values from blood tests in date range."""
        if not self.blood_tests:
            return {}
        
        values = {}
        for bt in self.blood_tests:
            bt_date = getattr(bt, "date", None) or getattr(bt, "timestamp", None)
            if bt_date:
                if isinstance(bt_date, datetime):
                    bt_date = bt_date.date()
                
                if start_date <= bt_date <= end_date:
                    # Try to find the biomarker value
                    value = getattr(bt, biomarker, None)
                    if value is not None:
                        if bt_date <= start_date + timedelta(days=30):
                            values["start"] = value
                        if bt_date >= end_date - timedelta(days=30):
                            values["end"] = value
        
        return values
    
    def _get_aligned_diary_data(
        self,
        start_date: date,
        end_date: date,
    ) -> TimeAlignedData:
        """Aggregate diary data for the time period."""
        
        data = TimeAlignedData(
            period_start=start_date,
            period_end=end_date,
        )
        
        if not self.diary:
            return data
        
        # Get all entries in the period
        entries = self.diary.get_entries(
            start_date=datetime.combine(start_date, datetime.min.time()),
            end_date=datetime.combine(end_date, datetime.max.time()),
        )
        
        # Aggregate by metric type
        metric_totals: Dict[str, List[float]] = {}
        
        for entry in entries:
            metric = entry.metric
            
            # Food entries
            if metric in ("food", "food_intake"):
                if isinstance(entry.value, dict) and "foods" in entry.value:
                    for food in entry.value["foods"]:
                        data.food_frequency[food] = data.food_frequency.get(food, 0) + 1
                elif isinstance(entry.value, str):
                    data.food_frequency[entry.value] = data.food_frequency.get(entry.value, 0) + 1
            
            # Activity entries
            elif metric in ("steps", "active_minutes", "exercise_type", "running", "walking"):
                if isinstance(entry.value, (int, float)):
                    if metric not in metric_totals:
                        metric_totals[metric] = []
                    metric_totals[metric].append(entry.value)
            
            # Vitals
            elif metric in ("weight", "blood_pressure_systolic", "blood_pressure_diastolic", 
                           "pulse", "blood_oxygen"):
                if isinstance(entry.value, (int, float)):
                    if metric not in metric_totals:
                        metric_totals[metric] = []
                    metric_totals[metric].append(entry.value)
            
            # Sleep
            elif metric in ("sleep_hours", "sleep_quality", "sleep_deep", "sleep_rem"):
                if isinstance(entry.value, (int, float)):
                    if metric not in metric_totals:
                        metric_totals[metric] = []
                    metric_totals[metric].append(entry.value)
            
            # Mood/Stress
            elif metric in ("mood", "stress_level", "energy_level"):
                if isinstance(entry.value, (int, float)):
                    if metric not in metric_totals:
                        metric_totals[metric] = []
                    metric_totals[metric].append(entry.value)
        
        # Calculate averages for vitals
        for metric, values in metric_totals.items():
            if values:
                data.vitals[metric] = values
                if metric in ("steps", "active_minutes"):
                    data.activities[metric] = sum(values)
                elif metric in ("sleep_hours",):
                    data.sleep[metric] = sum(values) / len(values)
        
        # Process medication diary if available
        if self.medication_diary:
            intakes = self.medication_diary.get_intakes(
                start_date=datetime.combine(start_date, datetime.min.time()),
                end_date=datetime.combine(end_date, datetime.max.time()),
            )
            for intake in intakes:
                name = intake.medication_name.lower()
                data.medications[name] = data.medications.get(name, 0) + 1
        
        return data
    
    def _attribute_change(
        self,
        biomarker: str,
        change: float,
        change_percent: float,
        diary_data: TimeAlignedData,
        period_days: int,
    ) -> List[FactorContribution]:
        """Determine which factors contributed to the biomarker change."""
        
        factors = []
        
        # Get known effects for this biomarker
        known_effects = self.get_effects_for_biomarker(biomarker)
        
        # Scale factor based on period (effects normalized to 30 days)
        period_scale = min(period_days / 30, 1.5)  # Cap at 1.5x for very long periods
        
        # Check food contributions
        for effect in known_effects:
            if effect.source != "food":
                continue
            
            # Check if user consumed this food
            for food_name, count in diary_data.food_frequency.items():
                # Flexible matching - check if effect factor is in food name or vice versa
                if effect.factor.lower() in food_name.lower() or food_name.lower() in effect.factor.lower():
                    # Calculate frequency factor (times per week)
                    times_per_week = (count / period_days) * 7
                    # Scale impact by frequency (capped at 2x for very frequent)
                    frequency_factor = min(times_per_week / 2, 2.0)  # Normalize to ~2x/week
                    # Apply effect magnitude scaled by frequency and period
                    impact = effect.effect_magnitude * frequency_factor * (period_days / 30)
                    
                    # Calculate actual estimated change
                    # If effect is "decrease" and change is negative, that's good (aligned)
                    # If effect is "decrease" and change is positive, that's opposite (wrong direction)
                    if effect.effect_type == "decrease":
                        actual_impact = change * impact / 100  # Negative change * positive impact = negative (decrease)
                    else:
                        actual_impact = change * impact / 100  # Positive change * positive impact = positive (increase)
                    
                    factors.append(FactorContribution(
                        source="food",
                        factor=food_name,
                        estimated_impact=actual_impact,
                        impact_percent=impact,
                        evidence_strength=effect.evidence,
                        description=f"Ate {food_name} {count} times ({times_per_week:.1f}/week) - {effect.mechanism}",
                    ))
        
        # Check medication contributions
        for effect in known_effects:
            if effect.source != "medication":
                continue
            
            # Check if user took this medication
            for med_name, count in diary_data.medications.items():
                # Flexible matching
                if effect.factor.lower() in med_name.lower() or med_name.lower() in effect.factor.lower():
                    # Calculate doses per day
                    doses_per_day = count / period_days
                    # Scale: full effect at ~1 dose/day
                    dose_factor = min(doses_per_day * 30, 2.0)  # Cap at 2x
                    impact = effect.effect_magnitude * dose_factor
                    
                    # Calculate actual change contribution
                    if effect.effect_type == "decrease":
                        actual_impact = change * impact / 100
                    else:
                        actual_impact = change * impact / 100
                    
                    factors.append(FactorContribution(
                        source="medication",
                        factor=med_name,
                        estimated_impact=actual_impact,
                        impact_percent=impact,
                        evidence_strength=effect.evidence,
                        description=f"Taking {med_name} ~{doses_per_day*30:.0f}x/month - {effect.mechanism}",
                    ))
        
        # Check activity contributions
        for effect in known_effects:
            if effect.source != "activity":
                continue
            
            total_minutes = 0
            for activity, minutes in diary_data.activities.items():
                if effect.factor in activity:
                    total_minutes += minutes
            
            if total_minutes > 0:
                # Scale impact by activity volume
                activity_factor = min(total_minutes / 150, 2.0)  # Normalize to 150 min/week
                impact = effect.effect_magnitude * activity_factor * period_scale
                
                factors.append(FactorContribution(
                    source="activity",
                    factor=effect.factor,
                    estimated_impact=-change * impact / 100,
                    impact_percent=impact,
                    evidence_strength=effect.evidence,
                    description=f"{total_minutes} min of {effect.factor} - {effect.mechanism}",
                ))
        
        # Check vital correlations
        for effect in known_effects:
            if effect.source != "vital":
                continue
            
            # Get vital values
            vital_values = diary_data.vitals.get(effect.factor, [])
            if not vital_values:
                continue
            
            avg_value = sum(vital_values) / len(vital_values)
            
            # Check if there's an abnormal pattern
            if effect.factor == "weight" and avg_value > 80:  # Overweight
                impact = effect.effect_magnitude * period_scale
            elif effect.factor in ("stress_level",) and avg_value > 3:  # High stress
                impact = effect.effect_magnitude * period_scale
            elif effect.factor == "sleep_hours" and avg_value < 7:  # Poor sleep
                impact = effect.effect_magnitude * period_scale
            else:
                continue
            
            factors.append(FactorContribution(
                source="vital",
                factor=effect.factor,
                estimated_impact=-change * impact / 100 if effect.effect_type == "decrease" else change * impact / 100,
                impact_percent=impact,
                evidence_strength=effect.evidence,
                description=f"Avg {effect.factor}: {avg_value:.1f} - {effect.mechanism}",
            ))
        
        # Sort by impact magnitude
        factors.sort(key=lambda f: abs(f.impact_percent), reverse=True)
        
        # Cap total attributed impact at 150% of actual change
        total_attributed = sum(f.impact_percent for f in factors)
        if total_attributed > 150:
            scale = 150 / total_attributed
            for f in factors:
                f.impact_percent *= scale
                f.estimated_impact *= scale
        
        return factors[:10]  # Top 10 factors
    
    def _calculate_confidence(self, factors: List[FactorContribution]) -> float:
        """Calculate confidence score based on evidence strength."""
        if not factors:
            return 0.0
        
        weights = {
            EvidenceStrength.STRONG: 1.0,
            EvidenceStrength.MODERATE: 0.6,
            EvidenceStrength.WEAK: 0.3,
            EvidenceStrength.ANECDOTAL: 0.1,
        }
        
        total_weight = 0.0
        weighted_sum = 0.0
        
        for f in factors:
            weight = weights.get(f.evidence_strength, 0.3)
            weighted_sum += weight * f.impact_percent
            total_weight += f.impact_percent
        
        if total_weight == 0:
            return 0.0
        
        return min(weighted_sum / total_weight, 1.0)
    
    def _generate_explanation(
        self,
        biomarker: str,
        start_value: float,
        end_value: float,
        change: float,
        change_percent: float,
        factors: List[FactorContribution],
    ) -> str:
        """Generate human-readable explanation."""
        
        direction = "decreased" if change < 0 else "increased"
        
        if not factors:
            return f"{biomarker.upper()} {direction} from {start_value:.1f} to {end_value:.1f} ({change_percent:+.1f}%). No clear contributing factors identified from diary data."
        
        # Group by source
        by_source: Dict[str, List[FactorContribution]] = {}
        for f in factors:
            if f.source not in by_source:
                by_source[f.source] = []
            by_source[f.source].append(f)
        
        parts = []
        
        if "medication" in by_source:
            meds = [f.factor for f in by_source["medication"]]
            parts.append(f"Medication: {', '.join(meds)}")
        
        if "food" in by_source:
            foods = list(set(f.factor for f in by_source["food"][:5]))
            parts.append(f"Diet: {', '.join(foods)}")
        
        if "activity" in by_source:
            activities = list(set(f.factor for f in by_source["activity"][:3]))
            parts.append(f"Activity: {', '.join(activities)}")
        
        if "vital" in by_source:
            vitals = [f"{f.factor} ({f.estimated_impact:+.1f}%)" for f in by_source["vital"][:2]]
            parts.append(f"Vitals: {', '.join(vitals)}")
        
        explanation = f"{biomarker.upper()} {direction} {abs(change_percent):.1f}% ({change:+.1f}) from {start_value:.1f} to {end_value:.1f}. "
        
        if parts:
            explanation += f"Likely factors: {'; '.join(parts)}."
        else:
            explanation += "Contributing factors identified but impact unclear."
        
        return explanation
    
    def _generate_recommendations(
        self,
        biomarker: str,
        factors: List[FactorContribution],
        change: float,
    ) -> List[str]:
        """Generate recommendations based on the analysis."""
        
        recommendations = []
        
        # Check if change is unfavorable
        unfavorable_changes = {
            "ldl": change > 0,
            "triglycerides": change > 0,
            "glucose": change > 0,
            "blood_pressure": change > 0,
            "crp": change > 0,
            "hdl": change < 0,
            "vitamin_d": change < 0,
            "ferritin": change < 0,
        }
        
        is_unfavorable = unfavorable_changes.get(biomarker, False)
        
        # Get foods that could help
        helpful_effects = self.get_effects_for_biomarker(biomarker)
        helpful_foods = [e for e in helpful_effects if e.effect_type == "decrease" and e.source == "food"]
        
        if is_unfavorable and helpful_foods:
            top_foods = [e.factor for e in helpful_foods[:3]]
            recommendations.append(
                f"Consider adding {', '.join(top_foods)} to your diet to help lower {biomarker}."
            )
        
        # Check for medication side effects to monitor
        med_factors = [f for f in factors if f.source == "medication"]
        for f in med_factors:
            if "statin" in f.factor and biomarker == "coq10":
                recommendations.append(
                    "Monitor CoQ10 levels - statins can deplete CoQ10. Consider supplementation."
                )
            elif "metformin" in f.factor and biomarker == "b12":
                recommendations.append(
                    "Consider B12 supplementation - metformin can reduce B12 absorption."
                )
        
        # Activity recommendations
        activity_factors = [f for f in factors if f.source == "activity"]
        if is_unfavorable and not activity_factors:
            recommendations.append(
                f"Regular exercise may help improve {biomarker}. Aim for 150 min/week moderate activity."
            )
        
        return recommendations
    
    def find_correlations(
        self,
        biomarker: str,
        time_window_days: int = 90,
    ) -> List[CorrelationResult]:
        """Find what correlates with a biomarker over time."""
        
        if not self.blood_tests or not self.diary:
            return []
        
        results = []
        
        # Get blood tests in range
        cutoff = datetime.now() - timedelta(days=time_window_days)
        
        for bt in self.blood_tests:
            bt_date = getattr(bt, "date", None) or getattr(bt, "timestamp", None)
            if bt_date and bt_date >= cutoff:
                value = getattr(bt, biomarker, None)
                if value is not None:
                    # Analyze period leading up to this test
                    period_start = bt_date.date() - timedelta(days=time_window_days)
                    period_end = bt_date.date()
                    
                    result = self.analyze_change(
                        biomarker=biomarker,
                        start_date=period_start,
                        end_date=period_end,
                        end_value=value,
                    )
                    results.append(result)
        
        return results
    
    def generate_insights(self, days: int = 30) -> List[Insight]:
        """Generate actionable insights from recent data."""
        
        insights = []
        
        if not self.diary:
            return insights
        
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        # Get recent diary data
        aligned_data = self._get_aligned_diary_data(start_date, end_date)
        
        # Check for patterns and generate insights
        
        # 1. Sleep insights
        if aligned_data.sleep.get("sleep_hours", 0) < 7:
            insights.append(Insight(
                id="sleep_deprivation",
                title="Sleep Deprivation Detected",
                message=f"You're averaging only {aligned_data.sleep.get('sleep_hours', 0):.1f} hours of sleep. Poor sleep can increase inflammation (CRP), cortisol, and affect blood sugar regulation.",
                insight_type="pattern",
                priority="high",
                action_items=[
                    "Aim for 7-9 hours of sleep",
                    "Establish consistent sleep schedule",
                    "Limit screen time before bed",
                ],
                estimated_impact="CRP +10%, cortisol +15%",
            ))
        
        # 2. Hydration insights
        water_intake = aligned_data.vitals.get("water_intake", [0])[0]
        if water_intake < 1500:
            insights.append(Insight(
                id="low_hydration",
                title="Low Hydration",
                message="Your water intake appears low. Adequate hydration supports nutrient absorption, kidney function, and energy levels.",
                insight_type="vital",
                priority="medium",
                action_items=[
                    "Drink at least 8 glasses of water daily",
                    "Keep a water bottle visible",
                    "Set hydration reminders",
                ],
                estimated_impact="Improved energy, better nutrient absorption",
            ))
        
        # 3. Activity insights
        total_steps = aligned_data.activities.get("steps", 0)
        if total_steps < days * 5000:  # Less than 5k/day average
            insights.append(Insight(
                id="low_activity",
                title="Low Activity Level",
                message=f"You're averaging {total_steps / days:.0f} steps/day. Regular movement improves HDL, reduces triglycerides, and supports weight management.",
                insight_type="activity",
                priority="high",
                action_items=[
                    "Aim for 10,000 steps daily",
                    "Take walking breaks every hour",
                    "Consider a standing desk",
                ],
                related_metrics=["hdl", "triglycerides", "weight"],
                estimated_impact="HDL +5-10%, triglycerides -10%",
            ))
        
        # 4. Food pattern insights
        high_sugar_foods = ["candy", "soda", "ice_cream", "cookies", "cake"]
        sugar_count = sum(aligned_data.food_frequency.get(f, 0) for f in high_sugar_foods)
        
        if sugar_count > 5:
            insights.append(Insight(
                id="high_sugar_intake",
                title="High Sugar Intake",
                message=f"You've had {sugar_count} high-sugar food entries this month. High sugar intake can negatively affect triglycerides, blood sugar, and inflammation.",
                insight_type="food",
                priority="medium",
                action_items=[
                    "Replace sugary snacks with fruit",
                    "Read nutrition labels for hidden sugars",
                    "Limit added sugars to 25g/day",
                ],
                related_metrics=["triglycerides", "glucose", "crp"],
                estimated_impact="Triglycerides +10-20%",
            ))
        
        # 5. Stress insights
        stress_values = aligned_data.vitals.get("stress_level", [])
        if stress_values and sum(stress_values) / len(stress_values) > 3.5:
            avg_stress = sum(stress_values) / len(stress_values)
            insights.append(Insight(
                id="high_stress",
                title="Elevated Stress Levels",
                message=f"Your average stress level is {avg_stress:.1f}/5. Chronic stress can raise cortisol, increase inflammation, and affect blood pressure.",
                insight_type="vital",
                priority="high",
                action_items=[
                    "Practice daily meditation or deep breathing",
                    "Consider yoga or progressive muscle relaxation",
                    "Ensure adequate sleep",
                ],
                related_metrics=["cortisol", "crp", "blood_pressure"],
                estimated_impact="Cortisol +15%, CRP +10%",
            ))
        
        # 6. Medication-related insights
        if self.medication_diary:
            due_today = self.medication_diary.get_due_today()
            if due_today:
                med_names = [s.name for s in due_today[:3]]
                insights.append(Insight(
                    id="medication_reminder",
                    title="Medications Due Today",
                    message=f"You have scheduled medications: {', '.join(med_names)}. Consistent adherence improves outcomes.",
                    insight_type="medication",
                    priority="medium",
                    action_items=[f"Take {m} as prescribed" for m in med_names],
                ))
        
        # 7. Blood test-based insights (if we have recent tests)
        if self.blood_tests:
            for bt in self.blood_tests[-3:]:  # Last 3 tests
                # Check LDL
                ldl = getattr(bt, "ldl", None)
                if ldl and ldl > 130:
                    insights.append(Insight(
                        id="elevated_ldl",
                        title=f"Elevated LDL Cholesterol",
                        message=f"Your LDL is {ldl} mg/dL (optimal: <100). LDL is the primary target for heart disease prevention.",
                        insight_type="biomarker",
                        biomarker="ldl",
                        priority="high",
                        action_items=[
                            "Reduce saturated fat intake",
                            "Increase fiber (oatmeal, beans, fruits)",
                            "Add omega-3 rich foods (salmon, walnuts)",
                            "Consult about statin therapy",
                        ],
                        estimated_impact="-20 to -30 mg/dL with lifestyle changes",
                    ))
                
                # Check Vitamin D
                vit_d = getattr(bt, "vitamin_d", None)
                if vit_d and vit_d < 30:
                    insights.append(Insight(
                        id="low_vitamin_d",
                        title="Low Vitamin D",
                        message=f"Your vitamin D is {vit_d} ng/mL (optimal: 30-60). Low vitamin D is associated with fatigue, bone loss, and immune dysfunction.",
                        insight_type="biomarker",
                        biomarker="vitamin_d",
                        priority="medium",
                        action_items=[
                            "Supplement with 2000-4000 IU vitamin D3",
                            "Get midday sun exposure (15-20 min)",
                            "Eat vitamin D rich foods (salmon, eggs, fortified foods)",
                        ],
                        estimated_impact="+10-20 ng/mL with supplementation",
                    ))
                
                # Check Ferritin
                ferritin = getattr(bt, "ferritin", None)
                if ferritin and ferritin < 30:
                    insights.append(Insight(
                        id="low_ferritin",
                        title="Low Ferritin (Iron)",
                        message=f"Your ferritin is {ferritin} ng/mL (optimal: 50-150). Low iron can cause fatigue, weakness, and impaired immune function.",
                        insight_type="biomarker",
                        biomarker="ferritin",
                        priority="high",
                        action_items=[
                            "Eat iron-rich foods (beef, lentils, spinach)",
                            "Pair iron with vitamin C for absorption",
                            "Avoid coffee/tea with iron-rich meals",
                            "Consider iron supplement",
                        ],
                        estimated_impact="+15-30 ng/mL with diet changes",
                    ))
        
        return insights


__all__ = [
    'CorrelationEngine',
    'CorrelationResult',
    'FactorContribution',
    'Insight',
    'TimeAlignedData',
    'KnownEffect',
    'EvidenceStrength',
]
