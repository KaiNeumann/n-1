"""
Add biomarker effects to top 100 legacy foods.

This script analyzes the nutritional content of foods and adds appropriate
biomarker effects based on established nutrient-biomarker relationships.
"""

import re
from pathlib import Path


def create_effect_source(nutrient: str) -> str:
    """Create a generic source for nutrient effects."""
    sources = {
        "iron": 'DataSource(url="https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/", title="Iron Fact Sheet", source_type="guideline")',
        "vitamin_c": 'DataSource(url="https://ods.od.nih.gov/factsheets/VitaminC-HealthProfessional/", title="Vitamin C Fact Sheet", source_type="guideline")',
        "vitamin_b12": 'DataSource(url="https://ods.od.nih.gov/factsheets/VitaminB12-HealthProfessional/", title="Vitamin B12 Fact Sheet", source_type="guideline")',
        "folate": 'DataSource(url="https://ods.od.nih.gov/factsheets/Folate-HealthProfessional/", title="Folate Fact Sheet", source_type="guideline")',
        "vitamin_d": 'DataSource(url="https://ods.od.nih.gov/factsheets/VitaminD-HealthProfessional/", title="Vitamin D Fact Sheet", source_type="guideline")',
        "vitamin_k": 'DataSource(url="https://ods.od.nih.gov/factsheets/VitaminK-HealthProfessional/", title="Vitamin K Fact Sheet", source_type="guideline")',
        "calcium": 'DataSource(url="https://ods.od.nih.gov/factsheets/Calcium-HealthProfessional/", title="Calcium Fact Sheet", source_type="guideline")',
        "magnesium": 'DataSource(url="https://ods.od.nih.gov/factsheets/Magnesium-HealthProfessional/", title="Magnesium Fact Sheet", source_type="guideline")',
        "potassium": 'DataSource(url="https://ods.od.nih.gov/factsheets/Potassium-HealthProfessional/", title="Potassium Fact Sheet", source_type="guideline")',
        "zinc": 'DataSource(url="https://ods.od.nih.gov/factsheets/Zinc-HealthProfessional/", title="Zinc Fact Sheet", source_type="guideline")',
        "fiber": 'DataSource(url="https://ods.od.nih.gov/factsheets/Fiber-HealthProfessional/", title="Dietary Fiber Fact Sheet", source_type="guideline")',
        "cholesterol": 'DataSource(url="https://www.ahajournals.org/doi/10.1161/CIR.0000000000000743", title="Dietary Cholesterol and Cardiovascular Risk", source_type="research")',
    }
    return sources.get(nutrient, sources["iron"])


def generate_effects_code(nutrition_data: dict) -> str:
    """Generate biomarker effects code based on nutrition data."""
    effects = []
    
    # Map nutrients to biomarkers and thresholds
    nutrient_effects = [
        ("iron", "Iron", 3.0, "mg"),
        ("vitamin_c", "Vitamin C", 10.0, "mg"),
        ("vitamin_b12", "Vitamin B12", 0.5, "mcg"),
        ("folate", "Folic Acid", 20.0, "mcg"),
        ("vitamin_d", "Vitamin D", 0.5, "mcg"),
        ("vitamin_k", "Vitamin K", 10.0, "mcg"),
        ("calcium", "Calcium", 50.0, "mg"),
        ("magnesium", "Magnesium", 20.0, "mg"),
        ("potassium", "Potassium", 200.0, "mg"),
        ("zinc", "Zinc", 2.0, "mg"),
        ("vitamin_b1", "Vitamin B1", 0.2, "mg"),
        ("vitamin_b2", "Vitamin B2", 0.2, "mg"),
        ("vitamin_b3", "Vitamin B3", 2.0, "mg"),
        ("vitamin_b6", "Vitamin B6", 0.2, "mg"),
        ("vitamin_e", "Vitamin E", 2.0, "mg"),
        ("vitamin_a", "Vitamin A", 100.0, "mcg"),
    ]
    
    for nutrient_key, biomarker_name, threshold, unit in nutrient_effects:
        # Check multiple possible key formats
        value = None
        for key in [nutrient_key, nutrient_key.replace("_", " "), nutrient_key.replace("vitamin_", "vitamin ")]:
            if key in nutrition_data and nutrition_data[key] is not None:
                try:
                    value = float(nutrition_data[key])
                    break
                except (ValueError, TypeError):
                    continue
        
        if value and value >= threshold:
            percent_rdi = min(100, int(value / threshold * 10))
            effects.append(f'''FoodEffect(
            target_type=EffectTargetType.BIOMARKER,
            target_name="{biomarker_name}",
            direction=EffectDirection.INCREASE,
            mechanism="Contains {value}{unit} of {nutrient_key.replace('_', ' ').title()} per 100g. Contributes to {biomarker_name} status.",
            sources=[{create_effect_source(nutrient_key.split('_')[0]) if '_' in nutrient_key else create_effect_source(nutrient_key)}],
            certainty=EffectCertainty.ESTABLISHED,
        )''')
    
    # Special cases
    if "fiber" in nutrition_data and nutrition_data["fiber"] is not None:
        try:
            fiber_val = float(nutrition_data["fiber"])
            if fiber_val >= 3.0:
                effects.append(f'''FoodEffect(
            target_type=EffectTargetType.BIOMARKER,
            target_name="Total Cholesterol",
            direction=EffectDirection.DECREASE,
            mechanism="Contains {fiber_val}g dietary fiber per 100g. Soluble fiber binds cholesterol in digestive tract.",
            sources=[{create_effect_source("fiber")}],
            certainty=EffectCertainty.ESTABLISHED,
        )''')
                effects.append(f'''FoodEffect(
            target_type=EffectTargetType.BIOMARKER,
            target_name="Glucose",
            direction=EffectDirection.DECREASE,
            mechanism="Fiber slows glucose absorption, helping stabilize blood sugar levels.",
            sources=[{create_effect_source("fiber")}],
            certainty=EffectCertainty.ESTABLISHED,
        )''')
        except (ValueError, TypeError):
            pass
    
    # Vitamin C enhances iron absorption
    has_iron = any(eff for eff in effects if "\"Iron\"" in eff)
    has_vit_c = any(eff for eff in effects if "\"Vitamin C\"" in eff)
    
    if has_iron and has_vit_c:
        effects.append('''FoodEffect(
            target_type=EffectTargetType.BIOMARKER,
            target_name="Iron",
            direction=EffectDirection.INCREASE,
            mechanism="Contains both iron and vitamin C. Vitamin C enhances non-heme iron absorption by 3-4x.",
            sources=[DataSource(url="https://ods.od.nih.gov/factsheets/Iron-HealthProfessional/", title="Iron Fact Sheet", source_type="guideline")],
            certainty=EffectCertainty.ESTABLISHED,
            modifiers=[EffectModifier(
                factor="vitamin_c_present",
                description="High vitamin C content enhances iron bioavailability",
                impact="3-4x increase",
                direction="enhances"
            )],
        )''')
    
    if effects:
        return ".add_effects([\n        " + ",\n        ".join(effects) + "\n    ])"
    return ""


