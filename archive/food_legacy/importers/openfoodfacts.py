"""
Open Food Facts API Importer

Provides lookup and search functionality for the Open Food Facts database.
https://world.openfoodfacts.org
"""

import requests
from typing import List, Dict, Any, Optional
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Food import Food
from importers import FoodImporter, register_importer


@register_importer
class OpenFoodFactsImporter(FoodImporter):
    """Importer for Open Food Facts API.
    
    Supports:
    - Lookup by barcode
    - Search by product name
    """
    
    BASE_URL = "https://world.openfoodfacts.org"
    
    @property
    def name(self) -> str:
        return "openfoodfacts"
    
    @property
    def display_name(self) -> str:
        return "Open Food Facts"
    
    @property
    def supports_search(self) -> bool:
        return True
    
    def _parse_nutriments(self, nutriments: Dict[str, Any]) -> Dict[str, float]:
        """Extract nutrition data from Open Food Facts format.
        
        Converts _100g suffixed keys to standard format and normalizes units.
        """
        result = {}
        for key, value in nutriments.items():
            if "_100g" in key and value is not None:
                # Remove _100g suffix
                nutrient_key = key.replace("_100g", "")
                try:
                    result[nutrient_key] = float(value)
                except (ValueError, TypeError):
                    continue
        return result
    
    def lookup(self, barcode: str) -> Optional[Food]:
        """Lookup food by barcode.
        
        Args:
            barcode: Product barcode (EAN/UPC)
            
        Returns:
            Food object with nutrition data, or None if not found
            
        Raises:
            ConnectionError: If API request fails
        """
        # Clean barcode
        barcode = str(barcode).strip()
        
        url = f"{self.BASE_URL}/api/v0/product/{barcode}.json"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if not data.get("product"):
                return None
            
            product = data["product"]
            nutriments = product.get("nutriments", {})
            
            if not nutriments:
                return None
            
            # Parse nutrition data
            nutrition_data = self._parse_nutriments(nutriments)
            
            if not nutrition_data:
                return None
            
            return Food(nutrition_data, 100)
            
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to query Open Food Facts API: {e}")
    
    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for products by name.
        
        Args:
            query: Product name or keywords
            limit: Maximum number of results (default 10)
            
        Returns:
            List of product dictionaries with keys: name, barcode, brand, 
            categories, image_url, url
            
        Raises:
            ConnectionError: If API request fails
        """
        url = f"{self.BASE_URL}/cgi/search.pl"
        params = {
            "search_terms": query,
            "search_simple": 1,
            "action": "process",
            "json": 1,
            "page_size": limit
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for product in data.get("products", [])[:limit]:
                results.append({
                    "name": product.get("product_name", "Unknown"),
                    "barcode": product.get("code", ""),
                    "brand": product.get("brands", ""),
                    "categories": product.get("categories", ""),
                    "image_url": product.get("image_url", ""),
                    "url": product.get("url", "")
                })
            
            return results
            
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to search Open Food Facts: {e}")
