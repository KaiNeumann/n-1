"""
Food Categorization Helper Script

Automatically suggests categories for Food items based on naming patterns.
Can categorize existing files or help categorize new foods.

Usage:
    python categorize_foods.py                    # Analyze and suggest categories
    python categorize_foods.py --apply            # Apply categories to files (backup first!)
    python categorize_foods.py --check            # Check categorization coverage
    python categorize_foods.py --stats            # Show category statistics

The script uses keyword matching to suggest categories:
    - beer: bier, beer, pils, ale, lager
    - bread: bread, toast, baguette, brötchen
    - cheese: cheese, käse, feta, cheddar
    - yogurt: yogurt, joghurt, quark
    - meat: meat, fleisch, chicken, beef
    - sausage: sausage, wurst
    - etc.
"""

import re
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Category keyword mappings
CATEGORY_KEYWORDS = {
    'beer': ['bier', 'beer', 'pils', 'ale', 'lager'],
    'water': ['wasser', 'water', 'mineral', 'aquell', 'rosbach'],
    'milk': ['milch', 'milk'],
    'bread': ['bread', 'toast', 'baguette', 'brötchen', 'sandwich', 'brot', 'biber', 'zopf', 'weggen', 'laugen', 'kranz', 'bürli', 'halbweiss', 'weissbrot', 'vollkornbrot', 'mischbrot', 'dinkelbrot', 'roggenbrot', 'mutschli', 'semmeli', 'pantli', 'brötli'],
    'cheese': ['cheese', 'käse', 'feta', 'cheddar', 'handkäse', 'raclette', 'alp', 'sbrinz', 'gruyère', 'rahm', 'brie', 'camembert', 'blanc_battu', 'appenzeller', 'emmentaler', 'tilsiter', 'gouda', 'edamer', 'mozzarella', 'parmesan', 'pecorino', 'ricotta', 'mascarpone', 'gorgonzola', 'schabziger', 'graubündner', 'vacherin', 'reblochon', 'roquefort', 'tomme', 'st_paulin', 'tête_de_moine', 'ziger', 'mutschli'], 
    'yogurt': ['yogurt', 'joghurt', 'quark', 'jogurt'],
    'soup': ['soup', 'suppe', 'eintopf', 'bouillon', 'brühe', 'consommé', 'fond', 'minestrone', 'terrines'],
    'pasta': ['pasta', 'spaghetti', 'noodle', 'nudel', 'linguine', 'tagliatelle', 'penne', 'fusilli', 'ravioli', 'spätzle', 'capeletti', 'gnocchi'],
    'meat': ['meat', 'fleisch', 'chicken', 'hähnchen', 'beef', 'rind', 'pork', 'schwein', 'schnitzel', 'rouladen', 'braten', 'steak', 'kalb', 'lamm', 'pute', 'ente', 'gans', 'leber', 'nier', 'zunge', 'bresaola', 'carpaccio', 'tartar', 'mett', 'aufschnitt', 'geschnetzeltes', 'ragout', 'gulasch', 'geschnetzeltes', 'voressen', 'mocken', 'eckstück', 'hase', 'hirsch', 'reh', 'wild', 'kaninchen', 'pferd', 'ziege', 'mostbröckli', 'prussien', 'pancetta', 'vitello', 'poulet', 'speck', 'kochspeck', 'rohessspeck'], 
    'sausage': ['sausage', 'wurst', 'schinken', 'knacker', 'pfefferbeisser', 'salami', 'bratwurst', 'cervelat', 'wienerle', 'schüblig', 'bierwurst', 'zungenwurst', 'blutwurst', 'leberwurst', 'weisswurst', 'bockwurst', 'grillwurst', 'mettwurst', 'brühwurst', 'geräuchert', 'coppa', 'cotechino', 'lyoner', 'landjäger', 'luganighe', 'kochwurst', 'kochwürste', 'pökelware', 'salsiz', 'zampone', 'saucisse', 'saucisson', 'mortadella', 'rohwurst', 'dauerwurst', 'wienerli', 'minipic', 'rohwürste'],
    'beverage': ['drink', 'getränk', 'saft', 'juice', 'cola', 'limo', 'schorle', 'limonade', 'kaffee', 'coffee', 'caffe', 'tee', 'tea', 'kakao', 'cocoa', 'alkoholfrei'],
    'snack': ['chip', 'crisp', 'cracker', 'snack', 'chocolate', 'schokolade', 'nuss', 'nut', 'mandel', 'haselnuss', 'walnuss', 'walnüsse', 'pecan', 'macadamia', 'cashew', 'pistazie', 'leckerli', 'twist', 'tuc', 'zwieback', 'kringel', 'locken', 'schokocreme', 'zartbitter', 'meersalz', 'pfeffer', 'antipasti', 'brunsli', 'kastanie', 'edelkastanie', 'maroni', 'gummibonbon', 'karamellen', 'bonbon', 'makronen', 'kokosmakronen', 'sonnenblumenkerne', 'pinienkerne', 'kern', 'kerne', 'samen', 'frites', 'pommes'], 
    'spread': ['spread', 'butter', 'peanut', 'nutella', 'marmelade', 'honig', 'honey', 'pesto', 'ketchup', 'senf', 'margarine', 'aufstrich', 'tabasco', 'sriracha', 'aioli', 'chili', 'fraiche', 'crème', 'creme', 'mayonnaise', 'mayo', 'hummus', 'dip', 'dressing'],
    'supplement': ['vitamin', 'supplement', 'probiotic', 'tablet', 'pill', 'powder', 'mineral', 'hefe', 'yeast', 'agar', 'biotic', 'energy', 'dextro', 'zinc', 'lecithin', 'bion', 'omni', 'fermentierter_teig', 'teig', 'sauerteig', 'sourdough'],
    'egg': ['egg', 'eier', 'eiweiss', 'eigelb', 'hühnerei'],
    'fruit': ['apple', 'apfel', 'banana', 'banane', 'pear', 'birne', 'berry', 'beere', 'orange', 'grape', 'fruit', 'aprikose', 'pfirsich', 'kirsche', 'pflaume', 'zwetschge', 'melone', 'wassermelone', 'kiwi', 'mango', 'ananas', 'erdbeere', 'himbeere', 'blaubeere', 'johannisbeere', 'stachelbeere', 'weintraube', 'traube', 'feige', 'dattel', 'mispel', 'medlar', 'quitte', 'pomelo', 'grapefruit', 'zitrone', 'limette', 'mandarine', 'clementine', 'pampelmuse', 'kaki', 'sharon', 'mirabelle', 'nektarine', 'papaya', 'passionsfrucht', 'maracuja', 'zitrusfrucht', 'früchte', 'kirsch', 'zitronat'],
    'vegetable': ['vegetable', 'gemüse', 'carrot', 'möhre', 'broccoli', 'blumenkohl', 'spinach', 'spinat', 'salad', 'salat', 'tomato', 'tomate', 'potato', 'kartoffel', 'gurke', 'zucchini', 'paprika', 'aubergine', 'kürbis', 'lauch', 'zwiebel', 'knoblauch', 'pilz', 'champignon', 'champignion', 'porree', 'fenchel', 'rettich', 'radieschen', 'rotkohl', 'weisskohl', 'spitzkohl', 'sauerkraut', 'mangold', 'rhabarber', 'alge', 'nori', 'artischocke', 'avocado', 'basilikum', 'bohnenkraut', 'schnittlauch', 'petersilie', 'kresse', 'rucola', 'endivie', 'chicorée', 'chicoree', 'chinakohl', 'pak choi', 'pastinake', 'sellerie', 'schwarzwurzel', 'topinambur', 'kohl', 'salat', 'tomate', 'federkohl', 'cicorino', 'kefe', 'wirz', 'rande', 'rote_beete', 'lattich', 'morchel', 'spargel', 'peperoni', 'karotte', 'maniok', 'zucchetti'],
    'fish': ['fish', 'fisch', 'salmon', 'lachs', 'tuna', 'thunfisch', 'shrimp', 'garnelen', 'dorsch', 'kabeljau', 'makrele', 'sardine', 'hering', 'forelle', 'zander', 'karpfen', 'aal', 'scholle', 'butt', 'seelachs', 'hering', 'egli', 'eierschwamm', 'hecht', 'felche', 'flunder'],
    'cereal': ['cereal', 'müsli', 'oat', 'hafer', 'corn', 'mais', 'dinkel', 'weizen', 'roggen', 'gerste', 'haferflocken', 'griess', 'grütze', 'polenta', 'hirse', 'buchweizen', 'reis', 'quinoa', 'amaranth', 'porridge', 'samen', 'seed', 'chia', 'leinsamen', 'linseed', 'sesam', 'sesame', 'mohn', 'poppy', 'kürbiskern', 'pumpkin', 'korn', 'getreide', 'mehl', 'flour', 'knöpfli', 'teigwaren', 'nudel', 'pasta'],
    'rice': ['rice', 'reis'],
    'oil': ['oil', 'öl', 'olive', 'öl', 'fett', 'schmalz'],
    'sweet': ['cake', 'kuchen', 'cookie', 'keks', 'pastry', 'gebäck', 'torte', 'muffin', 'kuchen', 'torte', 'gâteau', 'strudel', 'croissant', 'berliner', 'biscuit', 'waffel', 'sorbet', 'pudding', 'mousse', 'dessert', 'süss', 'zucker', 'lebkuchen', 'printen', 'spekulatius', 'stollen', 'marzipan', 'nougat', 'praline', 'trüffel', 'tiramisu', 'panna cotta', 'crème brûlée', 'crumble', 'clafoutis', 'tarte', 'quiche', 'galette', 'financier', 'madeleine', 'macaron', 'meringue', 'baiser', 'marshmallow', 'donut', 'muffin', 'cupcake', 'brownie', 'blondie', 'cookie', 'kekse', 'fasnachtschüechli', 'grittibänz', 'mailänderli', 'gugelhopf', 'gipfeli', 'stängel', 'blätterteigstängel', 'panettone', 'lemon_curd', 'schoggibrötli', 'schümliguetzli', 'petit_beurre'],  # Note: 'eis' is handled by COMPOUND_SUFFIXES
    'prepared': ['meal', 'gericht', 'ready', 'fertig', 'pizza', 'lasagne', 'auflauf', 'gratin', 'piccata', 'curry', 'geschnetzeltes', 'ragout', 'gulasch', 'pfanne', 'wok', 'nuggets', 'ratatouille', 'mix', 'burger', 'croque', 'monsieur', 'sandwich', 'wrap', 'burrito', 'taco', 'quesadilla', 'dulce_de_leche', 'samosa', 'frites', 'pommes', 'terrine'],
    'alcohol': ['wine', 'wein', 'spirit', 'spirituose', 'schnaps', 'whisky', 'rum', 'vodka', 'likör', 'aperitif', 'cocktail', 'calvados', 'brandy', 'cognac', 'sherry', 'wermut', 'vermouth'],
    'legume': ['bohne', 'bean', 'linse', 'lentil', 'erbse', 'pea', 'kichererbse', 'chickpea', 'soja', 'soy', 'tofu', 'lupine', 'edamame'],
    'spices': ['salz', 'pfeffer', 'gewürz', 'würze', 'kümmel', 'piment', 'kardamom', 'zimt', 'nelke', 'muskat', 'ingwer', 'kurkuma', 'paprikapulver', 'chillipulver', 'kräuter', 'dill', 'liebstöckel', 'estragon', 'schnittlauch', 'petersilie', 'basilikum', 'oregano', 'thymian', 'rosmarin', 'salbei', 'minze', 'pfefferminze', 'koriander', 'kümmel', 'anis', 'fenchelsamen', 'senfkörner', 'meerrettich', 'kren', 'wasabi'],
    'seafood': ['kalmar', 'tintenfisch', 'krake', 'kraken', 'oktopus', 'sepia', 'meeresfrüchte', 'garnelen', 'shrimps', 'scampi', 'krustentiere', 'hummer', 'languste', 'krebs', 'flusskrebs', 'seespinne', 'tang', 'alge', 'noriblatt', 'kaviar', 'rogen', 'miesmuschel', 'muschel', 'surimi', 'sardellenpaste', 'garnele', 'rollmops'],
}

