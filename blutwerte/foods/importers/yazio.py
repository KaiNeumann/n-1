"""
Yazio Importer

Importer for Yazio food database.
https://www.yazio.com

Note: Yazio doesn't have a public API, so this importer works with
exported data or manual entries.
"""

from typing import Optional, Dict, Any, List

from .. import Food, DataSource, create_source
from . import FoodImporter, register_importer


@register_importer
class YazioImporter(FoodImporter):
    """Importer for Yazio food data.
    
    Note: Yazio doesn't provide a public API. This importer is designed
    to work with exported data files or manual food entries.
    
    For automated import, consider using the FDDB or Nutritionix importers
    which support web APIs.
    """
    
    @property
    def name(self) -> str:
        return "yazio"
    
    @property
    def supports_lookup(self) -> bool:
        return False
    
    @property
    def supports_search(self) -> bool:
        return False
    
    def lookup(self, identifier: str) -> Optional[Food]:
        """Yazio does not support API lookup."""
        raise NotImplementedError(
            "Yazio does not provide a public API. "
            "Use migrated Yazio foods from blutwerte.foods.data.legacy.food_yazio_migrated"
        )
    
    def search(self, query: str, limit: int = 10) -> List[Food]:
        """Yazio does not support search."""
        raise NotImplementedError(
            "Yazio does not provide a public API. "
            "Use migrated Yazio foods from blutwerte.foods.data.legacy.food_yazio_migrated"
        )
    
    def import_from_dict(self, data: Dict[str, Any]) -> Food:
        """
        Import food from a dictionary (e.g., exported from Yazio).
        
        Args:
            data: Dictionary with Yazio food data
            
        Returns:
            Food object
            
        Example:
            >>> data = {
            ...     "name": "Yazio Food",
            ...     "calories": 100,
            ...     "protein": 5,
            ...     ...
            ... }
            >>> food = importer.import_from_dict(data)
        """
        # Extract nutrition data
        nutrition_data = {}
        
        mappings = {
            "calories": "calories",
            "protein": "protein",
            "fat": "fat",
            "carbohydrate": "carbohydrate",
            "fiber": "fiber",
            "sugar": "sugar",
        }
        
        for yazio_key, our_key in mappings.items():
            if yazio_key in data:
                nutrition_data[our_key] = data[yazio_key]
        
        # Create source
        source = create_source(
            url="https://www.yazio.com",
            title=f"Yazio - {data.get('name', 'Unknown')}",
            source_type="database"
        )
        
        return Food(
            name=data.get("name", "Yazio Food"),
            name_de=data.get("name", "Yazio Food"),
            nutrition_data=nutrition_data,
            nutrition_sources=[source]
        )
