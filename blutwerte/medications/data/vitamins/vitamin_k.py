"""
Vitamin K2 (MK-7) supplement.

Key effects:
- Coagulation factors (II, VII, IX, X) - vitamin K dependent
- May affect INR in patients on warfarin
- Bone health (osteocalcin carboxylation)
- Cardiovascular (matrix Gla protein)
"""

from blutwerte.medications.models import (
    Medication, MedicationEffect, Quote, RiskFactor,
    DrugInteraction, MonitoringRequirement,
    EffectTargetType, EffectDirection, FrequencyCategory
)


def create_vitamin_k2() -> Medication:
    """Create Vitamin K2 (MK-7) supplement profile"""
    
    # INR decrease (primary concern with warfarin)
    inr_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="INR",
        target_synonyms=["International Normalized Ratio", "Quick", "PT"],
        direction=EffectDirection.DECREASE,
        typical_magnitude="moderate",
        frequency_category=FrequencyCategory.VERY_COMMON,
        frequency_percentage=90.0,
        
        mechanism="Cofactor for gamma-carboxylation of clotting factors II, VII, IX, X; "
                 "antagonizes warfarin effect",
        
        clinical_significance="concerning",
        requires_monitoring=True,
        monitoring_recommendation="AVOID with warfarin unless specifically prescribed; "
                                "if used together, monitor INR frequently; "
                                "vitamin K intake should be consistent",
        
        risk_factors=[
            RiskFactor(
                factor_type="concurrent_med",
                description="Concurrent warfarin",
                concurrent_med="Warfarin",
                multiplier=10.0
            )
        ],
        
        evidence=[
            Quote(
                "Vitamin K antagonizes warfarin; INR decreases with supplementation",
                "Clinical guidelines",
                "guideline"
            ),
            Quote(
                "MK-7 has longer half-life than vitamin K1; more stable effect",
                "Pharmacokinetic studies",
                "research"
            )
        ],
        likelihood_score="A"
    )
    
    # Coagulation factors increase
    coag_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="Coagulation Factors",
        target_synonyms=["Factor II", "Factor VII", "Factor IX", "Factor X"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.COMMON,
        frequency_percentage=70.0,
        
        mechanism="Gamma-carboxylation activation of vitamin K-dependent clotting factors",
        
        clinical_significance="expected",
        requires_monitoring=False,
        
        evidence=[
            Quote(
                "Increases functional vitamin K-dependent clotting factors",
                "Clinical studies",
                "research"
            )
        ],
        likelihood_score="A"
    )
    
    # Osteocalcin activation (bone health)
    bone_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="Osteocalcin",
        target_synonyms=["Bone Gla Protein", "BGP"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.COMMON,
        frequency_percentage=60.0,
        
        mechanism="Carboxylation of osteocalcin → improved bone mineral binding; "
                 "directs calcium to bone",
        
        clinical_significance="expected",
        requires_monitoring=False,
        
        evidence=[
            Quote(
                "Increases carboxylated osteocalcin; improves bone density",
                "Clinical trials",
                "research"
            )
        ],
        likelihood_score="B"
    )
    
    # Matrix Gla protein (cardiovascular)
    mgp_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="Matrix Gla Protein",
        target_synonyms=["MGP", "ucMGP", "dp-ucMGP"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.COMMON,
        frequency_percentage=70.0,
        
        mechanism="Carboxylation of MGP → calcium binding → inhibition of vascular calcification",
        
        clinical_significance="expected",
        requires_monitoring=False,
        
        evidence=[
            Quote(
                "Reduces inactive ucMGP; may slow vascular calcification",
                "Clinical studies",
                "research"
            )
        ],
        likelihood_score="B"
    )
    
    return Medication(
        name="Vitamin K2",
        name_de="Vitamin K2",
        brand_names=["Vitamin K2", "MK-7", "Menaquinone-7"],
        synonyms=["vitamin_k2", "mk7", "menaquinone", "vitamin_k", "ATC:B02BA"],
        drug_class="Supplement",
        drug_subclass="Vitamin",
        
        available_doses=[(50, "mcg"), (100, "mcg"), (200, "mcg")],
        typical_dose_range=(100.0, 200.0),
        
        effects=[
            inr_effect,
            coag_effect,
            bone_effect,
            mgp_effect
        ],
        
        indications=[
            Quote("Bone health (with vitamin D)", "Supplement use", "clinical"),
            Quote("Cardiovascular health", "Supplement use", "clinical"),
            Quote("Vascular calcification prevention", "Supplement use", "clinical")
        ],
        
        contraindications=[
            Quote("Warfarin therapy (relative - requires careful monitoring)", "Drug interaction", "clinical"),
            Quote("Hypercoagulable states", "Precautionary", "clinical")
        ],
        
        drug_interactions=[
            DrugInteraction(
                interacting_drug="Warfarin",
                severity="contraindicated",
                effect_description="Antagonizes anticoagulant effect",
                mechanism="Vitamin K-dependent clotting factor synthesis",
                management="Avoid unless specifically prescribed; if used, keep dose consistent and monitor INR"
            ),
            DrugInteraction(
                interacting_drug="Vitamin D",
                severity="minor",
                effect_description="Synergistic bone effects",
                mechanism="K2 directs calcium, D3 increases absorption",
                management="Beneficial combination for bone health"
            )
        ],
        
        monitoring_protocol=[
            MonitoringRequirement(
                target_type=EffectTargetType.BIOMARKER,
                target_name="INR",
                baseline_required=False,
                frequency="Frequently if on warfarin",
                condition="concurrent_warfarin"
            )
        ],
        
        pregnancy_category="A",
        requires_prescription=False,
        controlled_substance=False,
        
        primary_sources=[
            Quote("Vitamin K2 supplementation trials", "https://pubmed.ncbi.nlm.nih.gov/", "research"),
            Quote("MK-7 pharmacokinetics", "https://pubmed.ncbi.nlm.nih.gov/", "research")
        ],
        
        last_updated="2024-01-15"
    )


__all__ = ['create_vitamin_k2']