# Exclusion patterns: these words should NOT trigger certain categories
# These are words that CONTAIN the keyword but are NOT that category
EXCLUSION_PATTERNS = {
    'alcohol': ['schwein'],  # "wein" should not match in "Schwein" (pork)
}

# Brand name to category mappings
# These are specific product brands and their categories
BRAND_CATEGORIES = {
    # Water brands
    'gerolsteiner': 'water',
    'rosbacher': 'water',
    'evian': 'water',
    'vittel': 'water',
    'volvic': 'water',
    'contrex': 'water',
    
    # Beer brands (when not obviously beer from name)
    'flensburger': 'beer',
    'krombacher': 'beer',
    'becks': 'beer',
    'altenmünster': 'beer',
    'schmucker': 'beer',
    
    # Chocolate/Candy brands
    'lindt': 'sweet',
    'lorenz': 'snack',
    'milka': 'sweet',
    'rittersport': 'sweet',
    'toblerone': 'sweet',
    'ferrero': 'sweet',
    
    # Snack brands
    'tuc': 'snack',
    'naturals': 'snack',
    'crunchips': 'snack',
    'funny_frisch': 'snack',
    
    # Spread brands
    'nutella': 'spread',
    
    # Pasta brands
    'barilla': 'pasta',
    'buitoni': 'pasta',
    
    # Cereal brands
    'kelloggs': 'cereal',
    'nestlé': 'cereal',
}

