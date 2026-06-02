"""
Patient data loader for YAML configuration files.

Handles loading and parsing of patient profiles from YAML files.
Supports temporal data, medication history, vitals tracking, and lab file references.
"""

import yaml
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

from ..medications.models import (
    PatientProfile, PatientMedication, VitalsSnapshot, 
    TemporalValue, Quote
)


class PatientLoader:
    """Load patient profiles from YAML files."""
    
    def __init__(self, patients_dir: str = "patients"):
        """
        Initialize loader.
        
        Args:
            patients_dir: Directory containing patient YAML files
        """
        self.patients_dir = Path(patients_dir)
        self.patients_dir.mkdir(parents=True, exist_ok=True)
    
    def load(self, patient_id: str) -> PatientProfile:
        """
        Load a patient profile from YAML file.
        
        Args:
            patient_id: Patient ID (e.g., "p001")
            
        Returns:
            PatientProfile object
            
        Raises:
            FileNotFoundError: If patient file doesn't exist
        """
        file_path = self.patients_dir / f"{patient_id}.yaml"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Patient file not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        return self._parse_patient_data(data)
    
    def _parse_patient_data(self, data: Dict[str, Any]) -> PatientProfile:
        """Parse YAML data into PatientProfile object."""
        # Basic patient info
        patient = PatientProfile(
            patient_id=data['patient_id'],
            name=data.get('name', ''),
            gender=data['gender'],
            birth_date=self._parse_date(data['birth_date'])
        )
        
        # Parse medications
        if 'medications' in data:
            patient.medications = [
                self._parse_temporal_med(med_data)
                for med_data in data['medications']
            ]
        
        # Parse conditions
        if 'conditions' in data:
            patient.conditions = [
                self._parse_temporal_condition(cond_data)
                for cond_data in data['conditions']
            ]
        
        # Parse vitals
        if 'vitals' in data:
            patient.vitals = [
                self._parse_vitals(vital_data)
                for vital_data in data['vitals']
            ]
        
        # Parse weight history
        if 'weight_history' in data:
            patient.weight_history = [
                self._parse_temporal_weight(weight_data)
                for weight_data in data['weight_history']
            ]
        
        # Parse lifestyle
        if 'lifestyle' in data:
            patient.lifestyle = [
                self._parse_temporal_lifestyle(lifestyle_data)
                for lifestyle_data in data['lifestyle']
            ]
        
        # Parse lab files
        if 'lab_files' in data:
            patient.lab_files = data['lab_files']
        
        return patient
    
    def _parse_date(self, date_value: Union[str, date, datetime]) -> date:
        """Parse date from various formats."""
        if isinstance(date_value, date):
            return date_value
        if isinstance(date_value, datetime):
            return date_value.date()
        if isinstance(date_value, str):
            # Try different formats
            for fmt in ['%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%d.%m.%Y']:
                try:
                    return datetime.strptime(date_value, fmt).date()
                except ValueError:
                    continue
        raise ValueError(f"Cannot parse date: {date_value}")
    
    def _parse_temporal_med(self, data: Dict) -> TemporalValue:
        """Parse temporal medication entry."""
        med_data = data['value']
        
        medication = PatientMedication(
            medication_name=med_data['medication_name'],
            dosage=float(med_data['dosage']),
            dosage_unit=med_data['dosage_unit'],
            frequency=med_data.get('frequency', 'once_daily'),
            administration_time=med_data.get('administration_time', 'morning'),
            start_date=self._parse_date(med_data.get('start_date', data['start_date'])),
            end_date=self._parse_date(med_data['end_date']) if 'end_date' in med_data else None,
            prescribed_for=med_data.get('prescribed_for', ''),
            notes=data.get('notes', '')
        )
        
        return TemporalValue(
            value=medication,
            start_date=self._parse_date(data['start_date']),
            end_date=self._parse_date(data['end_date']) if 'end_date' in data else None,
            notes=data.get('notes', '')
        )
    
    def _parse_temporal_condition(self, data: Dict) -> TemporalValue:
        """Parse temporal condition entry."""
        return TemporalValue(
            value=data['value'],
            start_date=self._parse_date(data['start_date']),
            end_date=self._parse_date(data['end_date']) if 'end_date' in data else None,
            notes=data.get('notes', '')
        )
    
    def _parse_vitals(self, data: Dict) -> VitalsSnapshot:
        """Parse vitals snapshot."""
        return VitalsSnapshot(
            timestamp=self._parse_date(data.get('date', data.get('timestamp'))),
            blood_pressure_systolic=data.get('blood_pressure_systolic'),
            blood_pressure_diastolic=data.get('blood_pressure_diastolic'),
            heart_rate=data.get('heart_rate'),
            weight=float(data['weight']) if 'weight' in data else None,
            temperature=float(data['temperature']) if 'temperature' in data else None,
            notes=data.get('notes', '')
        )
    
    def _parse_temporal_weight(self, data: Dict) -> TemporalValue:
        """Parse temporal weight entry."""
        return TemporalValue(
            value=float(data['value']),
            start_date=self._parse_date(data['start_date']),
            notes=data.get('notes', '')
        )
    
    def _parse_temporal_lifestyle(self, data: Dict) -> TemporalValue:
        """Parse temporal lifestyle entry."""
        return TemporalValue(
            value=data['value'],
            start_date=self._parse_date(data['start_date']),
            notes=data.get('notes', '')
        )
    
    def list_patients(self) -> List[str]:
        """
        List all available patient IDs.
        
        Returns:
            List of patient IDs
        """
        patient_files = self.patients_dir.glob("*.yaml")
        return [f.stem for f in patient_files if not f.name.startswith('_')]
    
    def save(self, patient: PatientProfile, backup: bool = True):
        """
        Save patient profile to YAML file.
        
        Args:
            patient: PatientProfile to save
            backup: If True, create backup of existing file
        """
        file_path = self.patients_dir / f"{patient.patient_id}.yaml"
        
        # Create backup if file exists
        if backup and file_path.exists():
            backup_path = file_path.with_suffix('.yaml.bak')
            backup_path.write_text(file_path.read_text())
        
        # Convert patient to dict
        data = self._patient_to_dict(patient)
        
        # Write YAML
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    def _patient_to_dict(self, patient: PatientProfile) -> Dict[str, Any]:
        """Convert PatientProfile to dictionary for YAML serialization."""
        data = {
            'patient_id': patient.patient_id,
            'name': patient.name,
            'gender': patient.gender,
            'birth_date': patient.birth_date.isoformat(),
        }
        
        # Add medications
        if patient.medications:
            data['medications'] = [
                self._temporal_med_to_dict(tv)
                for tv in patient.medications
            ]
        
        # Add conditions
        if patient.conditions:
            data['conditions'] = [
                self._temporal_condition_to_dict(tv)
                for tv in patient.conditions
            ]
        
        # Add vitals
        if patient.vitals:
            data['vitals'] = [
                self._vitals_to_dict(v)
                for v in patient.vitals
            ]
        
        # Add weight history
        if patient.weight_history:
            data['weight_history'] = [
                self._temporal_weight_to_dict(tv)
                for tv in patient.weight_history
            ]
        
        # Add lifestyle
        if patient.lifestyle:
            data['lifestyle'] = [
                self._temporal_lifestyle_to_dict(tv)
                for tv in patient.lifestyle
            ]
        
        # Add lab files
        if patient.lab_files:
            data['lab_files'] = patient.lab_files
        
        return data
    
    def _temporal_med_to_dict(self, tv: TemporalValue) -> Dict:
        """Convert TemporalValue[PatientMedication] to dict."""
        med = tv.value
        data = {
            'value': {
                'medication_name': med.medication_name,
                'dosage': med.dosage,
                'dosage_unit': med.dosage_unit,
                'frequency': med.frequency,
                'administration_time': med.administration_time,
                'prescribed_for': med.prescribed_for,
            },
            'start_date': tv.start_date.isoformat(),
        }
        if tv.end_date:
            data['end_date'] = tv.end_date.isoformat()
        if tv.notes:
            data['notes'] = tv.notes
        return data
    
    def _temporal_condition_to_dict(self, tv: TemporalValue) -> Dict:
        """Convert TemporalValue[str] to dict."""
        data = {
            'value': tv.value,
            'start_date': tv.start_date.isoformat(),
        }
        if tv.end_date:
            data['end_date'] = tv.end_date.isoformat()
        if tv.notes:
            data['notes'] = tv.notes
        return data
    
    def _vitals_to_dict(self, v: VitalsSnapshot) -> Dict:
        """Convert VitalsSnapshot to dict."""
        data = {
            'date': v.timestamp.isoformat(),
        }
        if v.blood_pressure_systolic:
            data['blood_pressure_systolic'] = v.blood_pressure_systolic
        if v.blood_pressure_diastolic:
            data['blood_pressure_diastolic'] = v.blood_pressure_diastolic
        if v.heart_rate:
            data['heart_rate'] = v.heart_rate
        if v.weight:
            data['weight'] = v.weight
        if v.temperature:
            data['temperature'] = v.temperature
        if v.notes:
            data['notes'] = v.notes
        return data
    
    def _temporal_weight_to_dict(self, tv: TemporalValue) -> Dict:
        """Convert TemporalValue[float] to dict."""
        data = {
            'value': tv.value,
            'start_date': tv.start_date.isoformat(),
        }
        if tv.notes:
            data['notes'] = tv.notes
        return data
    
    def _temporal_lifestyle_to_dict(self, tv: TemporalValue) -> Dict:
        """Convert TemporalValue[dict] to dict."""
        data = {
            'value': tv.value,
            'start_date': tv.start_date.isoformat(),
        }
        if tv.notes:
            data['notes'] = tv.notes
        return data


# Convenience function
def load_patient(patient_id: str, patients_dir: str = "patients") -> PatientProfile:
    """
    Load a patient profile by ID.
    
    Args:
        patient_id: Patient ID (e.g., "p001")
        patients_dir: Directory containing patient files
        
    Returns:
        PatientProfile object
    """
    loader = PatientLoader(patients_dir)
    return loader.load(patient_id)


__all__ = ['PatientLoader', 'load_patient']
