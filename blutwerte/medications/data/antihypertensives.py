"""
Angiotensin Receptor Blocker (ARB) medications.

Includes:
- Telmisartan (Micardis)
- Other ARBs
"""

from ...medications.models import (
    Medication, MedicationEffect, Quote, RiskFactor,
    DrugInteraction, MonitoringRequirement,
    EffectTargetType, EffectDirection, FrequencyCategory
)


def create_telmisartan() -> Medication:
    """
    Create complete Telmisartan profile.
    
    Angiotensin II Receptor Blocker (ARB) for hypertension.
    Generally well-tolerated with few metabolic side effects.
    
    Key effects:
    - Blood pressure reduction (primary)
    - Mild potassium increase (monitor with other K+-sparing drugs)
    - Mild creatinine increase (expected, usually stabilizes)
    - Renal protective effects in diabetes
    
    Sources:
    - FDA Prescribing Information
    - EMA Assessment Report
    - Clinical guidelines
    """
    
    # Blood pressure reduction (primary effect)
    bp_effect = MedicationEffect(
        target_type=EffectTargetType.VITAL_SIGN,
        target_name="Blood Pressure",
        target_synonyms=["BP", "Arterial Pressure", "Blutdruck"],
        direction=EffectDirection.DECREASE,
        typical_magnitude="moderate",
        frequency_category=FrequencyCategory.VERY_COMMON,
        frequency_percentage=85.0,
        
        mechanism="Selective AT1 receptor antagonism blocks angiotensin II effects: "
                 "vasoconstriction, aldosterone release, sympathetic activation, "
                 "and renal sodium reabsorption",
        
        clinical_significance="expected",
        requires_monitoring=True,
        monitoring_recommendation="Check BP 2-4 weeks after initiation/titration; "
                                "target < 130/80 mmHg for most patients",
        
        evidence=[
            Quote(
                "Reduces SBP by 15-20 mmHg and DBP by 10-15 mmHg",
                "Clinical studies",
                "research"
            ),
            Quote(
                "Long half-life (24 hours) allows once-daily dosing",
                "FDA Label",
                "fda_label"
            )
        ],
        likelihood_score="A"
    )
    
    # Potassium increase (mild, usually not significant)
    potassium_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="Potassium",
        target_synonyms=["Kalium", "K+", "A-K", "Serum Potassium"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.UNCOMMON,
        frequency_percentage=2.0,
        
        mechanism="Reduced aldosterone → decreased distal tubular K+ secretion",
        
        clinical_significance="monitor",
        requires_monitoring=True,
        monitoring_recommendation="Check K+ and creatinine 1-2 weeks after initiation; "
                                "more frequently if combining with K+-sparing diuretics",
        
        risk_factors=[
            RiskFactor(
                factor_type="concurrent_med",
                description="Concurrent potassium-sparing diuretic",
                concurrent_med="Spironolactone",
                multiplier=5.0
            ),
            RiskFactor(
                factor_type="concurrent_med",
                description="Concurrent ACE inhibitor",
                concurrent_med="ACE inhibitor",
                multiplier=3.0
            ),
            RiskFactor(
                factor_type="concurrent_med",
                description="Concurrent potassium supplements",
                concurrent_med="Potassium supplement",
                multiplier=4.0
            ),
            RiskFactor(
                factor_type="condition",
                description="Chronic kidney disease",
                condition="chronic_kidney_disease",
                multiplier=3.0
            ),
            RiskFactor(
                factor_type="condition",
                description="Diabetes mellitus",
                condition="diabetes",
                multiplier=1.5
            ),
            RiskFactor(
                factor_type="biomarker",
                description="Baseline K+ > 4.5 mmol/L",
                biomarker_name="Potassium",
                biomarker_range=(4.5, 10.0),
                multiplier=2.0
            )
        ],
        
        evidence=[
            Quote(
                "Hyperkalemia risk 1-3%, higher with concurrent K+-sparing drugs",
                "Clinical guidelines",
                "guideline"
            )
        ],
        likelihood_score="A"
    )
    
    # Creatinine increase (expected, usually stabilizes)
    creatinine_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="Creatinine",
        target_synonyms=["Kreatinin", "A-KREA", "Serum Creatinine"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.COMMON,
        frequency_percentage=10.0,
        
        mechanism="Efferent arteriole vasodilation in glomerulus reduces intraglomerular "
                 "pressure and GFR; this is EXPECTED and usually stabilizes within 2-4 weeks",
        
        clinical_significance="expected",
        requires_monitoring=True,
        monitoring_recommendation="Check creatinine at baseline, 1-2 weeks, and 1 month; "
                                "acceptable if increase < 30% from baseline and stabilizes; "
                                "discontinue if progressive rise or hyperkalemia develops",
        
        risk_factors=[
            RiskFactor(
                factor_type="condition",
                description="Bilateral renal artery stenosis",
                condition="renal_artery_stenosis",
                multiplier=5.0
            ),
            RiskFactor(
                factor_type="condition",
                description="Severe CHF",
                condition="congestive_heart_failure",
                multiplier=2.5
            ),
            RiskFactor(
                factor_type="condition",
                description="Volume depletion",
                condition="dehydration",
                multiplier=3.0
            )
        ],
        
        evidence=[
            Quote(
                "Creatinine increase 10-30% is expected; usually stabilizes within 2-4 weeks",
                "FDA Label",
                "fda_label"
            ),
            Quote(
                "Concern if increase > 30% or progressive despite continued therapy",
                "Clinical guidelines",
                "guideline"
            )
        ],
        likelihood_score="A"
    )
    
    # eGFR decrease (paired with creatinine)
    egfr_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="eGFR",
        target_synonyms=["GFR", "Glomerular Filtration Rate", "CKD-EPI"],
        direction=EffectDirection.DECREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.COMMON,
        frequency_percentage=10.0,
        
        mechanism="Corresponding decrease to creatinine elevation; hemodynamic effect, "
                 "not true nephrotoxicity",
        
        clinical_significance="expected",
        requires_monitoring=False,
        
        evidence=[
            Quote(
                "eGFR decrease 5-15% expected; renal protective long-term",
                "Clinical studies",
                "research"
            )
        ],
        likelihood_score="A"
    )
    
    # HbA1c improvement (in diabetes patients)
    hba1c_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="HbA1c",
        target_synonyms=["Glycated Hemoglobin", "V-HA1C"],
        direction=EffectDirection.DECREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.COMMON,
        frequency_percentage=15.0,
        
        mechanism="Improved insulin sensitivity; reduced oxidative stress; "
                 "renoprotective effects in diabetic nephropathy",
        
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
                "Reduces HbA1c by 0.1-0.3% in diabetic patients; renal protective",
                "Clinical trials",
                "research"
            )
        ],
        likelihood_score="A"
    )
    
    # Uric acid decrease (beneficial)
    uric_acid_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="Uric Acid",
        target_synonyms=["Harnsäure", "A-HS", "Serum Urate"],
        direction=EffectDirection.DECREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.COMMON,
        frequency_percentage=10.0,
        
        mechanism="Improved renal perfusion enhances uric acid excretion",
        
        clinical_significance="expected",
        requires_monitoring=False,
        
        evidence=[
            Quote(
                "Slight reduction in uric acid levels",
                "Clinical studies",
                "research"
            )
        ],
        likelihood_score="B"
    )
    
    # Hypotension symptom
    hypotension_symptom = MedicationEffect(
        target_type=EffectTargetType.SYMPTOM,
        target_name="Hypotension",
        target_synonyms=["Low Blood Pressure", "Orthostatic Hypotension"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.UNCOMMON,
        frequency_percentage=3.0,
        
        symptom_description="Dizziness, lightheadedness, especially on standing; "
                          "fatigue; first-dose effect possible",
        
        mechanism="Blood pressure reduction; more common with volume depletion",
        
        clinical_significance="monitor",
        requires_monitoring=False,
        
        risk_factors=[
            RiskFactor(
                factor_type="condition",
                description="Volume depletion",
                condition="dehydration",
                multiplier=3.0
            ),
            RiskFactor(
                factor_type="concurrent_med",
                description="Concurrent diuretic",
                concurrent_med="Diuretic",
                multiplier=2.0
            )
        ],
        
        evidence=[
            Quote(
                "First-dose hypotension more common in volume-depleted patients",
                "FDA Label",
                "fda_label"
            )
        ],
        likelihood_score="A"
    )
    
    # Angioedema (rare but serious)
    angioedema_effect = MedicationEffect(
        target_type=EffectTargetType.SYMPTOM,
        target_name="Angioedema",
        target_synonyms=["Swelling", "Angioneurotic Edema"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="severe",
        frequency_category=FrequencyCategory.RARE,
        frequency_percentage=0.1,
        
        symptom_description="Swelling of face, lips, tongue, or throat; "
                          "potentially life-threatening airway obstruction",
        
        mechanism="Bradykinin-mediated (less common than with ACE inhibitors); "
                 "can occur even without ACE inhibitor history",
        
        clinical_significance="emergency",
        requires_monitoring=False,
        
        evidence=[
            Quote(
                "Angioedema risk ~0.1-0.4%; less than ACE inhibitors",
                "FDA Label",
                "fda_label"
            ),
            Quote(
                "Discontinue immediately if angioedema develops; do not restart",
                "Clinical guidelines",
                "guideline"
            )
        ],
        likelihood_score="A"
    )
    
    return Medication(
        name="Telmisartan",
        name_de="Telmisartan",
        brand_names=["Micardis", "Pritor", "Kinzalmono"],
        synonyms=["telmisartan", "ATC:C09CA07", "ARB", "angiotensin_receptor_blocker"],
        drug_class="Antihypertensive",
        drug_subclass="Angiotensin Receptor Blocker (ARB)",
        
        available_doses=[(20, "mg"), (40, "mg"), (80, "mg")],
        typical_dose_range=(40.0, 80.0),
        
        effects=[
            bp_effect,
            potassium_effect,
            creatinine_effect,
            egfr_effect,
            hba1c_effect,
            uric_acid_effect,
            hypotension_symptom,
            angioedema_effect
        ],
        
        indications=[
            Quote("Hypertension (first-line)", "ESC/ESH Guidelines", "guideline"),
            Quote("Cardiovascular risk reduction (80mg dose)", "FDA Label", "fda_label"),
            Quote("Diabetic nephropathy", "KDIGO Guidelines", "guideline")
        ],
        
        contraindications=[
            Quote("Pregnancy ( Category D in 2nd/3rd trimester - fetal toxicity)", "FDA Label", "fda_label"),
            Quote("Hypersensitivity to telmisartan", "FDA Label", "fda_label"),
            Quote("Bilateral renal artery stenosis", "Clinical guidelines", "guideline"),
            Quote("Concomitant aliskiren in diabetes", "FDA Label", "fda_label")
        ],
        
        drug_interactions=[
            DrugInteraction(
                interacting_drug="Potassium supplements",
                severity="major",
                effect_description="Additive hyperkalemia risk",
                mechanism="Both increase potassium",
                management="Avoid combination or monitor K+ closely"
            ),
            DrugInteraction(
                interacting_drug="Spironolactone",
                severity="major",
                effect_description="Severe hyperkalemia risk",
                mechanism="Dual K+-sparing mechanisms",
                management="Contraindicated together unless compelling indication with close monitoring"
            ),
            DrugInteraction(
                interacting_drug="Lithium",
                severity="moderate",
                effect_description="Increased lithium levels",
                mechanism="Reduced lithium clearance",
                management="Monitor lithium levels if combination necessary"
            ),
            DrugInteraction(
                interacting_drug="NSAIDs",
                severity="moderate",
                effect_description="Reduced antihypertensive effect; renal risk",
                mechanism="NSAIDs counteract ARB renal effects",
                management="Monitor renal function and BP"
            ),
            DrugInteraction(
                interacting_drug="Diuretics",
                severity="minor",
                effect_description="Additive BP lowering; first-dose hypotension",
                mechanism="Synergistic blood pressure reduction",
                management="Start low dose; monitor for hypotension"
            )
        ],
        
        monitoring_protocol=[
            MonitoringRequirement(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Creatinine",
                baseline_required=True,
                frequency="1-2 weeks after initiation",
                condition="baseline_and_initiation"
            ),
            MonitoringRequirement(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Potassium",
                baseline_required=True,
                frequency="1-2 weeks after initiation",
                condition="baseline_and_initiation"
            ),
            MonitoringRequirement(
                target_type=EffectTargetType.VITAL_SIGN,
                target_name="Blood Pressure",
                baseline_required=True,
                frequency="2-4 weeks after initiation/titration",
                condition="until target achieved"
            )
        ],
        
        pregnancy_category="D",  # Contraindicated in 2nd/3rd trimester
        requires_prescription=True,
        controlled_substance=False,
        
        primary_sources=[
            Quote("FDA Prescribing Information - Telmisartan", "https://dailymed.nlm.nih.gov", "fda_label"),
            Quote("EMA Assessment Report", "https://ema.europa.eu", "guideline"),
            Quote("ESC/ESH Guidelines for Hypertension", "https://escardio.org", "guideline"),
            Quote("ONTARGET Trial", "https://pubmed.ncbi.nlm.nih.gov/", "research")
        ],
        
        last_updated="2024-01-15"
    )


# Export creation function
__all__ = ['create_telmisartan']
