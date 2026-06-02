"""
Comprehensive physical activities with biomarker effects.

This module defines activities across all categories and their documented effects
on blood biomarkers based on exercise physiology research.

Sources:
- American College of Sports Medicine (ACSM) guidelines
- Compendium of Physical Activities (Ainsworth et al.)
- Exercise physiology research
- Sports medicine literature
"""

from .. import (
    Activity, ActivityEffect, ActivityCategory, IntensityLevel,
)
from blutwerte.foods.sources import DataSource, create_source
from blutwerte.medications.models import EffectTargetType, EffectDirection


# =============================================================================
# CARDIOVASCULAR ACTIVITIES
# =============================================================================

def create_running() -> Activity:
    """Running/Jogging - high-impact cardiovascular exercise."""
    source = create_source(
        url="https://www.ncbi.nlm.nih.gov/pmc/articles/PMCPMC7140055/",
        title="Exercise and circulating cortisol levels: the intensity threshold effect",
        source_type="research"
    )
    source2 = create_source(
        url="https://www.ncbi.nlm.nih.gov/pmc/articles/PMCPMC4769848/",
        title="The effects of acute exercise on serum biomarkers in healthy subjects",
        source_type="research"
    )
    
    return Activity(
        name="Running",
        name_de="Laufen",
        category=ActivityCategory.CARDIO,
        description="High-impact cardiovascular exercise involving running at various speeds",
        calories_per_hour=600,
        intensity_range=[IntensityLevel.MODERATE, IntensityLevel.HIGH, IntensityLevel.MAXIMAL],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.VITAL_SIGN,
                target_name="Heart Rate",
                direction=EffectDirection.INCREASE,
                mechanism="Cardiovascular demand increases heart rate proportionally to intensity",
                duration_dependent=True,
                intensity_dependent=True,
                acute_effect="Increases linearly with intensity (up to 180+ bpm)",
                chronic_effect="Decreases resting heart rate by 5-10 bpm with regular training",
                sources=[source]
            ),
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Cortisol",
                direction=EffectDirection.INCREASE,
                mechanism="Physical stress triggers HPA axis activation",
                duration_dependent=True,
                intensity_dependent=True,
                acute_effect="Increases 20-100% depending on intensity and duration",
                chronic_effect="Better stress response regulation with training",
                sources=[source]
            ),
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="CK",
                direction=EffectDirection.INCREASE,
                mechanism="Muscle damage releases creatine kinase into bloodstream",
                duration_dependent=True,
                intensity_dependent=True,
                acute_effect="Can increase 2-5x after intense or prolonged running",
                chronic_effect="Lower baseline CK in trained runners",
                sources=[source2]
            ),
        ],
        sources=[source, source2]
    )


def create_jogging() -> Activity:
    """Jogging - moderate intensity running."""
    return Activity(
        name="Jogging",
        name_de="Joggen",
        category=ActivityCategory.CARDIO,
        description="Moderate-paced running at sustainable intensity",
        calories_per_hour=500,
        intensity_range=[IntensityLevel.MODERATE],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.VITAL_SIGN,
                target_name="Heart Rate",
                direction=EffectDirection.INCREASE,
                mechanism="Cardiovascular demand",
                duration_dependent=True,
                intensity_dependent=True,
                acute_effect="Elevates to 60-75% max HR"
            ),
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="HDL",
                direction=EffectDirection.INCREASE,
                mechanism="Regular aerobic exercise improves lipid profile",
                chronic_effect="5-10% increase with regular training"
            ),
        ],
        sources=[]
    )


def create_cycling() -> Activity:
    """Cycling - low-impact cardiovascular exercise."""
    source = create_source(
        url="https://www.ncbi.nlm.nih.gov/pmc/articles/PMCPMC6097225/",
        title="Effects of cycling on biomarkers of cardiovascular health",
        source_type="research"
    )
    
    return Activity(
        name="Cycling",
        name_de="Radfahren",
        category=ActivityCategory.CARDIO,
        description="Low-impact cardiovascular exercise on bicycle",
        calories_per_hour=500,
        intensity_range=[IntensityLevel.LOW, IntensityLevel.MODERATE, IntensityLevel.HIGH],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.VITAL_SIGN,
                target_name="Heart Rate",
                direction=EffectDirection.INCREASE,
                mechanism="Cardiovascular demand",
                duration_dependent=True,
                intensity_dependent=True,
                sources=[source]
            ),
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Triglycerides",
                direction=EffectDirection.DECREASE,
                mechanism="Regular aerobic exercise improves lipid metabolism",
                chronic_effect="10-20% reduction with regular training",
                sources=[source]
            ),
        ],
        sources=[source]
    )


