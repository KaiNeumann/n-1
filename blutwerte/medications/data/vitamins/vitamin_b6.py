"""Vitamin B6 (Pyridoxine) supplement."""

from blutwerte.medications.models import (
    Medication, MedicationEffect, Quote, RiskFactor,
    DrugInteraction, MonitoringRequirement,
    EffectTargetType, EffectDirection, FrequencyCategory
)

def create_vitamin_b6() -> Medication:
    b6 = Medication(
        name="Vitamin B6",
        name_de="Vitamin B6",
        brand_names=["Pyridoxine", "Pyridoxal-5-Phosphate", "P5P"],
        synonyms=["vitamin_b6", "pyridoxine", "pyridoxal", "ATC:A11HA02"],
        drug_class="Supplement",
        drug_subclass="Vitamin",
        available_doses=[(2, "mg"), (10, "mg"), (25, "mg"), (50, "mg"), (100, "mg")],
        typical_dose_range=(2.0, 10.0),
        effects=[
            MedicationEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Homocysteine",
                target_synonyms=["Homocystein", "A-HCY"],
                direction=EffectDirection.DECREASE,
                typical_magnitude="mild",
                frequency_category=FrequencyCategory.COMMON,
                frequency_percentage=60.0,
                mechanism="Cofactor for homocysteine metabolism (cystathionine beta-synthase)",
                clinical_significance="expected",
                requires_monitoring=False,
                evidence=[Quote("Reduces homocysteine 10-20% when deficient", "Clinical trials", "research")],
                likelihood_score="A"
            ),
            MedicationEffect(
                target_type=EffectTargetType.SYMPTOM,
                target_name="Peripheral Neuropathy",
                target_synonyms=["Nerve Damage", "Neuropathy", "Tingling"],
                direction=EffectDirection.INCREASE,
                typical_magnitude="moderate",
                frequency_category=FrequencyCategory.RARE,
                frequency_percentage=0.5,
                symptom_description="Sensory neuropathy: numbness, ataxia, burning; dose-dependent; reversible if caught early",
                mechanism="Toxic metabolite accumulation with chronic high-dose use",
                clinical_significance="concerning",
                requires_monitoring=False,
                monitoring_recommendation="Do not exceed 100mg/day long-term; caution >50mg/day",
                risk_factors=[RiskFactor(factor_type="condition", description="High-dose chronic use >100mg", condition="high_dose_b6", multiplier=10.0)],
                evidence=[Quote("Neurotoxicity at doses >100mg/day; usually reversible", "Case series", "research")],
                likelihood_score="A"
            )
        ],
        indications=[
            Quote("Vitamin B6 deficiency", "FDA approved", "fda_label"),
            Quote("Homocysteine lowering (with B12, folate)", "Clinical use", "clinical"),
            Quote("Morning sickness (doxylamine-pyridoxine)", "FDA approved", "fda_label"),
            Quote("General supplementation", "RDA 1.3-1.7mg", "clinical")
        ],
        contraindications=[
            Quote("None at standard doses", "Safety", "clinical")
        ],
        drug_interactions=[
            DrugInteraction(
                interacting_drug="Levodopa",
                severity="major",
                effect_description="Reduced levodopa efficacy",
                mechanism="B6 enhances peripheral decarboxylation of levodopa",
                management="Avoid concurrent use unless carbidopa included"
            ),
            DrugInteraction(
                interacting_drug="Isoniazid",
                severity="minor",
                effect_description="B6 depletion",
                mechanism="Isoniazid increases B6 excretion",
                management="B6 supplementation recommended with isoniazid (25-50mg)"
            )
        ],
        monitoring_protocol=[
            MonitoringRequirement(target_type=EffectTargetType.BIOMARKER, target_name="Homocysteine", baseline_required=False, frequency="If indicated", condition="hyperhomocysteinemia")
        ],
        pregnancy_category="A",
        requires_prescription=False,
        controlled_substance=False,
        primary_sources=[
            Quote("B6 toxicity review", "https://pubmed.ncbi.nlm.nih.gov/", "research")
        ],
        last_updated="2024-01-15"
    )
    return b6

__all__ = ['create_vitamin_b6']
