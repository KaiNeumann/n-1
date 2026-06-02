"""
Tests for food data factories.

Run with: pytest blutwerte/foods/tests/test_food_data.py -v
"""

import pytest

from blutwerte.foods.data import get_all_foods
from blutwerte.foods.data.vegetables import create_spinach, create_tomato
from blutwerte.foods.data.fruits import create_banana
from blutwerte.foods.data.proteins import create_beef, create_lentils
from blutwerte.foods.data.dairy import create_milk
from blutwerte.foods.data.grains import create_oats


class TestVegetableFactories:
    """Test vegetable factory functions"""
    
    def test_create_spinach(self):
        """Test spinach creation"""
        spinach = create_spinach()
        assert spinach.name == "Spinach"
        assert spinach.name_de == "Spinat"
        assert spinach.category == "vegetable"
        assert "vitamin k" in spinach.nutrition_data
        assert len(spinach.effects) > 0
        assert len(spinach.nutrition_sources) > 0
    
    def test_spinach_effects(self):
        """Test spinach has expected effects"""
        spinach = create_spinach()
        vitamin_k_effects = spinach.affects_biomarker("Vitamin K")
        assert len(vitamin_k_effects) > 0
        
        iron_effects = spinach.affects_biomarker("Iron")
        assert len(iron_effects) > 0
        # Iron effect should be VARIABLE
        assert iron_effects[0].direction.value == "variable"
    
    def test_create_tomato(self):
        """Test tomato creation"""
        tomato = create_tomato()
        assert tomato.name == "Tomato"
        assert tomato.category == "vegetable"
        assert "potassium" in tomato.nutrition_data


class TestFruitFactories:
    """Test fruit factory functions"""
    
    def test_create_banana(self):
        """Test banana creation"""
        banana = create_banana()
        assert banana.name == "Banana"
        assert banana.name_de == "Banane"
        assert banana.category == "fruit"
        assert banana.nutrition_data["potassium"] > 300
        
        # Should have potassium effect
        effects = banana.affects_biomarker("Potassium")
        assert len(effects) > 0


class TestProteinFactories:
    """Test protein factory functions"""
    
    def test_create_beef(self):
        """Test beef creation"""
        beef = create_beef()
        assert beef.name == "Beef"
        assert beef.category == "meat"
        assert beef.nutrition_data["iron"] > 2
        
        # Should have iron and B12 effects
        assert len(beef.affects_biomarker("Iron")) > 0
        assert len(beef.affects_biomarker("Vitamin B12")) > 0
    
    def test_create_lentils(self):
        """Test lentils creation"""
        lentils = create_lentils()
        assert lentils.name == "Lentils"
        assert lentils.category == "legume"
        
        # Iron effect should be VARIABLE (non-heme)
        iron_effects = lentils.affects_biomarker("Iron")
        assert len(iron_effects) > 0
        assert iron_effects[0].direction.value == "variable"


class TestDairyFactories:
    """Test dairy factory functions"""
    
    def test_create_milk(self):
        """Test milk creation"""
        milk = create_milk()
        assert milk.name == "Milk"
        assert milk.name_de == "Milch"
        assert milk.category == "dairy"
        assert milk.nutrition_data["calcium"] > 100


class TestGrainFactories:
    """Test grain factory functions"""
    
    def test_create_oats(self):
        """Test oats creation"""
        oats = create_oats()
        assert oats.name == "Oats"
        assert oats.category == "cereal"
        assert oats.nutrition_data["iron"] > 4


class TestAllFoods:
    """Test all foods collection"""
    
    def test_get_all_foods(self):
        """Test that we have 25 food factories"""
        foods = get_all_foods()
        assert len(foods) == 25
    
    def test_all_foods_have_german_names(self):
        """Test that all foods have German names"""
        foods = get_all_foods()
        for factory in foods:
            food = factory()
            assert food.name_de, f"{food.name} missing German name"
    
    def test_all_foods_have_nutrition_sources(self):
        """Test that all foods have nutrition sources"""
        foods = get_all_foods()
        for factory in foods:
            food = factory()
            assert len(food.nutrition_sources) > 0, f"{food.name} missing nutrition sources"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