def create_swimming() -> Activity:
    """Swimming - full-body low-impact exercise."""
    source = create_source(
        url="https://www.ncbi.nlm.nih.gov/pmc/articles/PMCPMC6421859/",
        title="Swimming training and biomarkers of health",
        source_type="research"
    )
    
    return Activity(
        name="Swimming",
        name_de="Schwimmen",
        category=ActivityCategory.CARDIO,
        description="Full-body cardiovascular exercise in water",
        calories_per_hour=550,
        intensity_range=[IntensityLevel.MODERATE, IntensityLevel.HIGH],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="CRP",
                direction=EffectDirection.DECREASE,
                mechanism="Regular swimming reduces systemic inflammation",
                chronic_effect="15-30% reduction in CRP with regular training",
                sources=[source]
            ),
        ],
        sources=[source]
    )


def create_hiit() -> Activity:
    """High-Intensity Interval Training (HIIT)."""
    source = create_source(
        url="https://www.ncbi.nlm.nih.gov/pmc/articles/PMCPMC6762185/",
        title="High-intensity interval training and metabolic biomarkers",
        source_type="research"
    )
    
    return Activity(
        name="HIIT",
        name_de="HIIT (Hochintensives Intervalltraining)",
        category=ActivityCategory.HIGH_INTENSITY,
        description="High-intensity interval training with alternating intense bursts and recovery",
        calories_per_hour=700,
        intensity_range=[IntensityLevel.HIGH, IntensityLevel.MAXIMAL],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Cortisol",
                direction=EffectDirection.INCREASE,
                mechanism="High physiological stress triggers cortisol release",
                duration_dependent=True,
                intensity_dependent=True,
                acute_effect="Significant elevation, especially in untrained individuals",
                sources=[source]
            ),
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Glucose",
                direction=EffectDirection.DECREASE,
                mechanism="Rapid glycogen depletion during intense intervals",
                duration_dependent=True,
                intensity_dependent=True,
                acute_effect="Can drop significantly during and after session",
                sources=[source]
            ),
        ],
        sources=[source]
    )


# =============================================================================
# STRENGTH ACTIVITIES
# =============================================================================

def create_weight_training() -> Activity:
    """Weight/Strength training - resistance exercise."""
    source = create_source(
        url="https://pubmed.ncbi.nlm.nih.gov/28177828/",
        title="Creatine kinase response to resistance training",
        source_type="research"
    )
    source2 = create_source(
        url="https://www.ncbi.nlm.nih.gov/pmc/articles/PMCPMC6279909/",
        title="Hormonal responses to resistance exercise",
        source_type="research"
    )
    
    return Activity(
        name="Weight Training",
        name_de="Krafttraining",
        category=ActivityCategory.STRENGTH,
        description="Resistance exercise using weights or machines",
        calories_per_hour=400,
        intensity_range=[IntensityLevel.MODERATE, IntensityLevel.HIGH],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="CK",
                direction=EffectDirection.INCREASE,
                mechanism="Eccentric muscle contractions cause micro-damage",
                duration_dependent=True,
                intensity_dependent=True,
                acute_effect="Can increase 5-20x after intense session",
                chronic_effect="Lower baseline but still elevated after workouts",
                sources=[source]
            ),
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Testosterone",
                direction=EffectDirection.INCREASE,
                mechanism="Large muscle group activation stimulates hormone production",
                duration_dependent=True,
                intensity_dependent=True,
                acute_effect="15-25% increase post-workout (men)",
                chronic_effect="Improved testosterone-to-cortisol ratio with training",
                sources=[source2]
            ),
        ],
        sources=[source, source2]
    )


def create_strength_training_light() -> Activity:
    """Light strength training."""
    return Activity(
        name="Strength Training (Light)",
        name_de="Krafttraining (Leicht)",
        category=ActivityCategory.STRENGTH,
        description="Light resistance training with higher repetitions",
        calories_per_hour=250,
        intensity_range=[IntensityLevel.LOW, IntensityLevel.MODERATE],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="CK",
                direction=EffectDirection.INCREASE,
                mechanism="Minor muscle stress",
                acute_effect="Mild elevation 1-2x normal"
            ),
        ],
        sources=[]
    )


def create_strength_training_vigorous() -> Activity:
    """Vigorous strength training."""
    return Activity(
        name="Strength Training (Vigorous)",
        name_de="Krafttraining (Intensiv)",
        category=ActivityCategory.STRENGTH,
        description="Heavy resistance training with maximal effort",
        calories_per_hour=500,
        intensity_range=[IntensityLevel.HIGH],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="CK",
                direction=EffectDirection.INCREASE,
                mechanism="Significant muscle damage from heavy loads",
                acute_effect="Can increase 10-30x after intense session",
                duration_dependent=True
            ),
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Cortisol",
                direction=EffectDirection.INCREASE,
                mechanism="High physiological stress",
                acute_effect="Moderate elevation post-workout"
            ),
        ],
        sources=[]
    )


# =============================================================================
# FLEXIBILITY ACTIVITIES
# =============================================================================

