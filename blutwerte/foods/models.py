"""
Core data models for the food system.

This module defines the complete data structures for foods, their nutritional content,
biomarker effects, and intake tracking.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum

from blutwerte.medications.models import EffectTargetType, EffectDirection
from .sources import DataSource
from .portions import Portion, Amount, CategoryPortionDefaults


class EffectCertainty(Enum):
    """
    Certainty level of a food effect.
    
    Some effects are well-established (vitamin K in spinach), while others
    depend on multiple factors (iron absorption from plant sources).
    """
    ESTABLISHED = "established"      # Well-documented, consistent effect
    VARIABLE = "variable"            # Depends on preparation, other foods, individual
    EMERGING = "emerging"            # Preliminary research, needs more study


@dataclass
class EffectModifier:
    """
    A factor that modifies the strength or certainty of a food effect.
    
    Example: Iron absorption from spinach is enhanced by vitamin C but
    inhibited by calcium and tannins.
    
    Attributes:
        factor: Name of the modifying factor (e.g., "vitamin_c_present")
        description: Human-readable description of the effect
        impact: Quantitative impact if known (e.g., "3-4x increase")
        direction: Whether it increases or decreases the main effect
        source: DataSource for this modifier information
    """
    factor: str
    description: str
    impact: Optional[str] = None
    direction: str = "enhances"  # "enhances" or "inhibits"
    source: Optional[DataSource] = None


@dataclass
class FoodEffect:
    """
    How a food affects a biomarker or vital sign.
    
    All food effects MUST include source references to ensure scientific
    validity and traceability.
    
    Attributes:
        target_type: Type of target (BIOMARKER, VITAL_SIGN, etc.)
        target_name: Name of the target using biomarker naming convention
                     (e.g., "Vitamin K", "Iron", "Folic Acid")
        direction: Effect direction (INCREASE, DECREASE, VARIABLE)
        mechanism: Detailed description of how the effect works
        sources: List of DataSource objects (REQUIRED)
        certainty: How well-established this effect is
        per_serving: Whether effect is per typical serving
        modifiers: Factors that modify this effect (optional)
        notes: Additional notes about bioavailability, preparation, etc.
        
    Example:
        >>> effect = FoodEffect(
        ...     target_type=EffectTargetType.BIOMARKER,
        ...     target_name="Vitamin K",
        ...     direction=EffectDirection.INCREASE,
        ...     mechanism="Rich in phylloquinone (vitamin K1). One cup cooked provides 888 mcg (987% DV)",
        ...     sources=[DataSource(
        ...         url="https://ods.od.nih.gov/factsheets/VitaminK-HealthProfessional/",
        ...         title="Vitamin K Fact Sheet for Health Professionals",
        ...         source_type="guideline"
        ...     )],
        ...     certainty=EffectCertainty.ESTABLISHED
        ... )
    """
    target_type: EffectTargetType
    target_name: str
    direction: EffectDirection
    mechanism: str
    sources: List[DataSource] = field(default_factory=list)
    certainty: EffectCertainty = EffectCertainty.ESTABLISHED
    per_serving: bool = True
    modifiers: List[EffectModifier] = field(default_factory=list)
    notes: Optional[str] = None
    
    def __post_init__(self):
        """Validate that sources are provided"""
        if not self.sources:
            raise ValueError(f"FoodEffect for {self.target_name} must have at least one source")


@dataclass
class Food:
    """
    Complete food profile with nutrition and biomarker effects.
    
    The Food class represents a specific food item with its nutritional
    composition and documented effects on biomarkers. It supports mathematical
    operations for combining foods and scaling quantities.
    
    Attributes:
        id: Internal UUID (not exposed in public API)
        name: English name of the food
        name_de: German name (required for patient-facing features)
        nutrition_data: Dict of nutrient name -> value per 100g
                       (using food_legacy naming: "vitamin k", "iron")
        category: Food category for portion defaults
        effects: List of FoodEffect objects documenting biomarker effects
        nutrition_sources: Sources for the nutrition data
        custom_portions: Portion overrides for this specific food
        weight: Current weight in grams (for mathematical operations)
        
    Example:
        >>> spinach = Food(
        ...     name="Spinach",
        ...     name_de="Spinat",
        ...     category="vegetable",
        ...     nutrition_data={"vitamin k": 483, "iron": 2.7, "folate": 194},
        ...     effects=[...],
        ...     nutrition_sources=[...]
        ... )
        >>> portion = spinach * gramm(100)  # 100g of spinach
    """
    # Identification
    name: str
    name_de: str
    id: UUID = field(default_factory=uuid4)
    
    # Nutrition (per 100g)
    nutrition_data: Dict[str, float] = field(default_factory=dict)
    
    # Categorization
    category: Optional[str] = None
    
    # Biomarker effects
    effects: List[FoodEffect] = field(default_factory=list)
    
    # Sources
    nutrition_sources: List[DataSource] = field(default_factory=list)
    
    # Portion overrides
    custom_portions: Dict[str, float] = field(default_factory=dict)
    
    # Current weight (for mathematical operations)
    weight: float = 0
    
    def __mul__(self, quantity: Union[Portion, Amount, int, float]) -> 'Food':
        """
        Scale food by a portion, amount, or multiplier.
        
        Args:
            quantity: Portion (scheibe, glas), Amount (gramm, kilo), or number
            
        Returns:
            New Food with scaled weight
            
        Examples:
            >>> bread * scheibe(2)      # 2 slices
            >>> apple * gramm(150)      # 150 grams
            >>> juice * 3               # Triple the amount
        """
        weight = self.weight
        
        if isinstance(quantity, Portion):
            # Check for custom portion size for this food
            amount = quantity.sizes.get(id(self))
            if amount is None:
                # Check for category default
                if self.category:
                    amount = CategoryPortionDefaults.get(self.category, quantity.name)
                # Use portion's default weight
                if amount is None:
                    amount = quantity.weight
            weight = amount
            
        elif isinstance(quantity, Amount):
            # Amount specifies total weight directly
            weight = quantity.value
            
        else:
            # Numeric multiplier
            weight = self.weight * quantity if self.weight else quantity * 100
        
        # Create new Food with scaled weight
        new_food = Food(
            name=self.name,
            name_de=self.name_de,
            nutrition_data=dict(self.nutrition_data),
            category=self.category,
            effects=list(self.effects),
            nutrition_sources=list(self.nutrition_sources),
            custom_portions=dict(self.custom_portions),
            weight=weight
        )
        return new_food
    
    def __add__(self, other: 'Food') -> 'Food':
        """
        Combine two foods (nutritionally weighted average).
        
        Args:
            other: Another Food to combine with
            
        Returns:
            New Food representing the combined nutrition
        """
        total_weight = self.weight + other.weight
        
        if total_weight == 0:
            return Food(name=f"{self.name}+{other.name}", name_de="", weight=0)
        
        # Weighted average of nutrition data
        all_nutrients = set(self.nutrition_data.keys()) | set(other.nutrition_data.keys())
        weighted_nutrition = {
            k: (self.nutrition_data.get(k, 0) * self.weight + 
                other.nutrition_data.get(k, 0) * other.weight) / total_weight
            for k in all_nutrients
        }
        
        # Combine effects (simple concatenation - analysis will handle)
        combined_effects = list(self.effects) + list(other.effects)
        
        return Food(
            name=f"{self.name}+{other.name}",
            name_de="",
            nutrition_data=weighted_nutrition,
            weight=total_weight,
            effects=combined_effects
        )
    
    def __truediv__(self, divisor: Union[int, float]) -> 'Food':
        """
        Divide food quantity.
        
        Args:
            divisor: Number to divide by
            
        Returns:
            New Food with divided weight
        """
        if divisor == 0:
            raise ValueError("Cannot divide by zero")
        
        return Food(
            name=self.name,
            name_de=self.name_de,
            nutrition_data=dict(self.nutrition_data),
            category=self.category,
            effects=list(self.effects),
            nutrition_sources=list(self.nutrition_sources),
            custom_portions=dict(self.custom_portions),
            weight=self.weight / divisor
        )
    
    def affects_biomarker(self, biomarker_name: str) -> List[FoodEffect]:
        """
        Get all effects on a specific biomarker.
        
        Args:
            biomarker_name: Name of the biomarker (e.g., "Vitamin K", "Iron")
            
        Returns:
            List of FoodEffect objects affecting this biomarker
        """
        return [
            effect for effect in self.effects
            if effect.target_name.lower() == biomarker_name.lower()
        ]
    
    def get_nutrient(self, name: str, amount: Optional[float] = None) -> float:
        """
        Get nutrient value (per 100g or for specific amount).
        
        Args:
            name: Nutrient name (e.g., "vitamin k", "iron")
            amount: Optional amount in grams (defaults to self.weight)
            
        Returns:
            Nutrient value for the specified amount
        """
        per_100g = self.nutrition_data.get(name, 0)
        target_weight = amount if amount is not None else self.weight
        return per_100g * target_weight / 100
    
    def set_category(self, category: str) -> 'Food':
        """
        Set food category for portion defaults.
        
        Args:
            category: Category name (e.g., "vegetable", "fruit", "meat")
            
        Returns:
            Self for method chaining
        """
        self.category = category
        return self
    
    def set_portion(self, portion: Portion, amount: Union[int, float]) -> 'Food':
        """
        Define a custom portion size for this food.
        
        Args:
            portion: Portion type (e.g., scheibe, stück)
            amount: Weight in grams for this portion
            
        Returns:
            Self for method chaining
        """
        self.custom_portions[portion.name] = amount
        portion.add(id(self), amount)
        return self
    
    def get_all_nutrients(self) -> Dict[str, float]:
        """
        Get all nutrients scaled to current weight.
        
        Returns:
            Dict of nutrient name -> value for current weight
        """
        if self.weight == 0:
            return {}
        return {
            name: value * self.weight / 100
            for name, value in self.nutrition_data.items()
        }
    
    def __str__(self) -> str:
        """String representation showing name and weight"""
        return f"Food({self.name}, {self.weight}g)"
    
    def __repr__(self) -> str:
        """Detailed representation"""
        return f"Food(name='{self.name}', name_de='{self.name_de}', weight={self.weight}g, effects={len(self.effects)})"


@dataclass
class FoodIntake:
    """
    A specific intake of food (with amount and timestamp).
    
    Used for tracking daily food consumption and analyzing
    cumulative effects on biomarkers.
    
    Attributes:
        food: The Food consumed
        amount: Amount consumed in grams
        timestamp: When the food was consumed
        notes: Optional notes about preparation, cooking method, etc.
        
    Example:
        >>> intake = FoodIntake(
        ...     food=spinach,
        ...     amount=100,
        ...     timestamp=datetime.now(),
        ...     notes="Steamed, served with lemon"
        ... )
    """
    food: Food
    amount: float
    timestamp: datetime
    notes: Optional[str] = None
    
    def get_nutrients(self) -> Dict[str, float]:
        """
        Get nutrients for this specific intake.
        
        Returns:
            Dict of nutrient name -> value for consumed amount
        """
        return self.food.get_all_nutrients() if self.food.weight == self.amount else {
            name: value * self.amount / 100
            for name, value in self.food.nutrition_data.items()
        }
    
    def get_effects(self) -> List[FoodEffect]:
        """
        Get biomarker effects for this intake.
        
        Returns:
            List of FoodEffect objects (scaled to amount if per_serving)
        """
        # Effects are generally not scaled - they indicate presence in the food
        # Analysis will determine actual impact based on amount
        return list(self.food.effects)
    
    def affects_biomarker(self, biomarker_name: str) -> List[FoodEffect]:
        """
        Check if this intake affects a specific biomarker.
        
        Args:
            biomarker_name: Name of the biomarker
            
        Returns:
            List of relevant FoodEffect objects
        """
        return self.food.affects_biomarker(biomarker_name)
