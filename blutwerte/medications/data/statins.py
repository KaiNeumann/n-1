"""
Statin medications (HMG-CoA reductase inhibitors).

Includes:
- Rosuvastatin (Crestor)
- Other statins
"""

from ...medications.models import (
    Medication, MedicationEffect, Quote, RiskFactor,
    DrugInteraction, MonitoringRequirement,
    EffectTargetType, EffectDirection, FrequencyCategory
)


def create_rosuvastatin() -> Medication:
    """
    Create complete Rosuvastatin profile.
    
    Potent HMG-CoA reductase inhibitor (statin) for dyslipidemia.
    Highly effective at lowering LDL with relatively low drug interaction potential.
    
    Key effects:
    - Dramatic LDL reduction (45-55% at 10mg, 55-63% at 20mg)
    - Mild triglyceride reduction
    - HDL increase
    - Rare liver enzyme elevations (1-3%)
    - Rare muscle effects (myalgia, rhabdomyolysis very rare)
    
    Sources:
    - FDA Prescribing Information
    - EMA Assessment Report
    - Statin safety guidelines
    """
    
    # LDL Cholesterol reduction (primary effect)
    ldl_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="LDL Cholesterol",
        target_synonyms=["LDL", "LDL-Cholesterin", "Low Density Lipoprotein"],
        direction=EffectDirection.DECREASE,
        typical_magnitude="severe",
        frequency_category=FrequencyCategory.VERY_COMMON,
        frequency_percentage=95.0,
        
        dose_dependent=True,
        
        mechanism="Competitive inhibition of HMG-CoA reductase → decreased hepatic "
                 "cholesterol synthesis → upregulation of LDL receptors → "
                 "increased LDL clearance from plasma",
        
        clinical_significance="expected",
        requires_monitoring=True,
        monitoring_recommendation="Check lipid panel 4-12 weeks after initiation/dose change, "
                                "then every 3-12 months. LDL goal: <100 mg/dL (or <70 for high risk)",
        
        evidence=[
            Quote(
                "5mg: 45% LDL reduction; 10mg: 52-55%; 20mg: 55-63%; 40mg: 63-70%",
                "Clinical trials",
                "research"
            ),
            Quote(
                "Most potent statin on mg-per-mg basis",
                "Clinical guidelines",
                "guideline"
            )
        ],
        likelihood_score="A"
    )
    
    # Total Cholesterol reduction
    total_chol_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="Total Cholesterol",
        target_synonyms=["Cholesterin", "A-CHOL", "Total Cholesterin"],
        direction=EffectDirection.DECREASE,
        typical_magnitude="moderate",
        frequency_category=FrequencyCategory.VERY_COMMON,
        frequency_percentage=95.0,
        
        mechanism="Parallel to LDL reduction; also reduces VLDL",
        
        clinical_significance="expected",
        requires_monitoring=False,
        
        evidence=[
            Quote(
                "30-40% reduction in total cholesterol at standard doses",
                "Clinical trials",
                "research"
            )
        ],
        likelihood_score="A"
    )
    
    # HDL Cholesterol increase
    hdl_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="HDL Cholesterol",
        target_synonyms=["HDL", "HDL-Cholesterin", "High Density Lipoprotein"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.VERY_COMMON,
        frequency_percentage=80.0,
        
        mechanism="Enhanced ApoA-I production; reduced CETP activity; "
                 "improved reverse cholesterol transport",
        
        clinical_significance="expected",
        requires_monitoring=False,
        
        evidence=[
            Quote(
                "8-14% increase in HDL-C at standard doses",
                "Clinical trials",
                "research"
            )
        ],
        likelihood_score="A"
    )
    
    # Triglycerides reduction
    tg_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="Triglycerides",
        target_synonyms=["Triglyceride", "A-TRG", "TG"],
        direction=EffectDirection.DECREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.VERY_COMMON,
        frequency_percentage=70.0,
        
        mechanism="Reduction in VLDL production; enhanced triglyceride clearance",
        
        clinical_significance="expected",
        requires_monitoring=False,
        
        evidence=[
            Quote(
                "10-25% reduction in triglycerides; more pronounced if baseline elevated",
                "Clinical trials",
                "research"
            )
        ],
        likelihood_score="A"
    )
    
    # ALT/AST elevation (rare, usually transient)
    alt_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="ALT",
        target_synonyms=["GPT", "Alanine Aminotransferase", "A-GPT"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.UNCOMMON,
        frequency_percentage=1.0,
        
        mechanism="Hepatocellular enzyme release; usually asymptomatic and transient; "
                 "true hepatotoxicity very rare (1 in 10,000)",
        
        clinical_significance="monitor",
        requires_monitoring=True,
        monitoring_recommendation="Check ALT at baseline, 12 weeks after initiation, "
                                "then annually; discontinue if ALT > 3x ULN on repeat",
        
        risk_factors=[
            RiskFactor(
                factor_type="concurrent_med",
                description="Concurrent gemfibrozil",
                concurrent_med="Gemfibrozil",
                multiplier=5.0
            ),
            RiskFactor(
                factor_type="concurrent_med",
                description="Heavy alcohol use",
                condition="alcohol_abuse",
                multiplier=3.0
            ),
            RiskFactor(
                factor_type="condition",
                description="Pre-existing liver disease",
                condition="liver_disease",
                multiplier=3.0
            )
        ],
        
        evidence=[
            Quote(
                "ALT > 3x ULN in 0.1-1% of patients; usually asymptomatic",
                "FDA Label",
                "fda_label"
            ),
            Quote(
                "Clinically apparent liver injury extremely rare (~1/10,000)",
                "LiverTox database",
                "research"
            )
        ],
        likelihood_score="A"
    )
    
    # AST elevation (similar to ALT)
    ast_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="AST",
        target_synonyms=["GOT", "Aspartate Aminotransferase", "A-GOT"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.UNCOMMON,
        frequency_percentage=1.0,
        
        mechanism="Same as ALT elevation",
        
        clinical_significance="monitor",
        requires_monitoring=False,  # Covered by ALT monitoring
        
        evidence=[
            Quote(
                "Parallel ALT/AST elevation pattern",
                "Clinical studies",
                "research"
            )
        ],
        likelihood_score="A"
    )
    
    # CK (Creatine Kinase) elevation (muscle effects)
    ck_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="Creatine Kinase",
        target_synonyms=["CK", "Kreatinin-Kinase", "A-CK", "CPK"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.RARE,
        frequency_percentage=0.5,
        
        mechanism="Muscular enzyme release; myocyte membrane permeability changes; "
                 "severe elevation (>10x ULN) indicates rhabdomyolysis",
        
        clinical_significance="monitor",
        requires_monitoring=False,
        monitoring_recommendation="Check CK if muscle symptoms (pain, weakness, dark urine); "
                                "discontinue if CK > 10x ULN without strenuous exercise "
                                "or if CK > 5x ULN with symptoms",
        
        risk_factors=[
            RiskFactor(
                factor_type="concurrent_med",
                description="Concurrent gemfibrozil",
                concurrent_med="Gemfibrozil",
                multiplier=15.0
            ),
            RiskFactor(
                factor_type="concurrent_med",
                description="Concurrent cyclosporine",
                concurrent_med="Cyclosporine",
                multiplier=10.0
            ),
            RiskFactor(
                factor_type="concurrent_med",
                description="Concurrent azole antifungals",
                concurrent_med="Azole antifungal",
                multiplier=5.0
            ),
            RiskFactor(
                factor_type="concurrent_med",
                description="Concurrent macrolide antibiotics",
                concurrent_med="Macrolide",
                multiplier=4.0
            ),
            RiskFactor(
                factor_type="age",
                description="Age > 80 years",
                age_min=80,
                multiplier=2.0
            ),
            RiskFactor(
                factor_type="condition",
                description="Renal impairment",
                condition="chronic_kidney_disease",
                multiplier=2.5
            ),
            RiskFactor(
                factor_type="condition",
                description="Hypothyroidism",
                condition="hypothyroidism",
                multiplier=2.0
            ),
            RiskFactor(
                factor_type="condition",
                description="High statin dose",
                condition="high_dose_statin",
                multiplier=2.0
            )
        ],
        
        evidence=[
            Quote(
                "Rhabdomyolysis risk ~1/10,000 patient-years",
                "FDA Label",
                "fda_label"
            ),
            Quote(
                "Myalgia reported in 5-10% of patients (often placebo-equivalent)",
                "Clinical trials",
                "research"
            )
        ],
        likelihood_score="A"
    )
    
    # Myalgia symptom
    myalgia_effect = MedicationEffect(
        target_type=EffectTargetType.SYMPTOM,
        target_name="Myalgia",
        target_synonyms=["Muscle Pain", "Muscle Soreness", "Statin-associated Muscle Symptoms"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.COMMON,
        frequency_percentage=5.0,  # True statin myopathy is lower than reported rates
        
        symptom_description="Muscle pain, soreness, weakness, or cramps; "
                          "usually bilateral and proximal; nocturnal cramps common",
        
        mechanism="Multiple mechanisms: CoQ10 depletion, altered cell membrane fluidity, "
                 "reduced mevalonate pathway products; often no CK elevation",
        
        clinical_significance="monitor",
        requires_monitoring=False,
        monitoring_recommendation="Assess symptom severity; check CK if severe; "
                                "consider dose reduction, switching statin, or alternate-day dosing; "
                                "CoQ10 supplementation controversial (may help some patients)",
        
        risk_factors=[
            RiskFactor(
                factor_type="concurrent_med",
                description="Concurrent gemfibrozil",
                concurrent_med="Gemfibrozil",
                multiplier=10.0
            ),
            RiskFactor(
                factor_type="concurrent_med",
                description="Vitamin D deficiency",
                condition="vitamin_d_deficiency",
                multiplier=2.0
            ),
            RiskFactor(
                factor_type="condition",
                description="Hypothyroidism",
                condition="hypothyroidism",
                multiplier=2.5
            ),
            RiskFactor(
                factor_type="condition",
                description="Strenuous exercise",
                condition="intense_exercise",
                multiplier=2.0
            )
        ],
        
        evidence=[
            Quote(
                "True statin myopathy ~1/1000; myalgia 5-10% (placebo-subtracted ~2-3%)",
                "Meta-analyses",
                "research"
            ),
            Quote(
                "Often reversible with dose reduction or switching to hydrophilic statin",
                "Clinical guidelines",
                "guideline"
            )
        ],
        likelihood_score="A"
    )
    
    # Clinical outcome: Cardiovascular risk reduction
    cv_outcome = MedicationEffect(
        target_type=EffectTargetType.CLINICAL_OUTCOME,
        target_name="Cardiovascular Risk",
        target_synonyms=["CV Risk", "Major Adverse Cardiac Events", "MACE"],
        direction=EffectDirection.DECREASE,
        typical_magnitude="moderate",
        frequency_category=FrequencyCategory.COMMON,
        frequency_percentage=25.0,  # Relative risk reduction
        
        outcome_metric="Reduction in major cardiovascular events (MI, stroke, CV death)",
        outcome_timeframe="1_year",
        
        mechanism="LDL reduction → decreased atherosclerotic plaque progression; "
                 "pleiotropic effects: improved endothelial function, reduced inflammation, "
                 "stabilization of atherosclerotic plaques",
        
        clinical_significance="expected",
        requires_monitoring=False,
        
        evidence=[
            Quote(
                "25-35% relative risk reduction in CV events; NNT ~50-100 over 5 years",
                "Meta-analyses (Cholesterol Treatment Trialists)",
                "research"
            ),
            Quote(
                "Benefit proportional to absolute LDL reduction",
                "Clinical guidelines",
                "guideline"
            )
        ],
        likelihood_score="A"
    )
    
    return Medication(
        name="Rosuvastatin",
        name_de="Rosuvastatin",
        brand_names=["Crestor", "Rosuvastatin", "Rozidal"],
        synonyms=["rosuvastatin", "ATC:C10AA07", "statin", "HMG-CoA_reductase_inhibitor"],
        drug_class="Lipid Lowering Agent",
        drug_subclass="Statin (HMG-CoA Reductase Inhibitor)",
        
        available_doses=[(5, "mg"), (10, "mg"), (20, "mg"), (40, "mg")],
        typical_dose_range=(5.0, 40.0),
        
        effects=[
            ldl_effect,
            total_chol_effect,
            hdl_effect,
            tg_effect,
            alt_effect,
            ast_effect,
            ck_effect,
            myalgia_effect,
            cv_outcome
        ],
        
        indications=[
            Quote("Primary hyperlipidemia", "FDA Label", "fda_label"),
            Quote("Mixed dyslipidemia", "FDA Label", "fda_label"),
            Quote("Hypertriglyceridemia", "FDA Label", "fda_label"),
            Quote("Primary prevention of cardiovascular disease", "FDA Label", "fda_label"),
            Quote("Secondary prevention of cardiovascular disease", "FDA Label", "fda_label"),
            Quote("Slowing progression of atherosclerosis", "FDA Label", "fda_label")
        ],
        
        contraindications=[
            Quote("Pregnancy and breastfeeding", "FDA Label", "fda_label"),
            Quote("Active liver disease", "FDA Label", "fda_label"),
            Quote("Hypersensitivity to rosuvastatin", "FDA Label", "fda_label"),
            Quote("Cyclosporine coadministration (contraindicated)", "FDA Label", "fda_label")
        ],
        
        drug_interactions=[
            DrugInteraction(
                interacting_drug="Gemfibrozil",
                severity="contraindicated",
                effect_description="Severe myopathy/rhabdomyolysis risk",
                mechanism="Dual lipid-lowering with additive myotoxicity",
                management="Contraindicated; use fenofibrate if combination necessary"
            ),
            DrugInteraction(
                interacting_drug="Cyclosporine",
                severity="contraindicated",
                effect_description="15-fold increase in rosuvastatin levels",
                mechanism="Cyclosporine inhibits statin metabolism/transporters",
                management="Contraindicated; use pravastatin if statin needed"
            ),
            DrugInteraction(
                interacting_drug="Warfarin",
                severity="moderate",
                effect_description="Potentiated anticoagulation",
                mechanism="Variable; monitor INR closely",
                management="Monitor INR frequently when starting/changing dose"
            ),
            DrugInteraction(
                interacting_drug="Antacids (aluminum/magnesium)",
                severity="minor",
                effect_description="50% reduction in rosuvastatin absorption",
                mechanism="Chelation in GI tract",
                management="Separate administration by 2 hours"
            )
        ],
        
        monitoring_protocol=[
            MonitoringRequirement(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Lipid Panel",
                baseline_required=True,
                frequency="4-12 weeks after initiation/dose change",
                condition="then_every_3_12_months"
            ),
            MonitoringRequirement(
                target_type=EffectTargetType.BIOMARKER,
                target_name="ALT",
                baseline_required=True,
                frequency="12 weeks after initiation",
                condition="then_annually"
            ),
            MonitoringRequirement(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Creatine Kinase",
                baseline_required=False,
                frequency="If muscle symptoms develop",
                condition="symptom_triggered"
            )
        ],
        
        pregnancy_category="X",  # Contraindicated in pregnancy
        requires_prescription=True,
        controlled_substance=False,
        
        primary_sources=[
            Quote("FDA Prescribing Information - Rosuvastatin", "https://dailymed.nlm.nih.gov", "fda_label"),
            Quote("EMA Assessment Report", "https://ema.europa.eu", "guideline"),
            Quote("Cholesterol Treatment Trialists Collaboration", "https://pubmed.ncbi.nlm.nih.gov/", "research"),
            Quote("Statin Safety Guidelines - ACC/AHA", "https://acc.org", "guideline"),
            Quote("LiverTox Database - Rosuvastatin", "https://livertox.nih.gov", "research")
        ],
        
        last_updated="2024-01-15"
    )


# Export creation function
__all__ = ['create_rosuvastatin']
