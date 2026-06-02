"""
Medication Diary Module

Tracks medication/supplement intake - both one-time and recurring.
Part of the universal health diary system.

Example:
    >>> from blutwerte.diary import MedicationDiary
    >>> 
    >>> med_diary = MedicationDiary(user_id="user001")
    >>> 
    >>> # One-time entry (took for headache)
    >>> med_diary.add_one_time(
    ...     name="Ibuprofen",
    ...     dosage=400,
    ...     unit="mg",
    ...     reason="Headache",
    ...     taken_at=datetime.now()
    ... )
    >>> 
    >>> # Regular medication
    >>> med_diary.add_regular(
    ...     name="Vitamin D",
    ...     dosage=2000,
    ...     unit="IU",
    ...     frequency="daily",
    ...     times_per_day=1,
    ...     start_date=date(2025, 1, 1)
    ... )
    >>> 
    >>> # Log that you took it today
    >>> med_diary.log_dose("Vitamin D", taken_at=datetime.now())
    >>> 
    >>> # Get adherence
    >>> adherence = med_diary.get_adherence("Vitamin D", days=30)
"""

from datetime import datetime, date, timedelta, time
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import json


class Frequency(Enum):
    """How often a medication is taken."""
    ONCE = "once"              # One-time only
    DAILY = "daily"           # Every day
    WEEKLY = "weekly"          # X times per week
    MONTHLY = "monthly"        # X times per month
    AS_NEEDED = "as_needed"    # PRN


class IntakeTime(Enum):
    """When during the day a medication is taken."""
    MORNING = "morning"       # Upon waking
    BREAKFAST = "breakfast"    # With breakfast
    LUNCH = "lunch"           # With lunch
    DINNER = "dinner"         # With dinner
    BEDTIME = "bedtime"      # Before sleep
    WITH_FOOD = "with_food"   # With food (any)
    EMPTY_STOMACH = "empty_stomach"  # Before meals


@dataclass
class MedicationSchedule:
    """
    A regularly scheduled medication/supplement.
    """
    id: str
    name: str
    dosage: float
    unit: str                    # mg, IU, ml, etc.
    frequency: Frequency
    times_per_day: int = 1
    intake_times: List[IntakeTime] = field(default_factory=list)
    
    # Optional
    instructions: str = ""
    reason: str = ""            # Why taking it (e.g., "for vitamin D deficiency")
    prescribed: bool = False    # Prescription or supplement
    
    # Timing
    start_date: date = field(default_factory=date.today)
    end_date: Optional[date] = None
    
    # Tracking
    reminder_enabled: bool = False
    notes: str = ""


@dataclass
class MedicationIntake:
    """
    A single intake event (when medication was actually taken).
    """
    id: str
    medication_name: str
    
    # What was taken
    dosage_taken: float
    unit: str
    
    # When
    taken_at: datetime
    
    # Context
    reason: str = ""           # Why taking now (e.g., "headache", "routine")
    symptoms: List[str] = field(default_factory=list)  # Current symptoms
    notes: str = ""
    
    # Source
    source: str = "manual"     # manual, device, import
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "medication_name": self.medication_name,
            "dosage_taken": self.dosage_taken,
            "unit": self.unit,
            "taken_at": self.taken_at.isoformat(),
            "reason": self.reason,
            "symptoms": self.symptoms,
            "notes": self.notes,
            "source": self.source,
        }