# Compound word suffixes and their implied categories
COMPOUND_SUFFIXES = {
    'saft': 'beverage',      # Apfelsaft → fruit juice
    'kuchen': 'sweet',       # Apfelkuchen → sweet/cake
    'torte': 'sweet',        # Obsttorte → sweet
    'strudel': 'sweet',      # Apfelstrudel → sweet
    'eis': 'sweet',          # Fruchteis → sweet
    'pudding': 'sweet',      # Milchpudding → sweet
    'mousse': 'sweet',       # Mousse au chocolat → sweet
    'gratin': 'prepared',    # Gemüsegratin → prepared
    'auflauf': 'prepared',   # Gemüseauflauf → prepared
    'pfanne': 'prepared',    # Gemüsepfanne → prepared
    'wok': 'prepared',       # Wokgemüse → prepared
    'gericht': 'prepared',   # Fischgericht → prepared
    'salat': 'vegetable',    # Gurkensalat → vegetable
    'suppe': 'soup',         # Gemüsesuppe → soup
    'brot': 'bread',         # Früchtebrot → bread
    'brötchen': 'bread',     # Schokobrötchen → bread
    'schnitte': 'bread',     # Honigschnitte → bread
    'toast': 'bread',        # Käsetoast → bread
    'fladen': 'bread',       # Zwiebelfladen → bread
    'gebäck': 'sweet',       # Mandelgebäck → sweet
    'konfitüre': 'spread',   # Erdbeerkonfitüre → spread
    'marmelade': 'spread',   # Orangenmarmelade → spread
    'gelee': 'spread',       # Johannisbeergelee → spread
    'sirup': 'beverage',     # Zuckersirup → beverage
    'essig': 'spread',       # Balsamicoessig → spread
    'sauce': 'prepared',     # Tomatensauce → prepared
    'soße': 'prepared',      # Jägersoße → prepared
    'dip': 'spread',         # Kräuterdip → spread
    'aufstrich': 'spread',   # Gemüseaufstrich → spread
    'zubereitet': 'prepared',  # Älplermagronen_zubereitet → prepared
    'konserve': 'vegetable',   # Artischocken_Konserve → vegetable (default to veg)
    'gepresst': 'supplement',  # Bäckerhefe_gepresst → supplement
    'getrocknet': 'fruit',     # Alge_Nori_getrocknet → fruit/veg
    '_roh': None,              # Keep as indicator but don't categorize yet
    '_gedämpft': 'vegetable',  # Gemüse_gedämpft → vegetable
    '_frittiert': 'prepared',  # Frühlingsrolle_frittiert → prepared
    '_gekocht': 'prepared',    # Reis_gekocht → prepared
    '_gebraten': 'meat',       # Fleisch_gebraten → meat
    '_geschnetzeltes': 'prepared',  # Geschnetzeltes → prepared
}


