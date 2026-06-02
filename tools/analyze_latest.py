#!/usr/bin/env python3
"""
Analyze latest blood test results against the biomarker database
"""

import csv
from datetime import datetime
from core.bloodtests import BiomarkerDatabase
from core.bloodtests import Category

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
            # Get interpretation
            interp = biomarker.interpret_value(value, unit, patient_data)
            range_obj = interp.get('range')
            
            status = interp['status']
            
            # Determine if outside normal/optimal
            is_outside = status in ['low', 'high']
            
            # Get normal range text
            normal_range_text = data['normal_range']
            if range_obj:
                min_val, max_val = range_obj.get_range(patient_data)
                if min_val and max_val:
                    normal_range_text = f"{min_val} - {max_val}"
                elif max_val:
                    normal_range_text = f"< {max_val}"
                elif min_val:
                    normal_range_text = f"> {min_val}"
            
            # Get sources
            sources = []
            if range_obj and range_obj.remarks:
                for quote in range_obj.remarks[:2]:
                    if quote.source and quote.source not in sources:
                        sources.append(quote.source)
            
            analysis.append({
                'name': biomarker.name,
                'name_de': biomarker.name_de or name,
                'value': value,
                'unit': unit,
                'normal_range': normal_range_text,
                'status': status,
                'is_outside': is_outside,
                'interpretation': interp.get('interpretation', []),
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
    report.append(f"- **Values outside reference range:** {len(outside)}")
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
            report.append(f"| **Reference Range** | {item['normal_range']} |")
            report.append(f"| **Status** | {item['status'].upper()} |")
            report.append(f"")
            
            # Interpretation
            if item['interpretation']:
                report.append(f"**Clinical Significance:**")
                for quote in item['interpretation'][:2]:
                    report.append(f"- {quote.text}")
                report.append(f"")
            
            # Sources
            if item['sources']:
                report.append(f"**Sources:**")
                for src in item['sources']:
                    report.append(f"- {src}")
                report.append(f"")
    
    # Normal values
    report.append(f"## ✅ Values Within Normal Range")
    report.append(f"")
    
    # Group by category
    from collections import defaultdict
    by_category = defaultdict(list)
    for item in normal:
        cat_name = item['categories'][0].value if item['categories'] else 'other'
        by_category[cat_name].append(item)
    
    for category, items in sorted(by_category.items()):
        report.append(f"### {category.replace('_', ' ').title()}")
        report.append(f"")
        report.append(f"| Test | Result | Unit | Reference |")
        report.append(f"|------|--------|------|----------|")
        for item in sorted(items, key=lambda x: x['name']):
            report.append(f"| {item['name_de']} | {item['value']} | {item['unit']} | {item['normal_range']} |")
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
    print(f"Found {len(results)} test results")
    print()
    
    # Analyze results
    analysis = analyze_results(results, patient_data, db)
    
    # Generate report
    report = generate_report(analysis, latest_date, patient_data)
    
    # Write report
    with open('blood_test_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("Report saved to blood_test_report.md")
    
    # Also print summary to console
    outside = [a for a in analysis if a['is_outside']]
    print(f"\n=== SUMMARY ===")
    print(f"Values outside reference range: {len(outside)}")
    for item in outside:
        print(f"  - {item['name_de']}: {item['value']} {item['unit']} ({item['status']})")

if __name__ == '__main__':
    main()
