"""Zinc supplement."""

from blutwerte.medications.models import (
    Medication, MedicationEffect, Quote, RiskFactor,
    DrugInteraction, MonitoringRequirement,
    EffectTargetType, EffectDirection, FrequencyCategory
)

def create_zinc() -> Medication:
    zinc = Medication(
        name="Zinc",
        name_de="Zink",
        brand_names=["Zinc", "Zinc Gluconate", "Zinc Picolinate", "Zinc Sulfate"],
        synonyms=["zinc", "zn", "zink", "ATC:A12CB01"],
        drug_class="Supplement",
        drug_subclass="Mineral",
        available_doses=[(5, "mg"), (15, "mg"), (25, "mg"), (50, "mg")],
        typical_dose_range=(10.0, 25.0),
        effects=[
            MedicationEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Copper",
                target_synonyms=["Kupfer", "Cu", "A-CU"],
                direction=EffectDirection.DECREASE,
                typical_magnitude="mild",
                frequency_category=FrequencyCategory.UNCOMMON,
                frequency_percentage=5.0,
                mechanism="High-dose zinc induces metallothionein, which binds copper and increases its excretion",
                clinical_significance="concerning",
                requires_monitoring=True,
                monitoring_recommendation="Monitor copper if taking >50mg zinc long-term; supplement ratio 10-15:1 (zinc:copper)",
                risk_factors=[RiskFactor(factor_type="condition", description="Dose >50mg daily", condition="high_dose_zinc", multiplier=5.0)],
                evidence=[Quote("Copper deficiency can occur with chronic high-dose zinc", "Clinical studies", "research")],
                likelihood_score="A"
            ),
            MedicationEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="HDL Cholesterol",
                target_synonyms=["HDL", "HDL-Cholesterin"],
                direction=EffectDirection.DECREASE,
                typical_magnitude="mild",
                frequency_category=FrequencyCategory.RARE,
                frequency_percentage=2.0,
                mechanism="Unknown; may be related to copper deficiency or direct effect",
                clinical_significance="monitor",
                requires_monitoring=False,
                risk_factors=[RiskFactor(factor_type="condition", description="High-dose zinc", condition="high_dose_zinc", multiplier=3.0)],
                evidence=[Quote("HDL may decrease with very high zinc doses", "Observational studies", "research")],
                likelihood_score="C"
            ),
            MedicationEffect(
                target_type=EffectTargetType.SYMPTOM,
                target_name="GI Upset",
                target_synonyms=["Nausea", "Stomach Pain", "Dyspepsia"],
                direction=EffectDirection.INCREASE,
                typical_magnitude="mild",
                frequency_category=FrequencyCategory.UNCOMMON,
                frequency_percentage=10.0,
                symptom_description="Nausea, stomach upset, metallic taste; take with food to reduce",
                mechanism="Irritation of gastric mucosa; zinc ion effects",
                clinical_significance="expected",
                requires_monitoring=False,
                monitoring_recommendation="Take with food if nausea occurs",
                evidence=[Quote("GI upset common if taken on empty stomach", "Clinical data", "research")],
                likelihood_score="A"
            ),
            MedicationEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Immune Function",
                target_synonyms=["WBC", "Immunity", "Lymphocytes"],
                direction=EffectDirection.INCREASE,
                typical_magnitude="mild",
                frequency_category=FrequencyCategory.COMMON,
                frequency_percentage=60.0,
                mechanism="Essential for immune cell function; deficiency impairs immunity",
                clinical_significance="expected",
                requires_monitoring=False,
                evidence=[Quote("Restores immune function in deficiency; benefits in common cold unclear", "Clinical trials", "research")],
                likelihood_score="B"
            )
        ],
        indications=[
            Quote("Zinc deficiency", "FDA approved", "fda_label"),
            Quote("Immune support", "Supplement use", "clinical"),
            Quote("Wound healing", "Clinical use", "clinical"),
            Quote("Common cold (lozenges)", "Evidence mixed", "research"),
            Quote("General supplementation", "RDA 8-11mg", "clinical")
        ],
        contraindications=[
            Quote("None at standard doses", "Safety", "clinical")
        ],
        drug_interactions=[
            DrugInteraction(
                interacting_drug="Tetracyclines",
                severity="moderate",
                effect_description="Reduced absorption of both",
                mechanism="Chelates in GI tract",
                management="Separate by 2-4 hours"
            ),
            DrugInteraction(
                interacting_drug="Quinolones",
                severity="moderate",
                effect_description="Reduced antibiotic absorption",
                mechanism="Chelates in GI tract",
                management="Separate by 2-4 hours"
            ),
            DrugInteraction(
                interacting_drug="Penicillamine",
                severity="moderate",
                effect_description="Reduced penicillamine absorption",
                mechanism="Chelates metal",
                management="Separate by 2 hours"
            ),
            DrugInteraction(
                interacting_drug="Thiazide diuretics",
                severity="minor",
                effect_description="Increased zinc excretion",
                mechanism="Renal losses",
                management="May need slightly higher zinc intake"
            ),
            DrugInteraction(
                interacting_drug="Copper supplements",
                severity="minor",
                effect_description="Competitive absorption",
                mechanism="Shared transport mechanisms",
                management="Take at different times; ratio 10-15:1 zinc:copper"
            )
        ],
        monitoring_protocol=[
            MonitoringRequirement(target_type=EffectTargetType.BIOMARKER, target_name="Zinc", baseline_required=False, frequency="If deficiency suspected", condition="diagnostic"),
            MonitoringRequirement(target_type=EffectTargetType.BIOMARKER, target_name="Copper", baseline_required=False, frequency="If high-dose long-term", condition="high_dose_zinc")
        ],
        pregnancy_category="A",
        requires_prescription=False,
        controlled_substance=False,
        primary_sources=[
            Quote("Zinc supplementation guidelines", "https://pubmed.ncbi.nlm.nih.gov/", "guideline"),
            Quote("Zinc-copper interactions", "https://pubmed.ncbi.nlm.nih.gov/", "research")
        ],
        last_updated="2024-01-15"
    )
    return zinc

__all__ = ['create_zinc']