def create_yoga() -> Activity:
    """Yoga - flexibility and mindfulness practice."""
    source = create_source(
        url="https://www.ncbi.nlm.nih.gov/pmc/articles/PMCPMC6145966/",
        title="Yoga and stress hormone regulation",
        source_type="research"
    )
    
    return Activity(
        name="Yoga",
        name_de="Yoga",
        category=ActivityCategory.FLEXIBILITY,
        description="Physical postures, breathing exercises, and meditation",
        calories_per_hour=200,
        intensity_range=[IntensityLevel.LOW, IntensityLevel.MODERATE],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Cortisol",
                direction=EffectDirection.DECREASE,
                mechanism="Parasympathetic activation and stress reduction",
                chronic_effect="10-20% reduction in baseline cortisol with regular practice",
                sources=[source]
            ),
        ],
        sources=[source]
    )


def create_pilates() -> Activity:
    """Pilates - core strength and flexibility."""
    return Activity(
        name="Pilates",
        name_de="Pilates",
        category=ActivityCategory.FLEXIBILITY,
        description="Core strengthening and flexibility exercise system",
        calories_per_hour=250,
        intensity_range=[IntensityLevel.LOW, IntensityLevel.MODERATE],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Cortisol",
                direction=EffectDirection.DECREASE,
                mechanism="Low-stress exercise with breathing focus",
                chronic_effect="Stress reduction with regular practice"
            ),
        ],
        sources=[]
    )


# =============================================================================
# WALKING ACTIVITIES
# =============================================================================

def create_walking_slow() -> Activity:
    """Slow walking - leisurely pace."""
    return Activity(
        name="Walking (Slow)",
        name_de="Gehen (Langsam)",
        category=ActivityCategory.WALKING,
        description="Walking at slow, leisurely pace (~2.5 mph)",
        calories_per_hour=180,
        intensity_range=[IntensityLevel.LOW],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.VITAL_SIGN,
                target_name="Heart Rate",
                direction=EffectDirection.INCREASE,
                mechanism="Minimal cardiovascular demand",
                acute_effect="Slight elevation above resting"
            ),
        ],
        sources=[]
    )


def create_walking_moderate() -> Activity:
    """Moderate walking - normal pace."""
    return Activity(
        name="Walking (Moderate)",
        name_de="Gehen (Mittel)",
        category=ActivityCategory.WALKING,
        description="Walking at normal pace (~3.5 mph)",
        calories_per_hour=250,
        intensity_range=[IntensityLevel.LOW, IntensityLevel.MODERATE],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Glucose",
                direction=EffectDirection.DECREASE,
                mechanism="Muscular glucose uptake",
                acute_effect="Modest glucose reduction",
                chronic_effect="Improved insulin sensitivity with regular walking"
            ),
        ],
        sources=[]
    )


def create_walking_brisk() -> Activity:
    """Brisk walking - exercise pace."""
    return Activity(
        name="Walking (Brisk)",
        name_de="Gehen (Schnell)",
        category=ActivityCategory.WALKING,
        description="Walking at brisk exercise pace (~4.0 mph)",
        calories_per_hour=320,
        intensity_range=[IntensityLevel.MODERATE],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.VITAL_SIGN,
                target_name="Heart Rate",
                direction=EffectDirection.INCREASE,
                mechanism="Cardiovascular demand",
                acute_effect="Elevates to 50-60% max HR"
            ),
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Triglycerides",
                direction=EffectDirection.DECREASE,
                mechanism="Regular aerobic activity improves lipid metabolism",
                chronic_effect="Modest improvements with regular brisk walking"
            ),
        ],
        sources=[]
    )


def create_walking_uphill() -> Activity:
    """Walking uphill - increased intensity."""
    return Activity(
        name="Walking (Uphill)",
        name_de="Gehen (Bergauf)",
        category=ActivityCategory.WALKING,
        description="Walking uphill or on incline",
        calories_per_hour=400,
        intensity_range=[IntensityLevel.MODERATE, IntensityLevel.HIGH],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.VITAL_SIGN,
                target_name="Heart Rate",
                direction=EffectDirection.INCREASE,
                mechanism="Increased workload from elevation gain",
                acute_effect="Significant elevation, comparable to light jogging"
            ),
        ],
        sources=[]
    )


def create_hiking() -> Activity:
    """Hiking - walking on trails/terrain."""
    return Activity(
        name="Hiking",
        name_de="Wandern",
        category=ActivityCategory.WALKING,
        description="Walking on natural terrain with elevation changes",
        calories_per_hour=450,
        intensity_range=[IntensityLevel.MODERATE, IntensityLevel.HIGH],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.VITAL_SIGN,
                target_name="Heart Rate",
                direction=EffectDirection.INCREASE,
                mechanism="Variable terrain increases cardiovascular demand",
                acute_effect="Moderate to high elevation depending on terrain"
            ),
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Vitamin D",
                direction=EffectDirection.INCREASE,
                mechanism="Sun exposure during outdoor activity",
                acute_effect="Synthesis in skin during daylight exposure",
                chronic_effect="Improved Vitamin D status with regular outdoor activity"
            ),
        ],
        sources=[]
    )


