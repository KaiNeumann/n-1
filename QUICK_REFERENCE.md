# Quick Reference Guide - N=1 Biomarkers

## 🚀 Quick Start

```python
from blutwerte import get_biomarker, search_biomarkers, list_biomarkers

# Get biomarker information
crp = get_biomarker("CRP")
print(crp.ranges["mg/l"])  # Access ranges in specific unit

# Search by partial name
results = search_biomarkers("troponin")

# List all biomarkers
all_names = list_biomarkers()
```

---

## 📊 Database Overview

- **90 biomarkers** verified
- **590 reference ranges**
- **35+ authoritative sources**
- **100% complete**

---

## 🔍 Most Common Biomarkers

### Diabetes (ADA 2024)
| Biomarker | Normal | Prediabetes | Diabetes |
|-----------|---------|-------------|----------|
| **Glucose (fasting)** | <100 mg/dL | 100-125 | ≥126 |
| **HbA1c** | <5.7% | 5.7-6.4% | ≥6.5% |
| **Glucose (random)** | <140 | 140-199 | ≥200 |

### Lipids (ESC/EAS 2019)
| Biomarker | Optimal | Borderline | High | Very High |
|-----------|---------|------------|------|-----------|
| **LDL** | <100 | 100-129 | 130-159 | ≥160 |
| **HDL (M/F)** | >60/>60 | 40-60/50-60 | <40/<50 | - |
| **Triglycerides** | <150 | 150-199 | 200-499 | ≥500 |

### Thyroid (ATA 2020)
| Biomarker | Normal | Subclinical | Overt |
|-----------|---------|-------------|-------|
| **TSH** | 0.5-4.0 | 4.0-10.0 | >10.0 |
| **FT4** | 0.8-1.8 | - | <0.8 or >1.8 |

### Kidney (KDIGO 2024)
| Biomarker | Normal | CKD Stage |
|-----------|---------|-----------|
| **eGFR** | >90 | G3a: 45-59, G3b: 30-44, G4: 15-29, G5: <15 |
| **Creatinine** | M: 0.7-1.3, F: 0.6-1.1 | Elevated in CKD |
| **UACR** | <30 | 30-300: Micro, >300: Macro |

### Cardiac (ESC 2023)
| Biomarker | Normal | Elevated | MI Suspected |
|-----------|---------|----------|--------------|
| **Troponin I** | <26 ng/L | 26-52 | >52 |
| **Troponin T** | <14 ng/L | 14-52 | >52 |
| **NT-proBNP** | <125 | 125-450 | >450 |

### CBC (NHS/Mayo)
| Biomarker | Normal (Male) | Normal (Female) |
|-----------|---------------|-----------------|
| **Hemoglobin** | 13.5-17.5 | 12.0-16.0 |
| **WBC** | 4.5-11.0 | 4.5-11.0 |
| **Platelets** | 150-400 | 150-400 |

### Electrolytes (Critical Values)
| Biomarker | Normal | Critical Low | Critical High |
|-----------|---------|--------------|---------------|
| **Sodium** | 135-145 | <120 or >160 | <115 or >165 |
| **Potassium** | 3.5-5.0 | <2.5 or >6.5 | <2.0 or >7.0 |
| **Calcium** | 8.5-10.5 | <7.0 or >13 | <6.5 or >14 |

---

## 📋 Biomarkers by Category

### 🩺 Critical (Emergency)
- Troponin I/T (MI)
- D-Dimer (VTE)
- Potassium (arrhythmia)
- Sodium (seizures)
- Calcium (tetany)
- Glucose (coma)

### 🔬 Routine Screening
- CBC (complete blood count)
- CMP (comprehensive metabolic panel)
- Lipid panel
- HbA1c
- TSH

### 🎯 Disease Monitoring
- **Diabetes**: Glucose, HbA1c, UACR
- **CKD**: Creatinine, eGFR, UACR, Cystatin C
- **Heart Failure**: NT-proBNP, Troponin
- **Liver Disease**: ALT, AST, Bilirubin, Albumin
- **Inflammation**: CRP, ESR

### 🧬 Specialized
- **Immunology**: IgA, IgG, IgM, IgE
- **Tumor Markers**: CEA, CA 19-9, PSA
- **Coagulation**: INR, PTT, D-Dimer
- **Vitamins**: B12, D, B6, Folate

---

## 🔬 Common Test Panels

### Basic Metabolic Panel
- Glucose, Calcium
- Sodium, Potassium, CO2, Chloride
- BUN (Urea), Creatinine

### Comprehensive Metabolic Panel
- BMP + Albumin, Total Protein
- ALP, ALT, AST, Bilirubin

### Lipid Panel
- Total Cholesterol
- HDL, LDL
- Triglycerides

### Liver Function Tests
- ALT, AST, ALP, GGT
- Bilirubin (Total, Direct)
- Albumin, Total Protein

### Cardiac Markers
- Troponin I or T
- CK-MB (optional)
- NT-proBNP (heart failure)
- D-Dimer (VTE)

### Iron Panel
- Serum Iron
- Ferritin
- TIBC or Transferrin
- Transferrin Saturation

---

## 💡 Clinical Tips

### Always Check:
1. **Units** - mg/dL vs mmol/L
2. **Reference range** - Lab-specific variations
3. **Age/Gender** - Pediatric, elderly, pregnancy
4. **Clinical context** - Symptoms, medications
5. **Trends** - Single value vs. serial testing

### Critical Values Require:
- Immediate physician notification
- Repeat testing
- Clinical correlation
- Potential intervention

### Common Confounders:
- **Hemolysis**: False ↑ K+, LDH
- **Lipemia**: Interferes with many tests
- **Medications**: Statins affect LFTs, Diuretics affect electrolytes
- **Recent meals**: Affects glucose, triglycerides

---

## 📚 Quick Lookup Tables

### Unit Conversions
| From | To | Multiply by |
|------|-----|-------------|
| mg/dL glucose | mmol/L | 0.0555 |
| mg/dL creatinine | µmol/L | 88.4 |
| mg/dL urea | mmol/L | 0.357 |
| mg/dL calcium | mmol/L | 0.25 |
| g/dL albumin | g/L | 10 |

### SI Prefixes
- **milli (m)**: 10⁻³
- **micro (µ)**: 10⁻⁶
- **nano (n)**: 10⁻⁹
- **pico (p)**: 10⁻¹²

---

## 🔗 Additional Resources

- Full Documentation: [README.md](README.md)
- Verification Report: [VERIFICATION_REPORT.md](VERIFICATION_REPORT.md)
- Medical Sources: [MEDICAL_SOURCES.md](MEDICAL_SOURCES.md)
- API Reference: Python docstrings in `blutwerte/` directory

---

**Version**: 1.0  
**Last Updated**: February 2025  
**Status**: ✅ 100% Verified
