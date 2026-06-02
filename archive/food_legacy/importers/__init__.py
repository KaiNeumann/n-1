"""
Food Importers Plugin System

This module provides a plugin architecture for importing food data from various sources.
New importers can be added by creating a module in this package and using the @register_importer decorator.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional, List, Any
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class FoodImporter(ABC):
    """Abstract base class for all food importers.
    
    Each importer represents a different source of food data (API, parser, etc.)
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier for this importer (e.g., 'openfoodfacts', 'fddb')."""
        pass
    
    @property
    @abstractmethod
    def display_name(self) -> str:
        """Human-readable name (e.g., 'Open Food Facts')."""
        pass
    
    @property
    def supports_lookup(self) -> bool:
        """Whether this importer supports lookup by ID/barcode."""
        return True
    
    @property
    def supports_search(self) -> bool:
        """Whether this importer supports searching by name."""
        return False
    
    @property
    def supports_parse(self) -> bool:
        """Whether this importer supports parsing text format."""
        return False
    
    def lookup(self, identifier: str) -> Optional[Any]:
        """Lookup food by ID, barcode, or other identifier.
        
        Args:
            identifier: The unique identifier for the food item
            
        Returns:
            Food object or None if not found
        """
        if not self.supports_lookup:
            raise NotImplementedError(f"{self.name} does not support lookup")
        return None
    
    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for foods by name.
        
        Args:
            query: Search term
            limit: Maximum number of results
            
        Returns:
            List of dictionaries with food information
        """
        if not self.supports_search:
            raise NotImplementedError(f"{self.name} does not support search")
        return []
    
    def parse(self, text: str) -> Optional[Any]:
        """Parse text format from this source.
        
        Args:
            text: Raw text to parse
            
        Returns:
            Food object or None if parsing failed
        """
        if not self.supports_parse:
            raise NotImplementedError(f"{self.name} does not support parsing")
        return None


# Registry of available importers
_registry: Dict[str, type] = {}


def register_importer(cls):
    """Decorator to register an importer class.
    
    Usage:
        @register_importer
        class MyImporter(FoodImporter):
            @property
            def name(self) -> str:
                return "my_source"
    """
    instance = cls()
    _registry[instance.name] = cls
    return cls


def get_importer(name: str) -> FoodImporter:
    """Get an importer instance by name.
    
    Args:
        name: The importer name (e.g., 'openfoodfacts')
        
    Returns:
        Instance of the requested importer
        
    Raises:
        ValueError: If importer not found
    """
    if name not in _registry:
        available = ", ".join(_registry.keys())
        raise ValueError(f"Unknown importer: '{name}'. Available: {available}")
    return _registry[name]()


def list_importers() -> List[str]:
    """List all registered importer names."""
    return list(_registry.keys())


def get_importer_info(name: str) -> Dict[str, Any]:
    """Get information about a registered importer.
    
    Returns:
        Dictionary with importer metadata
    """
    if name not in _registry:
        raise ValueError(f"Unknown importer: '{name}'")
    
    importer = _registry[name]()
    return {
        "name": importer.name,
        "display_name": importer.display_name,
        "supports_lookup": importer.supports_lookup,
        "supports_search": importer.supports_search,
        "supports_parse": importer.supports_parse
    }


# Auto-import all importers in this package
def _auto_import_importers():
    """Automatically discover and import all importer modules."""
    import importlib
    import pkgutil
    
    package_dir = os.path.dirname(__file__)
    for _, name, ispkg in pkgutil.iter_modules([package_dir]):
        if not ispkg and name not in ['base', '__init__']:
            try:
                importlib.import_module(f'{__name__}.{name}')
            except ImportError as e:
                print(f"Warning: Could not import importer '{name}': {e}")


# Auto-import on module load
_auto_import_importers()