# =============================================================================
# SPORTS ACTIVITIES
# =============================================================================

def create_basketball() -> Activity:
    """Basketball - team sport."""
    return Activity(
        name="Basketball",
        name_de="Basketball",
        category=ActivityCategory.SPORTS,
        description="Team sport involving running, jumping, and quick movements",
        calories_per_hour=550,
        intensity_range=[IntensityLevel.MODERATE, IntensityLevel.HIGH],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.VITAL_SIGN,
                target_name="Heart Rate",
                direction=EffectDirection.INCREASE,
                mechanism="High-intensity intermittent activity",
                acute_effect="Highly variable, frequent spikes"
            ),
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="CK",
                direction=EffectDirection.INCREASE,
                mechanism="Eccentric loading from jumping and stopping",
                acute_effect="Moderate elevation post-game"
            ),
        ],
        sources=[]
    )


def create_tennis() -> Activity:
    """Tennis - racquet sport."""
    return Activity(
        name="Tennis",
        name_de="Tennis",
        category=ActivityCategory.SPORTS,
        description="Racquet sport with quick directional changes",
        calories_per_hour=480,
        intensity_range=[IntensityLevel.MODERATE, IntensityLevel.HIGH],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="CK",
                direction=EffectDirection.INCREASE,
                mechanism="Upper body and leg muscle loading",
                acute_effect="Mild to moderate elevation"
            ),
        ],
        sources=[]
    )


def create_dancing_aerobic() -> Activity:
    """Aerobic dancing - choreographed exercise."""
    return Activity(
        name="Dancing (Aerobic)",
        name_de="Tanzen (Aerobic)",
        category=ActivityCategory.SPORTS,
        description="Choreographed dance-based aerobic exercise",
        calories_per_hour=400,
        intensity_range=[IntensityLevel.MODERATE],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.VITAL_SIGN,
                target_name="Heart Rate",
                direction=EffectDirection.INCREASE,
                mechanism="Sustained aerobic activity",
                acute_effect="Steady elevation to 60-70% max HR"
            ),
        ],
        sources=[]
    )


def create_dancing_ballroom() -> Activity:
    """Ballroom dancing - social dance."""
    return Activity(
        name="Dancing (Ballroom)",
        name_de="Tanzen (Standard/Latein)",
        category=ActivityCategory.SPORTS,
        description="Social partner dancing",
        calories_per_hour=250,
        intensity_range=[IntensityLevel.LOW, IntensityLevel.MODERATE],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Cortisol",
                direction=EffectDirection.DECREASE,
                mechanism="Social engagement and enjoyment reduce stress",
                chronic_effect="Stress reduction benefits"
            ),
        ],
        sources=[]
    )


# =============================================================================
# DAILY LIVING ACTIVITIES
# =============================================================================

def create_sleeping() -> Activity:
    """Sleeping - rest and recovery."""
    return Activity(
        name="Sleeping",
        name_de="Schlafen",
        category=ActivityCategory.SEDENTARY,
        description="Sleep and rest period",
        calories_per_hour=60,
        intensity_range=[IntensityLevel.REST],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Cortisol",
                direction=EffectDirection.DECREASE,
                mechanism="Lowest cortisol during deep sleep",
                acute_effect="Nadir levels during night",
                chronic_effect="Adequate sleep essential for cortisol regulation"
            ),
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Growth Hormone",
                direction=EffectDirection.INCREASE,
                mechanism="Pulsatile release during deep sleep phases",
                acute_effect="Major release during first half of night"
            ),
        ],
        sources=[]
    )


def create_eating_sitting() -> Activity:
    """Eating while sitting."""
    return Activity(
        name="Eating (Sitting)",
        name_de="Essen (Sitzend)",
        category=ActivityCategory.DAILY_LIVING,
        description="Meal consumption while seated",
        calories_per_hour=80,
        intensity_range=[IntensityLevel.REST],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Glucose",
                direction=EffectDirection.INCREASE,
                mechanism="Postprandial glucose rise from food intake",
                acute_effect="Rise depends on meal composition",
                duration_dependent=True
            ),
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Insulin",
                direction=EffectDirection.INCREASE,
                mechanism="Pancreatic response to glucose",
                acute_effect="Rise proportional to carbohydrate intake"
            ),
        ],
        sources=[]
    )


def create_grooming() -> Activity:
    """Personal grooming activities."""
    return Activity(
        name="Grooming",
        name_de="Körperpflege",
        category=ActivityCategory.DAILY_LIVING,
        description="Personal hygiene and grooming (washing, dressing, etc.)",
        calories_per_hour=120,
        intensity_range=[IntensityLevel.LOW],
        effects=[],
        sources=[]
    )


