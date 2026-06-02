"""Vitamin B3 (Niacin/Nicotinic Acid) supplement."""

from blutwerte.medications.models import (
    Medication, MedicationEffect, Quote, RiskFactor,
    DrugInteraction, MonitoringRequirement,
    EffectTargetType, EffectDirection, FrequencyCategory
)

def create_vitamin_b3() -> Medication:
    niacin = Medication(
        name="Vitamin B3",
        name_de="Vitamin B3",
        brand_names=["Niacin", "Nicotinic Acid", "Niacinamide"],
        synonyms=["vitamin_b3", "niacin", "nicotinic_acid", "ATC:A11HA01"],
        drug_class="Supplement",
        drug_subclass="Vitamin",
        available_doses=[(16, "mg"), (50, "mg"), (100, "mg"), (500, "mg")],
        typical_dose_range=(16.0, 100.0),
        effects=[
            MedicationEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="HDL Cholesterol",
                target_synonyms=["HDL", "HDL-Cholesterin"],
                direction=EffectDirection.INCREASE,
                typical_magnitude="moderate",
                frequency_category=FrequencyCategory.VERY_COMMON,
                frequency_percentage=85.0,
                dose_dependent=True,
                mechanism="Inhibits hepatic HDL clearance; increases ApoA-I synthesis",
                clinical_significance="expected",
                requires_monitoring=False,
                evidence=[Quote("HDL increase 15-35% at therapeutic doses (1-3g)", "Clinical trials", "research")],
                likelihood_score="A"
            ),
            MedicationEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Triglycerides",
                target_synonyms=["Triglyceride", "A-TRG"],
                direction=EffectDirection.DECREASE,
                typical_magnitude="moderate",
                frequency_category=FrequencyCategory.VERY_COMMON,
                frequency_percentage=80.0,
                mechanism="Inhibits hepatic VLDL synthesis",
                clinical_significance="expected",
                requires_monitoring=False,
                evidence=[Quote("TG reduction 20-30%", "Clinical trials", "research")],
                likelihood_score="A"
            ),
            MedicationEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="LDL Cholesterol",
                target_synonyms=["LDL", "LDL-Cholesterin"],
                direction=EffectDirection.DECREASE,
                typical_magnitude="moderate",
                frequency_category=FrequencyCategory.COMMON,
                frequency_percentage=70.0,
                mechanism="Reduces VLDL production and LDL formation",
                clinical_significance="expected",
                requires_monitoring=False,
                evidence=[Quote("LDL reduction 10-25%", "Clinical trials", "research")],
                likelihood_score="A"
            ),
            MedicationEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Uric Acid",
                target_synonyms=["Harnsäure", "A-HS"],
                direction=EffectDirection.INCREASE,
                typical_magnitude="mild",
                frequency_category=FrequencyCategory.UNCOMMON,
                frequency_percentage=5.0,
                mechanism="Competes with uric acid for renal excretion",
                clinical_significance="monitor",
                requires_monitoring=True,
                monitoring_recommendation="Check uric acid if history of gout",
                risk_factors=[RiskFactor(factor_type="condition", description="History of gout", condition="gout", multiplier=5.0)],
                evidence=[Quote("Can precipitate gout in susceptible individuals", "Clinical data", "research")],
                likelihood_score="A"
            ),
            MedicationEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Glucose",
                target_synonyms=["Glukose", "A-BZ"],
                direction=EffectDirection.INCREASE,
                typical_magnitude="mild",
                frequency_category=FrequencyCategory.UNCOMMON,
                frequency_percentage=5.0,
                mechanism="Insulin resistance induction at high doses",
                clinical_significance="monitor",
                requires_monitoring=True,
                monitoring_recommendation="Monitor glucose if diabetes or prediabetes",
                risk_factors=[RiskFactor(factor_type="condition", description="Diabetes", condition="diabetes", multiplier=3.0)],
                evidence=[Quote("Glucose may increase 5-10% at high doses", "Clinical trials", "research")],
                likelihood_score="A"
            ),
            MedicationEffect(
                target_type=EffectTargetType.SYMPTOM,
                target_name="Flushing",
                target_synonyms=["Niacin Flush", "Skin Redness"],
                direction=EffectDirection.INCREASE,
                typical_magnitude="moderate",
                frequency_category=FrequencyCategory.VERY_COMMON,
                frequency_percentage=70.0,
                symptom_description="Cutaneous flushing, warmth, itching; prostaglandin-mediated; tolerance develops",
                mechanism="Prostaglandin release from skin cells; vasodilation",
                clinical_significance="expected",
                requires_monitoring=False,
                monitoring_recommendation="Take with food; aspirin 325mg 30min before can reduce; extended-release reduces flush",
                evidence=[Quote("Flush occurs in 70%+ at therapeutic doses; not toxic", "Clinical data", "research")],
                likelihood_score="A"
            ),
            MedicationEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="AST",
                target_synonyms=["GOT", "A-GOT"],
                direction=EffectDirection.INCREASE,
                typical_magnitude="mild",
                frequency_category=FrequencyCategory.UNCOMMON,
                frequency_percentage=3.0,
                mechanism="Hepatic steatosis at high doses; dose-dependent",
                clinical_significance="monitor",
                requires_monitoring=True,
                monitoring_recommendation="Check LFTs at baseline and during therapy",
                evidence=[Quote("ALT/AST elevation >3x ULN in 0.5-3%", "Clinical trials", "research")],
                likelihood_score="A"
            )
        ],
        indications=[
            Quote("Dyslipidemia (therapeutic doses)", "Clinical use", "clinical"),
            Quote("Vitamin B3 deficiency (pellagra)", "FDA approved", "fda_label"),
            Quote("General supplementation", "RDA 16mg", "clinical")
        ],
        contraindications=[
            Quote("Active liver disease", "Safety", "clinical"),
            Quote("Active peptic ulcer disease", "Precaution", "clinical"),
            Quote("Arterial bleeding", "Precaution", "clinical")
        ],
        drug_interactions=[
            DrugInteraction(
                interacting_drug="Statins",
                severity="major",
                effect_description="Increased myopathy risk",
                mechanism="Additive effects",
                management="Monitor CK; increased risk with combination"
            ),
            DrugInteraction(
                interacting_drug="Aspirin",
                severity="minor",
                effect_description="Reduced flushing",
                mechanism="Prostaglandin inhibition",
                management="Beneficial - take aspirin 30min before niacin"
            ),
            DrugInteraction(
                interacting_drug="Antihypertensives",
                severity="minor",
                effect_description="Additive hypotension",
                mechanism="Vasodilation",
                management="Monitor BP"
            )
        ],
        monitoring_protocol=[
            MonitoringRequirement(target_type=EffectTargetType.BIOMARKER, target_name="Lipid Panel", baseline_required=True, frequency="6-8 weeks", condition="if_therapeutic_dose"),
            MonitoringRequirement(target_type=EffectTargetType.BIOMARKER, target_name="Liver Enzymes", baseline_required=True, frequency="Every 3-6 months", condition="if_therapeutic_dose"),
            MonitoringRequirement(target_type=EffectTargetType.BIOMARKER, target_name="Glucose", baseline_required=False, frequency="Periodically", condition="if_diabetes_risk")
        ],
        pregnancy_category="A",
        requires_prescription=False,
        controlled_substance=False,
        primary_sources=[
            Quote("AIM-HIGH Trial", "https://pubmed.ncbi.nlm.nih.gov/", "research"),
            Quote("HPS2-THRIVE Trial", "https://pubmed.ncbi.nlm.nih.gov/", "research")
        ],
        last_updated="2024-01-15"
    )
    return niacin

__all__ = ['create_vitamin_b3']
