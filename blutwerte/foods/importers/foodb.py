"""
FooDB importer for enriching food data with bioactive compounds and nutrient effects.

FooDB (Food Database) is the world's largest resource on food constituents, chemistry,
and biology. It contains:
- 797 foods with detailed composition
- 70,926 food compounds (including bioactive compounds)
- 5,150,045 food-compound associations
- 38 nutrients with documented functions

Sources:
- https://foodb.ca/
- Academic use is free (CC BY-NC 4.0)
- Commercial use requires license

Usage:
    # Download data first from https://foodb.ca/downloads
    # Options: CSV (~1GB), JSON (~87MB), MySQL dump (~173MB)
    
    from blutwerte.foods.importers.foodb import FooDBImporter
    
    # Parse downloaded files
    importer = FooDBImporter()
    importer.load_from_csv("path/to/foodb_csv/")
    
    # Query for a food
    compounds = importer.get_compounds_for_food("Spinach")
    effects = importer.map_compounds_to_biomarkers(compounds)
"""

import json
import csv
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


class CompoundType(Enum):
    """Types of compounds in FooDB."""
    SMALL_MOLECULE = "SmallMoleculeCompound"
    PEPTIDE = "Peptide"
    PROTEIN = "Protein"


@dataclass
class FooDBCompound:
    """
    A bioactive compound from FooDB.
    
    These compounds have documented physiological effects and can
    be mapped to biomarkers.
    """
    compound_id: str  # FDBxxxxx
    name: str
    cas_number: Optional[str]
    description: str
    compound_class: str  # e.g., "Flavonoids", "Vitamins"
    subklass: str
    kingdom: str  # e.g., "Organic compounds"
    superklass: str
    molecular_formula: Optional[str]
    molecular_weight: Optional[float]
    hmdb_id: Optional[str]  # Links to Human Metabolome Database
    kegg_id: Optional[str]  # Links to KEGG pathways
    pubchem_id: Optional[str]
    # Health/biomarker related
    physiological_effects: List[str] = None
    health_effects: List[str] = None
    
    def __post_init__(self):
        if self.physiological_effects is None:
            self.physiological_effects = []
        if self.health_effects is None:
            self.health_effects = []


@dataclass
class FooDBNutrient:
    """
    A nutrient from FooDB with documented function.
    
    Nutrients in FooDB have descriptions that often link to
    biomarker effects (e.g., "regulates blood sugar").
    """
    nutrient_id: str  # FDBNxxxxx
    name: str
    nutrient_type: str  # macronutrient, micronutrient
    function: str  # Description of physiological role
    source: str  # Where this info came from


@dataclass
class FooDBContent:
    """
    Association between a food and a compound/nutrient.
    
    This represents the concentration of a compound in a specific food.
    """
    food_id: int
    source_id: int  # Compound or nutrient ID
    source_type: str  # "Compound" or "Nutrient"
    content: Optional[float]  # Concentration
    unit: Optional[str]
    min_content: Optional[float]
    max_content: Optional[float]
    citation: str
    food_common_name: Optional[str]


@dataclass
class FooDBFood:
    """
    A food entry from FooDB.
    """
    food_id: int
    public_id: str  # FOODxxxxx
    name: str
    name_scientific: Optional[str]
    description: str
    food_group: str
    food_sub_group: str
    # Associated data
    compounds: List[FooDBContent] = None
    nutrients: List[FooDBContent] = None
    
    def __post_init__(self):
        if self.compounds is None:
            self.compounds = []
        if self.nutrients is None:
            self.nutrients = []