def create_showering() -> Activity:
    """Showering."""
    return Activity(
        name="Showering",
        name_de="Duschen",
        category=ActivityCategory.DAILY_LIVING,
        description="Personal hygiene in shower",
        calories_per_hour=100,
        intensity_range=[IntensityLevel.LOW],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.VITAL_SIGN,
                target_name="Heart Rate",
                direction=EffectDirection.INCREASE,
                mechanism="Hot water causes vasodilation and mild cardiovascular response",
                acute_effect="Slight elevation with hot water"
            ),
        ],
        sources=[]
    )


# =============================================================================
# SEDENTARY ACTIVITIES
# =============================================================================

def create_sitting_inactive() -> Activity:
    """Sitting inactive - minimal movement."""
    return Activity(
        name="Sitting (Inactive)",
        name_de="Sitzen (Inaktiv)",
        category=ActivityCategory.SEDENTARY,
        description="Sitting with minimal movement (watching TV, resting)",
        calories_per_hour=70,
        intensity_range=[IntensityLevel.REST],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Glucose",
                direction=EffectDirection.INCREASE,
                mechanism="Prolonged sitting impairs glucose clearance",
                chronic_effect="Associated with poorer glucose control over time"
            ),
        ],
        sources=[]
    )


def create_sitting_active() -> Activity:
    """Sitting active - desk work with some movement."""
    return Activity(
        name="Sitting (Active/Work)",
        name_de="Sitzen (Arbeit)",
        category=ActivityCategory.SEDENTARY,
        description="Sitting while working or studying with some movement",
        calories_per_hour=100,
        intensity_range=[IntensityLevel.LOW],
        effects=[],
        sources=[]
    )


def create_lying_resting() -> Activity:
    """Lying down resting."""
    return Activity(
        name="Lying (Resting)",
        name_de="Liegen (Ausruhen)",
        category=ActivityCategory.SEDENTARY,
        description="Reclining or lying down awake",
        calories_per_hour=65,
        intensity_range=[IntensityLevel.REST],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.VITAL_SIGN,
                target_name="Heart Rate",
                direction=EffectDirection.DECREASE,
                mechanism="Reduced gravitational stress on cardiovascular system",
                acute_effect="Lowest daytime heart rate"
            ),
        ],
        sources=[]
    )


def create_meditating() -> Activity:
    """Meditation practice."""
    return Activity(
        name="Meditating",
        name_de="Meditieren",
        category=ActivityCategory.SEDENTARY,
        description="Sitting meditation or mindfulness practice",
        calories_per_hour=70,
        intensity_range=[IntensityLevel.REST],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Cortisol",
                direction=EffectDirection.DECREASE,
                mechanism="Stress reduction through parasympathetic activation",
                acute_effect="Decreased cortisol during and after session",
                chronic_effect="Lower baseline cortisol with regular practice"
            ),
        ],
        sources=[]
    )


# =============================================================================
# HOUSEHOLD ACTIVITIES
# =============================================================================

def create_cleaning_light() -> Activity:
    """Light household cleaning."""
    return Activity(
        name="Cleaning (Light)",
        name_de="Putzen (Leicht)",
        category=ActivityCategory.HOUSEHOLD,
        description="Light cleaning tasks like dusting and tidying",
        calories_per_hour=150,
        intensity_range=[IntensityLevel.LOW],
        effects=[],
        sources=[]
    )


def create_cleaning_heavy() -> Activity:
    """Heavy household cleaning."""
    return Activity(
        name="Cleaning (Heavy)",
        name_de="Putzen (Schwer)",
        category=ActivityCategory.HOUSEHOLD,
        description="Heavy cleaning like scrubbing and moving furniture",
        calories_per_hour=250,
        intensity_range=[IntensityLevel.MODERATE],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="CK",
                direction=EffectDirection.INCREASE,
                mechanism="Physical exertion from scrubbing and lifting",
                acute_effect="Mild elevation after extended cleaning"
            ),
        ],
        sources=[]
    )


def create_vacuuming() -> Activity:
    """Vacuuming floors."""
    return Activity(
        name="Vacuuming",
        name_de="Staubsaugen",
        category=ActivityCategory.HOUSEHOLD,
        description="Vacuum cleaning floors and carpets",
        calories_per_hour=180,
        intensity_range=[IntensityLevel.LOW, IntensityLevel.MODERATE],
        effects=[],
        sources=[]
    )


def create_mopping() -> Activity:
    """Mopping floors."""
    return Activity(
        name="Mopping",
        name_de="Wischen",
        category=ActivityCategory.HOUSEHOLD,
        description="Mopping and washing floors",
        calories_per_hour=170,
        intensity_range=[IntensityLevel.LOW, IntensityLevel.MODERATE],
        effects=[],
        sources=[]
    )


