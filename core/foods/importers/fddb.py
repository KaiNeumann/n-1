"""
FDDB Parser Importer

Parses nutrient text copied from FDDB.info website.
https://fddb.info

FDDB provides nutrition data in a simple text format that can be copied.
This importer parses that format into Food objects.
"""

from typing import Optional, Dict, Any

from .. import Food, DataSource, create_source
from . import FoodImporter, register_importer


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
    def supports_lookup(self) -> bool:
        return False
    
    @property
    def supports_search(self) -> bool:
        return False
    
    @property
    def supports_parse(self) -> bool:
        """FDDB supports text parsing."""
        return True
    
    def lookup(self, identifier: str) -> Optional[Food]:
        """FDDB does not support API lookup."""
        raise NotImplementedError("FDDB only supports text parsing, not API lookup. Use parse() method.")
    
    def search(self, query: str, limit: int = 10) -> list:
        """FDDB does not support search."""
        raise NotImplementedError("FDDB does not support search")
    
    def parse(self, text: str) -> Optional[Food]:
        """Parse FDDB.info nutrient text format.
        
        Args:
            text: Copied nutrient text from FDDB.info
            
        Returns:
            Food object with parsed nutrition data, or None if parsing failed
            
        Example:
            >>> importer = FDDBImporter()
            >>> text = '''Apfel
            ... Brennwert
            ... 218 kJ
            ... Kalorien
            ... 52 kcal
            ... Protein
            ... 0,3 g'''
            >>> food = importer.parse(text)
        """
        nutrient_dict = {}
        lines = text.split('\n')
        skip = True
        food_name = None
        
        # First line is typically the food name
        if lines and lines[0].strip():
            food_name = lines[0].strip()
        
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
                        .replace('davon', '')
                        .replace('gesättigte', 'saturated')
                        .replace('fettsäuren', 'fatty acids')
                        .strip())
            
            # Parse value from next line
            value_str = next_line.strip().split()[0].replace(',', '.')
            
            try:
                value = float(value_str)
                nutrient_dict[nutriment] = value
            except ValueError:
                continue
            
            skip = True
        
        if not nutrient_dict:
            return None
        
        # Create source
        source = create_source(
            url="https://fddb.info",
            title=f"FDDB.info - {food_name or 'Unknown food'}",
            source_type="database"
        )
        
        return Food(
            name=food_name or "FDDB Food",
            name_de=food_name or "FDDB Food",
            nutrition_data=nutrient_dict,
            nutrition_sources=[source]
        )
