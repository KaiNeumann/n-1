#!/usr/bin/env python3
"""
Analyze latest blood test results against the biomarker database with patient-specific data
"""

import csv
import sys
from datetime import datetime
from collections import defaultdict

# Add blutwerte to path
sys.path.insert(0, 'D:\\Personal Data\\Kai Uwe\\Documents\\Kai\\projects\\Blutwerte')

from blutwerte.bloodtests import BiomarkerDatabase
from blutwerte.bloodtests import Category

def parse_value(val):
    """Parse a numeric value from CSV"""
    if not val or val.strip() == '':
        return None
    try:
        return float(val.replace(',', '.'))
    except:
        return None

def get_latest_results(csv_path):
    """Extract the latest blood test results from CSV"""
    results = {}
    dates = []
    latest_date = None
    latest_col = None
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        
        # Find all date columns (from column 4 onwards)
        for i, h in enumerate(headers[4:], start=4):
            if h and h.strip():
                try:
                    dates.append((i, datetime.strptime(h.strip(), '%Y-%m-%d')))
                except:
                    pass
        
        # Get the latest date
        if dates:
            latest_col = max(dates, key=lambda x: x[1])[0]
            latest_date = max(dates, key=lambda x: x[1])[1]
            
            # Read all rows
            for row in reader:
                if latest_col is not None and len(row) > latest_col:
                    name = row[0]  # German name
                    lab_id = row[1]  # Lab ID
                    unit = row[2]
                    normal_range = row[3]
                    value = parse_value(row[latest_col])
                    
                    if value is not None:
                        results[name] = {
                            'lab_id': lab_id,
                            'unit': unit,
                            'normal_range': normal_range,
                            'value': value
                        }
    
    return results, latest_date

def get_all_matching_ranges(biomarker, unit, patient_data):
    """Get all reference ranges that match the patient profile"""
    if unit not in biomarker.ranges:
        return []
    
    matching = []
    for r in biomarker.ranges[unit]:
        # Check if conditions match
        if r.conditions:
            matches = True
            if r.conditions.gender and patient_data.get('gender'):
                if r.conditions.gender != patient_data['gender']:
                    continue
            if r.conditions.age_min and patient_data.get('age'):
                if patient_data['age'] < r.conditions.age_min:
                    continue
            if r.conditions.age_max and patient_data.get('age'):
                if patient_data['age'] > r.conditions.age_max:
                    continue
            matching.append(r)
        else:
            matching.append(r)
    
    return matching

