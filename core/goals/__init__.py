"""
Goals & Progress Tracking Module

Track health goals, monitor progress, and celebrate achievements.

Example Usage:
    >>> from core.goals import GoalManager, Goal, GoalType
    >>> 
    >>> manager = GoalManager(user_id="user001")
    >>> 
    >>> # Add biomarker goals
    >>> manager.add_biomarker_goal("ldl", target=100, priority="high")
    >>> manager.add_biomarker_goal("vitamin_d", target=40, priority="medium")
    >>> 
    >>> # Track progress
    >>> progress = manager.get_progress("ldl")
    >>> print(f"LDL progress: {progress.percentage}%")
    >>> 
    >>> # Get all active goals
    >>> goals = manager.get_active_goals()
"""

from datetime import datetime, date, timedelta
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import json


class GoalType(Enum):
    BIOMARKER = "biomarker"       # LDL, Vitamin D, etc.
    WEIGHT = "weight"             # Body weight goal
    VITAL = "vital"               # Blood pressure, pulse
    HABIT = "habit"               # Daily habits (steps, sleep)
    COMPOUND = "compound"         # Multiple metrics combined


class GoalDirection(Enum):
    LOWER = "lower"               # Want to decrease (LDL, weight)
    HIGHER = "higher"             # Want to increase (HDL, vitamin D)
    MAINTAIN = "maintain"         # Want to stay stable
    RANGE = "range"               # Want to be in a range


class GoalPriority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class MilestoneType(Enum):
    STARTED = "started"           # Just started the goal
    PROGRESS_25 = "progress_25"   # 25% towards goal
    PROGRESS_50 = "progress_50"   # 50% towards goal
    PROGRESS_75 = "progress_75"   # 75% towards goal
    ACHIEVED = "achieved"         # Goal achieved
    MAINTAINED = "maintained"     # Maintained for 30+ days
    STREAK = "streak"             # Streak achievement


@dataclass
class Goal:
    """A health goal."""
    id: str
    name: str
    goal_type: GoalType
    
    # Target
    target_value: float
    direction: GoalDirection
    target_min: Optional[float] = None  # For RANGE goals
    target_max: Optional[float] = None  # For RANGE goals
    
    # Starting point
    start_value: Optional[float] = None
    start_date: date = field(default_factory=date.today)
    target_date: Optional[date] = None
    
    # Context
    metric: str = ""              # e.g., "ldl", "weight"
    unit: str = ""
    priority: GoalPriority = GoalPriority.MEDIUM
    description: str = ""
    
    # Tracking
    is_active: bool = True
    is_achieved: bool = False
    achieved_date: Optional[date] = None
    
    # Streaks
    current_streak: int = 0
    longest_streak: int = 0
    
    def get_progress_percentage(
        self,
        current_value: float,
    ) -> float:
        """Calculate progress percentage towards goal."""
        if self.is_achieved:
            return 100.0
        
        if self.start_value is None:
            return 0.0
        
        if self.direction == GoalDirection.LOWER:
            # Want to go from start_value down to target_value
            total_needed = self.start_value - self.target_value
            if total_needed <= 0:
                return 100.0  # Already at or below target
            achieved = self.start_value - current_value
            return max(0, min(100, (achieved / total_needed) * 100))
        
        elif self.direction == GoalDirection.HIGHER:
            # Want to go from start_value up to target_value
            total_needed = self.target_value - self.start_value
            if total_needed <= 0:
                return 100.0  # Already at or above target
            achieved = current_value - self.start_value
            return max(0, min(100, (achieved / total_needed) * 100))
        
        elif self.direction == GoalDirection.RANGE:
            # Want to be in range
            if self.target_min and self.target_max:
                if self.target_min <= current_value <= self.target_max:
                    return 100.0
                elif current_value < self.target_min:
                    return max(0, 100 - (self.target_min - current_value) * 10)
                else:
                    return max(0, 100 - (current_value - self.target_max) * 10)
        
        elif self.direction == GoalDirection.MAINTAIN:
            # Want to stay stable - check if within tolerance
            if self.target_value:
                tolerance = self.target_value * 0.05  # 5% tolerance
                if abs(current_value - self.target_value) <= tolerance:
                    return 100.0
                return max(0, 100 - abs(current_value - self.target_value) / tolerance * 100)
        
        return 0.0
    
    def is_goal_met(self, current_value: float) -> bool:
        """Check if goal is met."""
        if self.direction == GoalDirection.LOWER:
            return current_value <= self.target_value
        elif self.direction == GoalDirection.HIGHER:
            return current_value >= self.target_value
        elif self.direction == GoalDirection.RANGE:
            if self.target_min and self.target_max:
                return self.target_min <= current_value <= self.target_max
        elif self.direction == GoalDirection.MAINTAIN:
            if self.target_value:
                return abs(current_value - self.target_value) <= self.target_value * 0.05
        return False


