"""
Tests for the food database.

Run with: pytest core/foods/tests/test_database.py -v
"""

import pytest

from core.foods import Food, FoodDatabase, DataSource, EffectTargetType, EffectDirection, FoodEffect


class TestFoodDatabase:
    """Test FoodDatabase functionality"""
    
    @pytest.fixture
    def empty_db(self):
        """Create empty database"""
        return FoodDatabase()
    
    @pytest.fixture
    def sample_food(self):
        """Create sample food"""
        return Food(
            name="Test Apple",
            name_de="Test Apfel",
            category="fruit",
            nutrition_data={"calories": 52, "vitamin c": 5}
        )
    
    @pytest.fixture
    def food_with_effect(self):
        """Create food with biomarker effect"""
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
            category="fruit",
            nutrition_data={"vitamin c": 53},
            effects=[effect]
        )
    
    def test_add_food(self, empty_db, sample_food):
        """Test adding food to database"""
        empty_db.add(sample_food)
        assert empty_db.count() == 1
    
    def test_add_duplicate_raises_error(self, empty_db, sample_food):
        """Test adding duplicate food raises error"""
        empty_db.add(sample_food)
        with pytest.raises(ValueError, match="already exists"):
            empty_db.add(sample_food)
    
    def test_get_by_name(self, empty_db, sample_food):
        """Test getting food by name"""
        empty_db.add(sample_food)
        retrieved = empty_db.get("Test Apple")
        assert retrieved is not None
        assert retrieved.name == "Test Apple"
    
    def test_get_by_german_name(self, empty_db, sample_food):
        """Test getting food by German name"""
        empty_db.add(sample_food)
        retrieved = empty_db.get("Test Apfel")
        assert retrieved is not None
        assert retrieved.name == "Test Apple"
    
    def test_get_nonexistent(self, empty_db):
        """Test getting non-existent food"""
        retrieved = empty_db.get("Nonexistent")
        assert retrieved is None
    
    def test_search(self, empty_db):
        """Test searching foods"""
        food1 = Food(name="Apple Pie", name_de="Apfelkuchen", nutrition_data={})
        food2 = Food(name="Apple Juice", name_de="Apfelschorle", nutrition_data={})
        food3 = Food(name="Banana", name_de="Banane", nutrition_data={})
        
        empty_db.add(food1)
        empty_db.add(food2)
        empty_db.add(food3)
        
        results = empty_db.search("apple")
        assert len(results) == 2
        
        results = empty_db.search("Apfel")
        assert len(results) == 2
    
    def test_by_category(self, empty_db):
        """Test getting foods by category"""
        food1 = Food(name="Apple", name_de="Apfel", category="fruit", nutrition_data={})
        food2 = Food(name="Carrot", name_de="Karotte", category="vegetable", nutrition_data={})
        food3 = Food(name="Banana", name_de="Banane", category="fruit", nutrition_data={})
        
        empty_db.add(food1)
        empty_db.add(food2)
        empty_db.add(food3)
        
        fruits = empty_db.by_category("fruit")
        assert len(fruits) == 2
        
        vegetables = empty_db.by_category("vegetable")
        assert len(vegetables) == 1
    
    def test_get_affecting_biomarker(self, empty_db, food_with_effect):
        """Test getting foods affecting a biomarker"""
        empty_db.add(food_with_effect)
        
        foods = empty_db.get_affecting_biomarker("Vitamin C")
        assert len(foods) == 1
        assert foods[0].name == "Orange"
    
    def test_get_rich_in_nutrient(self, empty_db):
        """Test getting foods rich in nutrient"""
        food1 = Food(name="Spinach", name_de="Spinat", nutrition_data={"iron": 2.7})
        food2 = Food(name="Beef", name_de="Rind", nutrition_data={"iron": 2.6})
        food3 = Food(name="Apple", name_de="Apfel", nutrition_data={"iron": 0.1})
        
        empty_db.add(food1)
        empty_db.add(food2)
        empty_db.add(food3)
        
        rich_foods = empty_db.get_rich_in_nutrient("iron", min_amount=1.0)
        assert len(rich_foods) == 2
        # Should be sorted by amount (descending)
        assert rich_foods[0].name == "Spinach"
    
    def test_list_all(self, empty_db, sample_food):
        """Test listing all foods"""
        empty_db.add(sample_food)
        foods = empty_db.list_all()
        assert len(foods) == 1
        assert "Test Apple" in foods


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