def analyze_results(results, patient_data, db):
    """Analyze results against the database"""
    analysis = []
    
    for name, data in results.items():
        value = data['value']
        unit = data['unit']
        lab_id = data['lab_id']
        
        # Try to find the biomarker
        biomarker = db.get(name) or db.get(lab_id)
        
        if biomarker:
            # Get all matching ranges for this patient
            ranges = get_all_matching_ranges(biomarker, unit, patient_data)
            
            # Find normal range
            normal_range = None
            optimal_range = None
            
            for r in ranges:
                if 'normal' in r.label.lower():
                    normal_range = r
                elif 'optimal' in r.label.lower():
                    optimal_range = r
            
            # If no normal range, take first available
            if not normal_range and ranges:
                normal_range = ranges[0]
            
            # Determine status
            status = 'normal'
            in_normal = True
            in_optimal = True
            
            if normal_range:
                min_val, max_val = normal_range.get_range(patient_data)
                if min_val is not None and value < min_val:
                    status = 'low'
                    in_normal = False
                elif max_val is not None and value > max_val:
                    status = 'high'
                    in_normal = False
            
            if optimal_range:
                min_opt, max_opt = optimal_range.get_range(patient_data)
                if min_opt is not None and value < min_opt:
                    in_optimal = False
                elif max_opt is not None and value > max_opt:
                    in_optimal = False
            
            is_outside = not in_normal or (optimal_range and not in_optimal and in_normal)
            
            # Get normal range text
            normal_range_text = data['normal_range']
            if normal_range:
                min_val, max_val = normal_range.get_range(patient_data)
                if min_val and max_val:
                    normal_range_text = f"{min_val} - {max_val}"
                elif max_val:
                    normal_range_text = f"< {max_val}"
                elif min_val:
                    normal_range_text = f"> {min_val}"
            
            # Get optimal range text
            optimal_range_text = None
            if optimal_range:
                min_opt, max_opt = optimal_range.get_range(patient_data)
                if min_opt and max_opt:
                    optimal_range_text = f"{min_opt} - {max_opt}"
                elif max_opt:
                    optimal_range_text = f"< {max_opt}"
                elif min_opt:
                    optimal_range_text = f"> {min_opt}"
            
            # Get sources
            sources = []
            if normal_range and normal_range.remarks:
                for quote in normal_range.remarks[:2]:
                    if quote.source and quote.source not in sources:
                        sources.append(quote.source)
            if optimal_range and optimal_range.remarks:
                for quote in optimal_range.remarks[:2]:
                    if quote.source and quote.source not in sources:
                        sources.append(quote.source)
            
            # Get interpretation
            interpretation = []
            if status == 'low' and biomarker.interpretation.low:
                interpretation = biomarker.interpretation.low[:2]
            elif status == 'high' and biomarker.interpretation.high:
                interpretation = biomarker.interpretation.high[:2]
            
            analysis.append({
                'name': biomarker.name,
                'name_de': biomarker.name_de or name,
                'value': value,
                'unit': unit,
                'normal_range': normal_range_text,
                'optimal_range': optimal_range_text,
                'in_normal': in_normal,
                'in_optimal': in_optimal,
                'status': status,
                'is_outside': is_outside,
                'interpretation': interpretation,
                'sources': sources,
                'categories': biomarker.categories,
                'organs': biomarker.organs
            })
        else:
            # No database entry, just record the value
            analysis.append({
                'name': name,
                'name_de': name,
                'value': value,
                'unit': unit,
                'normal_range': data['normal_range'],
                'optimal_range': None,
                'in_normal': True,
                'in_optimal': None,
                'status': 'unknown',
                'is_outside': False,
                'interpretation': [],
                'sources': [],
                'categories': [],
                'organs': []
            })
    
    return analysis

