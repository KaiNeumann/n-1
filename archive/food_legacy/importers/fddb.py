"""
FDDB Parser Importer

Parses nutrient text copied from FDDB.info website.
https://fddb.info

FDDB provides nutrition data in a simple text format that can be copied.
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
class FDDBImporter(FoodImporter):
    """Parser for FDDB.info nutrient text format.
    
    Supports:
    - Parsing copied text from FDDB.info pages
    
    Example input:
        Brennwert
        108 kJ
        Kalorien
        26 kcal
        Protein
        1,3 g
        ...
    """
    
    @property
    def name(self) -> str:
        return "fddb"
    
    @property
    def display_name(self) -> str:
        return "FDDB.info"
    
    @property
    def supports_lookup(self) -> bool:
        return False
    
    @property
    def supports_parse(self) -> bool:
        return True
    
    def lookup(self, identifier: str) -> Optional[Food]:
        """FDDB does not support API lookup."""
        raise NotImplementedError("FDDB only supports text parsing, not API lookup")
    
    def parse(self, text: str) -> Optional[Food]:
        """Parse FDDB.info nutrient text format.
        
        Args:
            text: Copied nutrient text from FDDB.info
            
        Returns:
            Food object with parsed nutrition data, or None if parsing failed
        """
        nutrient_dict = {}
        lines = text.split('\n')
        skip = True
        
        for i in range(len(lines) - 1):
            if skip:
                skip = False
                continue
            
            line = lines[i].strip()
            next_line = lines[i + 1]
            
            # Skip headers and non-nutrient lines
            if any(skip_word in line for skip_word in [
                "Nährwerte", "Vitamine", "Mineralstoffe",
                "Brennwert", "% Kohlenhydrate", "% Fett", 
                "Broteinheiten"
            ]):
                skip = True
                continue
            
            # Skip lines where next line is kJ or headers
            if "kJ" in next_line or any(header in next_line for header in [
                "Nährwerte", "Vitamine", "Mineralstoffe"
            ]):
                skip = True
                continue
            
            # Clean and normalize nutrient name
            nutriment = (line.lower()
                        .replace('ungesät.', 'ungesättigte')
                        .replace('wassergehalt', 'water')
                        .replace('davon', ''))
            
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
            elif "%" in next_line:
                value = float(next_line.replace('%', '').replace(',', '.').strip())
            else:
                skip = True
                continue
            
            if value:
                nutrient_dict[nutriment] = value
            
            skip = True
        
        if not nutrient_dict:
            return None
        
        return Food(nutrient_dict, 100)
