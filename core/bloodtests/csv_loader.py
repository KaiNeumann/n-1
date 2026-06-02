"""
CSV loader for importing historical blood test data
"""

import csv
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class BloodTestRecord:
    """A single blood test measurement"""
    
    def __init__(self, biomarker_name: str, lab_id: str, unit: str, 
                 value: float, date: datetime, reference_range: Optional[str] = None):
        self.biomarker_name = biomarker_name
        self.lab_id = lab_id
        self.unit = unit
        self.value = value
        self.date = date
        self.reference_range = reference_range
    
    def __repr__(self):
        return f"BloodTestRecord({self.biomarker_name}: {self.value} {self.unit} on {self.date.date()})"


class BloodTestHistory:
    """History of blood tests from CSV file"""
    
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.records: List[BloodTestRecord] = []
        self.dates: List[datetime] = []
        self._load_csv()
    
    def _parse_range(self, range_str: str) -> Optional[Tuple[Optional[float], Optional[float]]]:
        """Parse a range string like '28.0 - 100' or '< 0.20'"""
        if not range_str or range_str == 'o.p.B.':
            return None
        
        range_str = range_str.strip()
        
        # Handle "< X" format
        if range_str.startswith('<'):
            try:
                max_val = float(range_str.replace('<', '').strip())
                return (None, max_val)
            except:
                return None
        
        # Handle "X - Y" format
        if '-' in range_str:
            parts = range_str.split('-')
            if len(parts) == 2:
                try:
                    min_val = float(parts[0].strip())
                    max_val = float(parts[1].strip())
                    return (min_val, max_val)
                except:
                    return None
        
        # Handle "ab X" format (greater than)
        if range_str.startswith('ab'):
            try:
                min_val = float(range_str.replace('ab', '').strip())
                return (min_val, None)
            except:
                return None
        
        return None
    
    def _load_csv(self):
        """Load and parse the CSV file"""
        with open(self.filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # Strip whitespace from fieldnames; many lab CSVs use ", "
            # separators, which leaves spaces embedded in the header keys.
            reader.fieldnames = [name.strip() for name in (reader.fieldnames or [])]

            # Get date columns (everything after 'Normalwert')
            fieldnames = reader.fieldnames or []
            date_columns = []
            found_normal = False

            for col in fieldnames:
                if found_normal:
                    try:
                        # Parse date from column name
                        date = datetime.strptime(col, '%Y-%m-%d')
                        date_columns.append((col, date))
                    except:
                        pass
                if col == 'Normalwert':
                    found_normal = True

            self.dates = [d for _, d in date_columns]

            # Parse each row
            for row in reader:
                biomarker = row['Wert'].strip()
                lab_id = row['Laborident'].strip()
                unit = row['Einheit'].strip()
                ref_range = row['Normalwert'].strip()
                
                # Parse each date column
                for col_name, date in date_columns:
                    value_str = row[col_name]
                    if value_str and value_str.strip():
                        try:
                            # Handle different number formats
                            value_str = value_str.replace(',', '.')
                            value = float(value_str)
                            
                            record = BloodTestRecord(
                                biomarker_name=biomarker,
                                lab_id=lab_id,
                                unit=unit,
                                value=value,
                                date=date,
                                reference_range=ref_range
                            )
                            self.records.append(record)
                        except ValueError:
                            # Skip non-numeric values
                            pass
    
    def get_records_for_biomarker(self, name: str) -> List[BloodTestRecord]:
        """Get all records for a specific biomarker"""
        return [r for r in self.records if r.biomarker_name.lower() == name.lower()]
    
    def get_records_for_date(self, date: datetime) -> List[BloodTestRecord]:
        """Get all records for a specific date"""
        return [r for r in self.records if r.date.date() == date.date()]
    
    def get_latest_value(self, biomarker_name: str) -> Optional[BloodTestRecord]:
        """Get the most recent measurement for a biomarker"""
        records = self.get_records_for_biomarker(biomarker_name)
        if not records:
            return None
        return max(records, key=lambda r: r.date)
    
    def get_value_at_date(self, biomarker_name: str, date: datetime) -> Optional[BloodTestRecord]:
        """Get the value for a biomarker at a specific date"""
        records = self.get_records_for_biomarker(biomarker_name)
        for r in records:
            if r.date.date() == date.date():
                return r
        return None
    
    def list_biomarkers(self) -> List[str]:
        """List all unique biomarker names in the history"""
        return sorted(set(r.biomarker_name for r in self.records))
    
    def list_dates(self) -> List[datetime]:
        """List all dates with measurements"""
        return sorted(set(r.date for r in self.records))
    
    def get_timeline(self, biomarker_name: str) -> List[Tuple[datetime, float]]:
        """Get timeline of values for a biomarker"""
        records = self.get_records_for_biomarker(biomarker_name)
        return [(r.date, r.value) for r in sorted(records, key=lambda x: x.date)]


def load_blood_tests(filepath: str) -> BloodTestHistory:
    """Load blood test history from CSV file"""
    return BloodTestHistory(filepath)
