"""Vitamin B12 (Cobalamin) supplement."""

from blutwerte.medications.models import (
    Medication, MedicationEffect, Quote, RiskFactor,
    DrugInteraction, MonitoringRequirement,
    EffectTargetType, EffectDirection, FrequencyCategory
)

def create_vitamin_b12() -> Medication:
    b12 = Medication(
        name="Vitamin B12",
        name_de="Vitamin B12",
        brand_names=["Cyanocobalamin", "Methylcobalamin", "Hydroxocobalamin", "Cobalamin"],
        synonyms=["vitamin_b12", "cobalamin", "cyanocobalamin", "ATC:B03BA01"],
        drug_class="Supplement",
        drug_subclass="Vitamin",
        available_doses=[(10, "mcg"), (50, "mcg"), (500, "mcg"), (1000, "mcg")],
        typical_dose_range=(10.0, 1000.0),
        effects=[
            MedicationEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Homocysteine",
                target_synonyms=["Homocystein", "A-HCY"],
                direction=EffectDirection.DECREASE,
                typical_magnitude="moderate",
                frequency_category=FrequencyCategory.COMMON,
                frequency_percentage=80.0,
                mechanism="Cofactor for methionine synthase (converts homocysteine to methionine)",
                clinical_significance="expected",
                requires_monitoring=False,
                evidence=[Quote("Reduces homocysteine 15-25% if deficient; less effect if replete", "Clinical trials", "research")],
                likelihood_score="A"
            ),
            MedicationEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Methylmalonic Acid",
                target_synonyms=["MMA", "Methylmalonsäure"],
                direction=EffectDirection.DECREASE,
                typical_magnitude="severe",
                frequency_category=FrequencyCategory.VERY_COMMON,
                frequency_percentage=95.0,
                mechanism="Cofactor for methylmalonyl-CoA mutase",
                clinical_significance="expected",
                requires_monitoring=False,
                evidence=[Quote("MMA normalizes with B12 repletion", "Clinical studies", "research")],
                likelihood_score="A"
            ),
            MedicationEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Hemoglobin",
                target_synonyms=["Hb", "Hämoglobin", "A-HB"],
                direction=EffectDirection.INCREASE,
                typical_magnitude="moderate",
                frequency_category=FrequencyCategory.COMMON,
                frequency_percentage=70.0,
                mechanism="Corrects megaloblastic anemia; essential for DNA synthesis in RBC precursors",
                clinical_significance="expected",
                requires_monitoring=False,
                evidence=[Quote("Corrects anemia in deficiency; reticulocytosis in 5-7 days", "Clinical studies", "research")],
                likelihood_score="A"
            ),
            MedicationEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="MCV",
                target_synonyms=["Mean Corpuscular Volume", "Erythrozytenvolumen"],
                direction=EffectDirection.DECREASE,
                typical_magnitude="moderate",
                frequency_category=FrequencyCategory.COMMON,
                frequency_percentage=70.0,
                mechanism="Normalization of macrocytosis in deficiency",
                clinical_significance="expected",
                requires_monitoring=False,
                evidence=[Quote("MCV normalizes over weeks with treatment", "Clinical studies", "research")],
                likelihood_score="A"
            ),
            MedicationEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Vitamin B12",
                target_synonyms=["B12", "Cobalamin", "Holotranscobalamin"],
                direction=EffectDirection.INCREASE,
                typical_magnitude="severe",
                frequency_category=FrequencyCategory.VERY_COMMON,
                frequency_percentage=99.0,
                mechanism="Direct supplementation increases serum levels",
                clinical_significance="expected",
                requires_monitoring=False,
                monitoring_recommendation="Serum B12 may not reflect tissue status; check MMA if concerns",
                evidence=[Quote("Serum B12 increases with supplementation", "Pharmacokinetic studies", "research")],
                likelihood_score="A"
            )
        ],
        indications=[
            Quote("Vitamin B12 deficiency", "FDA approved", "fda_label"),
            Quote("Pernicious anemia", "FDA approved", "fda_label"),
            Quote("Megaloblastic anemia", "FDA approved", "fda_label"),
            Quote("Homocysteine lowering", "Clinical use", "clinical"),
            Quote("Neuropathy from deficiency", "Clinical use", "clinical"),
            Quote("General supplementation (vegans, elderly)", "Supplement use", "clinical")
        ],
        contraindications=[
            Quote("Hypersensitivity to cobalamin", "Rare", "clinical"),
            Quote("Hereditary optic nerve atrophy (Leber disease) - relative", "Theoretical concern", "clinical")
        ],
        drug_interactions=[
            DrugInteraction(
                interacting_drug="Metformin",
                severity="moderate",
                effect_description="B12 malabsorption",
                mechanism="Metformin reduces B12 absorption by 30%",
                management="Monitor B12 annually if on metformin; supplement if needed"
            ),
            DrugInteraction(
                interacting_drug="PPIs (Omeprazole, etc.)",
                severity="moderate",
                effect_description="B12 malabsorption",
                mechanism="Reduced gastric acid impairs B12 liberation from food",
                management="Monitor B12 with long-term PPI use"
            ),
            DrugInteraction(
                interacting_drug="Colchicine",
                severity="minor",
                effect_description="Reduced B12 absorption",
                mechanism="Intestinal mucosal effects",
                management="Monitor B12 levels"
            )
        ],
        monitoring_protocol=[
            MonitoringRequirement(target_type=EffectTargetType.BIOMARKER, target_name="Vitamin B12", baseline_required=True, frequency="Annually if deficient or at risk", condition="deficiency_or_risk"),
            MonitoringRequirement(target_type=EffectTargetType.BIOMARKER, target_name="MMA", baseline_required=False, frequency="If B12 borderline", condition="diagnostic_uncertainty")
        ],
        pregnancy_category="A",
        requires_prescription=False,
        controlled_substance=False,
        primary_sources=[
            Quote("B12 deficiency guidelines", "https://pubmed.ncbi.nlm.nih.gov/", "guideline"),
            Quote("Metformin-B12 interaction studies", "https://pubmed.ncbi.nlm.nih.gov/", "research")
        ],
        last_updated="2024-01-15"
    )
    return b12

__all__ = ['create_vitamin_b12']