def suggest_category(food_name: str) -> Optional[str]:
    """Suggest a category for a food based on its name.
    
    Uses keyword matching, exclusion patterns, compound word decomposition,
    and brand name recognition.
    
    Args:
        food_name: The variable name of the food
        
    Returns:
        Suggested category or None if no match
    """
    food_name_lower = food_name.lower()
    
    # First try: Check brand names (highest confidence)
    for brand, category in BRAND_CATEGORIES.items():
        if brand in food_name_lower:
            return category
    
    # Second try: Check for compound word suffixes (high confidence)
    for suffix, category in COMPOUND_SUFFIXES.items():
        if suffix in food_name_lower:
            # Verify it's at the end or followed by underscore
            suffix_pos = food_name_lower.rfind(suffix)
            if suffix_pos >= 0:
                # Check if it's a true suffix (at end or followed by non-letter)
                after_suffix = food_name_lower[suffix_pos + len(suffix):]
                if not after_suffix or after_suffix.startswith('_') or not after_suffix[0].isalpha():
                    # Only return if we have a category (None means continue searching)
                    if category is not None:
                        return category
                    # If category is None (like _roh), continue to keyword matching
    
    # Third try: Direct keyword matching with exclusion patterns
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in food_name_lower:
                # Check exclusion patterns for this category
                if category in EXCLUSION_PATTERNS:
                    excluded = False
                    for exclusion in EXCLUSION_PATTERNS[category]:
                        # Check if the exclusion pattern appears in the food name
                        if exclusion in food_name_lower:
                            excluded = True
                            break
                    if excluded:
                        continue
                return category
    
    # Fourth try: Check if word ends with a category keyword (for alcohol)
    # This catches "Weisswein", "Rotwein" but not "Schwein" (which starts with schw)
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if food_name_lower.endswith(keyword):
                # Only apply if no exclusion pattern matched
                if category in EXCLUSION_PATTERNS:
                    excluded = False
                    for exclusion in EXCLUSION_PATTERNS[category]:
                        if exclusion in food_name_lower:
                            excluded = True
                            break
                    if excluded:
                        continue
                return category
    
    return None


