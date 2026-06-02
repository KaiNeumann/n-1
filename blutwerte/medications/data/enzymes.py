"""Nattokinase supplement (enzyme from fermented soy)."""

from blutwerte.medications.models import (
    Medication, MedicationEffect, Quote, RiskFactor,
    DrugInteraction, MonitoringRequirement,
    EffectTargetType, EffectDirection, FrequencyCategory
)

def create_nattokinase() -> Medication:
    nattokinase = Medication(
        name="Nattokinase",
        name_de="Nattokinase",
        brand_names=["Nattokinase", "NSK-SD", "Natto Extract"],
        synonyms=["nattokinase", "natto_kinase", "subtilisin_natto", "ATC:B01"],
        drug_class="Supplement",
        drug_subclass="Enzyme",
        available_doses=[(100, "mg"), (100, "FU"), (2000, "FU")],  # FU = Fibrinolytic Units
        typical_dose_range=(100.0, 2000.0),
        effects=[
            MedicationEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Fibrinogen",
                target_synonyms=["Fibrinogen", "Clotting Factor I"],
                direction=EffectDirection.DECREASE,
                typical_magnitude="mild",
                frequency_category=FrequencyCategory.UNCOMMON,
                frequency_percentage=15.0,
                mechanism="Fibrinolytic enzyme; degrades fibrin in clots",
                clinical_significance="expected",
                requires_monitoring=False,
                evidence=[Quote("Reduces fibrinogen 5-15% in some studies", "Clinical trials", "research")],
                likelihood_score="B"
            ),
            MedicationEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="INR",
                target_synonyms=["International Normalized Ratio", "Quick", "PT"],
                direction=EffectDirection.INCREASE,
                typical_magnitude="mild",
                frequency_category=FrequencyCategory.UNCOMMON,
                frequency_percentage=10.0,
                mechanism="Fibrinolytic and mild anticoagulant effects",
                clinical_significance="monitor",
                requires_monitoring=True,
                monitoring_recommendation="Monitor INR if on warfarin; discontinue 1-2 weeks before surgery",
                risk_factors=[RiskFactor(factor_type="concurrent_med", description="Concurrent warfarin", concurrent_med="Warfarin", multiplier=5.0)],
                evidence=[Quote("May increase INR when combined with anticoagulants", "Case reports", "research")],
                likelihood_score="C"
            ),
            MedicationEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="aPTT",
                target_synonyms=["PTT", "Activated Partial Thromboplastin Time"],
                direction=EffectDirection.INCREASE,
                typical_magnitude="mild",
                frequency_category=FrequencyCategory.UNCOMMON,
                frequency_percentage=10.0,
                mechanism="Mild intrinsic pathway effect",
                clinical_significance="monitor",
                requires_monitoring=False,
                evidence=[Quote("May prolong aPTT slightly", "Clinical studies", "research")],
                likelihood_score="C"
            ),
            MedicationEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="D-Dimer",
                target_synonyms=["D-Dimer", "Fibrin Degradation Products"],
                direction=EffectDirection.INCREASE,
                typical_magnitude="mild",
                frequency_category=FrequencyCategory.UNCOMMON,
                frequency_percentage=20.0,
                mechanism="Increased fibrin degradation from fibrinolytic activity",
                clinical_significance="expected",
                requires_monitoring=False,
                monitoring_recommendation="May interfere with D-dimer as diagnostic test for thrombosis",
                evidence=[Quote("Increases fibrin degradation products", "Clinical studies", "research")],
                likelihood_score="B"
            ),
            MedicationEffect(
                target_type=EffectTargetType.CLINICAL_OUTCOME,
                target_name="Bleeding Risk",
                target_synonyms=["Hemorrhage", "Bleeding"],
                direction=EffectDirection.INCREASE,
                typical_magnitude="mild",
                frequency_category=FrequencyCategory.UNCOMMON,
                frequency_percentage=3.0,
                mechanism="Fibrinolytic activity; additive with anticoagulants",
                clinical_significance="concerning",
                requires_monitoring=True,
                monitoring_recommendation="Caution with anticoagulants/antiplatelets; discontinue 1-2 weeks before surgery; report unusual bleeding",
                risk_factors=[
                    RiskFactor(factor_type="concurrent_med", description="Concurrent warfarin", concurrent_med="Warfarin", multiplier=5.0),
                    RiskFactor(factor_type="concurrent_med", description="Concurrent aspirin", concurrent_med="Aspirin", multiplier=3.0),
                    RiskFactor(factor_type="concurrent_med", description="Concurrent DOACs", concurrent_med="DOAC", multiplier=4.0),
                    RiskFactor(factor_type="condition", description="Bleeding disorders", condition="bleeding_disorder", multiplier=5.0),
                    RiskFactor(factor_type="condition", description="Surgery within 2 weeks", condition="upcoming_surgery", multiplier=10.0)
                ],
                evidence=[Quote("Bleeding risk increases with concurrent anticoagulants", "Case reports", "research")],
                likelihood_score="C"
            ),
            MedicationEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Blood Pressure",
                target_synonyms=["BP", "Arterial Pressure", "Blutdruck"],
                direction=EffectDirection.DECREASE,
                typical_magnitude="mild",
                frequency_category=FrequencyCategory.UNCOMMON,
                frequency_percentage=20.0,
                mechanism="Unknown; possible ACE inhibition (contains bacillopeptidase F)",
                clinical_significance="expected",
                requires_monitoring=False,
                evidence=[Quote("Small studies show 5-10 mmHg SBP reduction", "Small trials", "research")],
                likelihood_score="C"
            )
        ],
        indications=[
            Quote("Cardiovascular health", "Supplement use", "clinical"),
            Quote("Fibrinolytic support", "Traditional use", "clinical"),
            Quote("Blood pressure (limited evidence)", "Preliminary research", "research")
        ],
        contraindications=[
            Quote("Active bleeding or bleeding disorders", "Safety", "clinical"),
            Quote("Surgery within 2 weeks", "Bleeding risk", "clinical"),
            Quote("Concurrent anticoagulation (relative)", "Interaction", "clinical"),
            Quote("Soy allergy (natto is fermented soy)", "Allergy", "clinical")
        ],
        drug_interactions=[
            DrugInteraction(
                interacting_drug="Warfarin",
                severity="major",
                effect_description="Additive anticoagulation; unstable INR",
                mechanism="Fibrinolytic + vitamin K antagonist",
                management="Avoid or monitor INR closely; significant interaction risk"
            ),
            DrugInteraction(
                interacting_drug="Aspirin",
                severity="moderate",
                effect_description="Increased bleeding risk",
                mechanism="Additive antiplatelet/anticoagulant",
                management="Use caution; monitor for bleeding"
            ),
            DrugInteraction(
                interacting_drug="DOACs (Rivaroxaban, Apixaban, etc.)",
                severity="major",
                effect_description="Increased bleeding risk",
                mechanism="Additive anticoagulation",
                management="Avoid combination unless specifically advised"
            ),
            DrugInteraction(
                interacting_drug="Antihypertensives",
                severity="minor",
                effect_description="Additive BP lowering",
                mechanism="Both lower BP",
                management="Monitor BP"
            )
        ],
        monitoring_protocol=[
            MonitoringRequirement(target_type=EffectTargetType.BIOMARKER, target_name="INR", baseline_required=False, frequency="If on warfarin", condition="concurrent_warfarin"),
            MonitoringRequirement(target_type=EffectTargetType.CLINICAL_OUTCOME, target_name="Bleeding Signs", baseline_required=False, frequency="Ongoing", condition="watch_for_bruising")
        ],
        pregnancy_category="C",  # Insufficient data
        requires_prescription=False,
        controlled_substance=False,
        primary_sources=[
            Quote("Nattokinase fibrinolytic activity studies", "https://pubmed.ncbi.nlm.nih.gov/", "research"),
            Quote("Nattokinase safety review", "https://pubmed.ncbi.nlm.nih.gov/", "research")
        ],
        last_updated="2024-01-15"
    )
    return nattokinase

__all__ = ['create_nattokinase']
