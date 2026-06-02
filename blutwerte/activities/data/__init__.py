"""
Activity data module.

Comprehensive activity library with documented biomarker effects.
Includes activities from all categories: cardio, strength, flexibility,
walking, sports, daily living, household, and sedentary activities.
"""

from .common_activities import (
    # Cardio
    create_running,
    create_jogging,
    create_cycling,
    create_swimming,
    create_hiit,
    # Strength
    create_weight_training,
    create_strength_training_light,
    create_strength_training_vigorous,
    # Flexibility
    create_yoga,
    create_pilates,
    # Walking
    create_walking_slow,
    create_walking_moderate,
    create_walking_brisk,
    create_walking_uphill,
    create_hiking,
    # Sports
    create_basketball,
    create_tennis,
    create_dancing_aerobic,
    create_dancing_ballroom,
    # Daily Living
    create_sleeping,
    create_eating_sitting,
    create_grooming,
    create_showering,
    # Sedentary
    create_sitting_inactive,
    create_sitting_active,
    create_lying_resting,
    create_meditating,
    # Household
    create_cleaning_light,
    create_cleaning_heavy,
    create_vacuuming,
    create_mopping,
    create_cooking,
    create_dishwashing,
    create_laundry,
    create_ironing,
    create_gardening,
    create_gardening_digging,
    create_mowing_lawn,
    create_raking_leaves,
    create_sweeping,
    create_carrying_groceries,
    create_moving_furniture,
    create_stair_climbing,
    # Transportation
    create_driving,
    create_driving_heavy_traffic,
    create_riding_bus_train,
    create_cycling_transport,
    create_walking_transport,
    # Recreation/Work
    create_playing_with_children,
    create_walking_dog,
    create_shopping_light,
    create_shopping_heavy,
    create_reading,
    create_watching_tv,
    create_standing_light,
    create_sitting_meeting,
    create_desk_work_sitting,
    create_desk_work_standing,
    # Export
    get_all_activities,
)

__all__ = [
    # Cardio
    "create_running", "create_jogging", "create_cycling", "create_swimming", "create_hiit",
    # Strength
    "create_weight_training", "create_strength_training_light", "create_strength_training_vigorous",
    # Flexibility
    "create_yoga", "create_pilates",
    # Walking
    "create_walking_slow", "create_walking_moderate", "create_walking_brisk", "create_walking_uphill", "create_hiking",
    # Sports
    "create_basketball", "create_tennis", "create_dancing_aerobic", "create_dancing_ballroom",
    # Daily Living
    "create_sleeping", "create_eating_sitting", "create_grooming", "create_showering",
    # Sedentary
    "create_sitting_inactive", "create_sitting_active", "create_lying_resting", "create_meditating",
    # Household
    "create_cleaning_light", "create_cleaning_heavy", "create_vacuuming", "create_mopping",
    "create_cooking", "create_dishwashing", "create_laundry", "create_ironing",
    "create_gardening", "create_gardening_digging", "create_mowing_lawn", "create_raking_leaves",
    "create_sweeping", "create_carrying_groceries", "create_moving_furniture", "create_stair_climbing",
    # Transportation
    "create_driving", "create_driving_heavy_traffic", "create_riding_bus_train",
    "create_cycling_transport", "create_walking_transport",
    # Recreation/Work
    "create_playing_with_children", "create_walking_dog", "create_shopping_light", "create_shopping_heavy",
    "create_reading", "create_watching_tv", "create_standing_light",
    "create_sitting_meeting", "create_desk_work_sitting", "create_desk_work_standing",
    # Export
    "get_all_activities",
]
