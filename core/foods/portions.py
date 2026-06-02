"""
Portion system for food measurements.

This module provides standardized portion sizes and measurements for foods,
allowing intuitive quantity specification (e.g., "1 slice of bread", "2 bananas")
rather than just grams.

Portions are adapted from the legacy food system (food_legacy/Food.py).
"""

from typing import Union, Dict, List, Optional


class Amount:
    """
    Simple weight/volume multiplier.
    
    Used for specifying quantities in grams, kilograms, milliliters, or liters.
    
    Example:
        >>> from core.foods import gramm, kilo
        >>> apple = Food({"calories": 52})
        >>> portion = apple * gramm(250)  # 250g of apple
        >>> portion = apple * kilo(1)      # 1kg of apple
    """
    
    def __init__(self, value: Union[int, float]):
        self.value = value
    
    def __call__(self, amount: Union[int, float]) -> 'Amount':
        """Create a scaled amount"""
        return Amount(self.value * amount)


# Base units
gramm = Amount(1)
kilo = Amount(1000)
ml = Amount(1)
liter = Amount(1000)


class Portion:
    """
    Flexible portion sizes with per-food customization.
    
    Portions represent common serving sizes (slice, glass, piece, etc.)
    and can have custom weights defined for specific foods.
    
    Attributes:
        name: Portion name (e.g., "scheibe", "glas")
        weight: Default weight in grams/ml
        sizes: Dict mapping food instance IDs to custom weights
        
    Example:
        >>> from core.foods import scheibe, glas
        >>> bread = Food({"calories": 265}, category="bread")
        >>> portion = bread * scheibe(2)  # 2 slices (2 x 25g = 50g)
        >>> juice = Food({"calories": 45}, category="beverage")
        >>> portion = juice * glas(1)     # 1 glass (200ml)
    """
    
    def __init__(self, name: str, weight: Union[int, float] = 100, 
                 sizes: Optional[Dict[int, Union[int, float]]] = None):
        self.name: str = name
        self.weight: Union[int, float] = weight
        self.sizes: Dict[int, Union[int, float]] = sizes or {}
    
    def __call__(self, amount: Union[int, float] = 1, 
                 custom_weight: Optional[Union[int, float]] = None) -> 'Portion':
        """
        Create a modified portion.
        
        Args:
            amount: Number of portions (default 1)
            custom_weight: Override the base weight (default None = use standard weight)
            
        Returns:
            New Portion with calculated weight
            
        Examples:
            >>> scheibe(2)        # 2 standard slices (2 x 25g = 50g)
            >>> scheibe(2, 100)   # 2 big slices (2 x 100g = 200g)
            >>> scheibe(1, 100)   # 1 big slice (100g)
        """
        if custom_weight is not None:
            base_weight = custom_weight
            new_sizes = {}
        else:
            base_weight = self.weight if self.weight is not None else 100
            new_sizes = {}
            if self.sizes:
                for id_, val in self.sizes.items():
                    new_sizes[id_] = val * amount
        
        return Portion(self.name, base_weight * amount, new_sizes)
    
    def add(self, instance_id: int, amount: Optional[Union[int, float]] = None) -> 'Portion':
        """
        Add a custom size for a specific food instance.
        
        Args:
            instance_id: ID of the food instance
            amount: Custom weight (default to portion's standard weight)
            
        Returns:
            Self for method chaining
        """
        self.sizes[instance_id] = amount or self.weight
        return self
    
    def get(self, instance_id: int) -> Union[int, float]:
        """
        Get the size for a specific food instance.
        
        Returns the custom size if defined, otherwise the standard weight.
        """
        return self.sizes.get(instance_id, self.weight)