@dataclass
class GoalProgress:
    """Current progress towards a goal."""
    goal: Goal
    current_value: Optional[float]
    previous_value: Optional[float]
    percentage: float
    is_achieved: bool
    days_remaining: Optional[int]
    trend: str  # "improving", "declining", "stable"
    change_since_last: float
    projected_completion: Optional[date]
    notes: List[str] = field(default_factory=list)


@dataclass
class Milestone:
    """A milestone/achievement."""
    id: str
    goal_id: str
    milestone_type: MilestoneType
    achieved_date: date
    value_at_milestone: float
    description: str


@dataclass
class Achievement:
    """A badge or achievement."""
    id: str
    name: str
    description: str
    category: str  # "biomarker", "habit", "streak", "consistency"
    icon: str = ""
    achieved_date: Optional[date] = None
    progress: float = 0.0  # 0-100 if not yet achieved


class GoalManager:
    """
    Manages health goals and tracks progress.
    """
    
    # Default biomarker goals (recommended targets)
    DEFAULT_BIOMARKER_TARGETS = {
        "ldl": {"target": 100, "direction": "lower", "unit": "mg/dL"},
        "hdl": {"target": 60, "direction": "higher", "unit": "mg/dL"},
        "triglycerides": {"target": 150, "direction": "lower", "unit": "mg/dL"},
        "total_cholesterol": {"target": 200, "direction": "lower", "unit": "mg/dL"},
        "vitamin_d": {"target": 40, "direction": "higher", "unit": "ng/mL"},
        "ferritin": {"target": 50, "direction": "higher", "unit": "ng/mL"},
        "glucose": {"target": 100, "direction": "lower", "unit": "mg/dL"},
        "hba1c": {"target": 5.5, "direction": "lower", "unit": "%"},
        "crp": {"target": 1.0, "direction": "lower", "unit": "mg/L"},
        "bp_systolic": {"target": 120, "direction": "lower", "unit": "mmHg"},
        "bp_diastolic": {"target": 80, "direction": "lower", "unit": "mmHg"},
    }
    
    # Habit targets
    DEFAULT_HABIT_TARGETS = {
        "steps": {"target": 10000, "unit": "steps/day"},
        "sleep_hours": {"target": 8, "unit": "hours"},
        "water_intake": {"target": 2000, "unit": "ml"},
        "exercise_minutes": {"target": 150, "unit": "min/week"},
    }
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.goals: List[Goal] = []
        self.milestones: List[Milestone] = []
        self.achievements: List[Achievement] = []
        self._goal_counter = 0
    
    def _generate_id(self) -> str:
        self._goal_counter += 1
        return f"{self.user_id}_goal_{self._goal_counter}"
    
    def add_biomarker_goal(
        self,
        metric: str,
        target: float,
        direction: str = "lower",
        priority: str = "medium",
        description: str = "",
        target_date: Optional[date] = None,
    ) -> Goal:
        """Add a biomarker goal."""
        direction_enum = GoalDirection(direction)
        priority_enum = GoalPriority(priority)
        
        goal = Goal(
            id=self._generate_id(),
            name=f"{metric.upper()} {direction}",
            goal_type=GoalType.BIOMARKER,
            target_value=target,
            direction=direction_enum,
            metric=metric,
            unit=self.DEFAULT_BIOMARKER_TARGETS.get(metric, {}).get("unit", ""),
            priority=priority_enum,
            description=description or f"Target {metric} {direction} to {target}",
            target_date=target_date,
        )
        
        self.goals.append(goal)
        self._check_milestone(goal, None, "started")
        
        return goal
    
    def add_weight_goal(
        self,
        target_weight: float,
        current_weight: float,
        direction: str = "lower",
        priority: str = "medium",
        target_date: Optional[date] = None,
    ) -> Goal:
        """Add a weight goal."""
        direction_enum = GoalDirection(direction)
        
        goal = Goal(
            id=self._generate_id(),
            name=f"Weight {direction}",
            goal_type=GoalType.WEIGHT,
            target_value=target_weight,
            direction=direction_enum,
            start_value=current_weight,
            metric="weight",
            unit="kg",
            priority=GoalPriority(priority),
            description=f"Target weight: {target_weight} kg",
            target_date=target_date,
        )
        
        self.goals.append(goal)
        self._check_milestone(goal, current_weight, "started")
        
        return goal
    
    def add_habit_goal(
        self,
        habit: str,
        target: float,
        frequency: str = "daily",  # daily, weekly
        priority: str = "medium",
    ) -> Goal:
        """Add a habit goal (steps, sleep, etc.)."""
        direction = GoalDirection.HIGHER if target > 0 else GoalDirection.LOWER
        
        goal = Goal(
            id=self._generate_id(),
            name=f"{habit} Goal",
            goal_type=GoalType.HABIT,
            target_value=target,
            direction=direction,
            metric=habit,
            unit=self.DEFAULT_HABIT_TARGETS.get(habit, {}).get("unit", ""),
            priority=GoalPriority(priority),
            description=f"Target: {target} {self.DEFAULT_HABIT_TARGETS.get(habit, {}).get('unit', '')} {frequency}",
        )
        
        self.goals.append(goal)
        
        return goal
    
    def add_compound_goal(
        self,
        name: str,
        metrics: List[Dict[str, Any]],
        priority: str = "medium",
    ) -> Goal:
        """Add a goal tracking multiple metrics."""
        
        goal = Goal(
            id=self._generate_id(),
            name=name,
            goal_type=GoalType.COMPOUND,
            target_value=0,
            direction=GoalDirection.MAINTAIN,
            priority=GoalPriority(priority),
            description=f"Compound goal: {name}",
            metric=",".join(m["metric"] for m in metrics),
        )
        
        self.goals.append(goal)
        return goal
    
    def get_goal(self, goal_id: str) -> Optional[Goal]:
        """Get a specific goal."""
        for goal in self.goals:
            if goal.id == goal_id:
                return goal
        return None
    
    def get_goal_by_metric(self, metric: str) -> Optional[Goal]:
        """Get goal for a specific metric."""
        for goal in self.goals:
            if goal.metric == metric and goal.is_active:
                return goal
        return None
    
    def get_active_goals(
        self,
        goal_type: Optional[GoalType] = None,
        priority: Optional[GoalPriority] = None,
    ) -> List[Goal]:
        """Get active goals with optional filters."""
        goals = [g for g in self.goals if g.is_active]
        
        if goal_type:
            goals = [g for g in goals if g.goal_type == goal_type]
        
        if priority:
            goals = [g for g in goals if g.priority == priority]
        
        # Sort by priority
        priority_order = {GoalPriority.HIGH: 0, GoalPriority.MEDIUM: 1, GoalPriority.LOW: 2}
        goals.sort(key=lambda g: priority_order.get(g.priority, 3))
        
        return goals
    
    def update_goal_progress(
        self,
        metric: str,
        current_value: float,
        check_date: Optional[date] = None,
    ) -> Optional[GoalProgress]:
        """Update progress for a goal and return progress info."""
        today = check_date or date.today()
        
        goal = self.get_goal_by_metric(metric)
        if not goal:
            return None
        
        # Get previous value from last milestone or start
        previous_value = goal.start_value
        
        # Set start value if not yet set (first measurement becomes baseline)
        if goal.start_value is None:
            goal.start_value = current_value
            previous_value = current_value  # No previous for first measurement
        
        # Calculate progress
        percentage = goal.get_progress_percentage(current_value)
        is_achieved = goal.is_goal_met(current_value)
        
        # Calculate days remaining
        days_remaining = None
        projected_completion = None
        if goal.target_date and not is_achieved:
            days_remaining = (goal.target_date - today).days
            # Project when goal will be achieved based on current rate
            if goal.start_value and current_value != goal.start_value:
                days_elapsed = (today - goal.start_date).days
                if days_elapsed > 0:
                    rate = (goal.start_value - current_value) / days_elapsed
                    if rate != 0:
                        remaining = goal.start_value - goal.target_value
                        projected_days = int(remaining / rate)
                        projected_completion = today + timedelta(days=projected_days)
        
        # Determine trend
        trend = "stable"
        if previous_value and previous_value != current_value:
            if goal.direction == GoalDirection.LOWER:
                trend = "improving" if current_value < previous_value else "declining"
            else:
                trend = "improving" if current_value > previous_value else "declining"
        
        # Calculate change since last
        change_since_last = 0.0
        if previous_value:
            change_since_last = current_value - previous_value
        
        # Update goal if achieved
        if is_achieved and not goal.is_achieved:
            goal.is_achieved = True
            goal.is_active = False
            goal.achieved_date = today
            self._check_milestone(goal, current_value, "achieved")
        
        # Check milestones
        self._check_milestone(goal, current_value)
        
        return GoalProgress(
            goal=goal,
            current_value=current_value,
            previous_value=previous_value,
            percentage=percentage,
            is_achieved=is_achieved,
            days_remaining=days_remaining,
            trend=trend,
            change_since_last=change_since_last,
            projected_completion=projected_completion,
        )
    
    def _check_milestone(
        self,
        goal: Goal,
        current_value: Optional[float],
        force_type: Optional[str] = None,
    ):
        """Check and record milestones."""
        if current_value is None:
            return
        
        percentage = goal.get_progress_percentage(current_value)
        
        milestone_type = None
        
        if force_type == "started":
            milestone_type = MilestoneType.STARTED
        elif force_type == "achieved" or percentage >= 100:
            milestone_type = MilestoneType.ACHIEVED
        elif percentage >= 75:
            milestone_type = MilestoneType.PROGRESS_75
        elif percentage >= 50:
            milestone_type = MilestoneType.PROGRESS_50
        elif percentage >= 25:
            milestone_type = MilestoneType.PROGRESS_25
        
        if milestone_type:
            # Check if already recorded
            existing = [m for m in self.milestones 
                       if m.goal_id == goal.id and m.milestone_type == milestone_type]
            if not existing:
                milestone = Milestone(
                    id=f"{goal.id}_ms_{milestone_type.value}",
                    goal_id=goal.id,
                    milestone_type=milestone_type,
                    achieved_date=date.today(),
                    value_at_milestone=current_value,
                    description=f"{goal.name}: {milestone_type.value}",
                )
                self.milestones.append(milestone)
    
    def get_progress(
        self,
        metric: str,
        current_value: float,
    ) -> Optional[GoalProgress]:
        """Get progress for a specific metric."""
        return self.update_goal_progress(metric, current_value)
    
    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get summary for dashboard."""
        active_goals = self.get_active_goals()
        
        summary = {
            "total_goals": len(self.goals),
            "active_goals": len(active_goals),
            "achieved_goals": len([g for g in self.goals if g.is_achieved]),
            "high_priority_active": len([g for g in active_goals if g.priority == GoalPriority.HIGH]),
            "milestones_achieved": len(self.milestones),
            "goals_by_type": {},
            "goals_by_priority": {},
        }
        
        # Count by type
        for goal_type in GoalType:
            count = len([g for g in self.goals if g.goal_type == goal_type])
            summary["goals_by_type"][goal_type.value] = count
        
        # Count by priority
        for priority in GoalPriority:
            count = len([g for g in active_goals if g.priority == priority])
            summary["goals_by_priority"][priority.value] = count
        
        return summary
    
    def generate_recommendations(self) -> List[str]:
        """Generate recommendations based on goals and progress."""
        recommendations = []
        
        active_goals = self.get_active_goals()
        
        for goal in active_goals:
            if goal.goal_type == GoalType.BIOMARKER:
                recommendations.append(
                    f"Continue working on your {goal.metric} goal"
                )
            elif goal.goal_type == GoalType.HABIT:
                recommendations.append(
                    f"Track your {goal.metric} daily to maintain progress"
                )
        
        return recommendations
    
    def export_json(self, filepath: str):
        """Export goals to JSON."""
        data = {
            "user_id": self.user_id,
            "exported_at": datetime.now().isoformat(),
            "goals": [
                {
                    "id": g.id,
                    "name": g.name,
                    "goal_type": g.goal_type.value,
                    "target_value": g.target_value,
                    "direction": g.direction.value,
                    "target_min": g.target_min,
                    "target_max": g.target_max,
                    "start_value": g.start_value,
                    "start_date": g.start_date.isoformat() if g.start_date else None,
                    "target_date": g.target_date.isoformat() if g.target_date else None,
                    "metric": g.metric,
                    "unit": g.unit,
                    "priority": g.priority.value,
                    "description": g.description,
                    "is_active": g.is_active,
                    "is_achieved": g.is_achieved,
                    "achieved_date": g.achieved_date.isoformat() if g.achieved_date else None,
                }
                for g in self.goals
            ],
            "milestones": [
                {
                    "id": m.id,
                    "goal_id": m.goal_id,
                    "milestone_type": m.milestone_type.value,
                    "achieved_date": m.achieved_date.isoformat(),
                    "value_at_milestone": m.value_at_milestone,
                    "description": m.description,
                }
                for m in self.milestones
            ],
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def import_json(self, filepath: str) -> int:
        """Import goals from JSON."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
        
        for g_data in data.get("goals", []):
            goal = Goal(
                id=g_data["id"],
                name=g_data["name"],
                goal_type=GoalType(g_data["goal_type"]),
                target_value=g_data["target_value"],
                direction=GoalDirection(g_data["direction"]),
                target_min=g_data.get("target_min"),
                target_max=g_data.get("target_max"),
                start_value=g_data.get("start_value"),
                start_date=date.fromisoformat(g_data["start_date"]) if g_data.get("start_date") else date.today(),
                target_date=date.fromisoformat(g_data["target_date"]) if g_data.get("target_date") else None,
                metric=g_data.get("metric", ""),
                unit=g_data.get("unit", ""),
                priority=GoalPriority(g_data.get("priority", "medium")),
                description=g_data.get("description", ""),
                is_active=g_data.get("is_active", True),
                is_achieved=g_data.get("is_achieved", False),
                achieved_date=date.fromisoformat(g_data["achieved_date"]) if g_data.get("achieved_date") else None,
            )
            self.goals.append(goal)
            count += 1
        
        return count