def create_cooking() -> Activity:
    """Cooking and food preparation."""
    return Activity(
        name="Cooking",
        name_de="Kochen",
        category=ActivityCategory.HOUSEHOLD,
        description="Meal preparation and cooking",
        calories_per_hour=140,
        intensity_range=[IntensityLevel.LOW],
        effects=[],
        sources=[]
    )


def create_dishwashing() -> Activity:
    """Washing dishes."""
    return Activity(
        name="Dishwashing",
        name_de="Abwasch",
        category=ActivityCategory.HOUSEHOLD,
        description="Washing dishes and kitchen cleanup",
        calories_per_hour=120,
        intensity_range=[IntensityLevel.LOW],
        effects=[],
        sources=[]
    )


def create_laundry() -> Activity:
    """Doing laundry."""
    return Activity(
        name="Laundry",
        name_de="Wäsche",
        category=ActivityCategory.HOUSEHOLD,
        description="Washing, drying, and folding clothes",
        calories_per_hour=130,
        intensity_range=[IntensityLevel.LOW],
        effects=[],
        sources=[]
    )


def create_ironing() -> Activity:
    """Ironing clothes."""
    return Activity(
        name="Ironing",
        name_de="Bügeln",
        category=ActivityCategory.HOUSEHOLD,
        description="Ironing and pressing clothes",
        calories_per_hour=110,
        intensity_range=[IntensityLevel.LOW],
        effects=[],
        sources=[]
    )


def create_gardening() -> Activity:
    """General gardening."""
    return Activity(
        name="Gardening",
        name_de="Gartenarbeit",
        category=ActivityCategory.HOUSEHOLD,
        description="General gardening tasks like weeding and planting",
        calories_per_hour=250,
        intensity_range=[IntensityLevel.LOW, IntensityLevel.MODERATE],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Vitamin D",
                direction=EffectDirection.INCREASE,
                mechanism="Sun exposure during outdoor work",
                acute_effect="Vitamin D synthesis during daylight"
            ),
        ],
        sources=[]
    )


def create_gardening_digging() -> Activity:
    """Digging and heavy gardening."""
    return Activity(
        name="Gardening (Digging)",
        name_de="Gartenarbeit (Graben)",
        category=ActivityCategory.HOUSEHOLD,
        description="Heavy gardening work like digging and shoveling",
        calories_per_hour=350,
        intensity_range=[IntensityLevel.MODERATE, IntensityLevel.HIGH],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="CK",
                direction=EffectDirection.INCREASE,
                mechanism="Physical exertion from digging and lifting",
                acute_effect="Moderate elevation after extended work"
            ),
        ],
        sources=[]
    )


def create_mowing_lawn() -> Activity:
    """Mowing lawn with push mower."""
    return Activity(
        name="Lawn Mowing (Push)",
        name_de="Rasenmähen (Schieben)",
        category=ActivityCategory.HOUSEHOLD,
        description="Pushing lawn mower to cut grass",
        calories_per_hour=300,
        intensity_range=[IntensityLevel.MODERATE],
        effects=[],
        sources=[]
    )


def create_raking_leaves() -> Activity:
    """Raking leaves."""
    return Activity(
        name="Raking Leaves",
        name_de="Laubharken",
        category=ActivityCategory.HOUSEHOLD,
        description="Raking and collecting leaves",
        calories_per_hour=250,
        intensity_range=[IntensityLevel.LOW, IntensityLevel.MODERATE],
        effects=[],
        sources=[]
    )


def create_sweeping() -> Activity:
    """Sweeping floors or sidewalk."""
    return Activity(
        name="Sweeping",
        name_de="Kehren",
        category=ActivityCategory.HOUSEHOLD,
        description="Sweeping floors, sidewalk, or outdoor areas",
        calories_per_hour=160,
        intensity_range=[IntensityLevel.LOW],
        effects=[],
        sources=[]
    )


def create_carrying_groceries() -> Activity:
    """Carrying groceries."""
    return Activity(
        name="Carrying Groceries",
        name_de="Tragen von Einkäufen",
        category=ActivityCategory.HOUSEHOLD,
        description="Carrying shopping bags and groceries",
        calories_per_hour=200,
        intensity_range=[IntensityLevel.LOW, IntensityLevel.MODERATE],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.VITAL_SIGN,
                target_name="Heart Rate",
                direction=EffectDirection.INCREASE,
                mechanism="Weight-bearing cardiovascular demand",
                acute_effect="Elevation proportional to weight carried"
            ),
        ],
        sources=[]
    )


def create_moving_furniture() -> Activity:
    """Moving furniture and heavy items."""
    return Activity(
        name="Moving Furniture",
        name_de="Möbeltragen",
        category=ActivityCategory.HOUSEHOLD,
        description="Moving furniture and heavy household items",
        calories_per_hour=400,
        intensity_range=[IntensityLevel.MODERATE, IntensityLevel.HIGH],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="CK",
                direction=EffectDirection.INCREASE,
                mechanism="Heavy lifting causes muscle stress",
                acute_effect="Significant elevation after heavy moving"
            ),
        ],
        sources=[]
    )


