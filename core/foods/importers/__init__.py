"""
Base importer interface for food data sources.

Importers provide a consistent interface for fetching food data from
external sources like Open Food Facts, BLS (German Federal Food Key), etc.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from ..models import Food


class FoodImporter(ABC):
    """
    Base class for food data importers.
    
    Implementations must provide:
    - name: Identifier for this importer
    - lookup(): Fetch food by ID/barcode
    - Optionally: search() for searching by name
    
    Example:
        >>> class MyImporter(FoodImporter):
        ...     @property
        ...     def name(self):
        ...         return "my_source"
        ...     
        ...     def lookup(self, identifier: str) -> Union[Food, Dict, None]:
        ...         # Implementation
        ...         pass
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the unique name of this importer."""
        pass
    
    @property
    def supports_lookup(self) -> bool:
        """Whether this importer supports ID/barcode lookup."""
        return True
    
    @property
    def supports_search(self) -> bool:
        """Whether this importer supports name-based search."""
        return False
    
    @property
    def supports_raw_format(self) -> bool:
        """
        Can return intermediate dict format instead of Food object.
        
        This allows for validation/caching before creating Food objects.
        """
        return False
    
    @abstractmethod
    def lookup(self, identifier: str) -> Union['Food', Dict[str, Any], None]:
        """
        Look up food by ID or barcode.
        
        Args:
            identifier: Product ID, barcode, or other unique identifier
            
        Returns:
            Food object, raw dict (if supports_raw_format=True), or None
        """
        pass
    
    def search(self, query: str, limit: int = 10) -> List[Union['Food', Dict[str, Any]]]:
        """
        Search for foods by name.
        
        Args:
            query: Search string
            limit: Maximum number of results
            
        Returns:
            List of Food objects or dicts
            
        Raises:
            NotImplementedError: If search is not supported
        """
        raise NotImplementedError(f"{self.name} does not support search")


# Registry of available importers
_importer_registry: Dict[str, FoodImporter] = {}


def register_importer(importer_class):
    """
    Decorator to register an importer class.
    
    Example:
        >>> @register_importer
        ... class OpenFoodFactsImporter(FoodImporter):
        ...     pass
    """
    def decorator(cls):
        instance = cls()
        _importer_registry[instance.name] = instance
        return cls
    return decorator


def get_importer(name: str) -> Optional[FoodImporter]:
    """
    Get a registered importer by name.
    
    Args:
        name: Importer name
        
    Returns:
        FoodImporter instance or None
    """
    return _importer_registry.get(name)


def list_importers() -> List[str]:
    """
    List all registered importer names.
    
    Returns:
        List of importer names
    """
    return list(_importer_registry.keys())


# Import and register all importers
from .openfoodfacts import OpenFoodFactsImporter
from .bls import BLSImporter
from .fddb import FDDBImporter
from .nutritionix import NutritionixImporter
from .yazio import YazioImporter
from .foodb import FooDBImporter
from .foodb_mapping import FooDBMapper, COMPOUND_CLASS_TO_BIOMARKERS, SPECIFIC_COMPOUND_EFFECTS

__all__ = [
    "FoodImporter",
    "register_importer",
    "get_importer",
    "list_importers",
    # Importer classes
    "OpenFoodFactsImporter",
    "BLSImporter",
    "FDDBImporter",
    "NutritionixImporter",
    "YazioImporter",
    "FooDBImporter",
    # FooDB mapping
    "FooDBMapper",
    "COMPOUND_CLASS_TO_BIOMARKERS",
    "SPECIFIC_COMPOUND_EFFECTS",
]