def parse_nutrition_data(content: str) -> dict:
    """Extract nutrition data from food function content."""
    nutrition_data = {}
    
    # Find nutrition_data dict
    match = re.search(r'nutrition_data=\{(.*?)\n\s*\}', content, re.DOTALL)
    if match:
        data_str = match.group(1)
        # Parse key-value pairs
        pairs = re.findall(r'"(\w+)":\s*([\d.]+)', data_str)
        for key, value in pairs:
            nutrition_data[key] = value
    
    return nutrition_data


def process_food_file(file_path: Path, max_foods: int = 100) -> int:
    """Process a food file and add effects to foods."""
    content = file_path.read_text(encoding='utf-8')
    
    # Check if already has effects
    if ".add_effects" in content:
        print(f"  Skipping {file_path.name} - already has effects")
        return 0
    
    # Find all food creation functions
    pattern = r'(def create_\w+\(\) -> Food:.*?return Food\([^)]+\))'
    matches = list(re.finditer(pattern, content, re.DOTALL))
    
    if not matches:
        print(f"  No food functions found in {file_path.name}")
        return 0
    
    modified_count = 0
    modified_content = content
    
    for i, match in enumerate(matches[:max_foods]):
        func_content = match.group(1)
        
        # Parse nutrition data
        nutrition_data = parse_nutrition_data(func_content)
        
        if not nutrition_data:
            continue
        
        # Generate effects
        effects_code = generate_effects_code(nutrition_data)
        
        if effects_code:
            # Find the closing parenthesis of the Food constructor
            # Look for the pattern: sources=[...])  or just )
            old_pattern = r'(sources=\[[^\]]*\]\s*\)|\)\s*$)'
            
            # Replace with effects added
            if "sources=" in func_content:
                new_func = re.sub(
                    r'(sources=\[[^\]]*\]\s*\n\s*)\)',
                    r'\1)' + effects_code,
                    func_content
                )
            else:
                new_func = func_content.rstrip() + effects_code
            
            # Update content
            modified_content = modified_content.replace(func_content, new_func)
            modified_count += 1
    
    if modified_count > 0:
        # Ensure proper imports are present
        if "EffectCertainty" not in modified_content:
            # Add imports
            import_section = """from blutwerte.foods import Food, DataSource
from blutwerte.foods.models import FoodEffect, EffectCertainty, EffectModifier
from blutwerte.medications.models import EffectTargetType, EffectDirection"""
            modified_content = modified_content.replace(
                "from blutwerte.foods import Food, DataSource",
                import_section
            )
        
        file_path.write_text(modified_content, encoding='utf-8')
        print(f"  Modified {modified_count} foods in {file_path.name}")
    
    return modified_count


if __name__ == "__main__":
    legacy_dir = Path("blutwerte/foods/data/legacy")
    
    print("Adding biomarker effects to legacy foods...")
    print()
    
    total_modified = 0
    
    # Process files in priority order
    files_priority = [
        "food_bls_migrated.py",  # Curated German foods (74)
        "food_naehrwertdaten_ch_migrated.py",  # Swiss foods (26 from 1092)
    ]
    
    for filename in files_priority:
        file_path = legacy_dir / filename
        if file_path.exists():
            print(f"Processing {filename}...")
            remaining = 100 - total_modified
            if remaining <= 0:
                break
            count = process_food_file(file_path, remaining)
            total_modified += count
    
    print()
    print(f"Total: Added biomarker effects to {total_modified} foods")