def generate_report(analysis, latest_date, patient_data):
    """Generate a structured markdown report"""
    report = []
    report.append(f"# Blood Test Analysis Report")
    report.append(f"")
    report.append(f"**Test Date:** {latest_date.strftime('%Y-%m-%d')}")
    report.append(f"")
    report.append(f"## Patient Information")
    report.append(f"")
    report.append(f"- **Gender:** {patient_data['gender'].capitalize()}")
    report.append(f"- **Age:** {patient_data['age']} years")
    report.append(f"- **Height:** {patient_data['height']} cm")
    report.append(f"- **Weight:** {patient_data['weight']} kg")
    report.append(f"- **BMI:** {patient_data['weight'] / (patient_data['height']/100)**2:.1f} kg/m²")
    report.append(f"- **Smoking Status:** Former smoker (quit {patient_data['smoking_quit_years']} years ago)")
    report.append(f"")
    
    # Sort by status (outside first) then by name
    outside = [a for a in analysis if a['is_outside']]
    normal = [a for a in analysis if not a['is_outside'] and a['status'] != 'unknown']
    unknown = [a for a in analysis if a['status'] == 'unknown']
    
    # Summary
    report.append(f"## Summary")
    report.append(f"")
    report.append(f"- **Values outside normal/optimal range:** {len(outside)}")
    report.append(f"- **Values within normal range:** {len(normal)}")
    report.append(f"- **Values without database reference:** {len(unknown)}")
    report.append(f"")
    
    # Critical values outside range
    if outside:
        report.append(f"## ⚠️ Values Outside Reference Range")
        report.append(f"")
        
        for item in sorted(outside, key=lambda x: x['name']):
            status_emoji = "🔴" if item['status'] == 'high' else "🔵"
            report.append(f"### {status_emoji} {item['name_de']} ({item['name']})")
            report.append(f"")
            report.append(f"| Metric | Value |")
            report.append(f"|--------|-------|")
            report.append(f"| **Result** | **{item['value']} {item['unit']}** |")
            
            # Show both normal and optimal ranges with sources
            if item['normal_range']:
                report.append(f"| **Normal Range** | {item['normal_range']} |")
            if item['optimal_range']:
                report.append(f"| **Optimal Range** | {item['optimal_range']} |")
            
            status_text = item['status'].upper()
            if not item['in_normal']:
                status_text += " (Outside Normal)"
            elif item['optimal_range'] and not item['in_optimal']:
                status_text += " (Normal but Suboptimal)"
            
            report.append(f"| **Status** | {status_text} |")
            report.append(f"")
            
            # Interpretation
            if item['interpretation']:
                report.append(f"**Clinical Significance:**")
                for quote in item['interpretation']:
                    report.append(f"- {quote.text}")
                report.append(f"")
            
            # Sources
            if item['sources']:
                report.append(f"**Sources:**")
                for src in item['sources']:
                    report.append(f"- {src}")
                report.append(f"")
            
            report.append(f"---")
            report.append(f"")
    
    # Normal values
    report.append(f"## ✅ Values Within Normal/Optimal Range")
    report.append(f"")
    
    # Group by category
    by_category = defaultdict(list)
    for item in normal:
        cat_name = item['categories'][0].value if item['categories'] else 'other'
        by_category[cat_name].append(item)
    
    for category, items in sorted(by_category.items()):
        report.append(f"### {category.replace('_', ' ').title()}")
        report.append(f"")
        report.append(f"| Test | Result | Unit | Normal | Optimal |")
        report.append(f"|------|--------|------|--------|---------|")
        for item in sorted(items, key=lambda x: x['name']):
            optimal_str = item['optimal_range'] if item['optimal_range'] else '-'
            report.append(f"| {item['name_de']} | {item['value']} | {item['unit']} | {item['normal_range']} | {optimal_str} |")
        report.append(f"")
    
    # Unknown values
    if unknown:
        report.append(f"## 📋 Additional Tests (No Database Reference)")
        report.append(f"")
        report.append(f"| Test | Result | Unit | Lab Reference |")
        report.append(f"|------|--------|------|---------------|")
        for item in sorted(unknown, key=lambda x: x['name']):
            report.append(f"| {item['name_de']} | {item['value']} | {item['unit']} | {item['normal_range']} |")
        report.append(f"")
    
    report.append(f"---")
    report.append(f"")
    report.append(f"*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    report.append(f"")
    report.append(f"**Disclaimer:** This report is for informational purposes only and should not replace professional medical advice. Please consult with your healthcare provider for proper interpretation and clinical decision-making.")
    
    return '\n'.join(report)

def main():
    # Patient data
    patient_data = {
        'gender': 'male',
        'age': 56,
        'height': 180,
        'weight': 88,
        'smoking_quit_years': 26
    }
    
    # Initialize database
    db = BiomarkerDatabase()
    
    # Get latest results
    csv_path = 'blutbild.csv'
    results, latest_date = get_latest_results(csv_path)
    
    if latest_date is None:
        print("Error: No valid dates found in CSV")
        return
    
    print(f"Analyzing results from {latest_date.strftime('%Y-%m-%d')}")
    print(f"Patient: Male, 56 years old, 180cm, 88kg, BMI {patient_data['weight'] / (patient_data['height']/100)**2:.1f}")
    print(f"Found {len(results)} test results")
    print()
    
    # Analyze results
    analysis = analyze_results(results, patient_data, db)
    
    # Generate report
    report = generate_report(analysis, latest_date, patient_data)
    
    # Write report
    with open('blood_test_report_patient.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("Report saved to blood_test_report_patient.md")
    
    # Also print summary to console
    outside = [a for a in analysis if a['is_outside']]
    print(f"\n=== SUMMARY ===")
    print(f"Values outside reference range: {len(outside)}")
    for item in outside:
        status_detail = ""
        if not item['in_normal']:
            status_detail = " [OUTSIDE NORMAL]"
        elif not item['in_optimal']:
            status_detail = " [Normal but Suboptimal]"
        print(f"  - {item['name_de']}: {item['value']} {item['unit']} ({item['status']}){status_detail}")

if __name__ == '__main__':
    main()
