"""
Core data models for the activities system.

Activities represent physical exercises and their effects on biomarkers.
Unlike foods (nutrition) and medications (pharmacology), activities affect
biomarkers through physical stress, calorie expenditure, and hormonal responses.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from enum import Enum

from core.medications.models import EffectTargetType, EffectDirection
from core.foods.sources import DataSource


class ActivityCategory(Enum):
    """Categories of physical activities."""
    CARDIO = "cardio"                    # Running, cycling, swimming
    STRENGTH = "strength"                # Weight lifting, resistance training
    FLEXIBILITY = "flexibility"          # Yoga, stretching
    SPORTS = "sports"                    # Team sports, racquet sports, dancing
    HIGH_INTENSITY = "high_intensity"    # HIIT, CrossFit
    WALKING = "walking"                  # All walking activities
    DAILY_LIVING = "daily_living"        # Eating, grooming, showering
    SEDENTARY = "sedentary"              # Sleeping, sitting, resting
    HOUSEHOLD = "household"              # Cleaning, cooking, gardening
    TRANSPORTATION = "transportation"    # Driving, cycling as transport
    RECREATION = "recreation"            # Reading, shopping, leisure
    WORK = "work"                        # Desk work, meetings


class IntensityLevel(Enum):
    """Intensity levels for activities."""
    REST = "rest"                        # Resting, sleeping, minimal activity
    LOW = "low"                          # Easy conversation possible
    MODERATE = "moderate"                # Slightly breathless, can talk
    HIGH = "high"                        # Breathless, difficult to talk
    MAXIMAL = "maximal"                  # Maximum effort, cannot talk


@dataclass
class ActivityEffect:
    """
    How an activity affects a biomarker or vital sign.
    
    Unlike food effects (nutritional), activity effects depend on:
    - Duration of activity
    - Intensity level
    - Individual fitness level
    - Acute vs chronic exposure
    
    Attributes:
        target_type: Type of target (BIOMARKER, VITAL_SIGN)
        target_name: Name of the target (e.g., "CRP", "Heart Rate", "Cortisol")
        direction: Effect direction (INCREASE, DECREASE, VARIABLE)
        mechanism: How the effect occurs
        duration_dependent: Whether effect varies by activity duration
        intensity_dependent: Whether effect varies by intensity
        acute_effect: Effect immediately after activity
        chronic_effect: Effect from regular training (if different)
        sources: Research sources documenting this effect
    """
    target_type: EffectTargetType
    target_name: str
    direction: EffectDirection
    mechanism: str
    duration_dependent: bool = True
    intensity_dependent: bool = True
    acute_effect: Optional[str] = None  # e.g., "Increases during and immediately after"
    chronic_effect: Optional[str] = None  # e.g., "Decreases with regular training"
    sources: List[DataSource] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate that sources are provided."""
        # Sources are recommended but not strictly required for all effects
        # Some well-established effects (e.g., heart rate increase during exercise)
        # may not need individual citations
        pass


@dataclass
class Activity:
    """
    Physical activity with biomarker effects.
    
    Activities differ from foods in that their effects depend on:
    - How long you do them (duration)
    - How hard you do them (intensity)
    - Your fitness level (trained vs untrained)
    
    Attributes:
        name: Activity name (English)
        name_de: Activity name (German)
        category: Activity category
        description: Description of the activity
        calories_per_hour: Estimated calories burned per hour (average person)
        effects: List of biomarker effects
        intensity_range: Typical intensity range for this activity
        sources: Sources for activity data
    """
    name: str
    name_de: str
    category: ActivityCategory
    description: str
    calories_per_hour: float
    effects: List[ActivityEffect] = field(default_factory=list)
    intensity_range: List[IntensityLevel] = field(default_factory=list)
    sources: List[DataSource] = field(default_factory=list)
    
    def affects_biomarker(self, biomarker_name: str) -> List[ActivityEffect]:
        """
        Get all effects on a specific biomarker.
        
        Args:
            biomarker_name: Name of the biomarker
            
        Returns:
            List of ActivityEffect objects
        """
        return [
            effect for effect in self.effects
            if effect.target_name.lower() == biomarker_name.lower()
        ]
    
    def get_effects_by_intensity(self, intensity: IntensityLevel) -> List[ActivityEffect]:
        """
        Get effects relevant to a specific intensity level.
        
        Args:
            intensity: Intensity level
            
        Returns:
            List of ActivityEffect objects
        """
        if not self.intensity_range or intensity in self.intensity_range:
            return self.effects
        return []


@dataclass
class ActivitySession:
    """
    A specific instance of activity performed.
    
    This tracks actual activity data for a patient, similar to FoodIntake
    for foods.
    
    Attributes:
        activity: The Activity performed
        duration_minutes: How long the activity lasted
        intensity: Actual intensity level (may differ from activity default)
        timestamp: When the activity was performed
        calories_burned: Estimated calories burned (optional, can be calculated)
        heart_rate_avg: Average heart rate during activity (if tracked)
        heart_rate_max: Maximum heart rate during activity (if tracked)
        notes: Additional notes (e.g., "Felt tired", "PR achieved")
    """
    activity: Activity
    duration_minutes: int
    intensity: IntensityLevel
    timestamp: datetime
    calories_burned: Optional[float] = None
    heart_rate_avg: Optional[int] = None
    heart_rate_max: Optional[int] = None
    notes: Optional[str] = None
    
    def __post_init__(self):
        """Calculate calories if not provided."""
        if self.calories_burned is None:
            # Simple calculation: calories per hour * duration in hours
            hours = self.duration_minutes / 60
            self.calories_burned = self.activity.calories_per_hour * hours
    
    def get_effects(self) -> List[ActivityEffect]:
        """
        Get activity effects relevant to this session.
        
        Returns:
            List of ActivityEffect objects
        """
        return self.activity.get_effects_by_intensity(self.intensity)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "activity": self.activity.name,
            "duration_minutes": self.duration_minutes,
            "intensity": self.intensity.value,
            "timestamp": self.timestamp.isoformat(),
            "calories_burned": self.calories_burned,
            "heart_rate_avg": self.heart_rate_avg,
            "heart_rate_max": self.heart_rate_max,
            "notes": self.notes,
        }


@dataclass
class WeeklyActivitySummary:
    """
    Summary of activity over a week.
    
    Useful for tracking training load and its effects on biomarkers.
    
    Attributes:
        week_start: Start of the week
        total_sessions: Number of activity sessions
        total_duration_minutes: Total active time
        total_calories_burned: Total calories burned
        activities_by_category: Breakdown by category
        average_intensity: Average intensity across all sessions
    """
    week_start: datetime
    total_sessions: int = 0
    total_duration_minutes: int = 0
    total_calories_burned: float = 0.0
    activities_by_category: Dict[ActivityCategory, int] = field(default_factory=dict)
    average_intensity: Optional[IntensityLevel] = None
    
    @classmethod
    def from_sessions(cls, sessions: List[ActivitySession], week_start: datetime) -> 'WeeklyActivitySummary':
        """
        Create summary from list of sessions.
        
        Args:
            sessions: List of ActivitySession objects
            week_start: Start of week datetime
            
        Returns:
            WeeklyActivitySummary
        """
        summary = cls(week_start=week_start)
        
        for session in sessions:
            summary.total_sessions += 1
            summary.total_duration_minutes += session.duration_minutes
            summary.total_calories_burned += session.calories_burned or 0
            
            # Count by category
            category = session.activity.category
            summary.activities_by_category[category] = (
                summary.activities_by_category.get(category, 0) + 1
            )
        
        return summary