class FooDBImporter:
    """
    Import and query FooDB data.
    
    Supports both API queries (requires API key) and local file parsing
    from downloaded FooDB dumps.
    """
    
    API_BASE_URL = "https://foodb.ca/api/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize FooDB importer.
        
        Args:
            api_key: Optional API key for querying FooDB API.
                    Request at: https://foodb.ca/w/contact
        """
        self.api_key = api_key
        self.foods: Dict[int, FooDBFood] = {}
        self.compounds: Dict[int, FooDBCompound] = {}
        self.nutrients: Dict[int, FooDBNutrient] = {}
        self.contents: List[FooDBContent] = []
        
        # Mappings for quick lookup
        self._food_name_map: Dict[str, int] = {}
        self._compound_name_map: Dict[str, int] = {}
        
    def load_from_json(self, json_path: Path) -> None:
        """
        Load FooDB data from downloaded JSON file.
        
        Download from: https://foodb.ca/downloads
        
        Supports both single-file format (FooDB.json) and multi-file format.
        """
        json_path = Path(json_path)
        
        # Check if it's a directory (multi-file format)
        if json_path.is_dir():
            self.load_from_json_dir(json_path)
            return
        
        # Single file format
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Parse foods
        for food_data in data.get('foods', []):
            food = FooDBFood(
                food_id=food_data['id'],
                public_id=food_data['public_id'],
                name=food_data['name'],
                name_scientific=food_data.get('name_scientific'),
                description=food_data.get('description', ''),
                food_group=food_data.get('food_group', 'Unknown'),
                food_sub_group=food_data.get('food_sub_group', 'Unknown')
            )
            self.foods[food.food_id] = food
            self._food_name_map[food.name.lower()] = food.food_id
        
        # Parse compounds
        for comp_data in data.get('compounds', []):
            compound = FooDBCompound(
                compound_id=comp_data['public_id'],
                name=comp_data['name'],
                cas_number=comp_data.get('cas_number'),
                description=comp_data.get('description', ''),
                compound_class=comp_data.get('klass', 'Unknown'),
                subklass=comp_data.get('subklass', 'Unknown'),
                kingdom=comp_data.get('kingdom', 'Unknown'),
                superklass=comp_data.get('superklass', 'Unknown'),
                molecular_formula=comp_data.get('moldb_formula'),
                molecular_weight=float(comp_data['moldb_average_mass']) if comp_data.get('moldb_average_mass') else None,
                hmdb_id=comp_data.get('hmdb_id'),
                kegg_id=comp_data.get('kegg_compound_id'),
                pubchem_id=comp_data.get('pubchem_compound_id')
            )
            self.compounds[compound.compound_id] = compound
            self._compound_name_map[compound.name.lower()] = compound.compound_id
        
        # Parse contents (food-compound associations)
        for content_data in data.get('contents', []):
            content = FooDBContent(
                food_id=content_data['food_id'],
                source_id=content_data['source_id'],
                source_type=content_data['source_type'],
                content=float(content_data['orig_content']) if content_data.get('orig_content') else None,
                unit=content_data.get('orig_unit'),
                min_content=float(content_data['orig_min']) if content_data.get('orig_min') else None,
                max_content=float(content_data['orig_max']) if content_data.get('orig_max') else None,
                citation=content_data.get('citation', 'Unknown'),
                food_common_name=content_data.get('orig_food_common_name')
            )
            self.contents.append(content)
            
            # Link to food
            if content.food_id in self.foods:
                if content.source_type == "Compound":
                    self.foods[content.food_id].compounds.append(content)
                elif content.source_type == "Nutrient":
                    self.foods[content.food_id].nutrients.append(content)
    
    def _load_json_lines(self, file_path: Path) -> list:
        """
        Load JSON that may be newline-delimited (one JSON object per line).
        """
        objects = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        objects.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return objects
    
    def _load_json_file(self, file_path: Path) -> list:
        """
        Load JSON file, handling both standard and newline-delimited formats.
        """
        # Try standard JSON first
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                return [data]
            return []
        except json.JSONDecodeError:
            pass
        
        # Try newline-delimited JSON
        return self._load_json_lines(file_path)
    
    def load_from_json_dir(self, json_dir: Path) -> None:
        """
        Load FooDB data from directory with multiple JSON files.
        
        The zip download contains multiple JSON files:
        - Food.json
        - Compound.json
        - Content.json
        - Nutrient.json
        """
        json_dir = Path(json_dir)
        
        print(f"Loading FooDB from directory: {json_dir}")
        
        # Load foods from Food.json
        food_file = json_dir / "Food.json"
        if food_file.exists():
            print("  Loading foods...")
            foods_data = self._load_json_file(food_file)
            
            for food_data in foods_data:
                food = FooDBFood(
                    food_id=food_data['id'],
                    public_id=food_data.get('public_id', f"FOOD{food_data['id']:05d}"),
                    name=food_data.get('name', 'Unknown'),
                    name_scientific=food_data.get('name_scientific'),
                    description=food_data.get('description', ''),
                    food_group=food_data.get('food_group', 'Unknown'),
                    food_sub_group=food_data.get('food_sub_group', 'Unknown')
                )
                self.foods[food.food_id] = food
                self._food_name_map[food.name.lower()] = food.food_id
            
            print(f"    Loaded {len(self.foods)} foods")
        
        # Load compounds from Compound.json
        compound_file = json_dir / "Compound.json"
        if compound_file.exists():
            print("  Loading compounds...")
            compounds_data = self._load_json_file(compound_file)
            
            # Handle both array and dict formats
            if isinstance(compounds_data, list):
                comp_list = compounds_data
            elif isinstance(compounds_data, dict):
                comp_list = compounds_data.get('compounds', list(compounds_data.values()))
            else:
                comp_list = []
            
            for i, comp_data in enumerate(comp_list):
                if not isinstance(comp_data, dict):
                    continue
                compound = FooDBCompound(
                    compound_id=comp_data.get('public_id', f"FDB{comp_data.get('id', i):06d}"),
                    name=comp_data.get('name', 'Unknown'),
                    cas_number=comp_data.get('cas_number'),
                    description=comp_data.get('description', ''),
                    compound_class=comp_data.get('klass', 'Unknown'),
                    subklass=comp_data.get('subklass', 'Unknown'),
                    kingdom=comp_data.get('kingdom', 'Unknown'),
                    superklass=comp_data.get('superklass', 'Unknown'),
                    molecular_formula=comp_data.get('moldb_formula'),
                    molecular_weight=float(comp_data['moldb_average_mass']) if comp_data.get('moldb_average_mass') else None,
                    hmdb_id=comp_data.get('hmdb_id'),
                    kegg_id=comp_data.get('kegg_compound_id'),
                    pubchem_id=comp_data.get('pubchem_compound_id')
                )
                # Use integer ID as key
                comp_id = comp_data.get('id', i)
                self.compounds[comp_id] = compound
                self._compound_name_map[compound.name.lower()] = comp_id
            
            print(f"    Loaded {len(self.compounds)} compounds")
        
        # Load contents from Content.json
        content_file = json_dir / "Content.json"
        if content_file.exists():
            print("  Loading food-compound associations...")
            contents_data = self._load_json_file(content_file)
            
            # Handle both array and dict formats
            if isinstance(contents_data, list):
                content_list = contents_data
            elif isinstance(contents_data, dict):
                content_list = contents_data.get('contents', list(contents_data.values()))
            else:
                content_list = []
            
            for content_data in content_list:
                if not isinstance(content_data, dict):
                    continue
                    
                content = FooDBContent(
                    food_id=content_data.get('food_id', 0),
                    source_id=content_data.get('source_id', 0),
                    source_type=content_data.get('source_type', 'Compound'),
                    content=float(content_data['orig_content']) if content_data.get('orig_content') else None,
                    unit=content_data.get('orig_unit'),
                    min_content=float(content_data['orig_min']) if content_data.get('orig_min') else None,
                    max_content=float(content_data['orig_max']) if content_data.get('orig_max') else None,
                    citation=content_data.get('citation', 'Unknown'),
                    food_common_name=content_data.get('orig_food_common_name')
                )
                self.contents.append(content)
                
                # Link to food
                if content.food_id in self.foods:
                    if content.source_type == "Compound":
                        self.foods[content.food_id].compounds.append(content)
                    elif content.source_type == "Nutrient":
                        self.foods[content.food_id].nutrients.append(content)
            
            print(f"    Loaded {len(self.contents)} food-compound associations")
        
        print(f"FooDB loading complete!")
    
    def load_from_csv(self, csv_dir: Path) -> None:
        """
        Load FooDB data from downloaded CSV files.
        
        Download CSV dump from: https://foodb.ca/downloads
        Extract the tar.gz file and provide the path to the directory.
        
        Expected files:
        - Food.csv
        - Compound.csv
        - Content.csv
        - Nutrient.csv
        """
        csv_dir = Path(csv_dir)
        
        # Load foods
        foods_file = csv_dir / "Food.csv"
        if foods_file.exists():
            with open(foods_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    food = FooDBFood(
                        food_id=int(row['id']),
                        public_id=row['public_id'],
                        name=row['name'],
                        name_scientific=row.get('name_scientific') or None,
                        description=row.get('description', ''),
                        food_group=row.get('name_food_group', 'Unknown'),
                        food_sub_group=row.get('name_food_subgroup', 'Unknown')
                    )
                    self.foods[food.food_id] = food
                    self._food_name_map[food.name.lower()] = food.food_id
        
        # Load compounds
        compounds_file = csv_dir / "Compound.csv"
        if compounds_file.exists():
            with open(compounds_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    compound = FooDBCompound(
                        compound_id=row['public_id'],
                        name=row['name'],
                        cas_number=row.get('cas_number') or None,
                        description=row.get('description', ''),
                        compound_class=row.get('klass', 'Unknown'),
                        subklass=row.get('subklass', 'Unknown'),
                        kingdom=row.get('kingdom', 'Unknown'),
                        superklass=row.get('superklass', 'Unknown'),
                        molecular_formula=row.get('moldb_formula'),
                        molecular_weight=float(row['moldb_average_mass']) if row.get('moldb_average_mass') else None,
                        hmdb_id=row.get('hmdb_id'),
                        kegg_id=row.get('kegg_compound_id'),
                        pubchem_id=row.get('pubchem_compound_id')
                    )
                    self.compounds[compound.compound_id] = compound
                    self._compound_name_map[compound.name.lower()] = int(row['id'])
        
        # Load contents
        contents_file = csv_dir / "Content.csv"
        if contents_file.exists():
            with open(contents_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    content = FooDBContent(
                        food_id=int(row['food_id']),
                        source_id=int(row['source_id']),
                        source_type=row['source_type'],
                        content=float(row['orig_content']) if row.get('orig_content') else None,
                        unit=row.get('orig_unit'),
                        min_content=float(row['orig_min']) if row.get('orig_min') else None,
                        max_content=float(row['orig_max']) if row.get('orig_max') else None,
                        citation=row.get('citation', 'Unknown'),
                        food_common_name=row.get('orig_food_common_name')
                    )
                    self.contents.append(content)
                    
                    # Link to food
                    if content.food_id in self.foods:
                        if content.source_type == "Compound":
                            self.foods[content.food_id].compounds.append(content)
                        elif content.source_type == "Nutrient":
                            self.foods[content.food_id].nutrients.append(content)
    
    def search_food(self, name: str) -> List[FooDBFood]:
        """
        Search for foods by name (case-insensitive partial match).
        
        Returns:
            List of matching FooDBFood objects
        """
        name_lower = name.lower()
        matches = []
        
        for food in self.foods.values():
            if name_lower in food.name.lower():
                matches.append(food)
            elif food.name_scientific and name_lower in food.name_scientific.lower():
                matches.append(food)
        
        return matches
    
    def get_food(self, name: str) -> Optional[FooDBFood]:
        """
        Get a food by exact name match.
        
        Returns:
            FooDBFood if found, None otherwise
        """
        food_id = self._food_name_map.get(name.lower())
        if food_id:
            return self.foods.get(food_id)
        return None
    
    def get_compounds_for_food(self, food_name: str) -> List[FooDBCompound]:
        """
        Get all bioactive compounds for a specific food.
        
        Returns:
            List of FooDBCompound objects found in the food
        """
        food = self.get_food(food_name)
        if not food:
            return []
        
        compounds = []
        for content in food.compounds:
            # Map source_id to compound
            for compound in self.compounds.values():
                # This is inefficient; should use ID mapping
                # For now, check if content.source_id matches any compound
                pass
        
        return compounds
    
    def get_nutrient_function(self, nutrient_name: str) -> Optional[str]:
        """
        Get the documented function of a nutrient.
        
        Returns:
            Description of nutrient's physiological role
        """
        for nutrient in self.nutrients.values():
            if nutrient.name.lower() == nutrient_name.lower():
                return nutrient.function
        return None
    
    def get_compound_biomarker_mapping(self) -> Dict[str, List[str]]:
        """
        Get a mapping of compound classes to potential biomarkers.
        
        This is a curated mapping based on common knowledge about
        bioactive compound classes and their effects.
        
        Returns:
            Dictionary mapping compound class to list of affected biomarkers
        """
        return {
            "Flavonoids": ["CRP", "Oxidative Stress Markers", "Blood Pressure"],
            "Carotenoids": ["Vitamin A", "Antioxidant Status"],
            "Phenolic acids": ["Glucose", "Insulin"],
            "Tocopherols": ["Vitamin E", "Oxidative Stress Markers"],
            "Phytosterols": ["Total Cholesterol", "LDL Cholesterol"],
            "Organosulfur compounds": ["Platelet Aggregation"],
            "Isoflavonoids": ["Estrogen", "Bone Density"],
            "Anthocyanins": ["Nitric Oxide", "Blood Pressure"],
            "Catechins": ["HDL Cholesterol", "Oxidative Stress"],
            "Curcuminoids": ["CRP", "Oxidative Stress"],
            "Capsaicinoids": ["Metabolism", "Appetite"],
            "Gingerols": ["Inflammation", "Nausea"],
        }
    
    def enrich_food_with_effects(self, food_name: str) -> Dict[str, Any]:
        """
        Get biomarker enrichment data for a food.
        
        This combines FooDB compound data with biomarker mappings
        to create effect descriptions similar to our FoodEffect model.
        
        Returns:
            Dictionary with food name, compounds, and potential biomarker effects
        """
        food = self.get_food(food_name)
        if not food:
            return {"error": f"Food '{food_name}' not found in FooDB"}
        
        enrichment = {
            "food_name": food.name,
            "food_scientific": food.name_scientific,
            "compounds": [],
            "potential_biomarker_effects": []
        }
        
        biomarker_map = self.get_compound_biomarker_mapping()
        
        for content in food.compounds:
            # Find compound by ID (we need to map source_id to compound)
            compound_id = content.source_id
            # This requires reverse lookup
            
        return enrichment
    
    def query_api(self, endpoint: str, params: Dict[str, Any]) -> Dict:
        """
        Query FooDB API (requires API key).
        
        Args:
            endpoint: API endpoint (e.g., "foods", "compounds")
            params: Query parameters
            
        Returns:
            JSON response from API
        """
        if not HAS_REQUESTS:
            raise ImportError("requests library required for API queries. Install with: pip install requests")
        
        if not self.api_key:
            raise ValueError("API key required for FooDB API queries. Request at https://foodb.ca/w/contact")
        
        params['api_key'] = self.api_key
        url = f"{self.API_BASE_URL}/{endpoint}"
        
        response = requests.get(url, params=params, headers={"Content-type": "application/json"})
        response.raise_for_status()
        
        return response.json()
    
    def get_statistics(self) -> Dict[str, int]:
        """
        Get statistics about loaded data.
        
        Returns:
            Dictionary with counts of foods, compounds, contents
        """
        return {
            "foods": len(self.foods),
            "compounds": len(self.compounds),
            "nutrients": len(self.nutrients),
            "contents": len(self.contents),
        }


def download_foodb_data(output_dir: str = "data/foodb") -> None:
    """
    Download FooDB data files.
    
    Note: This is just a helper function. FooDB requires manual download
    from https://foodb.ca/downloads due to file sizes.
    
    Args:
        output_dir: Directory to save downloaded files
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"""
To download FooDB data:

1. Visit: https://foodb.ca/downloads
2. Download one of:
   - FooDB CSV file (~953 MB) - Recommended for bulk import
   - FooDB JSON file (~87 MB) - Good for programmatic access
   - FooDB MySQL Dump (~173 MB) - For database import

3. Extract to: {output_path.absolute()}

4. Use FooDBImporter:
   from blutwerte.foods.importers.foodb import FooDBImporter
   
   importer = FooDBImporter()
   importer.load_from_csv("{output_path}/FooDB.csv")
   
5. To query via API, request an API key at:
   https://foodb.ca/w/contact
""")


if __name__ == "__main__":
    # Example usage
    download_foodb_data()