def create_stair_climbing() -> Activity:
    """Climbing stairs."""
    return Activity(
        name="Stair Climbing",
        name_de="Treppensteigen",
        category=ActivityCategory.HOUSEHOLD,
        description="Walking up and down stairs",
        calories_per_hour=450,
        intensity_range=[IntensityLevel.MODERATE, IntensityLevel.HIGH],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.VITAL_SIGN,
                target_name="Heart Rate",
                direction=EffectDirection.INCREASE,
                mechanism="Vertical work increases cardiovascular demand",
                acute_effect="Rapid elevation, excellent for cardiovascular fitness"
            ),
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="LDL",
                direction=EffectDirection.DECREASE,
                mechanism="Regular stair climbing improves lipid profile",
                chronic_effect="Improved cholesterol levels with regular use"
            ),
        ],
        sources=[]
    )


# =============================================================================
# TRANSPORTATION ACTIVITIES
# =============================================================================

def create_driving() -> Activity:
    """Driving a car."""
    return Activity(
        name="Driving",
        name_de="Autofahren",
        category=ActivityCategory.TRANSPORTATION,
        description="Operating a motor vehicle",
        calories_per_hour=110,
        intensity_range=[IntensityLevel.LOW],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Cortisol",
                direction=EffectDirection.INCREASE,
                mechanism="Traffic stress can elevate cortisol",
                acute_effect="Variable elevation depending on traffic conditions"
            ),
        ],
        sources=[]
    )


def create_driving_heavy_traffic() -> Activity:
    """Driving in heavy traffic."""
    return Activity(
        name="Driving (Heavy Traffic)",
        name_de="Autofahren (Stau)",
        category=ActivityCategory.TRANSPORTATION,
        description="Driving in congested traffic conditions",
        calories_per_hour=100,
        intensity_range=[IntensityLevel.LOW],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Cortisol",
                direction=EffectDirection.INCREASE,
                mechanism="Traffic stress and frustration elevate cortisol",
                acute_effect="Notable elevation during stressful driving",
                chronic_effect="Regular stressful commuting associated with higher baseline cortisol"
            ),
            ActivityEffect(
                target_type=EffectTargetType.VITAL_SIGN,
                target_name="Blood Pressure",
                direction=EffectDirection.INCREASE,
                mechanism="Stress response causes vasoconstriction",
                acute_effect="Temporary elevation during stressful periods"
            ),
        ],
        sources=[]
    )


def create_riding_bus_train() -> Activity:
    """Riding as passenger on bus or train."""
    return Activity(
        name="Riding (Bus/Train)",
        name_de="ÖPNV Fahren",
        category=ActivityCategory.TRANSPORTATION,
        description="Sitting as passenger on public transportation",
        calories_per_hour=80,
        intensity_range=[IntensityLevel.REST],
        effects=[],
        sources=[]
    )


def create_cycling_transport() -> Activity:
    """Cycling for transportation."""
    return Activity(
        name="Cycling (Transport)",
        name_de="Radfahren (Transport)",
        category=ActivityCategory.TRANSPORTATION,
        description="Cycling as mode of transportation",
        calories_per_hour=350,
        intensity_range=[IntensityLevel.LOW, IntensityLevel.MODERATE],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="HDL",
                direction=EffectDirection.INCREASE,
                mechanism="Regular cycling improves cardiovascular health",
                chronic_effect="Improved lipid profile with regular commuting"
            ),
        ],
        sources=[]
    )


def create_walking_transport() -> Activity:
    """Walking for transportation."""
    return Activity(
        name="Walking (Transport)",
        name_de="Zu Fuß gehen",
        category=ActivityCategory.TRANSPORTATION,
        description="Walking as mode of transportation",
        calories_per_hour=220,
        intensity_range=[IntensityLevel.LOW],
        effects=[],
        sources=[]
    )


# =============================================================================
# SOCIAL/RECREATIONAL ACTIVITIES
# =============================================================================

def create_playing_with_children() -> Activity:
    """Playing with children."""
    return Activity(
        name="Playing with Children",
        name_de="Mit Kindern spielen",
        category=ActivityCategory.RECREATION,
        description="Active play with children",
        calories_per_hour=250,
        intensity_range=[IntensityLevel.LOW, IntensityLevel.MODERATE],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Cortisol",
                direction=EffectDirection.DECREASE,
                mechanism="Social bonding and enjoyment reduce stress",
                acute_effect="Stress reduction from positive social interaction"
            ),
        ],
        sources=[]
    )