class CategoryPortionDefaults:
    """
    Manages default portion sizes for food categories.
    
    Allows setting category-wide defaults that apply when a food doesn't have
    an explicit portion size defined.
    
    Example:
        # Set defaults
        CategoryPortionDefaults.set("beer", flasche, 500)
        CategoryPortionDefaults.set("bread", scheibe, 25)
        
        # Now all "beer" foods will use 500ml for flasche unless overridden
    """
    
    _defaults: Dict[str, Dict[str, Union[int, float]]] = {}
    
    @classmethod
    def set(cls, category: str, portion: Portion, amount: Union[int, float]):
        """
        Set a default portion size for a category.
        
        Args:
            category: Food category name (e.g., 'beer', 'bread', 'yogurt')
            portion: The Portion type (e.g., flasche, scheibe)
            amount: Default amount in grams/ml for this portion
        """
        if category not in cls._defaults:
            cls._defaults[category] = {}
        cls._defaults[category][portion.name] = amount
    
    @classmethod
    def get(cls, category: str, portion_name: str) -> Union[int, float, None]:
        """
        Get default portion size for a category.
        
        Args:
            category: Food category name
            portion_name: Name of the portion type
            
        Returns:
            Default amount or None if not set
        """
        if category in cls._defaults:
            return cls._defaults[category].get(portion_name)
        return None
    
    @classmethod
    def list_categories(cls) -> List[str]:
        """List all categories with defaults defined."""
        return list(cls._defaults.keys())
    
    @classmethod
    def get_category_defaults(cls, category: str) -> Dict[str, Union[int, float]]:
        """Get all default portions for a category."""
        return cls._defaults.get(category, {}).copy()


class PortionRegistry:
    """
    Global registry of portion types.
    
    Manages all defined portions and provides lookup by name.
    """
    
    def __init__(self):
        self.portions: Dict[str, Portion] = {}
    
    def create_portion(self, name: str, weight: Optional[Union[int, float]] = None) -> Portion:
        """
        Create and register a new portion type.
        
        Args:
            name: Portion name (German)
            weight: Default weight in grams/ml
            
        Returns:
            The created Portion
        """
        portion = Portion(name, weight if weight is not None else 100)
        self.portions[name] = portion
        return portion
    
    def get_portion_by_name(self, name: str) -> Optional[Portion]:
        """Get a portion by its name."""
        return self.portions.get(name)
    
    def get_portions_for_food_instance(self, food_instance) -> List[str]:
        """
        Get portion names that have custom sizes for a food instance.
        """
        return [
            portion_name for portion_name, portion in self.portions.items()
            if id(food_instance) in portion.sizes
        ]


# Global registry
Registry = PortionRegistry()


def _initialize_predefined_portions() -> None:
    """Register the 27 predefined Portion objects from
    knowledge/units/portions.jsonl. Each portion becomes a module-level
    name (``scheibe``, ``becher``, ``flasche`` etc.) so callers can do
    ``from core.foods import scheibe``.
    """
    from .portions_jsonl_loader import load_portions_from_jsonl
    for p in load_portions_from_jsonl().values():
        globals()[p["name"]] = Registry.create_portion(p["name"], p["weight_grams"])


_initialize_predefined_portions()

# Base units (Amount, not Portion — not "data", just base arithmetic helpers)
gramm = Amount(1)
kilo = Amount(1000)
ml = Amount(1)
liter = Amount(1000)

# Predefined category defaults
CategoryPortionDefaults.set("beer", flasche, 500)
CategoryPortionDefaults.set("beer", kleine_flasche, 330)
CategoryPortionDefaults.set("bread", scheibe, 25)
CategoryPortionDefaults.set("cheese", scheibe, 20)
CategoryPortionDefaults.set("yogurt", becher, 150)
CategoryPortionDefaults.set("soup", teller, 250)
CategoryPortionDefaults.set("pasta", teller, 210)
CategoryPortionDefaults.set("water", flasche, 750)
CategoryPortionDefaults.set("milk", glas, 200)
CategoryPortionDefaults.set("meat", portion, 100)
CategoryPortionDefaults.set("sausage", stück, 50)
CategoryPortionDefaults.set("beverage", flasche, 500)
CategoryPortionDefaults.set("snack", packung, 100)
CategoryPortionDefaults.set("spread", esslöffel, 15)
CategoryPortionDefaults.set("supplement", tablette, 1)
CategoryPortionDefaults.set("fruit", portion, 150)
CategoryPortionDefaults.set("vegetable", portion, 100)
CategoryPortionDefaults.set("fish", portion, 120)
CategoryPortionDefaults.set("cereal", becher, 50)
CategoryPortionDefaults.set("rice", teller, 180)
CategoryPortionDefaults.set("oil", esslöffel, 10)
CategoryPortionDefaults.set("sweet", stück, 80)
CategoryPortionDefaults.set("prepared", packung, 400)
CategoryPortionDefaults.set("alcohol", glas, 40)
CategoryPortionDefaults.set("legume", becher, 80)
CategoryPortionDefaults.set("spices", teelöffel, 5)
CategoryPortionDefaults.set("seafood", portion, 100)
