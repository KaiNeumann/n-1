"""
Amino acid supplements.

Includes:
- L-Arginine
- Other amino acids
"""

from ...medications.models import (
    Medication, MedicationEffect, Quote, RiskFactor,
    DrugInteraction, MonitoringRequirement,
    EffectTargetType, EffectDirection, FrequencyCategory
)


def create_larginine() -> Medication:
    """
    Create complete L-Arginine supplement profile.
    
    Semi-essential amino acid that is a substrate for nitric oxide synthesis.
    Commonly used for cardiovascular health, exercise performance, and erectile function.
    
    Key effects:
    - Blood pressure reduction (via NO production)
    - Enhanced exercise performance
    - Potential glucose metabolism benefits
    - Bleeding risk (theoretical with anticoagulants)
    
    Sources:
    - Supplement databases
    - Clinical trials on L-arginine
    """
    
    # Blood pressure reduction
    bp_effect = MedicationEffect(
        target_type=EffectTargetType.VITAL_SIGN,
        target_name="Blood Pressure",
        target_synonyms=["BP", "Arterial Pressure", "Blutdruck"],
        direction=EffectDirection.DECREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.UNCOMMON,
        frequency_percentage=15.0,
        
        dose_dependent=True,
        
        mechanism="Substrate for endothelial nitric oxide synthase (eNOS) → "
                 "increased NO production → vasodilation; "
                 "effects more pronounced in those with endothelial dysfunction",
        
        clinical_significance="expected",
        requires_monitoring=False,
        monitoring_recommendation="Monitor BP if taking antihypertensives; "
                                "may allow dose reduction of prescription meds",
        
        risk_factors=[
            RiskFactor(
                factor_type="concurrent_med",
                description="Concurrent antihypertensives",
                concurrent_med="Antihypertensive",
                multiplier=1.5
            ),
            RiskFactor(
                factor_type="condition",
                description="Endothelial dysfunction",
                condition="endothelial_dysfunction",
                multiplier=2.0
            ),
            RiskFactor(
                factor_type="condition",
                description="Hypertension",
                condition="hypertension",
                multiplier=1.8
            )
        ],
        
        evidence=[
            Quote(
                "SBP reduction 2-6 mmHg at 3-6g daily; more in hypertensive patients",
                "Meta-analyses",
                "research"
            ),
            Quote(
                "Effects modest compared to prescription antihypertensives",
                "Clinical trials",
                "research"
            )
        ],
        likelihood_score="B"
    )
    
    # HbA1c/glucose effects (modest)
    glucose_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="HbA1c",
        target_synonyms=["Glycated Hemoglobin", "V-HA1C"],
        direction=EffectDirection.DECREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.RARE,
        frequency_percentage=1.0,
        
        mechanism="Improved insulin sensitivity; enhanced glucose uptake; "
                 "improved endothelial function in diabetes",
        
        clinical_significance="expected",
        requires_monitoring=False,
        
        risk_factors=[
            RiskFactor(
                factor_type="condition",
                description="Diabetes mellitus",
                condition="diabetes",
                multiplier=3.0
            )
        ],
        
        evidence=[
            Quote(
                "HbA1c reduction 0.1-0.3% in diabetic patients; modest effect",
                "Clinical trials",
                "research"
            )
        ],
        likelihood_score="C"
    )
    
    # Nitric oxide increase (primary mechanism)
    no_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="Nitric Oxide",
        target_synonyms=["NO", "Nitrosative Stress Markers"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="moderate",
        frequency_category=FrequencyCategory.COMMON,
        frequency_percentage=70.0,
        
        mechanism="Direct substrate for NO synthesis; increases plasma arginine",
        
        clinical_significance="expected",
        requires_monitoring=False,
        
        evidence=[
            Quote(
                "Plasma arginine increases dose-dependently; "
                "NO metabolites increase 20-50%",
                "Pharmacokinetic studies",
                "research"
            )
        ],
        likelihood_score="A"
    )
    
    # Theoretical bleeding risk
    bleeding_risk = MedicationEffect(
        target_type=EffectTargetType.CLINICAL_OUTCOME,
        target_name="Bleeding Risk",
        target_synonyms=["Hemorrhage", "Coagulation"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.VERY_RARE,
        frequency_percentage=0.1,
        
        mechanism="Increased NO may inhibit platelet aggregation; "
                 "theoretical concern, not well documented",
        
        clinical_significance="monitor",
        requires_monitoring=False,
        monitoring_recommendation="Caution with anticoagulants/antiplatelets; "
                                "discontinue 2 weeks before surgery",
        
        risk_factors=[
            RiskFactor(
                factor_type="concurrent_med",
                description="Concurrent anticoagulants",
                concurrent_med="Warfarin",
                multiplier=3.0
            ),
            RiskFactor(
                factor_type="concurrent_med",
                description="Concurrent antiplatelets",
                concurrent_med="Aspirin",
                multiplier=2.0
            )
        ],
        
        evidence=[
            Quote(
                "Theoretical risk based on mechanism; limited clinical reports",
                "Case reports",
                "research"
            )
        ],
        likelihood_score="C"
    )
    
    # Herpes virus reactivation (rare)
    herpes_effect = MedicationEffect(
        target_type=EffectTargetType.SYMPTOM,
        target_name="Herpes Reactivation",
        target_synonyms=["Cold Sores", "Genital Herpes", "HSV Outbreak"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.RARE,
        frequency_percentage=0.5,
        
        symptom_description="Reactivation of latent herpes simplex virus; "
                          "cold sores or genital herpes outbreaks",
        
        mechanism="Arginine is essential for herpes virus replication; "
                 "high arginine may promote viral growth (lysine antagonizes)",
        
        clinical_significance="monitor",
        requires_monitoring=False,
        monitoring_recommendation="Avoid or reduce dose if history of frequent herpes outbreaks; "
                                "consider lysine supplementation to antagonize",
        
        risk_factors=[
            RiskFactor(
                factor_type="condition",
                description="History of frequent HSV outbreaks",
                condition="herpes_simplex",
                multiplier=5.0
            )
        ],
        
        evidence=[
            Quote(
                "Based on in vitro data and anecdotal reports; "
                "clinical significance uncertain",
                "In vitro studies",
                "research"
            )
        ],
        likelihood_score="C"
    )
    
    return Medication(
        name="L-Arginine",
        name_de="L-Arginin",
        brand_names=["L-Arginine", "Arginine", "Free Form Amino Acid"],
        synonyms=["arginine", "amino_acid", "supplement", "ATC:B05XB01"],
        drug_class="Supplement",
        drug_subclass="Amino Acid",
        
        available_doses=[(500, "mg"), (1000, "mg"), (3000, "mg")],
        typical_dose_range=(3000.0, 9000.0),  # 3-9g daily
        
        effects=[
            bp_effect,
            glucose_effect,
            no_effect,
            bleeding_risk,
            herpes_effect
        ],
        
        indications=[
            Quote("Cardiovascular health", "Supplement use", "clinical"),
            Quote("Exercise performance", "Athletic supplementation", "clinical"),
            Quote("Erectile dysfunction (adjunctive)", "Off-label use", "clinical"),
            Quote("Endothelial function support", "Supplement use", "clinical")
        ],
        
        contraindications=[
            Quote("Acute herpes outbreak (relative)", "Theoretical concern", "clinical"),
            Quote("Active bleeding or bleeding disorders (relative)", "Precautionary", "clinical")
        ],
        
        drug_interactions=[
            DrugInteraction(
                interacting_drug="Antihypertensives",
                severity="minor",
                effect_description="Additive BP lowering",
                mechanism="Both lower blood pressure",
                management="Monitor BP; may reduce need for prescription meds"
            ),
            DrugInteraction(
                interacting_drug="Sildenafil/Vardenafil",
                severity="minor",
                effect_description="Theoretical additive effect",
                mechanism="Both increase NO",
                management="Generally safe; monitor for excessive hypotension"
            ),
            DrugInteraction(
                interacting_drug="Anticoagulants",
                severity="minor",
                effect_description="Theoretical bleeding risk",
                mechanism="NO inhibits platelets",
                management="Monitor if high-dose arginine with anticoagulants"
            )
        ],
        
        monitoring_protocol=[
            MonitoringRequirement(
                target_type=EffectTargetType.VITAL_SIGN,
                target_name="Blood Pressure",
                baseline_required=False,
                frequency="Periodically if treating hypertension",
                condition="if_used_for_cv_health"
            )
        ],
        
        pregnancy_category="B",  # Generally considered safe
        requires_prescription=False,
        controlled_substance=False,
        
        primary_sources=[
            Quote("L-arginine meta-analysis for BP", "https://pubmed.ncbi.nlm.nih.gov/", "research"),
            Quote("Supplement safety databases", "Natural Medicines Database", "clinical")
        ],
        
        last_updated="2024-01-15"
    )


# Export creation function
__all__ = ['create_larginine']