class MedicationDiary:
    """
    Track medication and supplement intake - one-time and regular.
    """
    
    # Common medications with their typical dosages (for validation/suggestions)
    COMMON_MEDICATIONS = {
        # Vitamins
        "vitamin_d": {"typical_dosage": 2000, "unit": "IU", "frequency": "daily"},
        "vitamin_b12": {"typical_dosage": 1000, "unit": "mcg", "frequency": "daily"},
        "vitamin_c": {"typical_dosage": 500, "unit": "mg", "frequency": "daily"},
        "vitamin_b_complex": {"typical_dosage": 1, "unit": "tablet", "frequency": "daily"},
        
        # Minerals
        "iron": {"typical_dosage": 65, "unit": "mg", "frequency": "daily"},
        "magnesium": {"typical_dosage": 400, "unit": "mg", "frequency": "daily"},
        "zinc": {"typical_dosage": 15, "unit": "mg", "frequency": "daily"},
        "calcium": {"typical_dosage": 500, "unit": "mg", "frequency": "daily"},
        
        # Omega fatty acids
        "fish_oil": {"typical_dosage": 1000, "unit": "mg", "frequency": "daily"},
        "omega_3": {"typical_dosage": 2000, "unit": "mg", "frequency": "daily"},
        
        # Common OTC
        "ibuprofen": {"typical_dosage": 400, "unit": "mg", "frequency": "as_needed"},
        "paracetamol": {"typical_dosage": 500, "unit": "mg", "frequency": "as_needed"},
        "aspirin": {"typical_dosage": 100, "unit": "mg", "frequency": "as_needed"},
        
        # Supplements
        "coq10": {"typical_dosage": 100, "unit": "mg", "frequency": "daily"},
        "curcumin": {"typical_dosage": 500, "unit": "mg", "frequency": "daily"},
        "probiotics": {"typical_dosage": 1, "unit": "capsule", "frequency": "daily"},
        "multivitamin": {"typical_dosage": 1, "unit": "tablet", "frequency": "daily"},
    }
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.schedules: List[MedicationSchedule] = []
        self.intakes: List[MedicationIntake] = []
        self._intake_counter = 0
    
    def _generate_id(self) -> str:
        self._intake_counter += 1
        return f"{self.user_id}_med_{self._intake_counter}"
    
    def add_regular(
        self,
        name: str,
        dosage: float,
        unit: str,
        frequency: str = "daily",
        times_per_day: int = 1,
        intake_times: Optional[List[str]] = None,
        instructions: str = "",
        reason: str = "",
        prescribed: bool = False,
        start_date: Optional[date] = None,
    ) -> MedicationSchedule:
        """
        Add a regularly scheduled medication/supplement.
        
        Args:
            name: Medication name
            dosage: Amount per dose
            unit: Unit (mg, IU, ml, tablet, etc.)
            frequency: daily, weekly, monthly, as_needed
            times_per_day: How many times per day
            intake_times: When to take (morning, breakfast, etc.)
            instructions: Special instructions
            reason: Why taking it
            prescribed: Prescription or OTC/supplement
            start_date: When started
            
        Returns:
            Created MedicationSchedule
        """
        freq = Frequency(frequency) if isinstance(frequency, str) else frequency
        
        times = []
        if intake_times:
            for t in intake_times:
                if isinstance(t, str):
                    times.append(IntakeTime(t))
                else:
                    times.append(t)
        
        schedule = MedicationSchedule(
            id=f"{self.user_id}_{name.lower().replace(' ', '_')}",
            name=name,
            dosage=dosage,
            unit=unit,
            frequency=freq,
            times_per_day=times_per_day,
            intake_times=times,
            instructions=instructions,
            reason=reason,
            prescribed=prescribed,
            start_date=start_date or date.today(),
        )
        
        self.schedules.append(schedule)
        return schedule
    
    def add_one_time(
        self,
        name: str,
        dosage: float,
        unit: str,
        reason: str = "",
        symptoms: Optional[List[str]] = None,
        taken_at: Optional[datetime] = None,
        notes: str = "",
    ) -> MedicationIntake:
        """
        Record a one-time medication intake (e.g., ibuprofen for headache).
        
        Args:
            name: Medication name
            dosage: Amount taken
            unit: Unit (mg, ml, etc.)
            reason: Why taking it now
            symptoms: Current symptoms
            taken_at: When taken (default: now)
            notes: Additional notes
            
        Returns:
            Created MedicationIntake
        """
        intake = MedicationIntake(
            id=self._generate_id(),
            medication_name=name,
            dosage_taken=dosage,
            unit=unit,
            taken_at=taken_at or datetime.now(),
            reason=reason,
            symptoms=symptoms or [],
            notes=notes,
            source="manual",
        )
        
        self.intakes.append(intake)
        return intake
    
    def log_dose(
        self,
        medication_name: str,
        dosage: Optional[float] = None,
        taken_at: Optional[datetime] = None,
        notes: str = "",
    ) -> Optional[MedicationIntake]:
        """
        Log that a scheduled medication was taken.
        
        Args:
            medication_name: Name of medication
            dosage: Actual dosage taken (default: scheduled dosage)
            taken_at: When taken
            notes: Notes
            
        Returns:
            Created intake, or None if medication not found
        """
        # Find schedule
        schedule = None
        for s in self.schedules:
            if s.name.lower() == medication_name.lower():
                schedule = s
                break
        
        if not schedule:
            return None
        
        dosage = dosage or schedule.dosage
        
        intake = MedicationIntake(
            id=self._generate_id(),
            medication_name=schedule.name,
            dosage_taken=dosage,
            unit=schedule.unit,
            taken_at=taken_at or datetime.now(),
            reason=schedule.reason,
            notes=notes,
            source="manual",
        )
        
        self.intakes.append(intake)
        return intake
    
    def get_intakes(
        self,
        medication_name: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        days: Optional[int] = None,
        reason: Optional[str] = None,
    ) -> List[MedicationIntake]:
        """
        Get medication intakes with filters.
        
        Args:
            medication_name: Filter by medication
            start_date: Filter by start
            end_date: Filter by end
            days: Last N days
            reason: Filter by reason (e.g., "headache")
            
        Returns:
            List of intakes
        """
        results = self.intakes
        
        if medication_name:
            results = [i for i in results if i.medication_name.lower() == medication_name.lower()]
        
        if days:
            cutoff = datetime.now() - timedelta(days=days)
            results = [i for i in results if i.taken_at >= cutoff]
        elif start_date:
            results = [i for i in results if i.taken_at >= start_date]
        if end_date:
            results = [i for i in results if i.taken_at <= end_date]
        
        if reason:
            results = [i for i in results if reason.lower() in i.reason.lower()]
        
        results.sort(key=lambda x: x.taken_at, reverse=True)
        return results
    
    def get_schedules(self, active_only: bool = True) -> List[MedicationSchedule]:
        """
        Get medication schedules.
        
        Args:
            active_only: Only return active schedules (not ended)
            
        Returns:
            List of schedules
        """
        if active_only:
            today = date.today()
            return [s for s in self.schedules if s.end_date is None or s.end_date >= today]
        return self.schedules
    
    def get_adherence(
        self,
        medication_name: str,
        days: int = 30,
    ) -> Dict[str, Any]:
        """
        Calculate adherence for a medication.
        
        Args:
            medication_name: Name of medication
            days: Period to analyze
            
        Returns:
            Adherence statistics
        """
        # Find schedule
        schedule = None
        for s in self.schedules:
            if s.name.lower() == medication_name.lower():
                schedule = s
                break
        
        if not schedule:
            return {"error": "Medication not found in schedules"}
        
        # Get intakes
        intakes = self.get_intakes(medication_name=medication_name, days=days)
        
        # Calculate expected doses
        today = date.today()
        start = today - timedelta(days=days)
        
        expected_doses = 0
        current = start
        while current <= today:
            if schedule.frequency == Frequency.DAILY:
                expected_doses += schedule.times_per_day
            elif schedule.frequency == Frequency.WEEKLY:
                if current.weekday() == 0:  # Monday
                    expected_doses += schedule.times_per_day
            current += timedelta(days=1)
        
        taken_doses = len(intakes)
        
        adherence_rate = (taken_doses / expected_doses * 100) if expected_doses > 0 else 0
        
        return {
            "medication": schedule.name,
            "period_days": days,
            "expected_doses": expected_doses,
            "taken_doses": taken_doses,
            "missed_doses": expected_doses - taken_doses,
            "adherence_rate": round(adherence_rate, 1),
            "last_taken": intakes[0].taken_at.isoformat() if intakes else None,
        }
    
    def get_today_intakes(self) -> List[MedicationIntake]:
        """Get all intakes for today."""
        today = datetime.now().date()
        return [
            i for i in self.intakes
            if i.taken_at.date() == today
        ]
    
    def get_due_today(self) -> List[MedicationSchedule]:
        """Get medications that should be taken today."""
        schedules = self.get_schedules(active_only=True)
        today = date.today()
        weekday = today.weekday()
        
        due = []
        for s in schedules:
            if s.frequency == Frequency.DAILY:
                due.append(s)
            elif s.frequency == Frequency.WEEKLY:
                if weekday == 0:  # Monday
                    due.append(s)
            elif s.frequency == Frequency.AS_NEEDED:
                pass  # PRN - not scheduled
        
        return due
    
    def search_medication(self, query: str) -> List[str]:
        """
        Search for medications in common database.
        
        Args:
            query: Search query
            
        Returns:
            List of matching medication names
        """
        query = query.lower()
        return [
            name for name in self.COMMON_MEDICATIONS.keys()
            if query in name
        ]
    
    def export_json(self, filepath: str) -> None:
        """Export medication diary to JSON."""
        data = {
            "user_id": self.user_id,
            "exported_at": datetime.now().isoformat(),
            "schedules": [
                {
                    "id": s.id,
                    "name": s.name,
                    "dosage": s.dosage,
                    "unit": s.unit,
                    "frequency": s.frequency.value,
                    "times_per_day": s.times_per_day,
                    "intake_times": [t.value for t in s.intake_times],
                    "instructions": s.instructions,
                    "reason": s.reason,
                    "prescribed": s.prescribed,
                    "start_date": s.start_date.isoformat() if s.start_date else None,
                    "end_date": s.end_date.isoformat() if s.end_date else None,
                }
                for s in self.schedules
            ],
            "intakes": [i.to_dict() for i in self.intakes],
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def import_json(self, filepath: str) -> int:
        """Import medication diary from JSON."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
        
        # Import schedules
        for s_data in data.get("schedules", []):
            schedule = MedicationSchedule(
                id=s_data["id"],
                name=s_data["name"],
                dosage=s_data["dosage"],
                unit=s_data["unit"],
                frequency=Frequency(s_data["frequency"]),
                times_per_day=s_data.get("times_per_day", 1),
                intake_times=[IntakeTime(t) for t in s_data.get("intake_times", [])],
                instructions=s_data.get("instructions", ""),
                reason=s_data.get("reason", ""),
                prescribed=s_data.get("prescribed", False),
                start_date=date.fromisoformat(s_data["start_date"]) if s_data.get("start_date") else date.today(),
                end_date=date.fromisoformat(s_data["end_date"]) if s_data.get("end_date") else None,
            )
            self.schedules.append(schedule)
            count += 1
        
        # Import intakes
        for i_data in data.get("intakes", []):
            intake = MedicationIntake(
                id=i_data["id"],
                medication_name=i_data["medication_name"],
                dosage_taken=i_data["dosage_taken"],
                unit=i_data["unit"],
                taken_at=datetime.fromisoformat(i_data["taken_at"]),
                reason=i_data.get("reason", ""),
                symptoms=i_data.get("symptoms", []),
                notes=i_data.get("notes", ""),
                source=i_data.get("source", "import"),
            )
            self.intakes.append(intake)
            count += 1
        
        return count


__all__ = [
    'MedicationDiary',
    'MedicationSchedule',
    'MedicationIntake',
    'Frequency',
    'IntakeTime',
]
