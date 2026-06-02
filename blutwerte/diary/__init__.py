"""
Universal Health Diary Module

A flexible, extensible system for logging and tracking any health-related data.
Supports manual entries and automated feeds from devices (smartwatches, etc.).

Design Principles:
1. Generic - Not tied to specific data types
2. Extensible - Easy to add new metric types
3. Multi-source - Manual entry and automated feeds
4. Time-series - Store historical data with timestamps
5. Tagged - Allow categorization and filtering

Example Usage:
    >>> from blutwerte.diary import Diary, MetricType, EntrySource
    >>> 
    >>> # Create a diary
    >>> diary = Diary(user_id="user001")
    >>> 
    >>> # Add different types of entries
    >>> diary.add_entry(
    ...     metric="weight",
    ...     value=78.5,
    ...     unit="kg",
    ...     source=EntrySource.MANUAL,
    ...     timestamp=datetime.now()
    ... )
    >>> 
    >>> diary.add_entry(
    ...     metric="blood_pressure",
    ...     value={"systolic": 120, "diastolic": 80},
    ...     source=EntrySource.DEVICE,
    ...     device="omron_bp7350"
    ... )
    >>> 
    >>> diary.add_entry(
    ...     metric="food_intake",
    ...     value={"foods": ["oatmeal", "banana"], "calories": 450},
    ...     source=EntrySource.MANUAL
    ... )
    >>> 
    >>> # Query data
    >>> entries = diary.get_entries(metric="weight", days=30)
    >>> stats = diary.get_statistics("weight", days=7)
"""

from datetime import datetime, date, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass, field
import json

from blutwerte.diary.medication import (
    MedicationDiary,
    MedicationSchedule,
    MedicationIntake,
    Frequency,
    IntakeTime,
)


class EntrySource(Enum):
    """Source of the diary entry."""
    MANUAL = "manual"           # User manually entered
    DEVICE = "device"           # From smart device
    IMPORT = "import"           # Batch import from file
    API = "api"                 # From external API
    CALCULATED = "calculated"    # Derived/calculated value


class AggregationType(Enum):
    """How to aggregate multiple values."""
    AVERAGE = "average"
    SUM = "sum"
    MIN = "min"
    MAX = "max"
    LAST = "last"
    FIRST = "first"
    COUNT = "count"


@dataclass
class DiaryEntry:
    """
    A single diary entry for any metric.
    
    Flexible enough to store:
    - Simple values (weight: 78.5 kg)
    - Complex values (blood_pressure: {systolic: 120, diastolic: 80})
    - Lists (foods eaten, symptoms)
    - Nested data (workout with HR, distance, duration)
    """
    id: str
    metric: str                    # e.g., "weight", "blood_pressure", "mood"
    value: Any                     # Can be float, dict, list, or any JSON-serializable type
    unit: Optional[str] = None       # e.g., "kg", "mmHg", "bpm"
    
    # Metadata
    timestamp: datetime = field(default_factory=datetime.now)
    source: EntrySource = EntrySource.MANUAL
    source_device: Optional[str] = None  # e.g., "apple_watch", "omron_bp7350"
    source_id: Optional[str] = None     # ID from source system
    
    # Tags for filtering
    tags: List[str] = field(default_factory=list)
    notes: Optional[str] = None
    
    # Context
    context: Dict[str, Any] = field(default_factory=dict)
    # e.g., {"meal": "breakfast", "position": "sitting", "arm": "left"}
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "metric": self.metric,
            "value": self.value,
            "unit": self.unit,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source.value,
            "source_device": self.source_device,
            "source_id": self.source_id,
            "tags": self.tags,
            "notes": self.notes,
            "context": self.context,
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'DiaryEntry':
        """Create from dictionary."""
        data = data.copy()
        if isinstance(data.get("timestamp"), str):
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        if isinstance(data.get("source"), str):
            data["source"] = EntrySource(data["source"])
        return cls(**data)


@dataclass
class MetricDefinition:
    """
    Definition of a tracked metric.
    
    Allows specifying validation rules, display preferences, etc.
    """
    name: str                      # e.g., "weight"
    display_name: str              # e.g., "Body Weight"
    unit: str                      # e.g., "kg"
    
    # Validation
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    allowed_values: Optional[List[Any]] = None  # For enum-like metrics
    
    # Display preferences
    decimals: int = 1              # Number of decimal places
    normal_range_min: Optional[float] = None
    normal_range_max: Optional[float] = None
    
    # Categories
    category: str = "general"       # e.g., "vitals", "nutrition", "activity"
    description: Optional[str] = None
    
    # Validation function (optional)
    validator: Optional[Callable] = None


