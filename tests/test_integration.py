#!/usr/bin/env python3
"""
Integration test: Complete medication-aware blood test analysis.

Demonstrates:
1. Loading patient from YAML
2. Loading blood test results
3. Analyzing each biomarker against patient's medications
4. Generating explanation for abnormal values
5. Creating comprehensive report
"""

import sys
sys.path.insert(0, 'D:\\Personal Data\\Kai Uwe\\Documents\\Kai\\projects\\core')

from datetime import date
from core.patients.loader import load_patient
from core.medications import MedicationAnalyzer, get_database


def test_integration():
    """Test complete integration workflow."""
    print("=" * 70)
    print("MEDICATION-AWARE BLOOD TEST ANALYSIS - INTEGRATION TEST")
    print("=" * 70)
    
    # Step 1: Load patient
    print("\n[1] Loading patient profile...")
    patient = load_patient('p001', 'patients')
    print(f"  Patient: {patient.name} (ID: {patient.patient_id})")
    print(f"  Age: {patient.get_current_age()} years, Gender: {patient.gender}")
    
    # Step 2: Get current medications
    print("\n[2] Current medications:")
    current_meds = patient.get_current_medications()
    for med in current_meds:
        print(f"  - {med.medication_name} {med.dosage}{med.dosage_unit}")
    print(f"  Total: {len(current_meds)} medications")
    
    # Step 3: Prepare patient data for analysis
    print("\n[3] Preparing analysis...")
    patient_data = patient.get_patient_data_for_date(date.today())
    print(f"  Age for analysis: {patient_data['age']}")
    print(f"  Conditions: {', '.join(patient_data['conditions'])}")
    
    # Step 4: Define blood test results (from p001's latest blood test)
    print("\n[4] Blood test results to analyze:")
    blood_test_results = {
        'Potassium': {
            'value': 3.31,
            'unit': 'mmol/L',
            'reference': (3.5, 5.0)
        },
        'Sodium': {
            'value': 141.0,
            'unit': 'mmol/L',
            'reference': (136, 145)
        },
        'Creatinine': {
            'value': 0.86,
            'unit': 'mg/dL',
            'reference': (0.67, 1.17)
        },
        'LDL Cholesterol': {
            'value': 99.0,
            'unit': 'mg/dL',
            'reference': (0, 100)  # Optimal <100
        },
        'HDL Cholesterol': {
            'value': 38.9,
            'unit': 'mg/dL',
            'reference': (40, 60)  # >40 for males
        },
        'Triglycerides': {
            'value': 122.0,
            'unit': 'mg/dL',
            'reference': (0, 150)
        },
        'Glucose': {
            'value': 82.9,
            'unit': 'mg/dL',
            'reference': (70, 100)
        },
        'HbA1c': {
            'value': 5.0,
            'unit': '%',
            'reference': (0, 5.7)
        }
    }
    
    for biomarker, data in blood_test_results.items():
        ref_text = f"{data['reference'][0]}-{data['reference'][1]}"
        status = ""
        if data['value'] < data['reference'][0]:
            status = "LOW"
        elif data['value'] > data['reference'][1]:
            status = "HIGH"
        else:
            status = "NORMAL"
        print(f"  {biomarker:20s}: {data['value']:6.2f} {data['unit']:8s} (Ref: {ref_text:10s}) [{status}]")
    
    # Step 5: Analyze with medication effects
    print("\n[5] Analyzing with medication effects...")
    analyzer = MedicationAnalyzer()
    
    abnormal_results = []
    
    for biomarker, data in blood_test_results.items():
        analyses = analyzer.analyze_biomarker(
            biomarker_name=biomarker,
            value=data['value'],
            unit=data['unit'],
            reference_range=data['reference'],
            patient_medications=current_meds,
            patient_data=patient_data
        )
        
        if analyses:
            # Check if any medication explains the abnormality
            for analysis in analyses:
                if analysis.is_expected:
                    abnormal_results.append({
                        'biomarker': biomarker,
                        'value': data['value'],
                        'analysis': analysis
                    })
                    break
    
    # Step 6: Report results
    print("\n[6] MEDICATION ANALYSIS RESULTS:")
    print("-" * 70)
    
    if abnormal_results:
        print(f"\nFound {len(abnormal_results)} abnormal values explained by medications:\n")
        
        for result in abnormal_results:
            bio = result['biomarker']
            val = result['value']
            analysis = result['analysis']
            
            print(f"BIOMARKER: {bio}")
            print(f"Value: {val} {analysis.unit}")
            print(f"Status: {analysis.result.value.upper()}")
            print(f"Explained by: {analysis.medication}")
            print(f"Patient-specific probability: {analysis.patient_probability:.0f}%")
            print(f"\nClinical Explanation:")
            for line in analysis.explanation.split('\n')[:10]:  # First 10 lines
                if line.strip():
                    print(f"  {line}")
            
            if analysis.requires_monitoring:
                print(f"\nMonitoring Recommendation:")
                print(f"  {analysis.recommendation}")
            
            if analysis.sources:
                print(f"\nSources:")
                for source in analysis.sources[:2]:
                    print(f"  - {source}")
            
            print("-" * 70)
    else:
        print("\nNo medication-related abnormalities detected.")
    
    # Step 7: Summary statistics
    print("\n[7] SUMMARY:")
    print(f"  Total biomarkers analyzed: {len(blood_test_results)}")
    print(f"  Abnormal values found: {len([r for r in blood_test_results.values() if r['value'] < r['reference'][0] or r['value'] > r['reference'][1]])}")
    print(f"  Explained by medications: {len(abnormal_results)}")
    print(f"  Medications assessed: {len(current_meds)}")
    
    # Step 8: Generate medication summary
    print("\n[8] PATIENT MEDICATION SUMMARY:")
    print("-" * 70)
    summary = analyzer.generate_medication_summary(current_meds, patient_data)
    
    print(f"Total medications: {summary['total_medications']}")
    print(f"Medications with documented effects: {summary['medications_with_effects']}")
    print(f"Unique biomarkers affected: {len(summary['biomarkers_affected'])}")
    
    if summary['requires_monitoring']:
        print(f"\nMonitoring required for:")
        for item in summary['requires_monitoring'][:5]:
            print(f"  - {item['medication']}: {item['biomarker']}")
    
    if summary['drug_interactions']:
        print(f"\nDrug interactions identified: {len(summary['drug_interactions'])}")
        for interaction in summary['drug_interactions']:
            print(f"  - {interaction['drug1']} + {interaction['drug2']}: {interaction['severity']}")
    
    print("\n" + "=" * 70)
    print("INTEGRATION TEST COMPLETED SUCCESSFULLY!")
    print("=" * 70)


if __name__ == "__main__":
    try:
        test_integration()
    except Exception as e:
        print(f"\n[ERROR] Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
