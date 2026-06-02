"""
Omega-3 fatty acid supplements.

Includes:
- EPA/DHA (fish oil)
- Omega-3 concentrates
"""

from ...medications.models import (
    Medication, MedicationEffect, Quote, RiskFactor,
    DrugInteraction, MonitoringRequirement,
    EffectTargetType, EffectDirection, FrequencyCategory
)


def create_omega3() -> Medication:
    """
    Create complete Omega-3 (EPA/DHA) supplement profile.
    
    Essential fatty acids with potent anti-inflammatory and lipid effects.
    One of the most evidence-based supplements for cardiovascular health.
    
    Key effects:
    - Triglyceride reduction (20-30%)
    - HDL increase (modest)
    - LDL slight increase (at high doses)
    - Bleeding risk (mild antiplatelet effect)
    - Anti-inflammatory (CRP reduction)
    
    Sources:
    - REDUCE-IT trial (EPA)
    - STRENGTH trial
    - ASCEND trial
    """
    
    # Triglyceride reduction (primary effect)
    tg_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="Triglycerides",
        target_synonyms=["Triglyceride", "A-TRG", "TG"],
        direction=EffectDirection.DECREASE,
        typical_magnitude="moderate",
        frequency_category=FrequencyCategory.VERY_COMMON,
        frequency_percentage=90.0,
        
        dose_dependent=True,
        
        mechanism="Multiple: reduced hepatic VLDL synthesis, enhanced TG clearance, "
                 "activation of PPAR-alpha, inhibition of hepatic lipogenesis",
        
        clinical_significance="expected",
        requires_monitoring=False,
        monitoring_recommendation="Check lipid panel 8-12 weeks after starting; "
                                "effects evident at 2-4g EPA+DHA daily",
        
        risk_factors=[
            RiskFactor(
                factor_type="biomarker",
                description="High baseline TG (>200 mg/dL)",
                biomarker_name="Triglycerides",
                biomarker_range=(200, 1000),
                multiplier=1.5
            )
        ],
        
        evidence=[
            Quote(
                "20-30% reduction at 2-4g daily; dose-dependent",
                "Meta-analyses",
                "research"
            ),
            Quote(
                "Greater effect in patients with baseline TG > 200 mg/dL",
                "Clinical trials",
                "research"
            )
        ],
        likelihood_score="A"
    )
    
    # HDL increase (modest)
    hdl_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="HDL Cholesterol",
        target_synonyms=["HDL", "HDL-Cholesterin", "High Density Lipoprotein"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.COMMON,
        frequency_percentage=70.0,
        
        mechanism="Enhanced reverse cholesterol transport; increased ApoA-I production",
        
        clinical_significance="expected",
        requires_monitoring=False,
        
        evidence=[
            Quote(
                "1-3 mg/dL increase (modest); less clinically significant than TG effect",
                "Clinical trials",
                "research"
            )
        ],
        likelihood_score="A"
    )
    
    # LDL increase (paradoxical, at high doses)
    ldl_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="LDL Cholesterol",
        target_synonyms=["LDL", "LDL-Cholesterin", "Low Density Lipoprotein"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.COMMON,
        frequency_percentage=30.0,
        
        mechanism="Increased conversion of VLDL to LDL; shift to larger, less atherogenic particles",
        
        clinical_significance="expected",
        requires_monitoring=True,
        monitoring_recommendation="Monitor LDL at 8-12 weeks; "
                                "consider adding statin if significant rise; "
                                "particle size shift may be beneficial despite higher numbers",
        
        evidence=[
            Quote(
                "LDL may increase 5-10% at high doses (4g); particle size shifts to larger, "
                "less atherogenic pattern",
                "Clinical trials",
                "research"
            )
        ],
        likelihood_score="A"
    )
    
    # CRP reduction (anti-inflammatory)
    crp_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="C-Reactive Protein",
        target_synonyms=["CRP", "C-reaktives Protein", "hsCRP"],
        direction=EffectDirection.DECREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.COMMON,
        frequency_percentage=60.0,
        
        mechanism="Anti-inflammatory: reduced pro-inflammatory cytokines, "
                 "increased resolvins and protectins",
        
        clinical_significance="expected",
        requires_monitoring=False,
        
        evidence=[
            Quote(
                "10-25% reduction in CRP; variable response",
                "Clinical trials",
                "research"
            )
        ],
        likelihood_score="B"
    )
    
    # Bleeding risk (mild antiplatelet)
    bleeding_effect = MedicationEffect(
        target_type=EffectTargetType.CLINICAL_OUTCOME,
        target_name="Bleeding Risk",
        target_synonyms=["Hemorrhage", "Coagulation", "Platelet Function"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.UNCOMMON,
        frequency_percentage=3.0,
        
        mechanism="Incorporation into platelet membranes → reduced TXA2 synthesis → "
                 "mild antiplatelet effect (less than aspirin)",
        
        clinical_significance="monitor",
        requires_monitoring=False,
        monitoring_recommendation="Caution with anticoagulants; "
                                "discontinue 1 week before major surgery; "
                                "minor increase in bleeding time",
        
        risk_factors=[
            RiskFactor(
                factor_type="concurrent_med",
                description="Concurrent warfarin",
                concurrent_med="Warfarin",
                multiplier=2.5
            ),
            RiskFactor(
                factor_type="concurrent_med",
                description="Concurrent aspirin",
                concurrent_med="Aspirin",
                multiplier=2.0
            ),
            RiskFactor(
                factor_type="concurrent_med",
                description="High-dose omega-3 (>4g)",
                concurrent_med="High-dose Omega-3",
                multiplier=2.0
            ),
            RiskFactor(
                factor_type="condition",
                description="Bleeding disorders",
                condition="bleeding_disorder",
                multiplier=3.0
            )
        ],
        
        evidence=[
            Quote(
                "Slight prolongation of bleeding time; clinical bleeding rare",
                "Clinical trials",
                "research"
            ),
            Quote(
                "No significant bleeding risk in meta-analyses up to 4g daily",
                "Meta-analyses",
                "research"
            )
        ],
        likelihood_score="A"
    )
    
    # INR effect (mild)
    inr_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="INR",
        target_synonyms=["International Normalized Ratio", "Quick", "PT"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.UNCOMMON,
        frequency_percentage=5.0,
        
        mechanism="Mild anticoagulant effect; may potentiate warfarin",
        
        clinical_significance="monitor",
        requires_monitoring=True,
        monitoring_recommendation="Monitor INR more frequently when starting omega-3; "
                                "warfarin dose may need 10-20% reduction",
        
        risk_factors=[
            RiskFactor(
                factor_type="concurrent_med",
                description="Concurrent warfarin",
                concurrent_med="Warfarin",
                multiplier=5.0
            )
        ],
        
        evidence=[
            Quote(
                "INR may increase 0.2-0.5 with high-dose omega-3 and warfarin",
                "Case series",
                "research"
            )
        ],
        likelihood_score="B"
    )
    
    # Blood pressure reduction (modest)
    bp_effect = MedicationEffect(
        target_type=EffectTargetType.VITAL_SIGN,
        target_name="Blood Pressure",
        target_synonyms=["BP", "Arterial Pressure", "Blutdruck"],
        direction=EffectDirection.DECREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.COMMON,
        frequency_percentage=40.0,
        
        mechanism="Endothelial function improvement; NO enhancement; "
                 "anti-inflammatory effects on vasculature",
        
        clinical_significance="expected",
        requires_monitoring=False,
        
        evidence=[
            Quote(
                "SBP reduction 2-4 mmHg; modest effect",
                "Meta-analyses",
                "research"
            )
        ],
        likelihood_score="A"
    )
    
    return Medication(
        name="Omega-3 Fatty Acids",
        name_de="Omega-3 Fettsäuren",
        brand_names=["Fish Oil", "EPA/DHA", "Omega-3", "Lovaza", "Vascepa"],
        synonyms=["omega3", "epa", "dha", "fish_oil", "marine_oil", "ATC:C10AX06"],
        drug_class="Supplement",
        drug_subclass="Omega-3 Fatty Acid",
        
        available_doses=[(1000, "mg"), (2000, "mg"), (4000, "mg")],  # Total EPA+DHA
        typical_dose_range=(1000.0, 4000.0),
        
        effects=[
            tg_effect,
            hdl_effect,
            ldl_effect,
            crp_effect,
            bleeding_effect,
            inr_effect,
            bp_effect
        ],
        
        indications=[
            Quote("Hypertriglyceridemia (FDA approved at 4g)", "FDA Label", "fda_label"),
            Quote("Cardiovascular disease prevention (high-dose EPA)", "REDUCE-IT trial", "research"),
            Quote("General cardiovascular health", "Supplement use", "clinical")
        ],
        
        contraindications=[
            Quote("Fish/shellfish allergy (for fish-derived products)", "Allergy precaution", "clinical"),
            Quote("Active bleeding or bleeding disorders", "Precautionary", "clinical")
        ],
        
        drug_interactions=[
            DrugInteraction(
                interacting_drug="Warfarin",
                severity="moderate",
                effect_description="Increased INR/bleeding",
                mechanism="Additive anticoagulant effect",
                management="Monitor INR closely; dose reduction may be needed"
            ),
            DrugInteraction(
                interacting_drug="Aspirin",
                severity="minor",
                effect_description="Additive antiplatelet effect",
                mechanism="Both affect platelet function",
                management="Generally safe; caution with high doses of both"
            ),
            DrugInteraction(
                interacting_drug="Antihypertensives",
                severity="minor",
                effect_description="Additive BP lowering",
                mechanism="Both lower blood pressure",
                management="Monitor BP; beneficial interaction"
            )
        ],
        
        monitoring_protocol=[
            MonitoringRequirement(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Triglycerides",
                baseline_required=True,
                frequency="8-12 weeks after starting",
                condition="if_treating_hypertriglyceridemia"
            ),
            MonitoringRequirement(
                target_type=EffectTargetType.BIOMARKER,
                target_name="INR",
                baseline_required=False,
                frequency="More frequently when starting",
                condition="if_on_warfarin"
            )
        ],
        
        pregnancy_category="A",  # Essential nutrient
        requires_prescription=False,  # Supplements OTC; high-dose EPA (Vascepa) requires Rx
        controlled_substance=False,
        
        primary_sources=[
            Quote("REDUCE-IT Trial - EPA cardiovascular outcomes", "https://pubmed.ncbi.nlm.nih.gov/", "research"),
            Quote("Omega-3 meta-analyses for TG", "https://pubmed.ncbi.nlm.nih.gov/", "research"),
            Quote("FDA Label - EPA (Vascepa)", "https://dailymed.nlm.nih.gov", "fda_label")
        ],
        
        last_updated="2024-01-15"
    )


# Export creation function
__all__ = ['create_omega3']