def create_walking_dog() -> Activity:
    """Walking the dog."""
    return Activity(
        name="Walking Dog",
        name_de="Hundeausführung",
        category=ActivityCategory.RECREATION,
        description="Walking with dog for exercise",
        calories_per_hour=200,
        intensity_range=[IntensityLevel.LOW],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Cortisol",
                direction=EffectDirection.DECREASE,
                mechanism="Pet interaction and outdoor activity reduce stress",
                acute_effect="Stress reduction from pet companionship"
            ),
        ],
        sources=[]
    )


def create_shopping_light() -> Activity:
    """Light shopping."""
    return Activity(
        name="Shopping (Light)",
        name_de="Einkaufen (Leicht)",
        category=ActivityCategory.RECREATION,
        description="Casual shopping with light walking",
        calories_per_hour=140,
        intensity_range=[IntensityLevel.LOW],
        effects=[],
        sources=[]
    )


def create_shopping_heavy() -> Activity:
    """Heavy shopping with carrying."""
    return Activity(
        name="Shopping (Heavy)",
        name_de="Einkaufen (Schwer)",
        category=ActivityCategory.RECREATION,
        description="Shopping involving carrying bags and walking",
        calories_per_hour=200,
        intensity_range=[IntensityLevel.LOW, IntensityLevel.MODERATE],
        effects=[],
        sources=[]
    )


def create_reading() -> Activity:
    """Reading while sitting."""
    return Activity(
        name="Reading",
        name_de="Lesen",
        category=ActivityCategory.RECREATION,
        description="Reading books or other materials",
        calories_per_hour=80,
        intensity_range=[IntensityLevel.REST],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Cortisol",
                direction=EffectDirection.DECREASE,
                mechanism="Relaxation and mental engagement reduce stress",
                acute_effect="Stress reduction from enjoyable activity"
            ),
        ],
        sources=[]
    )


def create_watching_tv() -> Activity:
    """Watching television."""
    return Activity(
        name="Watching TV",
        name_de="Fernsehen",
        category=ActivityCategory.RECREATION,
        description="Sedentary screen time watching television",
        calories_per_hour=70,
        intensity_range=[IntensityLevel.REST],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Glucose",
                direction=EffectDirection.INCREASE,
                mechanism="Prolonged sitting impairs glucose metabolism",
                chronic_effect="Associated with poorer metabolic health"
            ),
        ],
        sources=[]
    )


def create_standing_light() -> Activity:
    """Standing with light activity."""
    return Activity(
        name="Standing (Light Activity)",
        name_de="Stehen (Leichte Aktivität)",
        category=ActivityCategory.RECREATION,
        description="Standing with minimal movement",
        calories_per_hour=100,
        intensity_range=[IntensityLevel.LOW],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Glucose",
                direction=EffectDirection.DECREASE,
                mechanism="Postural muscle activity improves glucose clearance",
                acute_effect="Better glucose control than prolonged sitting"
            ),
        ],
        sources=[]
    )


def create_sitting_meeting() -> Activity:
    """Sitting in meetings."""
    return Activity(
        name="Sitting (Meeting)",
        name_de="Sitzen (Besprechung)",
        category=ActivityCategory.WORK,
        description="Sitting during meetings or discussions",
        calories_per_hour=90,
        intensity_range=[IntensityLevel.LOW],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Cortisol",
                direction=EffectDirection.INCREASE,
                mechanism="Meeting stress can elevate cortisol",
                acute_effect="Variable elevation depending on meeting nature"
            ),
        ],
        sources=[]
    )


def create_desk_work_sitting() -> Activity:
    """Desk work while sitting."""
    return Activity(
        name="Desk Work (Sitting)",
        name_de="Schreibtischarbeit (Sitzend)",
        category=ActivityCategory.WORK,
        description="Computer work and desk tasks while sitting",
        calories_per_hour=100,
        intensity_range=[IntensityLevel.LOW],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Glucose",
                direction=EffectDirection.INCREASE,
                mechanism="Prolonged sitting impairs glucose metabolism",
                chronic_effect="Sedentary work associated with metabolic risk"
            ),
        ],
        sources=[]
    )


def create_desk_work_standing() -> Activity:
    """Desk work while standing."""
    return Activity(
        name="Desk Work (Standing)",
        name_de="Schreibtischarbeit (Stehend)",
        category=ActivityCategory.WORK,
        description="Computer work and desk tasks while standing",
        calories_per_hour=130,
        intensity_range=[IntensityLevel.LOW],
        effects=[
            ActivityEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Glucose",
                direction=EffectDirection.DECREASE,
                mechanism="Postural muscle engagement improves glucose clearance",
                acute_effect="Better metabolic response than sitting"
            ),
        ],
        sources=[]
    )


# =============================================================================
# EXPORT ALL ACTIVITIES
# =============================================================================

def get_all_activities():
    """Get all activity factory functions."""
    return [
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
        # Social/Recreation/Work
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
    ]


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
