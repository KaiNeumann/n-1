#!/usr/bin/env python3
"""
Test script for medication database and analysis engine.

Demonstrates analyzing a blood test result (low potassium) in the context
of the patient's Xipamid medication.
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from datetime import date
from core.medications import (
    get_database,
    MedicationAnalyzer,
    PatientMedication,
    PatientProfile
)


def test_basic_lookup():
    """Test basic medication lookup"""
    print("=" * 60)
    print("TEST 1: Basic Medication Lookup")
    print("=" * 60)
    
    db = get_database()
    print(f"\nDatabase contains {db.count()} medications")
    
    # Test various lookups
    lookups = ["Xipamid", "Bendroflumethiazide", "ATC:C03AA01"]
    for lookup in lookups:
        med = db.get(lookup)
        if med:
            print(f"[OK] Found by '{lookup}': {med.name}")
        else:
            print(f"[FAIL] Not found: {lookup}")
    
    # Test reverse lookup
    print("\nReverse lookup - drugs affecting Potassium:")
    k_drugs = db.get_affecting_biomarker("Potassium")
    for drug in k_drugs:
        print(f"  - {drug.name}")


def test_xipamid_details():
    """Test detailed Xipamid information"""
    print("\n" + "=" * 60)
    print("TEST 2: Xipamid (Bendroflumethiazide) Details")
    print("=" * 60)
    
    db = get_database()
    xipamid = db.get("Xipamid")
    
    if not xipamid:
        print("[ERROR] Xipamid not found in database")
        return
    
    print(f"\nMedication: {xipamid.name}")
    print(f"German Name: {xipamid.name_de}")
    print(f"Brand Names: {', '.join(xipamid.brand_names[:3])}")
    print(f"Drug Class: {xipamid.drug_class} ({xipamid.drug_subclass})")
    print(f"Available Doses: {[f'{d[0]}{d[1]}' for d in xipamid.available_doses]}")
    
    print(f"\nTotal Effects: {len(xipamid.effects)}")
    print("\nBiomarker Effects:")
    for effect in xipamid.get_biomarker_effects():
        print(f"  - {effect.target_name}: {effect.direction.value}")
        print(f"    Frequency: {effect.frequency_percentage}%")
        print(f"    Dose-dependent: {effect.dose_dependent}")
        if effect.dose_dependent and effect.dose_model:
            ranges = effect.dose_model.get_all_defined_ranges()
            for r in ranges:
                print(f"      {r.min_dose}-{r.max_dose}{r.dose_unit}: {r.frequency_percentage}%")


def test_potassium_analysis():
    """Test analyzing low potassium with Xipamid"""
    print("\n" + "=" * 60)
    print("TEST 3: Potassium Analysis - Patient Case")
    print("=" * 60)
    
    # Patient's actual data
    patient_med = PatientMedication(
        medication_name="Bendroflumethiazide",
        dosage=2.5,
        dosage_unit="mg",
        frequency="once_daily",
        administration_time="morning",
        start_date=date(2023, 3, 1),
        prescribed_for="hypertension"
    )
    
    patient_data = {
        'age': 56,
        'gender': 'male',
        'conditions': ['hypertension']
    }
    
    # Test result: Low potassium (3.31 mmol/L)
    analyzer = MedicationAnalyzer()
    
    analyses = analyzer.analyze_biomarker(
        biomarker_name="Potassium",
        value=3.31,
        unit="mmol/L",
        reference_range=(3.5, 5.0),
        patient_medications=[patient_med],
        patient_data=patient_data
    )
    
    print(f"\nAnalyzing Potassium: 3.31 mmol/L")
    print(f"Reference Range: 3.5 - 5.0 mmol/L")
    print(f"Status: LOW (below normal)")
    print(f"\nPatient Medications: Xipamid 2.5mg daily")
    print(f"Patient: Male, 56 years old")
    
    print("\n" + "-" * 60)
    print("ANALYSIS RESULTS:")
    print("-" * 60)
    
    for analysis in analyses:
        print(f"\nMedication: {analysis.medication}")
        print(f"Is Affected: {analysis.is_affected}")
        print(f"Is Expected: {analysis.is_expected}")
        print(f"Result: {analysis.result.value}")
        print(f"Base Probability: {analysis.probability:.1f}%")
        if analysis.patient_probability:
            print(f"Patient-Specific Probability: {analysis.patient_probability:.1f}%")
        print(f"Requires Monitoring: {analysis.requires_monitoring}")
        print(f"Urgency: {analysis.monitoring_urgency}")
        
        print("\nExplanation:")
        print(analysis.explanation)
        
        print("\nRecommendation:")
        print(analysis.recommendation)
        
        if analysis.sources:
            print("\nSources:")
            for source in analysis.sources:
                print(f"  - {source}")


def test_patient_profile():
    """Test patient profile creation"""
    print("\n" + "=" * 60)
    print("TEST 4: Patient Profile")
    print("=" * 60)
    
    patient = PatientProfile(
        patient_id="p001",
        name="Max Mustermann",
        gender="male",
        birth_date=date(1968, 5, 15)
    )
    
    print(f"\nPatient: {patient.name} (ID: {patient.patient_id})")
    print(f"Gender: {patient.gender}")
    print(f"Birth Date: {patient.birth_date}")
    print(f"Current Age: {patient.get_current_age()}")
    
    # Add medication
    from core.medications.models import TemporalValue
    
    xipamid = PatientMedication(
        medication_name="Bendroflumethiazide",
        dosage=2.5,
        dosage_unit="mg",
        frequency="once_daily",
        start_date=date(2023, 3, 1)
    )
    
    patient.medications.append(TemporalValue(
        value=xipamid,
        start_date=date(2023, 3, 1)
    ))
    
    print(f"\nCurrent Medications:")
    for med in patient.get_current_medications():
        print(f"  - {med.medication_name} {med.dosage}{med.dosage_unit}")
    
    # Get patient data for analysis
    data = patient.get_patient_data_for_date(date.today())
    print(f"\nPatient Data for Analysis:")
    print(f"  Age: {data['age']}")
    print(f"  Gender: {data['gender']}")
    print(f"  Medications: {len(data['medications'])}")


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("MEDICATION DATABASE TEST SUITE")
    print("=" * 60)
    
    try:
        test_basic_lookup()
        test_xipamid_details()
        test_potassium_analysis()
        test_patient_profile()
        
        print("\n" + "=" * 60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n[ERROR] TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
