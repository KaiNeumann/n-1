# N=1

**All about you.**

Diet. Fitness. Health. Blood. Medication. Activity. Sleep.

**Tracked. Computed. Analyzed.**

In clinical research, an *n=1 trial* is the most rigorous kind of study — a single subject, treated with the same discipline as a large trial. This project applies that idea to nutrition, fitness and health: one person, one dataset, science applied to the only n that matters — you.

This is the logical successor of the original `Food-and-Nutrition` project. It keeps the n=1 philosophy and extends it from food logging to a full personal health analysis system: blood biomarkers, medications, foods, activities, and patient profiles, all joined by the same n-of-1 discipline.

---

## Overview

`n-1` is a Python library for personal health analysis. It provides structured, evidence-based data about:

- **Blood test biomarkers** — 90+ markers with reference ranges, interpretations, and sources
- **Medications** — effects on biomarkers, drug interactions, dose-response modeling
- **Foods** — 8,400+ foods with nutrition data, biomarker effects, and source tracking
- **Activities** — exercise sessions with calorie burn and biomarker effects
- **Patient profiles** — temporal tracking of medications, conditions, vitals, and labs

The core idea: every input that can move a blood value should be tracked, modeled, and analyzed against the same set of biomarkers for the same one person.

## Key Features

### Blood Test Biomarker Database
- **90+ biomarkers** with reference ranges, interpretations, and sources
- **Multi-language support**: German and English names, synonyms, and lab IDs
- **Patient-specific ranges**: Age, gender, and condition-dependent reference values
- **Evidence-based**: All data sourced from clinical guidelines and peer-reviewed research

### Medication Database
- **13 medications** fully documented with effects on blood biomarkers
- **Dose-response modeling**: Effects vary with dosage
- **Drug interactions**: 30+ clinically significant interactions documented
- **Patient-specific risk factors**: Age, gender, conditions modify effect probabilities

### Food Database (migrated from the original project)
- **8,400+ foods** across BLS 4.0 (German), Swiss naehrwertdaten.ch, Open Food Facts, Yazio, and manual entries
- **Source tracking** for every food, nutrient value, and effect
- **Biomarker effects** — foods document how they move blood values (Vitamin K, Iron, etc.)
- **Effect modifiers** — vitamin C enhances iron absorption, tannins inhibit, etc.
- **Portion system** — 28 predefined portions (scheibe, becher, gramm, flasche, ...)
- **RDI comparisons** — DGE / WHO / FDA based recommendations

### Patient Management
- **Temporal tracking**: Medication history, dose changes, conditions
- **YAML-based profiles**: Human-readable, version-controlled patient data
- **Vitals tracking**: Blood pressure, weight trends over time
- **Lab file integration**: Link blood tests to patient profiles

### Smart Analysis
- **Context-aware interpretation**: Explains if abnormal values are medication- or food-related
- **Clinical explanations**: Mechanisms, probabilities, and recommendations
- **Source attribution**: Every clinical claim backed by references
- **Monitoring alerts**: Suggests when to recheck values

## Installation

```bash
pip install -e .
```

For development:
```bash
pip install -e ".[dev]"
```

## Quick Start

### 1. Look Up a Biomarker

```python
from core import get_biomarker

crp = get_biomarker("CRP")
print(f"Name: {crp.name}")
print(f"German: {crp.name_de}")  # C-reaktives Protein
print(f"Normal range: {crp.get_range_for_unit('mg/l')}")
```

### 2. Analyze a Blood Test with Medication Context

```python
from core.patients.loader import load_patient
from core.medications import MedicationAnalyzer

patient = load_patient('p001')
meds = patient.get_current_medications()

analyzer = MedicationAnalyzer()
analysis = analyzer.analyze_biomarker(
    biomarker_name="Potassium",
    value=3.31,
    unit="mmol/L",
    reference_range=(3.5, 5.0),
    patient_medications=meds,
    patient_data={'age': 57, 'gender': 'male'}
)

print(analysis.explanation)
# Shows: Patient is taking Bendroflumethiazide (Xipamid) 2.5mg
# The low potassium is EXPECTED with this medication (20% probability)
```

### 3. Search Medications Affecting a Biomarker

```python
from core.medications import get_database as med_db

db = med_db()
potassium_drugs = db.get_affecting_biomarker("Potassium")
for drug in potassium_drugs:
    effect = drug.get_effects_on_target('Potassium')[0]
    print(f"{drug.name}: {effect.direction.value}")
```

### 4. Analyze Food Intake Against a Biomarker

```python
from core.foods import FoodDatabase, FoodAnalyzer, FoodIntake
from datetime import datetime

db = FoodDatabase()
db.load_all()

analyzer = FoodAnalyzer()
intakes = [
    FoodIntake(db.get("Spinach"), 100, datetime.now()),
    FoodIntake(db.get("Banane"), 150, datetime.now()),
]
result = analyzer.analyze_biomarker("Vitamin K", intakes)
print(result.net_effect)  # "increase"
```

