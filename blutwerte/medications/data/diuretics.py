"""
Thiazide diuretic medications.

Includes:
- Bendroflumethiazide (Xipamid)
- Hydrochlorothiazide
- Other thiazides
"""

from ...medications.models import (
    Medication, MedicationEffect, Quote, RiskFactor,
    DrugInteraction, MonitoringRequirement,
    EffectTargetType, EffectDirection, FrequencyCategory
)

from ...medications.effects.dose_models import create_approximate_model


def create_xipamid() -> Medication:
    """
    Create complete Bendroflumethiazide (Xipamid) profile.
    
    Thiazide diuretic commonly used for hypertension and edema.
    Known for causing hypokalemia, hyponatremia, and metabolic effects.
    
    Dose-response for hypokalemia:
    - 2.5mg: ~10% risk of K+ < 3.5 mmol/L
    - 5mg: ~20% risk
    - 10mg: ~40% risk
    
    Sources:
    - FDA Prescribing Information
    - British National Formulary
    - PMID: 16960154 (thiazide electrolyte disturbances)
    """
    
    # Hypokalemia effect - the primary concern
    hypokalemia_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="Potassium",
        target_synonyms=["Kalium", "K+", "A-K", "Serum Potassium", "K"],
        direction=EffectDirection.DECREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.COMMON,
        frequency_percentage=15.0,
        
        # Dose-dependent effect
        dose_dependent=True,
        dose_model=create_approximate_model(
            typical_max_dose=5.0,
            low=(10.0, "10% risk of K+ < 3.5 at 2.5mg"),
            medium=(20.0, "20% risk of K+ < 3.5 at 5mg"),
            high=(40.0, "40% risk of K+ < 3.5 at 10mg")
        ),
        
        # Timing
        time_to_onset="days",
        duration="persistent",
        administration_time_relevant=True,  # Morning dosing affects afternoon K+
        
        # Mechanism
        mechanism="Increased distal tubular Na+ delivery stimulates aldosterone, "
                 "leading to enhanced K+ secretion in cortical collecting duct. "
                 "Dose-dependent effect.",
        
        # Clinical significance
        clinical_significance="monitor",
        requires_monitoring=True,
        monitoring_recommendation="Check K+ at 1-2 weeks after initiation/start, "
                                "then every 3-6 months; sooner if symptoms. "
                                "Consider K+ supplementation if < 3.5 mmol/L.",
        
        # Risk factors
        risk_factors=[
            RiskFactor(
                factor_type="biomarker",
                description="Baseline K+ < 3.8 mmol/L",
                biomarker_name="Potassium",
                biomarker_range=(0, 3.8),
                multiplier=2.0
            ),
            RiskFactor(
                factor_type="age",
                description="Age > 65 years",
                age_min=65,
                multiplier=1.5
            ),
            RiskFactor(
                factor_type="concurrent_med",
                description="Concurrent loop diuretic",
                concurrent_med="Furosemide",
                multiplier=2.5
            ),
            RiskFactor(
                factor_type="condition",
                description="History of hypokalemia",
                condition="hypokalemia",
                multiplier=1.8
            ),
            RiskFactor(
                factor_type="concurrent_med",
                description="Concurrent digoxin therapy",
                concurrent_med="Digoxin",
                multiplier=1.5
            )
        ],
        
        # Evidence
        evidence=[
            Quote(
                "Hypokalemia (serum K+ < 3.5 mmol/L) occurs in 5-20% of "
                "patients on thiazide diuretics, dose-dependent",
                "https://pubmed.ncbi.nlm.nih.gov/16960154/",
                "research"
            ),
            Quote(
                "Risk increased in elderly, higher doses, and concurrent "
                "potassium-wasting medications",
                "FDA Label - Bendroflumethiazide",
                "fda_label"
            ),
            Quote(
                "Morning administration recommended to minimize nocturia; "
                "afternoon blood tests may show lowest K+ levels",
                "Clinical Pharmacology",
                "clinical"
            )
        ],
        likelihood_score="A"
    )
    
    # Hyponatremia effect
    hyponatremia_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="Sodium",
        target_synonyms=["Natrium", "Na+", "A-NA", "Serum Sodium"],
        direction=EffectDirection.DECREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.UNCOMMON,
        frequency_percentage=2.0,
        
        dose_dependent=True,
        dose_model=create_approximate_model(
            typical_max_dose=5.0,
            low=(1.0, "1% risk of hyponatremia at 2.5mg"),
            medium=(2.0, "2% risk at 5mg"),
            high=(5.0, "5% risk at 10mg")
        ),
        
        time_to_onset="weeks",
        duration="persistent",
        
        mechanism="Impaired urinary diluting capacity leads to water retention. "
                 "More common in elderly women.",
        
        clinical_significance="concerning",
        requires_monitoring=True,
        monitoring_recommendation="Check Na+ 1-2 weeks after initiation in elderly; "
                                "symptoms: confusion, nausea, headache",
        
        risk_factors=[
            RiskFactor(
                factor_type="age",
                description="Age > 65 years",
                age_min=65,
                multiplier=3.0
            ),
            RiskFactor(
                factor_type="gender",
                description="Female gender",
                gender="female",
                multiplier=2.0
            ),
            RiskFactor(
                factor_type="condition",
                description="Low solute intake",
                condition="malnutrition",
                multiplier=2.5
            )
        ],
        
        evidence=[
            Quote(
                "Thiazide-induced hyponatremia: 2-3% incidence, higher in elderly",
                "https://pubmed.ncbi.nlm.nih.gov/",
                "research"
            )
        ],
        likelihood_score="A"
    )
    
    # Hypercalcemia effect
    hypercalcemia_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="Calcium",
        target_synonyms=["Kalzium", "Ca", "A-CA", "Serum Calcium"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.COMMON,
        frequency_percentage=8.0,
        
        dose_dependent=False,  # Effect plateaus at low doses
        
        time_to_onset="weeks",
        duration="persistent",
        
        mechanism="Enhanced Ca2+ reabsorption in distal tubule via "
                 "NCX1/NCKX2 transporters",
        
        clinical_significance="expected",
        requires_monitoring=False,
        monitoring_recommendation="",
        
        evidence=[
            Quote(
                "Thiazides reduce urinary calcium excretion by 40-50%",
                "https://pubmed.ncbi.nlm.nih.gov/",
                "research"
            )
        ],
        likelihood_score="A"
    )
    
    # Hyperuricemia effect
    hyperuricemia_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="Uric Acid",
        target_synonyms=["Harnsäure", "A-HS", "Serum Urate", "Urate"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.COMMON,
        frequency_percentage=10.0,
        
        mechanism="Competition for organic anion transporters in proximal tubule, "
                 "resulting in decreased uric acid secretion",
        
        clinical_significance="monitor",
        requires_monitoring=False,  # Only if gout history
        monitoring_recommendation="Check uric acid if gout history or symptoms",
        
        risk_factors=[
            RiskFactor(
                factor_type="condition",
                description="History of gout",
                condition="gout",
                multiplier=3.0
            )
        ],
        
        evidence=[
            Quote(
                "Can precipitate gout in predisposed individuals",
                "FDA Label",
                "fda_label"
            )
        ],
        likelihood_score="A"
    )
    
    # Glucose elevation effect
    glucose_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="Glucose",
        target_synonyms=["Glukose", "A-BZ", "Blood Sugar", "Fasting Glucose"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.COMMON,
        frequency_percentage=5.0,
        
        mechanism="Impaired insulin secretion (hypokalemia-related) and "
                 "peripheral glucose utilization. Dose-dependent.",
        
        clinical_significance="monitor",
        requires_monitoring=True,
        monitoring_recommendation="Check fasting glucose at baseline, then annually; "
                                "more frequently if diabetes risk factors",
        
        risk_factors=[
            RiskFactor(
                factor_type="condition",
                description="Diabetes mellitus",
                condition="diabetes",
                multiplier=2.5
            ),
            RiskFactor(
                factor_type="condition",
                description="Prediabetes",
                condition="prediabetes",
                multiplier=2.0
            ),
            RiskFactor(
                factor_type="condition",
                description="Obesity (BMI > 30)",
                condition="obesity",
                multiplier=1.8
            )
        ],
        
        evidence=[
            Quote(
                "Dose-dependent effect on glucose metabolism; "
                "usually reversible upon discontinuation",
                "https://pubmed.ncbi.nlm.nih.gov/",
                "research"
            )
        ],
        likelihood_score="A"
    )
    
    # HbA1c effect
    hba1c_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="HbA1c",
        target_synonyms=["Glycated Hemoglobin", "V-HA1C"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.UNCOMMON,
        frequency_percentage=3.0,
        
        mechanism="Secondary to glucose elevation; impaired insulin sensitivity",
        
        clinical_significance="monitor",
        requires_monitoring=False,
        
        evidence=[
            Quote(
                "Small increase in HbA1c (0.1-0.3%) possible in susceptible patients",
                "Clinical studies",
                "research"
            )
        ],
        likelihood_score="B"
    )
    
    # Creatinine effect (volume depletion)
    creatinine_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="Creatinine",
        target_synonyms=["Kreatinin", "A-KREA", "Serum Creatinine"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.UNCOMMON,
        frequency_percentage=2.0,
        
        time_to_onset="days",
        duration="transient",
        
        mechanism="Volume depletion causes prerenal azotemia; "
                 "usually reversible with hydration or dose reduction",
        
        clinical_significance="concerning",
        requires_monitoring=True,
        monitoring_recommendation="Check creatinine 1-2 weeks after initiation; "
                                "concerning if increase > 30% from baseline",
        
        risk_factors=[
            RiskFactor(
                factor_type="condition",
                description="Chronic kidney disease",
                condition="chronic_kidney_disease",
                multiplier=3.0
            ),
            RiskFactor(
                factor_type="condition",
                description="Volume depletion",
                condition="dehydration",
                multiplier=2.5
            )
        ],
        
        evidence=[
            Quote(
                "Reversible with dose reduction or discontinuation; "
                "concerning if persistent elevation",
                "Clinical guidelines",
                "clinical"
            )
        ],
        likelihood_score="B"
    )
    
    # Blood pressure reduction (vital sign effect)
    bp_effect = MedicationEffect(
        target_type=EffectTargetType.VITAL_SIGN,
        target_name="Blood Pressure",
        target_synonyms=["BP", "Arterial Pressure", "Blutdruck"],
        direction=EffectDirection.DECREASE,
        typical_magnitude="moderate",
        frequency_category=FrequencyCategory.VERY_COMMON,
        frequency_percentage=90.0,
        
        mechanism="Initial: Na+ and volume depletion. "
                 "Chronic: Vasodilation via unknown mechanism, "
                 "possibly related to smooth muscle ion channels",
        
        clinical_significance="expected",
        requires_monitoring=True,
        monitoring_recommendation="Check BP 2-4 weeks after initiation/titration; "
                                "target < 130/80 mmHg for most patients",
        
        evidence=[
            Quote(
                "Reduces SBP by 10-20 mmHg and DBP by 5-10 mmHg",
                "Hypertension guidelines",
                "guideline"
            )
        ],
        likelihood_score="A"
    )
    
    # Blood pressure symptoms
    hypotension_symptom = MedicationEffect(
        target_type=EffectTargetType.SYMPTOM,
        target_name="Hypotension",
        target_synonyms=["Low Blood Pressure", "Orthostatic Hypotension"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.UNCOMMON,
        frequency_percentage=5.0,
        
        symptom_description="Dizziness, lightheadedness, especially on standing",
        
        mechanism="Volume depletion and vasodilation",
        
        clinical_significance="monitor",
        requires_monitoring=False,
        
        risk_factors=[
            RiskFactor(
                factor_type="age",
                description="Age > 65",
                age_min=65,
                multiplier=2.0
            )
        ],
        
        evidence=[
            Quote(
                "Orthostatic hypotension more common in elderly",
                "Clinical experience",
                "clinical"
            )
        ],
        likelihood_score="B"
    )
    
    return Medication(
        name="Bendroflumethiazide",
        name_de="Xipamid",
        brand_names=["Xipamid", "Aprinox", "Centyl", "Naturetin", "Neo-NaClex"],
        synonyms=["bendroflumethiazid", "ATC:C03AA01", "thiazide", "thiazide_diuretic"],
        drug_class="Diuretic",
        drug_subclass="Thiazide",
        
        available_doses=[(2.5, "mg"), (5, "mg"), (10, "mg")],
        typical_dose_range=(2.5, 5.0),
        
        effects=[
            hypokalemia_effect,
            hyponatremia_effect,
            hypercalcemia_effect,
            hyperuricemia_effect,
            glucose_effect,
            hba1c_effect,
            creatinine_effect,
            bp_effect,
            hypotension_symptom
        ],
        
        indications=[
            Quote("Hypertension (first-line agent)", "ESC/ESH Guidelines", "guideline"),
            Quote("Edema (heart failure, cirrhosis, nephrotic syndrome)", "FDA Label", "fda_label"),
            Quote("Prevention of kidney stones (hypercalciuria)", "Clinical guidelines", "guideline")
        ],
        
        contraindications=[
            Quote("Anuria", "FDA Label", "fda_label"),
            Quote("Sulfonamide hypersensitivity", "FDA Label", "fda_label"),
            Quote("Severe renal impairment (CrCl < 30 mL/min)", "FDA Label", "fda_label"),
            Quote("Severe hepatic impairment", "FDA Label", "fda_label")
        ],
        
        drug_interactions=[
            DrugInteraction(
                interacting_drug="Lithium",
                severity="major",
                effect_description="Reduced lithium clearance causes lithium toxicity",
                mechanism="Thiazides decrease lithium renal clearance by 20-40%",
                management="Avoid concurrent use or reduce lithium dose by 50% and monitor levels closely"
            ),
            DrugInteraction(
                interacting_drug="Digoxin",
                severity="major",
                effect_description="Hypokalemia increases digoxin toxicity risk",
                mechanism="Low K+ enhances digoxin binding to Na+/K+-ATPase",
                management="Monitor K+ closely; maintain K+ > 4.0 mmol/L; may need K+ supplementation"
            ),
            DrugInteraction(
                interacting_drug="NSAIDs",
                severity="moderate",
                effect_description="Reduced diuretic efficacy; increased renal risk",
                mechanism="NSAIDs inhibit prostaglandin-mediated renal vasodilation",
                management="Monitor renal function; consider alternative analgesics"
            ),
            DrugInteraction(
                interacting_drug="Corticosteroids",
                severity="moderate",
                effect_description="Additive hypokalemia risk",
                mechanism="Both cause K+ wasting",
                management="Monitor K+ closely; consider K+ supplementation prophylactically"
            ),
            DrugInteraction(
                interacting_drug="Beta-agonists",
                severity="minor",
                effect_description="Additive hypokalemia",
                mechanism="Both stimulate K+ shift into cells",
                management="Monitor K+ if high-dose beta-agonist therapy"
            )
        ],
        
        monitoring_protocol=[
            MonitoringRequirement(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Potassium",
                baseline_required=True,
                frequency="3-6 months",
                condition="routine"
            ),
            MonitoringRequirement(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Sodium",
                baseline_required=True,
                frequency="1-2 weeks after initiation",
                condition="if age > 65"
            ),
            MonitoringRequirement(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Creatinine",
                baseline_required=True,
                frequency="1-2 weeks after initiation",
                condition="routine"
            ),
            MonitoringRequirement(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Glucose",
                baseline_required=True,
                frequency="annually",
                condition="if diabetes risk factors"
            ),
            MonitoringRequirement(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Uric Acid",
                baseline_required=True,
                frequency="if gout history",
                condition="symptoms of gout"
            ),
            MonitoringRequirement(
                target_type=EffectTargetType.VITAL_SIGN,
                target_name="Blood Pressure",
                baseline_required=True,
                frequency="2-4 weeks after initiation/titration",
                condition="until target achieved"
            )
        ],
        
        pregnancy_category="B",  # Generally avoided in pregnancy, category D in 2nd/3rd trimester
        requires_prescription=True,
        controlled_substance=False,
        
        primary_sources=[
            Quote("FDA Prescribing Information - Bendroflumethiazide", "https://dailymed.nlm.nih.gov", "fda_label"),
            Quote("British National Formulary", "https://bnf.nice.org.uk", "guideline"),
            Quote("ESC/ESH Guidelines for Hypertension", "https://escardio.org", "guideline"),
            Quote("Thiazide-associated electrolyte disturbances", "https://pubmed.ncbi.nlm.nih.gov/16960154/", "research")
        ],
        
        last_updated="2024-01-15"
    )


# Export creation function
__all__ = ['create_xipamid']