class ProgressTracker:
    """
    Tracks progress over time for any metric.
    Works with diary data to show trends.
    """
    
    def __init__(self, diary=None, blood_tests=None, goal_manager: Optional[GoalManager] = None):
        self.diary = diary
        self.blood_tests = blood_tests or []
        self.goal_manager = goal_manager
    
    def get_metric_history(
        self,
        metric: str,
        days: int = 30,
        source: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get history of a metric."""
        if not self.diary:
            return []
        
        entries = self.diary.get_entries(
            metric=metric,
            days=days,
        )
        
        if source:
            entries = [e for e in entries if e.source_device == source]
        
        return [
            {
                "date": e.timestamp.date(),
                "value": e.value,
                "source": e.source.value if hasattr(e.source, 'value') else str(e.source),
            }
            for e in entries
        ]
    
    def get_average(self, metric: str, days: int = 30) -> Optional[float]:
        """Get average value for a metric."""
        history = self.get_metric_history(metric, days)
        
        values = []
        for entry in history:
            if isinstance(entry["value"], (int, float)):
                values.append(float(entry["value"]))
            elif isinstance(entry["value"], dict):
                # Handle compound values like blood pressure
                if "systolic" in entry["value"]:
                    values.append(float(entry["value"]["systolic"]))
        
        if values:
            return sum(values) / len(values)
        return None
    
    def get_weekly_summary(self, days: int = 7) -> Dict[str, Any]:
        """Get weekly summary of all tracked metrics."""
        summary = {
            "period_days": days,
            "metrics": {},
        }
        
        if not self.diary:
            return summary
        
        # Get all unique metrics
        metrics = self.diary.get_metrics()
        
        for metric in metrics:
            avg = self.get_average(metric, days)
            if avg is not None:
                history = self.get_metric_history(metric, days)
                values = [h["value"] for h in history if isinstance(h["value"], (int, float))]
                
                summary["metrics"][metric] = {
                    "average": round(avg, 2),
                    "entries": len(values),
                    "min": min(values) if values else None,
                    "max": max(values) if values else None,
                }
                
                # Check goal progress if available
                if self.goal_manager:
                    progress = self.goal_manager.get_progress(metric, avg)
                    if progress:
                        summary["metrics"][metric]["goal_progress"] = {
                            "percentage": round(progress.percentage, 1),
                            "is_achieved": progress.is_achieved,
                            "trend": progress.trend,
                        }
        
        return summary


__all__ = [
    'GoalManager',
    'Goal',
    'GoalType',
    'GoalDirection',
    'GoalPriority',
    'GoalProgress',
    'Milestone',
    'MilestoneType',
    'Achievement',
    'ProgressTracker',
]
