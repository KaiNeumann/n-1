"""
Nutritionix API Importer

Provides natural language food lookup via the Nutritionix API.
https://developer.nutritionix.com

Requires API credentials (app_id and app_key).
"""

import os
from typing import List, Dict, Any, Optional

from .. import Food, DataSource, create_source
from . import FoodImporter, register_importer


@register_importer
class NutritionixImporter(FoodImporter):
    """Importer for Nutritionix API.
    
    Supports:
    - Natural language food lookup (e.g., "1 large apple")
    
    Requires API credentials. Get them at: https://developer.nutritionix.com/admin/access_details
    """
    
    API_URL = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    
    # Nutrition attribute mapping (Nutritionix attr_id to Food names)
    NUTRITION_ATTRIBUTES = {
        203: "protein",
        204: "fat",
        205: "carbohydrate",
        208: "calories",
        209: "starch",
        210: "sucrose",
        211: "glucose",
        212: "fructose",
        213: "lactose",
        214: "maltose",
        221: "alcohol",
        255: "water",
        260: "mannitol",
        261: "sorbitol",
        262: "caffeine",
        269: "sugar",
        291: "fiber",
        301: "calcium",
        303: "iron",
        304: "magnesium",
        305: "phosphorus",
        306: "potassium",
        307: "sodium",
        309: "zinc",
        312: "copper",
        313: "fluoride",
        315: "manganese",
        317: "selenium",
        318: "vitamin a",
        319: "retinol",
        321: "beta carotene",
        322: "alpha carotene",
        323: "vitamin e",
        324: "vitamin d",
        325: "vitamin d2",
        326: "vitamin d3",
        401: "vitamin c",
        404: "thiamin",
        405: "riboflavin",
        406: "niacin",
        410: "pantothenic acid",
        415: "vitamin b6",
        418: "vitamin b12",
        430: "vitamin k",
        431: "folic acid",
        515: "glutamic acid",
        573: "vitamin e",
        601: "cholesterol",
        605: "trans fat",
        606: "saturated-fat",
        645: "monounsaturated fat",
        646: "polyunsaturated fat"
    }
    
    def __init__(self, app_id: Optional[str] = None, app_key: Optional[str] = None):
        """Initialize with API credentials.
        
        Args:
            app_id: Nutritionix app ID (or set NUTRITIONIX_APP_ID env var)
            app_key: Nutritionix app key (or set NUTRITIONIX_APP_KEY env var)
        """
        self.app_id = app_id or os.getenv("NUTRITIONIX_APP_ID")
        self.app_key = app_key or os.getenv("NUTRITIONIX_APP_KEY")
    
    @property
    def name(self) -> str:
        return "nutritionix"
    
    @property
    def supports_search(self) -> bool:
        return True
    
    def lookup(self, identifier: str) -> Optional[Food]:
        """
        Look up food by natural language query.
        
        Args:
            identifier: Natural language query (e.g., "1 large apple")
            
        Returns:
            Food object or None
            
        Raises:
            ImportError: If requests not installed
            ValueError: If API credentials not set
        """
        try:
            import requests
        except ImportError:
            raise ImportError("requests package required. Install with: pip install requests")
        
        if not self.app_id or not self.app_key:
            raise ValueError(
                "Nutritionix API credentials required. "
                "Set NUTRITIONIX_APP_ID and NUTRITIONIX_APP_KEY environment variables "
                "or pass to constructor."
            )
        
        headers = {
            "Content-Type": "application/json",
            "x-app-id": self.app_id,
            "x-app-key": self.app_key,
        }
        
        data = {
            "query": identifier,
            "timezone": "US/Eastern"
        }
        
        try:
            response = requests.post(self.API_URL, headers=headers, json=data, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            if "foods" not in result or not result["foods"]:
                return None
            
            food_data = result["foods"][0]
            return self._create_food_from_nutritionix(food_data)
            
        except requests.RequestException as e:
            print(f"Error querying Nutritionix: {e}")
            return None
    
    def search(self, query: str, limit: int = 10) -> List[Food]:
        """Search foods by natural language query.
        
        Args:
            query: Search query
            limit: Maximum results
            
        Returns:
            List of Food objects
        """
        # Nutritionix natural API returns multiple foods in one query
        food = self.lookup(query)
        if food:
            return [food]
        return []
    
    def _create_food_from_nutritionix(self, data: Dict) -> Food:
        """Create Food object from Nutritionix API response."""
        nutrition_data = {}
        
        # Map nutrients
        for attr_id, attr_name in self.NUTRITION_ATTRIBUTES.items():
            value = data.get(attr_name)
            if value is not None:
                nutrition_data[attr_name] = value
        
        # Get food name
        food_name = data.get("food_name", "Unknown")
        brand = data.get("brand_name")
        if brand:
            food_name = f"{brand} {food_name}"
        
        # Create source
        source = create_source(
            url="https://developer.nutritionix.com",
            title=f"Nutritionix - {food_name}",
            source_type="database"
        )
        
        return Food(
            name=food_name,
            name_de=food_name,  # Nutritionix is primarily English
            nutrition_data=nutrition_data,
            nutrition_sources=[source]
        )
