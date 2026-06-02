"""
Tests for the portion system.

Run with: pytest blutwerte/foods/tests/test_portions.py -v
"""

import pytest

from blutwerte.foods import (
    Amount, Portion, CategoryPortionDefaults, Registry,
    gramm, kilo, scheibe, glas, flasche, portion,
    becher, tasse, teller
)


class TestAmount:
    """Test Amount class"""
    
    def test_create_amount(self):
        """Test creating Amount"""
        amt = Amount(100)
        assert amt.value == 100
    
    def test_scale_amount(self):
        """Test scaling Amount"""
        gram = Amount(1)
        two_hundred = gram(200)
        assert two_hundred.value == 200
    
    def test_predefined_units(self):
        """Test predefined units"""
        assert gramm(100).value == 100
        assert kilo(1).value == 1000


class TestPortion:
    """Test Portion class"""
    
    def test_create_portion(self):
        """Test creating Portion"""
        p = Portion("test", 50)
        assert p.name == "test"
        assert p.weight == 50
    
    def test_portion_call(self):
        """Test calling portion to scale"""
        slice_portion = Portion("slice", 25)
        two_slices = slice_portion(2)
        assert two_slices.weight == 50
    
    def test_portion_custom_weight(self):
        """Test portion with custom weight"""
        slice_portion = Portion("slice", 25)
        big_slice = slice_portion(1, custom_weight=50)
        assert big_slice.weight == 50
    
    def test_add_custom_size(self):
        """Test adding custom size for food instance"""
        p = Portion("slice", 25)
        p.add(id(self), 30)  # Use test instance ID
        assert p.get(id(self)) == 30


class TestCategoryPortionDefaults:
    """Test CategoryPortionDefaults class"""
    
    def test_set_default(self):
        """Test setting category default"""
        CategoryPortionDefaults.set("test_category", scheibe, 30)
        assert CategoryPortionDefaults.get("test_category", "scheibe") == 30
    
    def test_get_nonexistent(self):
        """Test getting non-existent default"""
        result = CategoryPortionDefaults.get("nonexistent", "scheibe")
        assert result is None
    
    def test_list_categories(self):
        """Test listing categories"""
        cats = CategoryPortionDefaults.list_categories()
        assert isinstance(cats, list)
        assert "beer" in cats  # Predefined
        assert "bread" in cats


class TestRegistry:
    """Test PortionRegistry"""
    
    def test_get_portion_by_name(self):
        """Test getting portion by name"""
        p = Registry.get_portion_by_name("scheibe")
        assert p is not None
        assert p.name == "scheibe"
    
    def test_get_nonexistent_portion(self):
        """Test getting non-existent portion"""
        p = Registry.get_portion_by_name("nonexistent")
        assert p is None
    
    def test_predefined_portions(self):
        """Test that predefined portions exist"""
        portions = [
            "becher", "beutel", "dose", "eins", "esslöffel",
            "flasche", "glas", "handvoll", "kleine_flasche", "kugel",
            "packung", "pad", "portion", "pott", "prise",
            "scheibe", "schnapsglas", "schüssel", "stück", "tablette",
            "tafel", "tasse", "teelöffel", "teller", "topf", "tüte", "zehe"
        ]
        
        for name in portions:
            p = Registry.get_portion_by_name(name)
            assert p is not None, f"Portion '{name}' not found"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