class Diary:
    """
    Universal health diary for tracking any metric over time.
    
    Can store:
    - Vital signs (weight, BP, pulse, temperature)
    - Nutrition (food, calories, macros)
    - Activity (workouts, steps, sleep)
    - Mood and symptoms
    - Lab results
    - And any custom metric
    """
    
    # Pre-defined metric definitions
    DEFAULT_METRICS = {
        # Vital Signs
        "weight": MetricDefinition(
            name="weight", display_name="Body Weight", unit="kg",
            category="vitals", normal_range_min=50, normal_range_max=150,
            decimals=1, description="Body weight in kilograms"
        ),
        "blood_pressure_systolic": MetricDefinition(
            name="blood_pressure_systolic", display_name="Blood Pressure (Systolic)", 
            unit="mmHg", category="vitals", normal_range_min=90, normal_range_max=120,
            decimals=0
        ),
        "blood_pressure_diastolic": MetricDefinition(
            name="blood_pressure_diastolic", display_name="Blood Pressure (Diastolic)", 
            unit="mmHg", category="vitals", normal_range_min=60, normal_range_max=80,
            decimals=0
        ),
        "pulse": MetricDefinition(
            name="pulse", display_name="Heart Rate", unit="bpm",
            category="vitals", normal_range_min=60, normal_range_max=100,
            decimals=0, description="Resting heart rate"
        ),
        "blood_oxygen": MetricDefinition(
            name="blood_oxygen", display_name="Blood Oxygen (SpO2)", unit="%",
            category="vitals", normal_range_min=95, normal_range_max=100,
            decimals=0
        ),
        "temperature": MetricDefinition(
            name="temperature", display_name="Body Temperature", unit="°C",
            category="vitals", normal_range_min=36.1, normal_range_max=37.2,
            decimals=1
        ),
        
        # Nutrition
        "calories": MetricDefinition(
            name="calories", display_name="Calories", unit="kcal",
            category="nutrition", decimals=0
        ),
        "protein": MetricDefinition(
            name="protein", display_name="Protein", unit="g",
            category="nutrition", decimals=0
        ),
        "carbs": MetricDefinition(
            name="carbs", display_name="Carbohydrates", unit="g",
            category="nutrition", decimals=0
        ),
        "fat": MetricDefinition(
            name="fat", display_name="Fat", unit="g",
            category="nutrition", decimals=0
        ),
        "fiber": MetricDefinition(
            name="fiber", display_name="Fiber", unit="g",
            category="nutrition", decimals=0
        ),
        
        # Activity
        "steps": MetricDefinition(
            name="steps", display_name="Steps", unit="steps",
            category="activity", decimals=0
        ),
        "distance": MetricDefinition(
            name="distance", display_name="Distance", unit="km",
            category="activity", decimals=2
        ),
        "active_minutes": MetricDefinition(
            name="active_minutes", display_name="Active Minutes", unit="min",
            category="activity", decimals=0
        ),
        "sleep_hours": MetricDefinition(
            name="sleep_hours", display_name="Sleep Duration", unit="hours",
            category="activity", normal_range_min=7, normal_range_max=9,
            decimals=1
        ),
        
        # Blood Tests (for lab results)
        "glucose_fasting": MetricDefinition(
            name="glucose_fasting", display_name="Fasting Glucose", unit="mg/dL",
            category="blood_test", normal_range_min=70, normal_range_max=100,
            decimals=0
        ),
        "ldl": MetricDefinition(
            name="ldl", display_name="LDL Cholesterol", unit="mg/dL",
            category="blood_test", normal_range_min=0, normal_range_max=100,
            decimals=0
        ),
        "hdl": MetricDefinition(
            name="hdl", display_name="HDL Cholesterol", unit="mg/dL",
            category="blood_test", normal_range_min=40, normal_range_max=60,
            decimals=0
        ),
        
        # ============ NEW: Extended Health Tracking ============
        
        # Hydration
        "water_intake": MetricDefinition(
            name="water_intake", display_name="Water Intake", unit="ml",
            category="nutrition", normal_range_min=1500, normal_range_max=4000,
            decimals=0, description="Daily water consumption"
        ),
        "caffeine_intake": MetricDefinition(
            name="caffeine_intake", display_name="Caffeine Intake", unit="mg",
            category="nutrition", normal_range_min=0, normal_range_max=400,
            decimals=0, description="Caffeine from coffee, tea, energy drinks"
        ),
        "alcohol_intake": MetricDefinition(
            name="alcohol_intake", display_name="Alcohol Intake", unit="g",
            category="nutrition", normal_range_min=0, normal_range_max=30,
            decimals=0, description="Alcohol consumption in grams"
        ),
        
        # Sleep (detailed)
        "sleep_quality": MetricDefinition(
            name="sleep_quality", display_name="Sleep Quality", unit="rating",
            category="activity", allowed_values=["terrible", "poor", "fair", "good", "excellent"],
            description="Sleep quality rating"
        ),
        "sleep_deep": MetricDefinition(
            name="sleep_deep", display_name="Deep Sleep", unit="hours",
            category="activity", normal_range_min=1, normal_range_max=3,
            decimals=1
        ),
        "sleep_rem": MetricDefinition(
            name="sleep_rem", display_name="REM Sleep", unit="hours",
            category="activity", normal_range_min=1.5, normal_range_max=2.5,
            decimals=1
        ),
        
        # Steps & Activity (detailed)
        "active_calories": MetricDefinition(
            name="active_calories", display_name="Active Calories Burned", unit="kcal",
            category="activity", decimals=0
        ),
        "exercise_type": MetricDefinition(
            name="exercise_type", display_name="Exercise Type", unit="",
            category="activity", description="Type of exercise performed"
        ),
        
        # Mood & Wellbeing
        "mood": MetricDefinition(
            name="mood", display_name="Mood", unit="rating",
            category="wellbeing", allowed_values=["terrible", "bad", "okay", "good", "great"],
            description="Overall mood (terrible/bad/okay/good/great)"
        ),
        "stress_level": MetricDefinition(
            name="stress_level", display_name="Stress Level", unit="rating",
            category="wellbeing", allowed_values=[1, 2, 3, 4, 5],
            description="Stress level 1-5"
        ),
        
        # Medication reference (use MedicationDiary for tracking)
        "medication_taken": MetricDefinition(
            name="medication_taken", display_name="Medication Taken", unit="boolean",
            category="symptoms", allowed_values=[0, 1],
            description="Whether medication was taken (use MedicationDiary for detailed tracking)"
        ),
        
        # Headache & Migraine Tracking
        "headache": MetricDefinition(
            name="headache", display_name="Headache", unit="boolean",
            category="symptoms", allowed_values=[0, 1],
            description="Had a headache (0=no, 1=yes)"
        ),
        "headache_severity": MetricDefinition(
            name="headache_severity", display_name="Headache Severity", unit="rating",
            category="symptoms", allowed_values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            description="Headache severity 1-10"
        ),
        "headache_location": MetricDefinition(
            name="headache_location", display_name="Headache Location", unit="",
            category="symptoms", allowed_values=["left", "right", "both", "front", "back", "whole"],
            description="Where the headache is located"
        ),
        "headache_type": MetricDefinition(
            name="headache_type", display_name="Headache Type", unit="",
            category="symptoms", allowed_values=["tension", "migraine", "cluster", "sinus", "other"],
            description="Type of headache"
        ),
        "migraine_ aura": MetricDefinition(
            name="migraine_aura", display_name="Migraine Aura", unit="boolean",
            category="symptoms", allowed_values=[0, 1],
            description="Had aura symptoms (0=no, 1=yes)"
        ),
        "migraine_triggers": MetricDefinition(
            name="migraine_triggers", display_name="Migraine Triggers", unit="",
            category="symptoms", description="Potential triggers (stress, weather, food, etc.)"
        ),
        
        # General Symptoms
        "pain_level": MetricDefinition(
            name="pain_level", display_name="Pain Level", unit="rating",
            category="symptoms", allowed_values=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            description="General pain level 0-10"
        ),
        "fatigue_level": MetricDefinition(
            name="fatigue_level", display_name="Fatigue Level", unit="rating",
            category="symptoms", allowed_values=[1, 2, 3, 4, 5],
            description="Fatigue level 1-5"
        ),
        "digestion_quality": MetricDefinition(
            name="digestion_quality", display_name="Digestion Quality", unit="rating",
            category="symptoms", allowed_values=[1, 2, 3, 4, 5],
            description="Digestion quality 1-5"
        ),
        
        # Weather (for correlation)
        "weather": MetricDefinition(
            name="weather", display_name="Weather", unit="",
            category="environment", allowed_values=["sunny", "cloudy", "rainy", "stormy", "snowy", "foggy"],
            description="Current weather condition"
        ),
        "barometric_pressure": MetricDefinition(
            name="barometric_pressure", display_name="Barometric Pressure", unit="hPa",
            category="environment", normal_range_min=980, normal_range_max=1040,
            decimals=0, description="Atmospheric pressure"
        ),
        "temperature_outdoor": MetricDefinition(
            name="temperature_outdoor", display_name="Outdoor Temperature", unit="°C",
            category="environment", decimals=0
        ),
        
        # Women-specific
        "menstrual_cycle_day": MetricDefinition(
            name="menstrual_cycle_day", display_name="Menstrual Cycle Day", unit="",
            category="cycle", allowed_values=list(range(1, 29)),
            description="Day in menstrual cycle (1-28)"
        ),
        "period_flow": MetricDefinition(
            name="period_flow", display_name="Period Flow", unit="",
            category="cycle", allowed_values=["none", "light", "medium", "heavy"],
            description="Menstrual flow intensity"
        ),
        "hormonal_symptoms": MetricDefinition(
            name="hormonal_symptoms", display_name="Hormonal Symptoms", unit="",
            category="cycle", description="Symptoms like bloating, cramps, mood swings"
        ),
    }
    
    def __init__(self, user_id: str, name: Optional[str] = None):
        """
        Initialize a new diary.
        
        Args:
            user_id: Unique user identifier
            name: Optional name for this diary
        """
        self.user_id = user_id
        self.name = name or f"Diary for {user_id}"
        self.entries: List[DiaryEntry] = []
        self.metrics: Dict[str, MetricDefinition] = dict(self.DEFAULT_METRICS)
        self._entry_counter = 0
    
    def _generate_id(self) -> str:
        """Generate unique entry ID."""
        self._entry_counter += 1
        return f"{self.user_id}_{self._entry_counter}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def register_metric(self, definition: MetricDefinition) -> None:
        """
        Register a new metric type.
        
        Args:
            definition: MetricDefinition for the new metric
        """
        self.metrics[definition.name] = definition
    
    def add_entry(
        self,
        metric: str,
        value: Any,
        unit: Optional[str] = None,
        timestamp: Optional[datetime] = None,
        source: EntrySource = EntrySource.MANUAL,
        source_device: Optional[str] = None,
        source_id: Optional[str] = None,
        tags: Optional[List[str]] = None,
        notes: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        validate: bool = True,
    ) -> DiaryEntry:
        """
        Add a new diary entry.
        
        Args:
            metric: Metric name (e.g., "weight", "blood_pressure")
            value: Value to store (any JSON-serializable type)
            unit: Unit of measurement (auto-detected if metric registered)
            timestamp: When the entry was recorded
            source: How the entry was created
            source_device: Device that created the entry
            source_id: ID from source system (for deduplication)
            tags: Optional tags for filtering
            notes: Optional notes
            context: Additional context (meal, position, etc.)
            validate: Whether to validate the value
            
        Returns:
            Created DiaryEntry
            
        Raises:
            ValueError: If validation fails
        """
        # Auto-detect unit from metric definition
        if unit is None and metric in self.metrics:
            unit = self.metrics[metric].unit
        
        # Validate if enabled and metric is registered
        if validate and metric in self.metrics:
            self._validate_value(metric, value)
        
        # Create entry
        entry = DiaryEntry(
            id=self._generate_id(),
            metric=metric,
            value=value,
            unit=unit,
            timestamp=timestamp or datetime.now(),
            source=source,
            source_device=source_device,
            source_id=source_id,
            tags=tags or [],
            notes=notes,
            context=context or {},
        )
        
        self.entries.append(entry)
        return entry
    
    def _validate_value(self, metric: str, value: Any) -> None:
        """Validate a value against metric definition."""
        definition = self.metrics.get(metric)
        if not definition:
            return
        
        # Check value type for numeric metrics
        if definition.min_value is not None or definition.max_value is not None:
            if not isinstance(value, (int, float)):
                raise ValueError(f"Metric '{metric}' requires numeric value, got {type(value)}")
            
            if definition.min_value is not None and value < definition.min_value:
                raise ValueError(f"Value {value} below minimum {definition.min_value} for {metric}")
            
            if definition.max_value is not None and value > definition.max_value:
                raise ValueError(f"Value {value} above maximum {definition.max_value} for {metric}")
        
        # Check allowed values
        if definition.allowed_values is not None:
            if value not in definition.allowed_values:
                raise ValueError(f"Value {value} not in allowed values: {definition.allowed_values}")
    
    def get_entries(
        self,
        metric: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        days: Optional[int] = None,
        source: Optional[EntrySource] = None,
        source_device: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: Optional[int] = None,
    ) -> List[DiaryEntry]:
        """
        Query diary entries with filters.
        
        Args:
            metric: Filter by metric name
            start_date: Filter by start date
            end_date: Filter by end date
            days: Filter by last N days
            source: Filter by source type
            source_device: Filter by device
            tags: Filter by tags (any match)
            limit: Maximum number of entries to return
            
        Returns:
            List of matching entries (ordered by timestamp descending)
        """
        results = self.entries
        
        # Apply filters
        if metric:
            results = [e for e in results if e.metric == metric]
        
        if days:
            cutoff = datetime.now() - timedelta(days=days)
            results = [e for e in results if e.timestamp >= cutoff]
        elif start_date:
            results = [e for e in results if e.timestamp >= start_date]
        if end_date:
            results = [e for e in results if e.timestamp <= end_date]
        
        if source:
            results = [e for e in results if e.source == source]
        
        if source_device:
            results = [e for e in results if e.source_device == source_device]
        
        if tags:
            results = [e for e in results if any(t in e.tags for t in tags)]
        
        # Sort by timestamp descending (newest first)
        results.sort(key=lambda e: e.timestamp, reverse=True)
        
        if limit:
            results = results[:limit]
        
        return results
    
    def get_latest(self, metric: str) -> Optional[DiaryEntry]:
        """Get the most recent entry for a metric."""
        entries = self.get_entries(metric=metric, limit=1)
        return entries[0] if entries else None
    
    def get_statistics(
        self,
        metric: str,
        days: int = 7,
        aggregation: AggregationType = AggregationType.AVERAGE,
    ) -> Dict[str, Any]:
        """
        Get statistics for a metric over a time period.
        
        Args:
            metric: Metric name
            days: Number of days to analyze
            aggregation: How to aggregate multiple values
            
        Returns:
            Dictionary with statistics
        """
        entries = self.get_entries(metric=metric, days=days)
        
        if not entries:
            return {"count": 0, "error": "No entries found"}
        
        # Extract numeric values (for simple metrics)
        values = []
        for entry in entries:
            if isinstance(entry.value, (int, float)):
                values.append(float(entry.value))
            elif isinstance(entry.value, dict):
                # For compound metrics like BP, extract systolic
                if "systolic" in entry.value:
                    values.append(float(entry.value["systolic"]))
        
        if not values:
            return {"count": len(entries), "note": "No numeric values to aggregate"}
        
        # Calculate statistics
        stats = {
            "count": len(values),
            "days": days,
            "first_date": min(e.timestamp for e in entries).isoformat(),
            "last_date": max(e.timestamp for e in entries).isoformat(),
        }
        
        if aggregation == AggregationType.AVERAGE:
            stats["average"] = sum(values) / len(values)
        elif aggregation == AggregationType.SUM:
            stats["sum"] = sum(values)
        elif aggregation == AggregationType.MIN:
            stats["min"] = min(values)
        elif aggregation == AggregationType.MAX:
            stats["max"] = max(values)
        elif aggregation == AggregationType.LAST:
            stats["last"] = values[0] if values else None
        elif aggregation == AggregationType.FIRST:
            stats["first"] = values[-1] if values else None
        elif aggregation == AggregationType.COUNT:
            stats["count"] = len(values)
        
        # Add definition info if available
        if metric in self.metrics:
            definition = self.metrics[metric]
            stats["unit"] = definition.unit
            stats["display_name"] = definition.display_name
            
            if definition.normal_range_min:
                stats["normal_range"] = {
                    "min": definition.normal_range_min,
                    "max": definition.normal_range_max
                }
                if "average" in stats:
                    in_range = stats["normal_range"]["min"] <= stats["average"] <= stats["normal_range"]["max"]
                    stats["in_normal_range"] = in_range
        
        return stats
    
    def get_trend(self, metric: str, days: int = 30) -> Dict[str, Any]:
        """
        Calculate trend for a metric over time.
        
        Args:
            metric: Metric name
            days: Number of days to analyze
            
        Returns:
            Dictionary with trend information
        """
        entries = self.get_entries(metric=metric, days=days)
        
        if len(entries) < 2:
            return {"trend": "insufficient_data", "entries": len(entries)}
        
        # Get values with timestamps
        values = []
        for entry in entries:
            if isinstance(entry.value, (int, float)):
                values.append((entry.timestamp, float(entry.value)))
        
        if len(values) < 2:
            return {"trend": "insufficient_numeric_data", "entries": len(values)}
        
        # Sort by timestamp
        values.sort(key=lambda x: x[0])
        
        # Calculate simple linear trend
        first_value = values[0][1]
        last_value = values[-1][1]
        change = last_value - first_value
        percent_change = (change / first_value * 100) if first_value != 0 else 0
        
        return {
            "metric": metric,
            "days": days,
            "entries": len(values),
            "first_value": first_value,
            "last_value": last_value,
            "change": change,
            "percent_change": round(percent_change, 1),
            "trend": "increasing" if change > 0 else "decreasing" if change < 0 else "stable",
        }
    
    def get_metrics(self) -> List[str]:
        """Get list of all tracked metrics."""
        return list(set(e.metric for e in self.entries))
    
    def import_batch(
        self,
        entries: List[Dict],
        source: EntrySource = EntrySource.IMPORT,
        device: Optional[str] = None,
    ) -> Dict[str, int]:
        """
        Import multiple entries at once (for batch imports from devices).
        
        Args:
            entries: List of entry dictionaries
            source: Source type for all entries
            device: Device name for all entries
            
        Returns:
            Dictionary with import statistics
        """
        stats = {"added": 0, "skipped": 0, "errors": 0}
        
        for entry_data in entries:
            try:
                # Check for duplicate (by source_id)
                if entry_data.get("source_id"):
                    existing = [e for e in self.entries if e.source_id == entry_data["source_id"]]
                    if existing:
                        stats["skipped"] += 1
                        continue
                
                # Add entry
                self.add_entry(
                    metric=entry_data["metric"],
                    value=entry_data["value"],
                    unit=entry_data.get("unit"),
                    timestamp=entry_data.get("timestamp"),
                    source=source,
                    source_device=entry_data.get("source_device") or device,
                    source_id=entry_data.get("source_id"),
                    tags=entry_data.get("tags"),
                    notes=entry_data.get("notes"),
                    context=entry_data.get("context"),
                )
                stats["added"] += 1
                
            except Exception as e:
                stats["errors"] += 1
                if stats["errors"] <= 5:  # Limit error logging
                    print(f"Import error: {e}")
        
        return stats
    
    def export_json(self, filepath: str) -> None:
        """Export diary to JSON file."""
        data = {
            "user_id": self.user_id,
            "name": self.name,
            "exported_at": datetime.now().isoformat(),
            "entries": [e.to_dict() for e in self.entries],
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def import_json(self, filepath: str) -> int:
        """Import diary from JSON file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
        for entry_data in data.get("entries", []):
            self.add_entry(
                metric=entry_data["metric"],
                value=entry_data["value"],
                unit=entry_data.get("unit"),
                timestamp=datetime.fromisoformat(entry_data["timestamp"]) if entry_data.get("timestamp") else None,
                source=EntrySource(entry_data["source"]) if entry_data.get("source") else EntrySource.IMPORT,
                source_device=entry_data.get("source_device"),
                source_id=entry_data.get("source_id"),
                tags=entry_data.get("tags"),
                notes=entry_data.get("notes"),
                context=entry_data.get("context"),
                validate=False,  # Skip validation on import
            )
            count += 1
        
        return count


# Convenience functions
def create_diary(user_id: str, name: Optional[str] = None) -> Diary:
    """Create a new diary for a user."""
    return Diary(user_id=user_id, name=name)


__all__ = [
    'Diary',
    'DiaryEntry',
    'MetricDefinition',
    'EntrySource',
    'AggregationType',
    'create_diary',
    'MedicationDiary',
    'MedicationSchedule',
    'MedicationIntake',
    'Frequency',
    'IntakeTime',
]
