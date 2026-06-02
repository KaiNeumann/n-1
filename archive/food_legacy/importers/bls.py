"""
BLS (Bundeslebensmittelschlüssel) German Food Database Importer

Imports food data from the German Federal Food Key (BLS) 4.0.
This is the official German national nutrient database with ~7,140 foods.

Source: https://blsdb.de/download
License: CC BY 4.0
Citation: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS),
          Version 4.0 - Deutsche Nährstoffdatenbank. Karlsruhe.
          DOI: 10.25826/Data20251217-134202-0

Usage:
    from importers import get_importer
    
    bls = get_importer("bls")
    
    # Search for foods
    results = bls.search("Apfel")  # Returns list of matching foods
    
    # Get specific food by ID
    food = bls.lookup("BLS_12345")  # Returns Food object
"""

from typing import List, Dict, Any, Optional
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Food import Food
from importers import FoodImporter, register_importer


@register_importer
class BLSImporter(FoodImporter):
    """Importer for German BLS (Bundeslebensmittelschlüssel) database.
    
    The official German national nutrient database with ~7,140 foods.
    Data is loaded from Excel file on-demand.
    """
    
    # Class-level cache for the dataframe
    _df = None
    _column_mapping = None
    
    @property
    def name(self) -> str:
        return "bls"
    
    @property
    def display_name(self) -> str:
        return "Bundeslebensmittelschlüssel (BLS 4.0)"
    
    @property
    def supports_search(self) -> bool:
        return True
    
    def _load_data(self):
        """Load BLS data from Excel file (cached)."""
        if BLSImporter._df is not None:
            return BLSImporter._df
        
        try:
            import pandas as pd
        except ImportError:
            raise ImportError(
                "BLS importer requires pandas. "
                "Install with: pip install pandas openpyxl"
            )
        
        # Find BLS file
        possible_paths = [
            Path('BLS_4_0_Daten_2025_DE.xlsx'),
            Path('BLS_4_0_2025_DE/BLS_4_0_Daten_2025_DE.xlsx'),
            Path('/tmp/BLS_4_0_2025_DE/BLS_4_0_Daten_2025_DE.xlsx'),
        ]
        
        filepath = None
        for path in possible_paths:
            if path.exists():
                filepath = path
                break
        
        if not filepath:
            raise FileNotFoundError(
                "BLS database file not found. "
                "Please download from https://blsdb.de/download "
                "and extract BLS_4_0_Daten_2025_DE.xlsx"
            )
        
        # Load Excel
        BLSImporter._df = pd.read_excel(filepath, sheet_name=0)
        
        # Build column mapping
        BLSImporter._column_mapping = self._get_column_mapping(BLSImporter._df)
        
        return BLSImporter._df
    
    def _get_column_mapping(self, df) -> Dict[str, str]:
        """Map BLS column names to Food class nutrient names."""
        if BLSImporter._column_mapping is not None:
            return BLSImporter._column_mapping
        
        mapping = {}
        
        column_patterns = {
            'ENERCJ Energie (Kilojoule)': 'kilojoules',
            'ENERCC Energie (Kilokalorien)': 'calories',
            'PROT Protein': 'protein',
            'FAT Fett': 'fat',
            'CHOCDF Kohlenhydrate': 'carbohydrate',
            'FIBTG Ballaststoffe': 'fiber',
            'SUGAR Zucker': 'sugar',
            'STARCH Stärke': 'starch',
            'FASAT Fettsäuren gesättigt': 'saturated_fat',
            'FAMS Fettsäuren einfach ungesättigt': 'monounsaturated_fat',
            'FAPU Fettsäuren mehrfach ungesättigt': 'polyunsaturated_fat',
            'CHOLE Cholesterin': 'cholesterol',
            'NA Natrium': 'sodium',
            'K Kalium': 'potassium',
            'CA Calcium': 'calcium',
            'MG Magnesium': 'magnesium',
            'P Phosphor': 'phosphorus',
            'FE Eisen': 'iron',
            'ZN Zink': 'zinc',
            'MN Mangan': 'manganese',
            'CU Kupfer': 'copper',
            'ID Jod': 'iodine',
            'SE Selen': 'selenium',
            'CL Chlorid': 'chloride',
            'VITA Vitamin A': 'vitamin_a',
            'VITD Vitamin D': 'vitamin_d',
            'VITE Vitamin E': 'vitamin_e',
            'VITK Vitamin K': 'vitamin_k',
            'VITB1 Vitamin B1': 'vitamin_b1',
            'VITB2 Vitamin B2': 'vitamin_b2',
            'VITB6 Vitamin B6': 'vitamin_b6',
            'VITB12 Vitamin B12': 'vitamin_b12',
            'VITC Vitamin C': 'vitamin_c',
            'FOL Folsäure': 'vitamin_b9',
            'NIA Niacin': 'vitamin_b3',
            'PANTAC Pantothensäure': 'vitamin_b5',
            'BIOT Biotin': 'vitamin_b7',
            'VIT Carotinoide': 'provitamin_a',
            'WATER Wasser': 'water',
            'ALC Alkohol (Ethanol)': 'alcohol',
            'CAFF Koffein': 'caffeine',
            'NACL Natriumchlorid (Salz)': 'salt',
        }
        
        for col in df.columns:
            col_str = str(col)
            for pattern, nutrient in column_patterns.items():
                if pattern in col_str:
                    mapping[col_str] = nutrient
                    break
        
        BLSImporter._column_mapping = mapping
        return mapping
    
    def _row_to_food(self, row, column_mapping) -> Optional[Food]:
        """Convert a DataFrame row to a Food object."""
        import pandas as pd
        
        nutrients = {}
        
        for bls_col, food_key in column_mapping.items():
            if bls_col in row.index:
                value = row[bls_col]
                if not pd.isna(value):
                    try:
                        float_val = float(value)
                        if abs(float_val) >= 0.001:
                            nutrients[food_key] = round(float_val, 3)
                    except (ValueError, TypeError):
                        pass
        
        if not nutrients:
            return None
        
        return Food(nutrients, 100)
    
    def search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search for foods in BLS database.
        
        Args:
            query: Search term (German food name)
            limit: Maximum number of results
            
        Returns:
            List of dictionaries with keys: id, name, category
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("BLS importer requires pandas. Install with: pip install pandas")
        
        df = self._load_data()
        
        # Find name column
        name_col = None
        for col in df.columns:
            col_str = str(col).lower()
            if 'lebensmittelbezeichnung' in col_str or 'food name' in col_str:
                name_col = col
                break
        
        if not name_col:
            return []
        
        # Search (case-insensitive)
        query_lower = query.lower()
        mask = df[name_col].str.lower().str.contains(query_lower, na=False)
        matches = df[mask].head(limit)
        
        results = []
        for idx, row in matches.iterrows():
            # Try to get BLS code
            code = None
            for col in ['BLS Code', 'BLS_Code', 'Code']:
                if col in df.columns:
                    code = str(row.get(col, ''))
                    if code and code != 'nan':
                        break
            
            if not code:
                code = f"BLS_{idx}"
            
            results.append({
                'id': code,
                'name': str(row[name_col]),
                'category': 'german_bls'
            })
        
        return results
    
    def lookup(self, identifier: str) -> Optional[Food]:
        """Get a specific food by BLS code.
        
        Args:
            identifier: BLS code (e.g., "BLS_12345")
            
        Returns:
            Food object or None if not found
        """
        try:
            import pandas as pd
        except ImportError:
            raise ImportError("BLS importer requires pandas. Install with: pip install pandas")
        
        df = self._load_data()
        column_mapping = self._column_mapping
        
        # Try to find by BLS code
        code_col = None
        for col in ['BLS Code', 'BLS_Code', 'Code']:
            if col in df.columns:
                code_col = col
                break
        
        if code_col:
            # Search for exact code match
            mask = df[code_col].astype(str) == identifier
            matches = df[mask]
            
            if len(matches) > 0:
                return self._row_to_food(matches.iloc[0], column_mapping)
        
        # If not found by code, try as index
        if identifier.startswith('BLS_'):
            try:
                idx = int(identifier.split('_')[1])
                if idx < len(df):
                    return self._row_to_food(df.iloc[idx], column_mapping)
            except (ValueError, IndexError):
                pass
        
        return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the BLS database."""
        try:
            df = self._load_data()
            return {
                'total_foods': len(df),
                'source': 'Bundeslebensmittelschlüssel (BLS) 4.0',
                'license': 'CC BY 4.0',
                'citation': 'Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS), Version 4.0',
            }
        except Exception as e:
            return {
                'error': str(e),
                'message': 'Database file not found or error loading'
            }
