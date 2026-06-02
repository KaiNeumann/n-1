"""
Food database with indexing and search capabilities.

Provides storage and retrieval of Food objects with multiple indexes
for efficient lookup by name, category, and biomarker effects.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union
from uuid import UUID

from .models import Food, FoodEffect
from .sources import DataSource


@dataclass
class FoodDatabase:
    """
    Container for all foods with multiple indexes.
    
    Provides efficient lookup by:
    - Name (primary and German)
    - Category
    - Nutrient content
    - Biomarker effects
    
    Attributes:
        _foods: Dict of UUID -> Food
        _by_name: Dict of lowercase name -> UUID
        _by_name_de: Dict of German name -> UUID
        _by_category: Dict of category -> List[UUID]
        _by_biomarker: Dict of biomarker name -> List[UUID]
    """
    
    _foods: Dict[UUID, Food] = field(default_factory=dict)
    _by_name: Dict[str, UUID] = field(default_factory=dict)
    _by_name_de: Dict[str, UUID] = field(default_factory=dict)
    _by_category: Dict[str, List[UUID]] = field(default_factory=dict)
    _by_biomarker: Dict[str, List[UUID]] = field(default_factory=dict)
    
    def add(self, food: Food) -> None:
        """
        Add a food to the database.
        
        Args:
            food: Food object to add
            
        Raises:
            ValueError: If food with same name already exists
        """
        # Check for duplicates
        if food.name.lower() in self._by_name:
            raise ValueError(f"Food '{food.name}' already exists in database")
        
        # Store food
        self._foods[food.id] = food
        
        # Index by name
        self._by_name[food.name.lower()] = food.id
        if food.name_de:
            self._by_name_de[food.name_de.lower()] = food.id
        
        # Index by category
        if food.category:
            if food.category not in self._by_category:
                self._by_category[food.category] = []
            self._by_category[food.category].append(food.id)
        
        # Index by biomarker effects
        for effect in food.effects:
            biomarker = effect.target_name.lower()
            if biomarker not in self._by_biomarker:
                self._by_biomarker[biomarker] = []
            if food.id not in self._by_biomarker[biomarker]:
                self._by_biomarker[biomarker].append(food.id)
    
    def get(self, name_or_id: Union[str, UUID]) -> Optional[Food]:
        """
        Get a food by name or UUID.
        
        Args:
            name_or_id: Food name (English or German) or UUID
            
        Returns:
            Food object or None if not found
        """
        if isinstance(name_or_id, UUID):
            return self._foods.get(name_or_id)
        
        # Try by English name
        food_id = self._by_name.get(name_or_id.lower())
        if food_id:
            return self._foods.get(food_id)
        
        # Try by German name
        food_id = self._by_name_de.get(name_or_id.lower())
        if food_id:
            return self._foods.get(food_id)
        
        return None
    
    def search(self, query: str) -> List[Food]:
        """
        Search for foods by partial name match.
        
        Args:
            query: Search string
            
        Returns:
            List of matching Food objects
        """
        query_lower = query.lower()
        results = []
        
        for food in self._foods.values():
            if (query_lower in food.name.lower() or 
                query_lower in food.name_de.lower()):
                results.append(food)
        
        return results
    
    def by_category(self, category: str) -> List[Food]:
        """
        Get all foods in a category.
        
        Args:
            category: Category name (e.g., "vegetable", "fruit")
            
        Returns:
            List of Food objects
        """
        food_ids = self._by_category.get(category, [])
        return [self._foods[food_id] for food_id in food_ids]
    
    def get_affecting_biomarker(self, biomarker_name: str) -> List[Food]:
        """
        Get all foods that affect a specific biomarker.
        
        Args:
            biomarker_name: Name of the biomarker (e.g., "Vitamin K", "Iron")
            
        Returns:
            List of Food objects with effects on this biomarker
        """
        food_ids = self._by_biomarker.get(biomarker_name.lower(), [])
        return [self._foods[food_id] for food_id in food_ids]
    
    def get_rich_in_nutrient(self, nutrient: str, min_amount: float = 10) -> List[Food]:
        """
        Get foods rich in a specific nutrient.
        
        Args:
            nutrient: Nutrient name (e.g., "vitamin k", "iron")
            min_amount: Minimum amount per 100g to be considered "rich"
            
        Returns:
            List of Food objects sorted by nutrient content (highest first)
        """
        results = []
        nutrient_lower = nutrient.lower()
        
        for food in self._foods.values():
            if nutrient_lower in food.nutrition_data:
                if food.nutrition_data[nutrient_lower] >= min_amount:
                    results.append(food)
        
        # Sort by nutrient content (descending)
        results.sort(key=lambda f: f.nutrition_data.get(nutrient_lower, 0), reverse=True)
        return results
    
    def list_all(self) -> List[str]:
        """
        List all food names in the database.
        
        Returns:
            List of food names
        """
        return [food.name for food in self._foods.values()]
    
    def list_categories(self) -> List[str]:
        """
        List all categories in the database.
        
        Returns:
            List of category names
        """
        return list(self._by_category.keys())
    
    def count(self) -> int:
        """Get total number of foods in database."""
        return len(self._foods)
    
    def load_from_module(self, module_name: str) -> None:
        """
        Load foods from a data module.
        
        Args:
            module_name: Name of module containing food factory functions
            
        Example:
            >>> db.load_from_module("blutwerte.foods.data.vegetables")
        """
        import importlib
        
        try:
            module = importlib.import_module(module_name)
            
            # Look for factory functions (create_* functions)
            for attr_name in dir(module):
                if attr_name.startswith("create_"):
                    factory = getattr(module, attr_name)
                    if callable(factory):
                        try:
                            food = factory()
                            if isinstance(food, Food):
                                self.add(food)
                        except Exception as e:
                            print(f"Warning: Could not create food from {attr_name}: {e}")
        except ImportError as e:
            raise ImportError(f"Could not import module {module_name}: {e}")
    
    def load_all(self) -> None:
        """
        Load all foods. Prefers JSONL under knowledge/foods/, falls back to Python.
        """
        from .jsonl_loader import load_foods_from_jsonl, load_foods_from_python

        loaded = load_foods_from_jsonl()
        if not loaded:
            loaded = load_foods_from_python()
        for food in loaded.values():
            try:
                self.add(food)
            except ValueError:
                continue  # duplicate name from cross-source overlap

    def _load_all_python(self) -> None:
        """Legacy Python-authored food loader. Only used as fallback."""
        modules = [
            "blutwerte.foods.data.vegetables",
            "blutwerte.foods.data.fruits",
            "blutwerte.foods.data.proteins.meat",
            "blutwerte.foods.data.proteins.fish",
            "blutwerte.foods.data.proteins.eggs",
            "blutwerte.foods.data.proteins.legumes",
            "blutwerte.foods.data.proteins.plant",
            "blutwerte.foods.data.dairy",
            "blutwerte.foods.data.grains",
        ]

        for module in modules:
            try:
                self.load_from_module(module)
            except ImportError:
                pass  # Module might not exist yet


# Global database instance
db = FoodDatabase()