### 5. Load Historical Blood Test Data

```python
from core import load_blood_tests

history = load_blood_tests("blutbild.csv")
timeline = history.get_timeline("Cholesterin")

for date, value in timeline:
    print(f"{date}: {value} mg/dL")
```

## Project Structure

```
n-1/
├── core/             # Main Python package (the n=1 core)
│   ├── bloodtests/        # Biomarker database and CSV import/export
│   ├── medications/       # Medication database and analysis engine
│   ├── foods/             # 8,400+ foods, importers, RDI, analysis
│   ├── activities/        # Exercise sessions and effects
│   ├── patients/          # YAML patient profiles
│   ├── diary/             # Daily intake / activity logs
│   ├── goals/             # Health goals
│   ├── reports/           # Report generation
│   ├── correlation/       # Cross-domain correlation analysis
│   └── data/              # Patient, lab, intake data
├── archive/
│   └── food_legacy/       # Verbatim snapshot of the original
│                          #   Food-and-Nutrition project (preserved
│                          #   for reference; fully migrated)
├── tests/                 # Test suite
├── data/                  # Raw data files
├── patients/              # Patient YAML files
├── setup.py
└── README.md
```

## Medication Database

### Prescription Medications

| Medication | Class | Key Effects |
|------------|-------|-------------|
| Bendroflumethiazide (Xipamid) | Thiazide diuretic | Decreases K+, Na+; increases Ca2+, glucose |
| Telmisartan | ARB | Increases K+, creatinine (expected); decreases BP |
| Rosuvastatin | Statin | Decreases LDL 45-63%, TG 20-30%; rare ALT elevation |
| Escitalopram | SSRI | Decreases Na+ (SIADH); bleeding risk; QT prolongation |

### Supplements

| Supplement | Key Effects | Interactions |
|------------|-------------|--------------|
| Omega-3 | Decreases TG 20-30%, mild INR increase | Warfarin |
| Vitamin D3 | Increases calcium, decreases PTH | Thiazides |
| Vitamin K2 | Affects coagulation | Warfarin (major) |
| Nattokinase | Fibrinolytic | Anticoagulants (major) |

## Example: Explaining an Abnormal Result

### Traditional Report
```
Potassium: 3.31 mmol/L (LOW)
Reference: 3.5 - 5.0
```

### With n-1 Context
```
Potassium: 3.31 mmol/L (LOW)
Reference: 3.5 - 5.0

MEDICATION ANALYSIS:
EXPLAINED by Bendroflumethiazide (Xipamid) 2.5mg daily
Expected effect probability: 20%

Mechanism: Thiazide stimulates aldosterone leading to 
increased K+ secretion in distal tubule

Patient risk factors: Age 57, dose 2.5mg, no additional risks

Sources: PMID 16960154, FDA Label

RECOMMENDATION:
- This is an EXPECTED medication effect
- Consistent with patient's Xipamid therapy
- Recheck potassium in 2-4 weeks
- Consider dietary K+ increase or supplementation
- Discuss with physician if persistent below 3.5 mmol/L
```

## Data Sources

### Medical
- FDA Prescribing Information
- Clinical practice guidelines (ESC, ADA, KDIGO, etc.)
- Peer-reviewed research (PubMed)
- Medical laboratory references
- DocCheck medical lexicon

### Food (migrated from the original project)
- **BLS 4.0** — German Federal Food Key (Bundeslebensmittelschlüssel), 7,140 foods
- **naehrwertdaten.ch** — Swiss Federal Food Safety database, ~1,000 foods
- **Open Food Facts** — Crowdsourced global database
- **Yazio** — Nutrition tracking platform data
- **FooDB** — Bioactive compound enrichment
- **USDA FoodData Central** — Manual entries
- **FDDB.info** — Text parser (port from original project)
- **Nutritionix** — Natural language API (port from original project)

## Lineage

This project is the direct successor of **`Food-and-Nutrition`**, the original
n=1 project. Everything from the old project has been preserved:

- All food data, importers, portion system, and RDI logic migrated to
  `core/foods/`
- The original source tree is preserved verbatim in `archive/food_legacy/` for
  reference
- See `MIGRATION.md` and `MIGRATION_COMPLETE.md` for the full migration record

The rebrand to **N=1** reflects the broader scope: blood biomarkers, medications,
activities, and patient profiles, all joined by the same n-of-1 discipline.

## License

MIT License

## Disclaimer

This library is for informational purposes only and should not be used as a substitute for professional medical advice. Always consult with healthcare providers for interpretation of blood test results.
