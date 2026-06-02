"""
Tests for food data, now sourced from knowledge/foods/ JSONL.

The previous version of this file imported create_* factory functions
from blutwerte.foods.data.* modules. After the JSONL migration (see
docs/MIGRATION_TO_JSON.md), those modules were deleted; this test
file now loads from the JSONL knowledge base and asserts the same
shape on the reconstructed Food objects.
"""

import pytest

from blutwerte.foods.jsonl_loader import load_foods_from_jsonl
from blutwerte.foods.models import Food


PRIORITY_FOODS = [
    "Spinach", "Tomato", "Potato", "Bell Pepper", "Kale", "Broccoli",
    "Banana", "Orange", "Avocado", "Strawberry",
    "Beef", "Chicken Breast", "Salmon", "Egg", "Lentils", "Tofu",
    "Milk", "Yogurt", "Cheddar Cheese",
    "Oats", "Quinoa", "Brown Rice",
]


@pytest.fixture(scope="module")
def foods():
    return load_foods_from_jsonl()


class TestVegetableFactories:
    """Test vegetable food reconstruction from JSONL."""

    def test_create_spinach(self, foods):
        spinach = foods.get("spinach")
        assert isinstance(spinach, Food)
        assert spinach.name == "Spinach"
        assert spinach.name_de == "Spinat"
        assert spinach.category == "vegetable"
        assert "vitamin k" in spinach.nutrition_data
        assert len(spinach.effects) > 0
        assert len(spinach.nutrition_sources) > 0

    def test_spinach_effects(self, foods):
        spinach = foods["spinach"]
        vitamin_k_effects = spinach.affects_biomarker("Vitamin K")
        assert len(vitamin_k_effects) > 0

        iron_effects = spinach.affects_biomarker("Iron")
        assert len(iron_effects) > 0
        assert iron_effects[0].direction.value == "variable"

    def test_create_tomato(self, foods):
        tomato = foods["tomato"]
        assert tomato.name == "Tomato"
        assert tomato.category == "vegetable"
        assert "potassium" in tomato.nutrition_data


class TestFruitFactories:
    """Test fruit food reconstruction from JSONL."""

    def test_create_banana(self, foods):
        banana = foods["banana"]
        assert banana.name == "Banana"
        assert banana.name_de == "Banane"
        assert banana.category == "fruit"
        assert banana.nutrition_data["potassium"] > 300
        effects = banana.affects_biomarker("Potassium")
        assert len(effects) > 0


class TestProteinFactories:
    """Test protein food reconstruction from JSONL."""

    def test_create_beef(self, foods):
        beef = foods["beef"]
        assert beef.name == "Beef"
        assert beef.category == "meat"
        assert beef.nutrition_data["iron"] > 2
        assert len(beef.affects_biomarker("Iron")) > 0
        assert len(beef.affects_biomarker("Vitamin B12")) > 0

    def test_create_lentils(self, foods):
        lentils = foods["lentils"]
        assert lentils.name == "Lentils"
        assert lentils.category == "legume"
        iron_effects = lentils.affects_biomarker("Iron")
        assert len(iron_effects) > 0
        assert iron_effects[0].direction.value == "variable"


class TestDairyFactories:
    """Test dairy food reconstruction from JSONL."""

    def test_create_milk(self, foods):
        milk = foods["milk"]
        assert milk.name == "Milk"
        assert milk.name_de == "Milch"
        assert milk.category == "dairy"
        assert milk.nutrition_data["calcium"] > 100


class TestGrainFactories:
    """Test grain food reconstruction from JSONL."""

    def test_create_oats(self, foods):
        oats = foods["oats"]
        assert oats.name == "Oats"
        assert oats.category == "cereal"
        assert oats.nutrition_data["iron"] > 4


class TestAllFoods:
    """Test all priority foods present in JSONL."""

    def test_priority_foods_present(self, foods):
        for name in PRIORITY_FOODS:
            assert name.lower() in foods, f"{name} missing from JSONL"

    def test_all_foods_have_german_names(self, foods):
        for name in PRIORITY_FOODS:
            food = foods[name.lower()]
            assert food.name_de, f"{food.name} missing German name"

    def test_all_foods_have_nutrition_sources(self, foods):
        for name in PRIORITY_FOODS:
            food = foods[name.lower()]
            assert len(food.nutrition_sources) > 0, f"{food.name} missing nutrition sources"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
