"""
Yazio Parser Importer

Parses nutrient text copied from Yazio.com website.
https://www.yazio.com

Yazio provides nutrition data in a simple text format that can be copied.
This importer parses that format into Food objects.
"""

from typing import Optional, Dict, Any
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Food import Food
from importers import FoodImporter, register_importer


@register_importer
class YazioImporter(FoodImporter):
    """Parser for Yazio.com nutrient text format.
    
    Supports:
    - Parsing copied text from Yazio.com pages
    
    Example input:
        Nährwerte
        pro Portion
        Brennwert
        266 kcal
        1.114 kJ
        Fett
        12,7 g
        ...
    """
    
    @property
    def name(self) -> str:
        return "yazio"
    
    @property
    def display_name(self) -> str:
        return "Yazio"
    
    @property
    def supports_lookup(self) -> bool:
        return False
    
    @property
    def supports_parse(self) -> bool:
        return True
    
    def lookup(self, identifier: str) -> Optional[Food]:
        """Yazio does not support API lookup."""
        raise NotImplementedError("Yazio only supports text parsing, not API lookup")
    
    def parse(self, text: str) -> Optional[Food]:
        """Parse Yazio.com nutrient text format.
        
        Args:
            text: Copied nutrient text from Yazio.com
            
        Returns:
            Food object with parsed nutrition data, or None if parsing failed
        """
        nutrient_dict = {}
        lines = text.split('\n')
        skip = False
        
        for i in range(len(lines) - 1):
            if skip:
                skip = False
                continue
            
            line = lines[i].strip()
            next_line = lines[i + 1]
            
            # Skip headers and non-nutrient lines
            skip_keywords = [
                "<", "kJ", "pro Portion", "Nährwerte", 
                "Vitamine", "Mineralstoffe"
            ]
            
            if any(kw in line for kw in skip_keywords):
                continue
            
            if any(kw in next_line for kw in skip_keywords):
                continue
            
            # Clean and normalize nutrient name
            nutriment = line.lower().replace('ungesät.', 'ungesättigte')
            
            value = 0.0
            
            # Parse value with unit
            if "kcal" in next_line:
                value = float(next_line.replace('kcal', '').replace(',', '.').strip())
            elif "mg" in next_line:
                value = float(next_line.replace('mg', '').replace(',', '.').strip()) / 1000
            elif "μg" in next_line:
                value = float(next_line.replace('μg', '').replace(',', '.').strip()) / 1000000
            elif "g" in next_line:
                value = float(next_line.replace('g', '').replace(',', '.').strip())
            else:
                continue
            
            if value:
                nutrient_dict[nutriment] = value
            
            skip = True
        
        if not nutrient_dict:
            return None
        
        return Food(nutrient_dict, 100)
