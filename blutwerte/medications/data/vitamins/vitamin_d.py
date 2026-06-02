"""
Vitamin D3 (Cholecalciferol) supplement.

Key effects:
- Calcium increase (primary)
- PTH decrease
- Bone health biomarkers
- Uric acid increase (rare)
- Kidney stone risk (with high doses)
"""

from blutwerte.medications.models import (
    Medication, MedicationEffect, Quote, RiskFactor,
    DrugInteraction, MonitoringRequirement,
    EffectTargetType, EffectDirection, FrequencyCategory
)


def create_vitamin_d3() -> Medication:
    """Create Vitamin D3 (Cholecalciferol) supplement profile"""
    
    # Calcium increase (primary effect)
    calcium_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="Calcium",
        target_synonyms=["Kalzium", "Ca", "A-CA", "Serum Calcium"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.COMMON,
        frequency_percentage=30.0,
        
        dose_dependent=True,
        
        mechanism="Vitamin D enhances intestinal calcium absorption (active transport); "
                 "increases renal calcium reabsorption; mobilizes bone calcium",
        
        clinical_significance="expected",
        requires_monitoring=False,
        monitoring_recommendation="Monitor calcium if taking high doses (>4000 IU) or "
                                "if history of hypercalcemia; check at 8-12 weeks",
        
        risk_factors=[
            RiskFactor(
                factor_type="concurrent_med",
                description="Concurrent thiazide diuretics",
                concurrent_med="Thiazide",
                multiplier=3.0
            ),
            RiskFactor(
                factor_type="condition",
                description="Primary hyperparathyroidism",
                condition="hyperparathyroidism",
                multiplier=5.0
            ),
            RiskFactor(
                factor_type="condition",
                description="Sarcoidosis",
                condition="sarcoidosis",
                multiplier=5.0
            ),
            RiskFactor(
                factor_type="condition",
                description="History of kidney stones",
                condition="kidney_stones",
                multiplier=2.0
            )
        ],
        
        evidence=[
            Quote(
                "Calcium increases 0.1-0.3 mg/dL with repletion; "
                "hypercalcemia rare at standard doses",
                "Clinical studies",
                "research"
            )
        ],
        likelihood_score="A"
    )
    
    # PTH decrease
    pth_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="Parathyroid Hormone",
        target_synonyms=["PTH", "Intact PTH", "Parathormon"],
        direction=EffectDirection.DECREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.COMMON,
        frequency_percentage=70.0,
        
        mechanism="Negative feedback: increased calcium and direct vitamin D effects "
                 "on parathyroid gland suppress PTH secretion",
        
        clinical_significance="expected",
        requires_monitoring=False,
        
        evidence=[
            Quote(
                "PTH decreases 15-30% with vitamin D repletion; "
                "beneficial for bone health",
                "Clinical studies",
                "research"
            )
        ],
        likelihood_score="A"
    )
    
    # Uric acid increase (rare, at high doses)
    uric_acid_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="Uric Acid",
        target_synonyms=["Harnsäure", "A-HS", "Serum Urate"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.RARE,
        frequency_percentage=1.0,
        
        mechanism="Increased calcium may reduce uric acid excretion; "
                 "competition for renal tubular transport",
        
        clinical_significance="monitor",
        requires_monitoring=False,
        
        risk_factors=[
            RiskFactor(
                factor_type="condition",
                description="History of gout",
                condition="gout",
                multiplier=5.0
            )
        ],
        
        evidence=[
            Quote(
                "Rare case reports of hyperuricemia with high-dose vitamin D",
                "Case reports",
                "research"
            )
        ],
        likelihood_score="C"
    )
    
    # Kidney stone risk
    stone_risk = MedicationEffect(
        target_type=EffectTargetType.CLINICAL_OUTCOME,
        target_name="Kidney Stones",
        target_synonyms=["Nephrolithiasis", "Renal Calculi", "Urinary Stones"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.RARE,
        frequency_percentage=0.5,
        
        mechanism="Hypercalciuria from increased calcium absorption; "
                 "urinary calcium excretion increases",
        
        clinical_significance="concerning",
        requires_monitoring=False,
        monitoring_recommendation="Use caution with high doses (>4000 IU) in stone formers; "
                                "ensure adequate hydration; consider lower doses",
        
        risk_factors=[
            RiskFactor(
                factor_type="condition",
                description="History of kidney stones",
                condition="kidney_stones",
                multiplier=5.0
            ),
            RiskFactor(
                factor_type="condition",
                description="Hypercalciuria",
                condition="hypercalciuria",
                multiplier=10.0
            ),
            RiskFactor(
                factor_type="concurrent_med",
                description="Concurrent thiazide diuretics",
                concurrent_med="Thiazide",
                multiplier=2.0  # Thiazides actually reduce stone risk
            )
        ],
        
        evidence=[
            Quote(
                "Slight increase in stone risk with high-dose calcium/vitamin D; "
                "standard doses likely safe",
                "Clinical trials",
                "research"
            )
        ],
        likelihood_score="B"
    )
    
    return Medication(
        name="Vitamin D3",
        name_de="Vitamin D3",
        brand_names=["Vitamin D3", "Cholecalciferol", "Vitamine D"],
        synonyms=["vitamin_d3", "cholecalciferol", "vitamin_d", "ATC:A11CC05"],
        drug_class="Supplement",
        drug_subclass="Vitamin",
        
        available_doses=[(400, "IU"), (1000, "IU"), (2000, "IU"), (5000, "IU")],
        typical_dose_range=(1000.0, 4000.0),
        
        effects=[
            calcium_effect,
            pth_effect,
            uric_acid_effect,
            stone_risk
        ],
        
        indications=[
            Quote("Vitamin D deficiency", "Clinical guidelines", "guideline"),
            Quote("Bone health", "Supplement use", "clinical"),
            Quote("Immune support", "Supplement use", "clinical"),
            Quote("Muscle function", "Supplement use", "clinical")
        ],
        
        contraindications=[
            Quote("Hypercalcemia", "Safety precaution", "clinical"),
            Quote("Vitamin D toxicity", "Safety precaution", "clinical"),
            Quote("Granulomatous diseases (sarcoidosis, TB) - high doses", "Risk of hypercalcemia", "clinical")
        ],
        
        drug_interactions=[
            DrugInteraction(
                interacting_drug="Thiazide diuretics",
                severity="moderate",
                effect_description="Hypercalcemia risk",
                mechanism="Both increase calcium",
                management="Monitor calcium levels; usually beneficial for bones"
            ),
            DrugInteraction(
                interacting_drug="Orlistat",
                severity="moderate",
                effect_description="Reduced vitamin D absorption",
                mechanism="Fat malabsorption",
                management="Take vitamin D at different time; monitor levels"
            ),
            DrugInteraction(
                interacting_drug="Glucocorticoids",
                severity="moderate",
                effect_description="Reduced vitamin D effect",
                mechanism="Steroids impair vitamin D metabolism",
                management="May need higher vitamin D doses"
            )
        ],
        
        monitoring_protocol=[
            MonitoringRequirement(
                target_type=EffectTargetType.BIOMARKER,
                target_name="25-OH Vitamin D",
                baseline_required=True,
                frequency="8-12 weeks after starting",
                condition="target_30_50_ng_mL"
            ),
            MonitoringRequirement(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Calcium",
                baseline_required=False,
                frequency="If high-dose or risk factors",
                condition="high_dose_or_risk"
            )
        ],
        
        pregnancy_category="A",
        requires_prescription=False,
        controlled_substance=False,
        
        primary_sources=[
            Quote("Endocrine Society Vitamin D Guidelines", "https://pubmed.ncbi.nlm.nih.gov/", "guideline"),
            Quote("IOM Vitamin D Report", "https://pubmed.ncbi.nlm.nih.gov/", "guideline")
        ],
        
        last_updated="2024-01-15"
    )


__all__ = ['create_vitamin_d3']
