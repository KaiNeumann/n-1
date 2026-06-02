"""
Open Food Facts importer.

Fetches food data from the Open Food Facts database.
API documentation: https://world.openfoodfacts.org/data
"""

from typing import Any, Dict, Optional, Union

from .. import Food, DataSource, create_source
from . import FoodImporter, register_importer


@register_importer
class OpenFoodFactsImporter(FoodImporter):
    """
    Importer for Open Food Facts database.
    
    Open Food Facts is a free, open database of food products from around the world.
    
    Example:
        >>> importer = OpenFoodFactsImporter()
        >>> food = importer.lookup("3017620422003")  # Nutella
        >>> print(food.name)
    """
    
    API_BASE = "https://world.openfoodfacts.org/api/v2"
    
    @property
    def name(self) -> str:
        return "openfoodfacts"
    
    @property
    def supports_search(self) -> bool:
        return True
    
    def lookup(self, identifier: str) -> Union[Food, Dict[str, Any], None]:
        """
        Look up food by barcode.
        
        Args:
            barcode: Product barcode (EAN-13 or EAN-8)
            
        Returns:
            Food object or None if not found
        """
        try:
            import requests
            
            url = f"{self.API_BASE}/product/{identifier}.json"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") != 1:
                return None
            
            product = data.get("product", {})
            return self._create_food(product, identifier)
            
        except ImportError:
            raise ImportError("requests package required. Install with: pip install requests")
        except Exception as e:
            print(f"Error fetching from Open Food Facts: {e}")
            return None
    
    def search(self, query: str, limit: int = 10) -> list:
        """
        Search for foods by name.
        
        Args:
            query: Search string
            limit: Maximum number of results
            
        Returns:
            List of Food objects
        """
        try:
            import requests
            
            url = f"{self.API_BASE}/search"
            params = {
                "search_terms": query,
                "page_size": limit,
                "fields": "product_name,nutriments,code"
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            products = data.get("products", [])
            
            foods = []
            for product in products[:limit]:
                food = self._create_food(product, product.get("code", ""))
                if food:
                    foods.append(food)
            
            return foods
            
        except ImportError:
            raise ImportError("requests package required. Install with: pip install requests")
        except Exception as e:
            print(f"Error searching Open Food Facts: {e}")
            return []
    
    def _create_food(self, product: Dict, barcode: str) -> Optional[Food]:
        """
        Create Food object from Open Food Facts product data.
        
        Args:
            product: Product data from API
            barcode: Product barcode
            
        Returns:
            Food object or None
        """
        name = product.get("product_name", "")
        if not name:
            return None
        
        # Extract nutrition data
        nutriments = product.get("nutriments", {})
        nutrition_data = {}
        
        # Map Open Food Facts nutrient names to our format
        mapping = {
            "energy-kcal_100g": "calories",
            "proteins_100g": "protein",
            "carbohydrates_100g": "carbohydrate",
            "fat_100g": "fat",
            "fiber_100g": "fiber",
            "sugars_100g": "sugar",
            "salt_100g": "salt",
            "sodium_100g": "sodium",
            "iron_100g": "iron",
            "calcium_100g": "calcium",
            "potassium_100g": "potassium",
            "magnesium_100g": "magnesium",
            "zinc_100g": "zinc",
            "vitamin-c_100g": "vitamin c",
            "vitamin-d_100g": "vitamin d",
            "vitamin-b12_100g": "vitamin b12",
            "folates_100g": "folate",
            "vitamin-k_100g": "vitamin k",
        }
        
        for off_key, our_key in mapping.items():
            value = nutriments.get(off_key)
            if value is not None:
                # Convert mg to g where needed
                if off_key in ["iron_100g", "calcium_100g", "potassium_100g", 
                              "magnesium_100g", "zinc_100g", "vitamin-c_100g",
                              "vitamin-d_100g", "vitamin-b12_100g", "folates_100g",
                              "vitamin-k_100g"]:
                    # Values in OFF are already per 100g in the specified unit
                    nutrition_data[our_key] = value
                else:
                    nutrition_data[our_key] = value
        
        # Get German name if available
        name_de = product.get("product_name_de", "")
        
        # Create source
        source = create_source(
            url=f"https://world.openfoodfacts.org/product/{barcode}",
            title=f"Open Food Facts - {name}",
            source_type="database"
        )
        
        return Food(
            name=name,
            name_de=name_de,
            nutrition_data=nutrition_data,
            nutrition_sources=[source]
        )
