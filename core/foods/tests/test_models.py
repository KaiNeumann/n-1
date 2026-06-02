"""
Tests for the food system models.

Run with: pytest core/foods/tests/test_models.py -v
"""

import pytest
from datetime import datetime

from core.foods import (
    Food, FoodEffect, FoodIntake, EffectModifier, EffectCertainty,
    DataSource, EffectTargetType, EffectDirection,
    gramm, scheibe, portion
)


class TestDataSource:
    """Test DataSource creation and validation"""
    
    def test_create_source(self):
        """Test creating a DataSource"""
        source = DataSource(
            url="https://example.com",
            title="Example Source",
            source_type="research"
        )
        assert source.url == "https://example.com"
        assert source.title == "Example Source"
        assert source.source_type == "research"
        assert source.access_date is not None  # Auto-set
    
    def test_source_types(self):
        """Test valid source types"""
        for st in ["research", "database", "guideline", "government"]:
            source = DataSource(url="https://test.com", title="Test", source_type=st)
            assert source.source_type == st


class TestFoodEffect:
    """Test FoodEffect creation and validation"""
    
    def test_create_effect(self):
        """Test creating a FoodEffect"""
        source = DataSource(
            url="https://ods.od.nih.gov",
            title="NIH Fact Sheet",
            source_type="guideline"
        )
        
        effect = FoodEffect(
            target_type=EffectTargetType.BIOMARKER,
            target_name="Vitamin K",
            direction=EffectDirection.INCREASE,
            mechanism="Rich in vitamin K1",
            sources=[source],
            certainty=EffectCertainty.ESTABLISHED
        )
        
        assert effect.target_name == "Vitamin K"
        assert effect.direction == EffectDirection.INCREASE
        assert effect.certainty == EffectCertainty.ESTABLISHED
    
    def test_effect_requires_source(self):
        """Test that FoodEffect requires at least one source"""
        with pytest.raises(ValueError, match="must have at least one source"):
            FoodEffect(
                target_type=EffectTargetType.BIOMARKER,
                target_name="Iron",
                direction=EffectDirection.INCREASE,
                mechanism="Contains iron",
                sources=[]  # Empty sources
            )
    
    def test_variable_effect_with_modifiers(self):
        """Test creating variable effect with modifiers"""
        source = DataSource(
            url="https://example.com",
            title="Research",
            source_type="research"
        )
        
        modifier = EffectModifier(
            factor="vitamin_c_present",
            description="Enhances absorption",
            impact="3-4x increase",
            direction="enhances"
        )
        
        effect = FoodEffect(
            target_type=EffectTargetType.BIOMARKER,
            target_name="Iron",
            direction=EffectDirection.VARIABLE,
            mechanism="Variable absorption",
            sources=[source],
            certainty=EffectCertainty.VARIABLE,
            modifiers=[modifier]
        )
        
        assert len(effect.modifiers) == 1
        assert effect.modifiers[0].factor == "vitamin_c_present"


class TestFood:
    """Test Food creation and operations"""
    
    @pytest.fixture
    def sample_food(self):
        """Create a sample food for testing"""
        return Food(
            name="Test Food",
            name_de="Test Lebensmittel",
            category="test",
            nutrition_data={
                "calories": 100,
                "protein": 5,
                "vitamin c": 30
            }
        )
    
    def test_create_food(self, sample_food):
        """Test creating a Food"""
        assert sample_food.name == "Test Food"
        assert sample_food.name_de == "Test Lebensmittel"
        assert sample_food.category == "test"
        assert sample_food.nutrition_data["calories"] == 100
    
    def test_food_uuid_internal(self, sample_food):
        """Test that Food has internal UUID"""
        assert sample_food.id is not None
        # UUID should be internal - not exposed in common operations
    
    def test_multiply_by_gramm(self, sample_food):
        """Test scaling food by gramm"""
        portion = sample_food * gramm(200)
        assert portion.weight == 200
    
    def test_multiply_by_number(self, sample_food):
        """Test scaling food by number"""
        portion = sample_food * 2.5
        assert portion.weight == 250  # 2.5 * 100 default
    
    def test_add_foods(self):
        """Test combining two foods"""
        food1 = Food(name="Food1", name_de="", nutrition_data={"calories": 100}, weight=100)
        food2 = Food(name="Food2", name_de="", nutrition_data={"calories": 200}, weight=100)
        
        combined = food1 + food2
        assert combined.weight == 200
        assert combined.nutrition_data["calories"] == 150  # Weighted average
    
    def test_divide_food(self, sample_food):
        """Test dividing food"""
        food = sample_food * gramm(300)
        half = food / 2
        assert half.weight == 150
    
    def test_divide_by_zero(self, sample_food):
        """Test dividing by zero raises error"""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            sample_food / 0
    
    def test_get_nutrient(self, sample_food):
        """Test getting nutrient values"""
        # Per 100g (default)
        assert sample_food.get_nutrient("calories") == 0  # weight is 0
        
        # After setting weight
        food_200g = sample_food * gramm(200)
        assert food_200g.get_nutrient("calories") == 200
    
    def test_affects_biomarker(self):
        """Test checking biomarker effects"""
        source = DataSource(url="https://test.com", title="Test", source_type="research")
        effect = FoodEffect(
            target_type=EffectTargetType.BIOMARKER,
            target_name="Vitamin K",
            direction=EffectDirection.INCREASE,
            mechanism="Test",
            sources=[source]
        )
        
        food = Food(
            name="Test",
            name_de="",
            effects=[effect]
        )
        
        effects = food.affects_biomarker("Vitamin K")
        assert len(effects) == 1
        
        effects = food.affects_biomarker("vitamin k")  # Case insensitive
        assert len(effects) == 1
        
        effects = food.affects_biomarker("Iron")
        assert len(effects) == 0


class TestFoodIntake:
    """Test FoodIntake creation and methods"""
    
    @pytest.fixture
    def sample_food(self):
        """Create a sample food"""
        source = DataSource(url="https://test.com", title="Test", source_type="research")
        effect = FoodEffect(
            target_type=EffectTargetType.BIOMARKER,
            target_name="Vitamin C",
            direction=EffectDirection.INCREASE,
            mechanism="Contains vitamin C",
            sources=[source]
        )
        return Food(
            name="Orange",
            name_de="Orange",
            nutrition_data={"vitamin c": 53},
            effects=[effect]
        )
    
    def test_create_intake(self, sample_food):
        """Test creating a FoodIntake"""
        intake = FoodIntake(
            food=sample_food,
            amount=150,
            timestamp=datetime.now()
        )
        
        assert intake.food.name == "Orange"
        assert intake.amount == 150
    
    def test_get_nutrients(self, sample_food):
        """Test getting nutrients for intake"""
        intake = FoodIntake(
            food=sample_food,
            amount=100,
            timestamp=datetime.now()
        )
        
        nutrients = intake.get_nutrients()
        assert nutrients["vitamin c"] == 53
    
    def test_get_effects(self, sample_food):
        """Test getting effects for intake"""
        intake = FoodIntake(
            food=sample_food,
            amount=100,
            timestamp=datetime.now()
        )
        
        effects = intake.get_effects()
        assert len(effects) == 1
        assert effects[0].target_name == "Vitamin C"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