def parse_food_file(filepath: str) -> List[Tuple[str, str, Optional[str]]]:
    """Parse a Python file and extract Food definitions.
    
    Args:
        filepath: Path to the Python file
        
    Returns:
        List of tuples (food_name, line_content, suggested_category)
    """
    foods = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Pattern to match: variable_name = Food(...)
    pattern = r'^(\w+)\s*=\s*Food\('
    
    for i, line in enumerate(lines):
        match = re.match(pattern, line.strip())
        if match:
            food_name = match.group(1)
            suggested = suggest_category(food_name)
            foods.append((food_name, line.strip(), suggested))
    
    return foods


def analyze_files(filepaths: List[str]) -> Tuple[Dict[str, List[Tuple[str, str]]], List[Tuple[str, str]]]:
    """Analyze multiple files and group foods by suggested category.
    
    Args:
        filepaths: List of Python file paths
        
    Returns:
        Dictionary mapping categories to lists of (food_name, file_path)
    """
    categorized = {}
    uncategorized = []
    
    for filepath in filepaths:
        if not os.path.exists(filepath):
            print(f"Warning: File not found: {filepath}")
            continue
            
        foods = parse_food_file(filepath)
        
        for food_name, line_content, category in foods:
            if category:
                if category not in categorized:
                    categorized[category] = []
                categorized[category].append((food_name, filepath))
            else:
                uncategorized.append((food_name, filepath))
    
    return categorized, uncategorized


def generate_category_code(food_name: str, category: str) -> str:
    """Generate the code to add a category to a food.
    
    Args:
        food_name: Name of the food variable
        category: Category to assign
        
    Returns:
        Python code string
    """
    return f"{food_name}.set_category('{category}')"


