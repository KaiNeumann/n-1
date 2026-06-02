"""
Activities system for tracking exercise and physical activity effects on biomarkers.

This module provides models and analysis for understanding how physical activities
affect blood test values, similar to how foods affect biomarkers through nutrition.

Example:
    >>> from blutwerte.activities import Activity, ActivitySession, load_activities
    >>>
    >>> # Look up an activity
    >>> running = load_activities()["running"]
    >>>
    >>> # Log a session
    >>> session = ActivitySession(
    ...     activity=running,
    ...     duration_minutes=30,
    ...     intensity=IntensityLevel.MODERATE,
    ...     timestamp=datetime.now()
    ... )
    >>>
    >>> # Check effects
    >>> effects = session.get_effects()
    >>> for effect in effects:
    ...     print(f"{effect.target_name}: {effect.direction.value}")
"""

from .models import (
    Activity,
    ActivityEffect,
    ActivitySession,
    WeeklyActivitySummary,
    ActivityCategory,
    IntensityLevel,
)
from .jsonl_loader import load_activities, load_activities_from_jsonl, load_activities_from_python

__all__ = [
    # Models
    "Activity",
    "ActivityEffect",
    "ActivitySession",
    "WeeklyActivitySummary",
    # Enums
    "ActivityCategory",
    "IntensityLevel",
    # JSONL loaders
    "load_activities",
    "load_activities_from_jsonl",
    "load_activities_from_python",
]
