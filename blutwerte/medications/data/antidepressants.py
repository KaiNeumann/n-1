"""
SSRI antidepressant medications.

Includes:
- Escitalopram (Cipralex/Lexapro)
- Other SSRIs
"""

from ...medications.models import (
    Medication, MedicationEffect, Quote, RiskFactor,
    DrugInteraction, MonitoringRequirement,
    EffectTargetType, EffectDirection, FrequencyCategory
)


def create_escitalopram() -> Medication:
    """
    Create complete Escitalopram profile.
    
    Selective Serotonin Reuptake Inhibitor (SSRI) for depression and anxiety.
    Generally well-tolerated with fewer metabolic side effects than older antidepressants.
    
    Key effects:
    - Sodium decrease (SIADH) - dose-dependent, more common in elderly
    - Weight changes (variable)
    - QT prolongation (rare, dose-dependent)
    - Platelet dysfunction (mild bleeding risk)
    
    Sources:
    - FDA Prescribing Information
    - EMA Assessment Report
    - QT prolongation warnings
    """
    
    # Sodium decrease (SIADH) - most clinically significant effect
    sodium_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="Sodium",
        target_synonyms=["Natrium", "Na+", "A-NA", "Serum Sodium"],
        direction=EffectDirection.DECREASE,
        typical_magnitude="moderate",
        frequency_category=FrequencyCategory.UNCOMMON,
        frequency_percentage=2.5,
        
        mechanism="Syndrome of Inappropriate Antidiuretic Hormone (SIADH): "
                 "SSRI stimulates ADH release → water retention → dilutional hyponatremia",
        
        time_to_onset="weeks",  # Usually within first 2-4 weeks
        
        clinical_significance="concerning",
        requires_monitoring=True,
        monitoring_recommendation="Check Na+ 2-4 weeks after initiation and dose increases "
                                "in patients >65 or with risk factors; "
                                "symptoms: confusion, headache, nausea, seizures if severe",
        
        risk_factors=[
            RiskFactor(
                factor_type="age",
                description="Age > 65 years",
                age_min=65,
                multiplier=4.0
            ),
            RiskFactor(
                factor_type="gender",
                description="Female gender",
                gender="female",
                multiplier=2.5
            ),
            RiskFactor(
                factor_type="concurrent_med",
                description="Concurrent diuretics",
                concurrent_med="Diuretic",
                multiplier=5.0
            ),
            RiskFactor(
                factor_type="condition",
                description="Low body weight",
                condition="low_body_weight",
                multiplier=2.0
            ),
            RiskFactor(
                factor_type="condition",
                description="History of hyponatremia",
                condition="hyponatremia",
                multiplier=3.0
            )
        ],
        
        evidence=[
            Quote(
                "Hyponatremia occurs in 0.5-5% of SSRI users; 10-20% in elderly",
                "Meta-analyses",
                "research"
            ),
            Quote(
                "Usually develops within 2 weeks of initiation",
                "FDA Label",
                "fda_label"
            ),
            Quote(
                "Most cases resolve within 2 weeks of discontinuation",
                "Clinical studies",
                "research"
            )
        ],
        likelihood_score="A"
    )
    
    # Platelet dysfunction (mild)
    platelet_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="Platelet Function",
        target_synonyms=["Thrombozyten", "Bleeding Time", "Platelet Aggregation"],
        direction=EffectDirection.DECREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.COMMON,
        frequency_percentage=10.0,
        
        mechanism="Serotonin depletion from platelets → impaired platelet aggregation; "
                 "SSRIs have antiplatelet effects similar to low-dose aspirin",
        
        clinical_significance="monitor",
        requires_monitoring=False,
        monitoring_recommendation="Be aware of increased bleeding risk; "
                                "monitor for bruising, epistaxis, GI bleeding",
        
        risk_factors=[
            RiskFactor(
                factor_type="concurrent_med",
                description="Concurrent NSAIDs",
                concurrent_med="NSAID",
                multiplier=3.0
            ),
            RiskFactor(
                factor_type="concurrent_med",
                description="Concurrent anticoagulants",
                concurrent_med="Warfarin",
                multiplier=4.0
            ),
            RiskFactor(
                factor_type="concurrent_med",
                description="Concurrent antiplatelets",
                concurrent_med="Aspirin",
                multiplier=3.0
            ),
            RiskFactor(
                factor_type="condition",
                description="History of GI bleeding",
                condition="gi_bleeding",
                multiplier=3.0
            )
        ],
        
        evidence=[
            Quote(
                "2-3x increased risk of GI bleeding; additive with NSAIDs",
                "Epidemiological studies",
                "research"
            ),
            Quote(
                "Surgical bleeding risk increased; consider stopping 7-14 days pre-surgery",
                "Surgical guidelines",
                "guideline"
            )
        ],
        likelihood_score="A"
    )
    
    # Weight increase (common long-term)
    weight_effect = MedicationEffect(
        target_type=EffectTargetType.VITAL_SIGN,
        target_name="Body Weight",
        target_synonyms=["Weight", "Gewicht", "BMI"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.COMMON,
        frequency_percentage=10.0,
        
        mechanism="Multiple: increased appetite/carbohydrate cravings, "
                 "improved mood → better eating, metabolic effects; "
                 "usually gradual over months",
        
        clinical_significance="monitor",
        requires_monitoring=False,
        monitoring_recommendation="Monitor weight at follow-up visits; "
                                "consider dietary counseling if significant gain; "
                                "switching to less weight-promoting agent if problematic",
        
        evidence=[
            Quote(
                "Average gain 1-5 kg over 6-12 months; variable among individuals",
                "Clinical trials",
                "research"
            ),
            Quote(
                "Escitalopram less weight gain than paroxetine, more than fluoxetine",
                "Comparative studies",
                "research"
            )
        ],
        likelihood_score="B"
    )
    
    # QT prolongation (rare but important)
    qt_effect = MedicationEffect(
        target_type=EffectTargetType.BIOMARKER,
        target_name="QT Interval",
        target_synonyms=["QTc", "Corrected QT", "ECG QT"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.RARE,
        frequency_percentage=0.5,
        
        dose_dependent=True,
        
        mechanism="hERG potassium channel blockade → delayed ventricular repolarization; "
                 "risk increases with dose, especially >20mg",
        
        clinical_significance="concerning",
        requires_monitoring=False,
        monitoring_recommendation="Avoid in congenital long QT syndrome; "
                                "avoid concurrent QT-prolonging drugs; "
                                "ECG monitoring if risk factors present; "
                                "maximum dose 20mg (10mg if >65 years)",
        
        risk_factors=[
            RiskFactor(
                factor_type="condition",
                description="Congenital long QT syndrome",
                condition="long_qt_syndrome",
                multiplier=10.0
            ),
            RiskFactor(
                factor_type="condition",
                description="Hypokalemia",
                condition="hypokalemia",
                multiplier=5.0
            ),
            RiskFactor(
                factor_type="condition",
                description="Hypomagnesemia",
                condition="hypomagnesemia",
                multiplier=5.0
            ),
            RiskFactor(
                factor_type="condition",
                description="Bradycardia",
                condition="bradycardia",
                multiplier=3.0
            ),
            RiskFactor(
                factor_type="concurrent_med",
                description="Other QT-prolonging drugs",
                concurrent_med="QT prolonging drug",
                multiplier=5.0
            ),
            RiskFactor(
                factor_type="age",
                description="Age > 65",
                age_min=65,
                multiplier=2.0
            )
        ],
        
        evidence=[
            Quote(
                "QTc increase 5-10ms at 10mg, 10-15ms at 20mg; "
                "Torsades de Pointes very rare",
                "FDA Warning",
                "fda_label"
            ),
            Quote(
                "Maximum recommended dose 10mg if >65 years due to QT risk",
                "FDA Label",
                "fda_label"
            )
        ],
        likelihood_score="A"
    )
    
    # Sexual dysfunction (common, clinically important)
    sexual_dysfunction = MedicationEffect(
        target_type=EffectTargetType.SYMPTOM,
        target_name="Sexual Dysfunction",
        target_synonyms=["Libido decreased", "Erectile Dysfunction", "Anorgasmia", "Delayed Ejaculation"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="moderate",
        frequency_category=FrequencyCategory.COMMON,
        frequency_percentage=15.0,
        
        symptom_description="Decreased libido, delayed orgasm, erectile dysfunction, "
                          "anorgasmia; often dose-dependent; may persist or develop over time",
        
        mechanism="Serotonergic effects on sexual response pathways; "
                 "increased serotonin inhibits dopamine and norepinephrine",
        
        clinical_significance="monitor",
        requires_monitoring=False,
        monitoring_recommendation="Screen for sexual side effects at follow-up "
                                "(patients may not volunteer this information); "
                                "options: dose reduction, drug holiday, adjunctive therapy, "
                                "or switching to non-SSRI antidepressant",
        
        evidence=[
            Quote(
                "10-20% in controlled trials; up to 40-50% in practice; "
                "often underreported",
                "Meta-analyses",
                "research"
            ),
            Quote(
                "Escitalopram less sexual side effects than paroxetine",
                "Comparative studies",
                "research"
            )
        ],
        likelihood_score="A"
    )
    
    # Insomnia OR somnolence (paradoxical, both can occur)
    sleep_effect = MedicationEffect(
        target_type=EffectTargetType.SYMPTOM,
        target_name="Sleep Disturbance",
        target_synonyms=["Insomnia", "Somnolence", "Sleepiness", "Sedation"],
        direction=EffectDirection.VARIABLE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.COMMON,
        frequency_percentage=15.0,
        
        symptom_description="Can cause insomnia (especially if taken late) OR "
                          "somnolence (especially early in treatment); "
                          "variable between individuals",
        
        mechanism="Serotonergic effects on sleep architecture; activation vs sedation",
        
        clinical_significance="expected",
        requires_monitoring=False,
        monitoring_recommendation="If insomnia: take in morning; "
                                "if somnolence: take at bedtime; "
                                "usually improves after 2-4 weeks",
        
        evidence=[
            Quote(
                "Insomnia 10-15%, somnolence 5-10%; varies by individual",
                "Clinical trials",
                "research"
            )
        ],
        likelihood_score="A"
    )
    
    # Gastrointestinal effects
    gi_effect = MedicationEffect(
        target_type=EffectTargetType.SYMPTOM,
        target_name="GI Symptoms",
        target_synonyms=["Nausea", "Diarrhea", "Dyspepsia", "Abdominal Pain"],
        direction=EffectDirection.INCREASE,
        typical_magnitude="mild",
        frequency_category=FrequencyCategory.COMMON,
        frequency_percentage=20.0,
        
        symptom_description="Nausea (most common), diarrhea, dyspepsia; "
                          "usually transient (1-2 weeks)",
        
        mechanism="Serotonergic effects on GI motility and sensation",
        
        clinical_significance="expected",
        requires_monitoring=False,
        monitoring_recommendation="Usually self-limited; take with food if nausea; "
                                "consider dose reduction if persistent",
        
        evidence=[
            Quote(
                "GI effects in 15-25%; usually resolve within 2 weeks",
                "Clinical trials",
                "research"
            )
        ],
        likelihood_score="A"
    )
    
    return Medication(
        name="Escitalopram",
        name_de="Escitalopram",
        brand_names=["Cipralex", "Lexapro", "Esertia"],
        synonyms=["escitalopram", "ATC:N06AB10", "SSRI", "selective_serotonin_reuptake_inhibitor"],
        drug_class="Antidepressant",
        drug_subclass="SSRI (Selective Serotonin Reuptake Inhibitor)",
        
        available_doses=[(5, "mg"), (10, "mg"), (20, "mg")],
        typical_dose_range=(10.0, 20.0),
        
        effects=[
            sodium_effect,
            platelet_effect,
            weight_effect,
            qt_effect,
            sexual_dysfunction,
            sleep_effect,
            gi_effect
        ],
        
        indications=[
            Quote("Major Depressive Disorder (MDD)", "FDA Label", "fda_label"),
            Quote("Generalized Anxiety Disorder (GAD)", "FDA Label", "fda_label"),
            Quote("Panic Disorder with or without agoraphobia", "FDA Label", "fda_label"),
            Quote("Social Anxiety Disorder", "FDA Label", "fda_label"),
            Quote("Obsessive-Compulsive Disorder (OCD)", "Off-label but evidence-based", "research")
        ],
        
        contraindications=[
            Quote("Concurrent MAO inhibitors (or within 14 days)", "FDA Label", "fda_label"),
            Quote("Concurrent pimozide", "FDA Label", "fda_label"),
            Quote("Hypersensitivity to escitalopram or citalopram", "FDA Label", "fda_label"),
            Quote("Congenital long QT syndrome (relative contraindication)", "Clinical guidelines", "guideline")
        ],
        
        drug_interactions=[
            DrugInteraction(
                interacting_drug="MAO inhibitors",
                severity="contraindicated",
                effect_description="Serotonin syndrome, hypertensive crisis",
                mechanism="Additive serotonergic effects",
                management="Contraindicated; 14-day washout required"
            ),
            DrugInteraction(
                interacting_drug="Tramadol",
                severity="major",
                effect_description="Increased seizure risk; serotonin syndrome",
                mechanism="Dual serotonergic mechanism",
                management="Avoid or use with caution; monitor for serotonin syndrome"
            ),
            DrugInteraction(
                interacting_drug="NSAIDs",
                severity="moderate",
                effect_description="Increased bleeding risk",
                mechanism="Additive antiplatelet effects",
                management="Monitor for bleeding; consider PPI if high GI risk"
            ),
            DrugInteraction(
                interacting_drug="Warfarin",
                severity="moderate",
                effect_description="Increased INR/bleeding",
                mechanism="Platelet dysfunction + interaction with metabolism",
                management="Monitor INR closely when starting/changing dose"
            ),
            DrugInteraction(
                interacting_drug="QT-prolonging drugs",
                severity="major",
                effect_description="Additive QT prolongation",
                mechanism="Dual hERG channel blockade",
                management="Avoid combination; ECG monitoring if unavoidable"
            )
        ],
        
        monitoring_protocol=[
            MonitoringRequirement(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Sodium",
                baseline_required=False,
                frequency="2-4 weeks after initiation",
                condition="if_age_over_65_or_risk_factors"
            ),
            MonitoringRequirement(
                target_type=EffectTargetType.SYMPTOM,
                target_name="Mood/Suicidality",
                baseline_required=True,
                frequency="Weekly for first 4 weeks, then periodically",
                condition="especially_under_age_25"
            )
        ],
        
        pregnancy_category="C",  # Risk cannot be ruled out
        requires_prescription=True,
        controlled_substance=False,
        
        primary_sources=[
            Quote("FDA Prescribing Information - Escitalopram", "https://dailymed.nlm.nih.gov", "fda_label"),
            Quote("EMA Assessment Report", "https://ema.europa.eu", "guideline"),
            Quote("FDA Drug Safety Communication: QT prolongation", "https://fda.gov", "fda_label"),
            Quote("SSRI-induced hyponatremia meta-analysis", "https://pubmed.ncbi.nlm.nih.gov/", "research")
        ],
        
        last_updated="2024-01-15"
    )


# Export creation function
__all__ = ['create_escitalopram']
