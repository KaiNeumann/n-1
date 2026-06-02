"""
Food analysis engine for biomarker effects.

This module provides analysis capabilities to understand how food intake
affects biomarkers and to generate recommendations.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

from .models import Food, FoodEffect, FoodIntake, EffectCertainty
from .sources import DataSource
from .rdi import compare_to_rdi, RDI


class ImpactLevel(Enum):
    """Level of estimated impact on a biomarker"""
    SIGNIFICANT = "significant"    # >50% of RDI or major effect
    MODERATE = "moderate"          # 20-50% of RDI or noticeable effect
    MINOR = "minor"                # <20% of RDI or slight effect
    NEGLIGIBLE = "negligible"      # Minimal impact


@dataclass
class FoodContribution:
    """
    Contribution of a specific food to a biomarker effect.
    
    Attributes:
        food_name: Name of the food
        effect: The FoodEffect that applies
        amount_consumed: Amount consumed in grams
        estimated_impact: Significance of the impact
        nutrient_amount: Amount of relevant nutrient provided
    """
    food_name: str
    effect: FoodEffect
    amount_consumed: float
    estimated_impact: ImpactLevel
    nutrient_amount: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "food_name": self.food_name,
            "effect_direction": self.effect.direction.value,
            "mechanism": self.effect.mechanism,
            "amount_consumed_g": self.amount_consumed,
            "estimated_impact": self.estimated_impact.value,
            "nutrient_amount": self.nutrient_amount,
        }


@dataclass
class FoodAnalysisResult:
    """
    Result of analyzing food effects on a biomarker.
    
    Attributes:
        biomarker_name: Name of the biomarker analyzed
        current_value: Current measured value (if available)
        food_contributions: List of foods contributing to the effect
        net_effect: Overall direction of effect (increase, decrease, mixed, neutral)
        recommendation: Optional recommendation based on analysis
        sources: Combined sources from all effects
    """
    biomarker_name: str
    current_value: Optional[float] = None
    food_contributions: List[FoodContribution] = field(default_factory=list)
    net_effect: str = "neutral"  # "increase", "decrease", "mixed", "neutral"
    recommendation: Optional[str] = None
    sources: List[DataSource] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "biomarker_name": self.biomarker_name,
            "current_value": self.current_value,
            "net_effect": self.net_effect,
            "recommendation": self.recommendation,
            "food_contributions": [c.to_dict() for c in self.food_contributions],
        }


@dataclass
class FoodRecommendation:
    """
    A food-based recommendation to improve a biomarker.
    
    Attributes:
        food_name: Name of recommended food
        food_category: Category for alternatives
        target_biomarker: Biomarker to improve
        target_direction: "increase" or "decrease"
        rationale: Why this food helps
        serving_suggestion: How much to consume
        priority: Priority level (high/medium/low)
        sources: Supporting sources
    """
    food_name: str
    food_category: str
    target_biomarker: str
    target_direction: str
    rationale: str
    serving_suggestion: str
    priority: str = "medium"  # "high", "medium", "low"
    sources: List[DataSource] = field(default_factory=list)


class FoodAnalyzer:
    """
    Analyze how food intake affects biomarkers.
    
    Can be used standalone or combined with medication analysis.
    
    Example:
        >>> analyzer = FoodAnalyzer()
        >>> intakes = [FoodIntake(spinach, 100, datetime.now())]
        >>> result = analyzer.analyze_biomarker("Vitamin K", intakes)
        >>> print(result.net_effect)  # "increase"
    """
    
    def __init__(self, food_db=None):
        """
        Initialize analyzer.
        
        Args:
            food_db: Optional FoodDatabase for looking up foods
        """
        self.food_db = food_db
    
    def analyze_biomarker(
        self,
        biomarker_name: str,
        food_intakes: List[FoodIntake],
        current_value: Optional[float] = None,
        unit: Optional[str] = None
    ) -> FoodAnalysisResult:
        """
        Analyze food effects on a specific biomarker.
        
        Args:
            biomarker_name: Name of biomarker (e.g., "Vitamin K", "Iron")
            food_intakes: List of food intakes to analyze
            current_value: Optional current measured value
            unit: Unit of measurement
            
        Returns:
            FoodAnalysisResult with contributions and net effect
        """
        contributions = []
        all_sources = []
        
        for intake in food_intakes:
            # Get effects for this biomarker
            effects = intake.affects_biomarker(biomarker_name)
            
            for effect in effects:
                # Estimate impact level
                impact = self._estimate_impact(effect, intake.amount, biomarker_name)
                
                # Get nutrient amount if applicable
                nutrient_amount = None
                if effect.target_name.lower() in intake.food.nutrition_data:
                    nutrient_amount = intake.food.get_nutrient(
                        effect.target_name.lower(), 
                        intake.amount
                    )
                
                contribution = FoodContribution(
                    food_name=intake.food.name,
                    effect=effect,
                    amount_consumed=intake.amount,
                    estimated_impact=impact,
                    nutrient_amount=nutrient_amount
                )
                contributions.append(contribution)
                all_sources.extend(effect.sources)
        
        # Determine net effect
        net_effect = self._calculate_net_effect(contributions)
        
        # Generate recommendation
        recommendation = self._generate_recommendation(
            biomarker_name, net_effect, contributions, current_value
        )
        
        return FoodAnalysisResult(
            biomarker_name=biomarker_name,
            current_value=current_value,
            food_contributions=contributions,
            net_effect=net_effect,
            recommendation=recommendation,
            sources=all_sources
        )
    
    def analyze_daily_intake(
        self,
        food_intakes: List[FoodIntake],
        biomarkers_of_interest: Optional[List[str]] = None
    ) -> Dict[str, FoodAnalysisResult]:
        """
        Analyze full day's food intake.
        
        Args:
            food_intakes: All food consumed
            biomarkers_of_interest: Specific biomarkers to analyze (None = all found)
            
        Returns:
            Dict of biomarker name -> FoodAnalysisResult
        """
        # Collect all biomarkers affected by these foods
        if biomarkers_of_interest is None:
            biomarkers = set()
            for intake in food_intakes:
                for effect in intake.food.effects:
                    biomarkers.add(effect.target_name)
            biomarkers_of_interest = sorted(list(biomarkers))
        
        # Analyze each biomarker
        results = {}
        for biomarker in biomarkers_of_interest:
            results[biomarker] = self.analyze_biomarker(biomarker, food_intakes)
        
        return results
    
    def get_recommendations(
        self,
        biomarker_name: str,
        target_direction: str,
        current_intake: List[FoodIntake],
        limit: int = 5
    ) -> List[FoodRecommendation]:
        """
        Get food recommendations to improve a biomarker.
        
        Args:
            biomarker_name: Biomarker to target
            target_direction: "increase" or "decrease"
            current_intake: Current food intake (to avoid duplicates)
            limit: Maximum number of recommendations
            
        Returns:
            List of FoodRecommendation objects
        """
        # This would typically query a food database for foods
        # that affect the biomarker in the desired direction
        # For now, return a placeholder
        recommendations = []
        
        # TODO: Query food_db for foods affecting this biomarker
        # and generate recommendations based on nutrient density
        
        return recommendations
    
    def _estimate_impact(
        self, 
        effect: FoodEffect, 
        amount_consumed: float,
        biomarker_name: str
    ) -> ImpactLevel:
        """
        Estimate impact level of a food effect.
        
        Args:
            effect: The FoodEffect
            amount_consumed: Amount consumed in grams
            biomarker_name: Name of biomarker
            
        Returns:
            ImpactLevel enum value
        """
        # Get RDI for comparison
        from .rdi import get_rdi
        rdi = get_rdi(biomarker_name.lower())
        
        if rdi and rdi.reference:
            # Calculate percentage of RDI from this serving
            # This is a simplified calculation
            nutrient_per_100g = effect.target_name.lower()
            if hasattr(effect, 'nutrient_per_100g'):
                # Would need access to food's nutrition data
                percentage = (amount_consumed / 100) * 100  # Simplified
                
                if percentage > 50:
                    return ImpactLevel.SIGNIFICANT
                elif percentage > 20:
                    return ImpactLevel.MODERATE
                elif percentage > 5:
                    return ImpactLevel.MINOR
        
        # Default based on effect certainty
        if effect.certainty == EffectCertainty.ESTABLISHED:
            return ImpactLevel.MODERATE
        elif effect.certainty == EffectCertainty.VARIABLE:
            return ImpactLevel.MINOR
        else:
            return ImpactLevel.NEGLIGIBLE
    
    def _calculate_net_effect(self, contributions: List[FoodContribution]) -> str:
        """
        Calculate overall net effect from contributions.
        
        Args:
            contributions: List of food contributions
            
        Returns:
            "increase", "decrease", "mixed", or "neutral"
        """
        if not contributions:
            return "neutral"
        
        increases = sum(1 for c in contributions 
                       if c.effect.direction.value == "increase")
        decreases = sum(1 for c in contributions 
                       if c.effect.direction.value == "decrease")
        variables = sum(1 for c in contributions 
                       if c.effect.direction.value == "variable")
        
        # Weight by impact level
        def weight(contribution):
            weights = {
                ImpactLevel.SIGNIFICANT: 3,
                ImpactLevel.MODERATE: 2,
                ImpactLevel.MINOR: 1,
                ImpactLevel.NEGLIGIBLE: 0
            }
            return weights.get(contribution.estimated_impact, 1)
        
        increase_weight = sum(weight(c) for c in contributions 
                             if c.effect.direction.value == "increase")
        decrease_weight = sum(weight(c) for c in contributions 
                             if c.effect.direction.value == "decrease")
        
        if increase_weight > 0 and decrease_weight > 0:
            return "mixed"
        elif increase_weight > 0:
            return "increase"
        elif decrease_weight > 0:
            return "decrease"
        elif variables > 0:
            return "variable"
        else:
            return "neutral"
    
    def _generate_recommendation(
        self,
        biomarker_name: str,
        net_effect: str,
        contributions: List[FoodContribution],
        current_value: Optional[float]
    ) -> Optional[str]:
        """
        Generate a recommendation based on analysis.
        
        Args:
            biomarker_name: Name of biomarker
            net_effect: Calculated net effect
            contributions: List of contributions
            current_value: Current measured value
            
        Returns:
            Recommendation string or None
        """
        if not contributions:
            return f"No foods in your intake affect {biomarker_name}."
        
        if net_effect == "increase":
            foods = ", ".join([c.food_name for c in contributions[:3]])
            return f"Your current intake includes {foods}, which may increase {biomarker_name}."
        
        elif net_effect == "decrease":
            foods = ", ".join([c.food_name for c in contributions[:3]])
            return f"Your current intake includes {foods}, which may decrease {biomarker_name}."
        
        elif net_effect == "mixed":
            return f"Your intake has mixed effects on {biomarker_name}. Review individual food contributions."
        
        return None
    
    def compare_to_rdi(
        self,
        food_intakes: List[FoodIntake],
        nutrients: Optional[List[str]] = None
    ) -> Dict[str, Dict[str, Any]]:
        """
        Compare daily intake to RDI values.
        
        Args:
            food_intakes: List of food intakes
            nutrients: Specific nutrients to check (None = all)
            
        Returns:
            Dict of nutrient name -> comparison results
        """
        # Aggregate nutrients from all intakes
        totals = {}
        for intake in food_intakes:
            nutrients_consumed = intake.get_nutrients()
            for nutrient, amount in nutrients_consumed.items():
                totals[nutrient] = totals.get(nutrient, 0) + amount
        
        # Compare each to RDI
        results = {}
        for nutrient, total in totals.items():
            if nutrients is None or nutrient in nutrients:
                results[nutrient] = compare_to_rdi(total, nutrient)
        
        return results