def print_suggestions(categorized: Dict, uncategorized: List):
    """Print categorization suggestions in a readable format."""
    print("=" * 70)
    print("FOOD CATEGORIZATION SUGGESTIONS")
    print("=" * 70)
    
    # Print categorized foods
    print("\n[OK] SUGGESTED CATEGORIZATIONS:\n")
    for category in sorted(categorized.keys()):
        foods = categorized[category]
        print(f"\n{category.upper()} ({len(foods)} items):")
        for food_name, filepath in foods:
            filename = os.path.basename(filepath)
            print(f"  - {food_name}")
            print(f"    Add: {generate_category_code(food_name, category)}")
            print(f"    File: {filename}")
    
    # Print uncategorized foods
    if uncategorized:
        print("\n\n? UNCLASSIFIED FOODS (no keyword match):\n")
        for food_name, filepath in uncategorized:
            filename = os.path.basename(filepath)
            print(f"  - {food_name} ({filename})")
        print(f"\nTotal unclassified: {len(uncategorized)}")


def print_statistics(categorized: Dict, uncategorized: List):
    """Print statistics about categorization coverage."""
    total_categorized = sum(len(foods) for foods in categorized.values())
    total_uncategorized = len(uncategorized)
    total = total_categorized + total_uncategorized
    
    print("=" * 70)
    print("CATEGORIZATION STATISTICS")
    print("=" * 70)
    print(f"\nTotal foods analyzed: {total}")
    print(f"Categorized: {total_categorized} ({100*total_categorized/total:.1f}%)")
    print(f"Uncategorized: {total_uncategorized} ({100*total_uncategorized/total:.1f}%)")
    
    print("\n\nBreakdown by category:")
    print("-" * 40)
    for category in sorted(categorized.keys()):
        count = len(categorized[category])
        print(f"  {category:20s}: {count:3d} ({100*count/total:5.1f}%)")


def check_existing_categories(filepath: str) -> List[str]:
    """Check which foods already have categories assigned.
    
    Args:
        filepath: Path to Python file
        
    Returns:
        List of food names that already have categories
    """
    categorized = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to find set_category calls
    pattern = r'(\w+)\.set_category\('
    matches = re.findall(pattern, content)
    
    return matches


def main():
    """Main entry point."""
    # Default files to analyze
    default_files = [
        'food_openfoodfacts_manual.py',
        'food_other_manual.py',
        'food_yazio_manual.py',
        'food_naehrwertdaten_ch.py'
    ]
    
    # Parse command line arguments
    show_stats = '--stats' in sys.argv
    check_mode = '--check' in sys.argv
    
    # Get files to analyze (use defaults or from args)
    files_to_analyze = []
    for arg in sys.argv[1:]:
        if not arg.startswith('--'):
            files_to_analyze.append(arg)
    
    if not files_to_analyze:
        files_to_analyze = default_files
    
    print(f"Analyzing files: {', '.join(files_to_analyze)}\n")
    
    # Analyze files
    categorized, uncategorized = analyze_files(files_to_analyze)
    
    # Check for already categorized foods
    already_categorized = []
    for filepath in files_to_analyze:
        if os.path.exists(filepath):
            already_categorized.extend(check_existing_categories(filepath))
    
    # Remove already categorized from suggestions
    for category in list(categorized.keys()):
        categorized[category] = [
            (name, fp) for name, fp in categorized[category]
            if name not in already_categorized
        ]
        if not categorized[category]:
            del categorized[category]
    
    uncategorized = [
        (name, fp) for name, fp in uncategorized
        if name not in already_categorized
    ]
    
    # Output based on mode
    if show_stats:
        print_statistics(categorized, uncategorized)
        print(f"\n\nAlready categorized: {len(already_categorized)}")
    else:
        print_suggestions(categorized, uncategorized)
    
    print("\n" + "=" * 70)
    print("\nTip: To categorize a food, add this after its definition:")
    print("  food_name.set_category('category_name')")
    print("\nOr when creating the food:")
    print("  food_name = Food({...}, category='category_name')")


if __name__ == '__main__':
    main()
