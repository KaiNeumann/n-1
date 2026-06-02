"""
Nutritionix API Importer

Provides natural language food lookup via the Nutritionix API.
https://developer.nutritionix.com

Requires API credentials (app_id and app_key).
"""

import requests
import json
from typing import List, Dict, Any, Optional
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Food import Food
from importers import FoodImporter, register_importer


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
        208: "kcal",
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
    def display_name(self) -> str:
        return "Nutritionix"
    
    def _get_headers(self) -> Dict[str, str]:
        """Get API request headers."""
        if not self.app_id or not self.app_key:
            raise ValueError(
                "Nutritionix API credentials required. "
                "Pass app_id and app_key to constructor or set "
                "NUTRITIONIX_APP_ID and NUTRITIONIX_APP_KEY environment variables."
            )
        
        return {
            "Content-Type": "application/json",
            "x-app-id": self.app_id,
            "x-app-key": self.app_key
        }
    
    def lookup(self, query: str) -> Optional[Food]:
        """Lookup food by natural language query.
        
        Args:
            query: Natural language description (e.g., "1 large apple", "grilled chicken breast")
            
        Returns:
            Food object with nutrition data per 100g, or None if not found
            
        Raises:
            ConnectionError: If API request fails
            ValueError: If API credentials not provided
        """
        headers = self._get_headers()
        data = {
            "query": query,
            "timezone": "Europe/Berlin"
        }
        
        try:
            response = requests.post(
                self.API_URL,
                headers=headers,
                data=json.dumps(data),
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            
            if not result.get("foods"):
                return None
            
            food_data = result["foods"][0]
            serving_weight = food_data.get("serving_weight_grams", 100)
            
            if serving_weight == 0:
                serving_weight = 100
            
            # Convert to per 100g
            nutriments = {}
            for item in food_data.get("full_nutrients", []):
                attr_id = item.get("attr_id")
                value = item.get("value")
                
                if attr_id in self.NUTRITION_ATTRIBUTES and value is not None:
                    nutrient_name = self.NUTRITION_ATTRIBUTES[attr_id]
                    # Normalize to per 100g
                    nutriments[nutrient_name] = (value * 100) / serving_weight
            
            if not nutriments:
                return None
            
            return Food(nutriments, 100)
            
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to query Nutritionix API: {e}")
