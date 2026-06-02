"""
FooDB to Biomarker mapping utilities.

This module provides curated mappings between FooDB compounds/nutrients
and blood biomarkers, enabling automatic enrichment of food data.

The mappings are based on:
- Published research on bioactive compounds
- Nutrient-biomarker relationships
- Physiological effects documented in FooDB
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class BiomarkerCategory(Enum):
    """Categories of biomarkers affected by food compounds."""
    INFLAMMATION = "inflammation"
    LIPID_PROFILE = "lipid_profile"
    GLUCOSE_METABOLISM = "glucose_metabolism"
    OXIDATIVE_STRESS = "oxidative_stress"
    CARDIOVASCULAR = "cardiovascular"
    VITAMIN_STATUS = "vitamin_status"
    MINERAL_STATUS = "mineral_status"
    HORMONAL = "hormonal"


@dataclass
class CompoundBiomarkerEffect:
    """
    Maps a FooDB compound to a biomarker effect.
    
    Similar to FoodEffect but derived from FooDB compound data.
    """
    compound_name: str
    compound_class: str
    biomarker_name: str
    effect_direction: str  # "increase", "decrease", "variable"
    mechanism: str
    evidence_level: str  # "strong", "moderate", "emerging"
    magnitude: Optional[str] = None  # e.g., "10-20% reduction"
    

# Curated mapping: Compound classes → Biomarkers
COMPOUND_CLASS_TO_BIOMARKERS = {
    # Flavonoids (polyphenols)
    "Flavonoids": {
        "biomarkers": ["CRP", "IL-6", "TNF-alpha"],
        "direction": "decrease",
        "mechanism": "Anti-inflammatory properties; reduce pro-inflammatory cytokines",
        "evidence": "strong",
        "examples": ["Quercetin", "Kaempferol", "Myricetin"]
    },
    "Anthocyanins": {
        "biomarkers": ["Nitric Oxide", "Blood Pressure", "Oxidative Stress"],
        "direction": "variable",
        "mechanism": "Improve endothelial function and vasodilation; antioxidant effects",
        "evidence": "strong",
        "examples": ["Cyanidin", "Delphinidin", "Malvidin"]
    },
    "Catechins": {
        "biomarkers": ["LDL Cholesterol", "Oxidative Stress", "Blood Pressure"],
        "direction": "decrease",
        "mechanism": "Inhibit LDL oxidation; improve endothelial function",
        "evidence": "strong",
        "examples": ["EGCG", "Epicatechin"]
    },
    
    # Carotenoids
    "Carotenoids": {
        "biomarkers": ["Vitamin A", "Oxidative Stress", "Antioxidant Status"],
        "direction": "increase",
        "mechanism": "Provitamin A activity; antioxidant protection",
        "evidence": "strong",
        "examples": ["Beta-carotene", "Lycopene", "Lutein"]
    },
    
    # Phenolic acids
    "Phenolic acids": {
        "biomarkers": ["Glucose", "Insulin"],
        "direction": "decrease",
        "mechanism": "Improve insulin sensitivity; reduce glucose absorption",
        "evidence": "moderate",
        "examples": ["Chlorogenic acid", "Ferulic acid", "Caffeic acid"]
    },
    
    # Isoflavonoids (phytoestrogens)
    "Isoflavonoids": {
        "biomarkers": ["Estrogen", "Bone Density", "HDL Cholesterol"],
        "direction": "variable",
        "mechanism": "Estrogenic activity; bind to estrogen receptors",
        "evidence": "moderate",
        "examples": ["Genistein", "Daidzein", "Glycitein"]
    },
    
    # Organosulfur compounds
    "Organosulfur compounds": {
        "biomarkers": ["Platelet Aggregation", "Blood Pressure"],
        "direction": "decrease",
        "mechanism": "Anti-thrombotic properties; vasodilation",
        "evidence": "moderate",
        "examples": ["Allicin", "Diallyl disulfide", "S-allyl cysteine"]
    },
    
    # Phytosterols
    "Phytosterols": {
        "biomarkers": ["Total Cholesterol", "LDL Cholesterol"],
        "direction": "decrease",
        "mechanism": "Compete with cholesterol for absorption in intestine",
        "evidence": "strong",
        "magnitude": "8-10% LDL reduction",
        "examples": ["Beta-sitosterol", "Campesterol", "Stigmasterol"]
    },
    
    # Tocopherols (Vitamin E)
    "Tocopherols": {
        "biomarkers": ["Vitamin E", "Oxidative Stress", "LDL Oxidation"],
        "direction": "increase",
        "mechanism": "Antioxidant protection of cell membranes",
        "evidence": "strong",
        "examples": ["Alpha-tocopherol", "Gamma-tocopherol"]
    },
    
    # Curcuminoids
    "Curcuminoids": {
        "biomarkers": ["CRP", "Oxidative Stress", "Blood Glucose"],
        "direction": "decrease",
        "mechanism": "Potent anti-inflammatory and antioxidant effects",
        "evidence": "strong",
        "examples": ["Curcumin", "Demethoxycurcumin"]
    },
    
    # Capsaicinoids
    "Capsaicinoids": {
        "biomarkers": ["Metabolism", "Energy Expenditure"],
        "direction": "increase",
        "mechanism": "Thermogenic effect; increase metabolic rate",
        "evidence": "moderate",
        "examples": ["Capsaicin", "Dihydrocapsaicin"]
    },
    
    # Gingerols
    "Gingerols": {
        "biomarkers": ["Inflammation", "Nausea", "Blood Sugar"],
        "direction": "decrease",
        "mechanism": "Anti-inflammatory; improves insulin sensitivity",
        "evidence": "moderate",
        "examples": ["6-Gingerol", "8-Gingerol", "10-Gingerol"]
    },
    
    # Resveratrol
    "Resveratrol": {
        "biomarkers": ["Oxidative Stress", "Inflammation", "Platelet Aggregation"],
        "direction": "decrease",
        "mechanism": "Antioxidant; anti-inflammatory; cardioprotective",
        "evidence": "moderate",
        "examples": ["Trans-resveratrol"]
    },
    
    # Glucosinolates
    "Glucosinolates": {
        "biomarkers": ["Detoxification Enzymes", "Oxidative Stress"],
        "direction": "increase",
        "mechanism": "Induce Phase II detoxification enzymes",
        "evidence": "moderate",
        "examples": ["Sulforaphane", "Glucoraphanin"]
    },
    
    # Saponins
    "Saponins": {
        "biomarkers": ["Cholesterol", "Immune Function"],
        "direction": "decrease",
        "mechanism": "Bind bile acids; enhance immune response",
        "evidence": "emerging",
        "examples": ["Avenacosides", "Ginsenosides"]
    },
    
    # =========================================================================
    # EXPANDED MAPPINGS - More compound classes
    # =========================================================================
    
    # Fatty Acids and Lipids
    "Fatty Acyls": {
        "biomarkers": ["Triglycerides", "HDL Cholesterol", "LDL Cholesterol"],
        "direction": "variable",
        "mechanism": "Different fatty acids have different effects on lipid profile",
        "evidence": "strong",
        "examples": ["Oleic acid", "Linoleic acid", "Palmitic acid"]
    },
    "Glycerolipids": {
        "biomarkers": ["Triglycerides", "Metabolic Syndrome"],
        "direction": "variable",
        "mechanism": "Energy storage; cell membrane structure",
        "evidence": "strong",
        "examples": ["Triacylglycerols", "Monogalactosyldiacylglycerol"]
    },
    "Sphingolipids": {
        "biomarkers": ["Cell Membrane Health", "Cognitive Function"],
        "direction": "increase",
        "mechanism": "Structural component of cell membranes; nerve myelin",
        "evidence": "moderate",
        "examples": ["Ceramides", "Sphingomyelin"]
    },
    "Steroids and steroid derivatives": {
        "biomarkers": ["Hormone Levels", "Cholesterol"],
        "direction": "variable",
        "mechanism": "Precursors for steroid hormones; plant sterols",
        "evidence": "moderate",
        "examples": ["Cholesterol", "Beta-sitosterol"]
    },
    
    # Vitamins and Co-factors
    "Prenol lipids": {
        "biomarkers": ["Antioxidant Status", "Vitamin A", "Coenzyme Q10"],
        "direction": "increase",
        "mechanism": "Precursors for vitamins and antioxidants",
        "evidence": "strong",
        "examples": ["Retinol", "Ubiquinone", "Vitamin K"]
    },
    
    # Phenolic compounds (expanded)
    "Phenolic acids and derivatives": {
        "biomarkers": ["Glucose", "Insulin", "Oxidative Stress"],
        "direction": "decrease",
        "mechanism": "Antioxidant; improve insulin sensitivity",
        "evidence": "moderate",
        "examples": ["Hydroxybenzoic acids", "Hydroxycinnamic acids"]
    },
    "Stilbenes": {
        "biomarkers": ["Oxidative Stress", "Inflammation", "Blood Pressure"],
        "direction": "decrease",
        "mechanism": "Potent antioxidant and anti-inflammatory effects",
        "evidence": "moderate",
        "examples": ["Resveratrol", "Piceatannol"]
    },
    "Tannins": {
        "biomarkers": ["Protein Binding", "Antioxidant Status"],
        "direction": "variable",
        "mechanism": "Bind proteins and minerals; strong antioxidant",
        "evidence": "moderate",
        "examples": ["Proanthocyanidins", "Ellagitannins"]
    },
    "Lignans": {
        "biomarkers": ["Estrogen", "Hormone Balance", "Antioxidant Status"],
        "direction": "variable",
        "mechanism": "Phytoestrogenic activity; antioxidant",
        "evidence": "moderate",
        "examples": ["Secoisolariciresinol", "Matairesinol"]
    },
    "Coumarins and derivatives": {
        "biomarkers": ["Blood Clotting", "Oxidative Stress"],
        "direction": "decrease",
        "mechanism": "Anti-coagulant properties; antioxidant",
        "evidence": "moderate",
        "examples": ["Umbelliferone", "Esculetin"]
    },
    
    # Alkaloids (some bioactive)
    "Indoles and derivatives": {
        "biomarkers": ["Detoxification", "Estrogen Metabolism"],
        "direction": "increase",
        "mechanism": "Support Phase I/II detoxification; indole-3-carbinol",
        "evidence": "moderate",
        "examples": ["Indole-3-carbinol", "Glucobrassicin"]
    },
    "Isoquinolines and derivatives": {
        "biomarkers": ["Neurotransmitters", "Smooth Muscle"],
        "direction": "variable",
        "mechanism": "Affect dopamine and other neurotransmitters",
        "evidence": "moderate",
        "examples": ["Papaverine", "Berberine"]
    },
    
    # Amino acids and proteins
    "Amino acids and derivatives": {
        "biomarkers": ["Protein Synthesis", "Muscle Building", "Neurotransmitters"],
        "direction": "increase",
        "mechanism": "Building blocks for proteins and neurotransmitters",
        "evidence": "strong",
        "examples": ["Glutamine", "Arginine", "Tryptophan"]
    },
    "Peptides": {
        "biomarkers": ["Blood Pressure", "Immune Function", "Digestion"],
        "direction": "variable",
        "mechanism": "Bioactive peptides from protein digestion",
        "evidence": "moderate",
        "examples": ["Lactopeptides", "ACE-inhibitory peptides"]
    },
    
    # Nucleotides
    "Purine nucleosides": {
        "biomarkers": ["Cell Energy", "DNA/RNA Synthesis"],
        "direction": "increase",
        "mechanism": "Precursors for ATP and nucleic acids",
        "evidence": "strong",
        "examples": ["Adenosine", "Guanosine"]
    },
    "Pyrimidine nucleosides": {
        "biomarkers": ["Cell Energy", "DNA/RNA Synthesis"],
        "direction": "increase",
        "mechanism": "Precursors for nucleic acids",
        "evidence": "strong",
        "examples": ["Cytidine", "Uridine"]
    },
    
    # Carbohydrates
    "Carbohydrates and carbohydrate conjugates": {
        "biomarkers": ["Glucose", "Insulin", "Fiber"],
        "direction": "variable",
        "mechanism": "Energy source; fiber affects glucose absorption",
        "evidence": "strong",
        "examples": ["Glucose", "Fructose", "Dietary Fiber"]
    },
    
    # Organosulfur (expanded)
    "Isothiocyanates": {
        "biomarkers": ["Detoxification Enzymes", "Cancer Risk", "Oxidative Stress"],
        "direction": "increase",
        "mechanism": "Induce Phase II detoxification; anti-cancer properties",
        "evidence": "strong",
        "examples": ["Sulforaphane", "Phenethyl isothiocyanate"]
    },
    "Thiols": {
        "biomarkers": ["Antioxidant Status", "Detoxification"],
        "direction": "increase",
        "mechanism": "Glutathione precursors; antioxidant defense",
        "evidence": "moderate",
        "examples": ["Glutathione", "Cysteine", "N-acetylcysteine"]
    },
    
    # Terpenes
    "Diterpenes": {
        "biomarkers": ["Inflammation", "Blood Pressure"],
        "direction": "decrease",
        "mechanism": "Anti-inflammatory; affects prostaglandin synthesis",
        "evidence": "moderate",
        "examples": ["Carnosic acid", "Carnosol"]
    },
    "Triterpenes": {
        "biomarkers": ["Inflammation", "Cholesterol", "Immune Function"],
        "direction": "decrease",
        "mechanism": "Anti-inflammatory; may affect cholesterol metabolism",
        "evidence": "moderate",
        "examples": ["Oleanolic acid", "Ursolic acid"]
    },
    
    # Other bioactive
    "Betalains": {
        "biomarkers": ["Antioxidant Status", "Oxidative Stress"],
        "direction": "increase",
        "mechanism": "Potent antioxidant pigments",
        "evidence": "moderate",
        "examples": ["Betanin", "Vulgaxanthin"]
    },
    "Carotenoids": {
        "biomarkers": ["Vitamin A", "Lutein", "Lycopene", "Antioxidant Status"],
        "direction": "increase",
        "mechanism": "Provitamin A activity; antioxidant pigments",
        "evidence": "strong",
        "examples": ["Beta-carotene", "Alpha-carotene", "Zeaxanthin"]
    },
    
    # Minerals (inorganic)
    "Inorganic minerals": {
        "biomarkers": ["Electrolyte Balance", "Bone Health", "Nerve Function"],
        "direction": "increase",
        "mechanism": "Essential minerals for bodily functions",
        "evidence": "strong",
        "examples": ["Potassium", "Calcium", "Magnesium", "Iron", "Zinc"]
    },
}


# Specific compound → biomarker mappings (for well-researched compounds)
SPECIFIC_COMPOUND_EFFECTS = {
    # Iron
    "Iron": {
        "biomarkers": ["Iron", "Ferritin", "Hemoglobin", "Transferrin Saturation"],
        "direction": "increase",
        "mechanism": "Essential component of hemoglobin and myoglobin; oxygen transport",
        "evidence": "strong"
    },
    
    # Vitamin B12
    "Cyanocobalamin": {
        "biomarkers": ["Vitamin B12", "Homocysteine", "Methylmalonic Acid"],
        "direction": "increase",
        "mechanism": "Co-factor for methionine synthase; essential for DNA synthesis",
        "evidence": "strong"
    },
    
    # Folate
    "Folic acid": {
        "biomarkers": ["Folic Acid", "Homocysteine"],
        "direction": "increase",
        "mechanism": "Co-factor for one-carbon metabolism; DNA synthesis",
        "evidence": "strong"
    },
    
    # Vitamin D
    "Cholecalciferol": {
        "biomarkers": ["Vitamin D", "PTH", "Calcium", "Phosphorus"],
        "direction": "increase",
        "mechanism": "Regulates calcium absorption and bone metabolism",
        "evidence": "strong"
    },
    
    # Vitamin K
    "Phylloquinone": {
        "biomarkers": ["Vitamin K", "INR", "Coagulation Factors"],
        "direction": "increase",
        "mechanism": "Co-factor for gamma-carboxylation of clotting factors",
        "evidence": "strong"
    },
    
    # Omega-3 fatty acids
    "EPA": {
        "biomarkers": ["Triglycerides", "Inflammation", "Platelet Aggregation"],
        "direction": "decrease",
        "mechanism": "Precursor for anti-inflammatory eicosanoids",
        "evidence": "strong",
        "magnitude": "20-30% triglyceride reduction"
    },
    "DHA": {
        "biomarkers": ["Triglycerides", "HDL Cholesterol"],
        "direction": "decrease",
        "mechanism": "Improves lipid profile; membrane fluidity",
        "evidence": "strong"
    },
    
    # Potassium
    "Potassium": {
        "biomarkers": ["Potassium", "Blood Pressure", "Sodium"],
        "direction": "increase",
        "mechanism": "Counteracts sodium effects; vasodilation",
        "evidence": "strong"
    },
    
    # Magnesium
    "Magnesium": {
        "biomarkers": ["Magnesium", "Blood Pressure", "Glucose"],
        "direction": "increase",
        "mechanism": "Co-factor for >300 enzymes; insulin sensitivity",
        "evidence": "strong"
    },
    
    # Zinc
    "Zinc": {
        "biomarkers": ["Zinc", "Immune Function", "Wound Healing"],
        "direction": "increase",
        "mechanism": "Essential for immune cell function and protein synthesis",
        "evidence": "strong"
    },
    
    # Calcium
    "Calcium": {
        "biomarkers": ["Calcium", "PTH", "Bone Density"],
        "direction": "increase",
        "mechanism": "Bone structure; muscle contraction; signaling",
        "evidence": "strong"
    },
    
    # Fiber (not a compound but important)
    "Dietary fiber": {
        "biomarkers": ["Total Cholesterol", "LDL Cholesterol", "Glucose", "Insulin"],
        "direction": "decrease",
        "mechanism": "Binds bile acids; slows glucose absorption",
        "evidence": "strong",
        "magnitude": "5-10% cholesterol reduction per 7g fiber"
    },
}


class FooDBMapper:
    """
    Maps FooDB compounds and nutrients to biomarker effects.
    
    This class provides methods to:
    1. Look up biomarker effects for compound classes
    2. Map specific compounds to biomarkers
    3. Generate FoodEffect-compatible descriptions
    """
    
    def __init__(self):
        self.class_mappings = COMPOUND_CLASS_TO_BIOMARKERS
        self.compound_mappings = SPECIFIC_COMPOUND_EFFECTS
    
    def get_effects_for_compound_class(self, compound_class: str) -> Optional[Dict]:
        """
        Get biomarker effects for a compound class.
        
        Args:
            compound_class: FooDB compound class (e.g., "Flavonoids")
            
        Returns:
            Dictionary with biomarkers, direction, mechanism, evidence
        """
        return self.class_mappings.get(compound_class)
    
    def get_effects_for_compound(self, compound_name: str) -> Optional[Dict]:
        """
        Get biomarker effects for a specific compound.
        
        Args:
            compound_name: Compound name (e.g., "Quercetin")
            
        Returns:
            Dictionary with biomarkers, direction, mechanism, evidence
        """
        return self.compound_mappings.get(compound_name)
    
    def map_food_compounds_to_effects(
        self, 
        compounds: List[Dict[str, Any]]
    ) -> List[CompoundBiomarkerEffect]:
        """
        Map a list of food compounds to biomarker effects.
        
        Args:
            compounds: List of compound dictionaries with 'name' and 'klass' keys
            
        Returns:
            List of CompoundBiomarkerEffect objects
        """
        effects = []
        
        for compound in compounds:
            compound_name = compound.get('name', '')
            compound_class = compound.get('klass', '')
            
            # Check specific compound first
            specific = self.get_effects_for_compound(compound_name)
            if specific:
                for biomarker in specific['biomarkers']:
                    effects.append(CompoundBiomarkerEffect(
                        compound_name=compound_name,
                        compound_class=compound_class,
                        biomarker_name=biomarker,
                        effect_direction=specific['direction'],
                        mechanism=specific['mechanism'],
                        evidence_level=specific['evidence'],
                        magnitude=specific.get('magnitude')
                    ))
            
            # Then check compound class
            class_effect = self.get_effects_for_compound_class(compound_class)
            if class_effect:
                # Avoid duplicates
                existing_biomarkers = {e.biomarker_name for e in effects}
                for biomarker in class_effect['biomarkers']:
                    if biomarker not in existing_biomarkers:
                        effects.append(CompoundBiomarkerEffect(
                            compound_name=compound_name,
                            compound_class=compound_class,
                            biomarker_name=biomarker,
                            effect_direction=class_effect['direction'],
                            mechanism=class_effect['mechanism'],
                            evidence_level=class_effect['evidence'],
                            magnitude=class_effect.get('magnitude')
                        ))
        
        return effects
    
    def generate_food_effect_description(
        self, 
        effects: List[CompoundBiomarkerEffect]
    ) -> Dict[str, Any]:
        """
        Generate a consolidated biomarker effect description.
        
        Groups effects by biomarker and summarizes them.
        
        Returns:
            Dictionary with biomarker summaries
        """
        biomarker_summary = {}
        
        for effect in effects:
            biomarker = effect.biomarker_name
            
            if biomarker not in biomarker_summary:
                biomarker_summary[biomarker] = {
                    'direction': effect.effect_direction,
                    'mechanisms': [],
                    'compounds': [],
                    'evidence_levels': []
                }
            
            biomarker_summary[biomarker]['mechanisms'].append(effect.mechanism)
            biomarker_summary[biomarker]['compounds'].append(effect.compound_name)
            biomarker_summary[biomarker]['evidence_levels'].append(effect.evidence_level)
        
        # Consolidate mechanisms
        for biomarker, data in biomarker_summary.items():
            unique_mechanisms = list(set(data['mechanisms']))
            data['primary_mechanism'] = unique_mechanisms[0] if unique_mechanisms else ""
            data['compounds'] = list(set(data['compounds']))
            data['strongest_evidence'] = min(
                data['evidence_levels'],
                key=lambda x: {'strong': 0, 'moderate': 1, 'emerging': 2}.get(x, 3)
            )
        
        return biomarker_summary


def get_biomarker_categories() -> Dict[str, List[str]]:
    """
    Get mapping of biomarker categories to specific biomarkers.
    
    Returns:
        Dictionary mapping category to list of biomarkers
    """
    return {
        BiomarkerCategory.INFLAMMATION.value: [
            "CRP", "IL-6", "TNF-alpha", "ESR"
        ],
        BiomarkerCategory.LIPID_PROFILE.value: [
            "Total Cholesterol", "LDL Cholesterol", "HDL Cholesterol", 
            "Triglycerides", "ApoB"
        ],
        BiomarkerCategory.GLUCOSE_METABOLISM.value: [
            "Glucose", "HbA1c", "Insulin", "HOMA-IR"
        ],
        BiomarkerCategory.OXIDATIVE_STRESS.value: [
            "Oxidative Stress", "MDA", "Antioxidant Status", "ORAC"
        ],
        BiomarkerCategory.CARDIOVASCULAR.value: [
            "Blood Pressure", "Nitric Oxide", "Homocysteine", "Platelet Aggregation"
        ],
        BiomarkerCategory.VITAMIN_STATUS.value: [
            "Vitamin A", "Vitamin D", "Vitamin E", "Vitamin K", "Vitamin B12",
            "Folic Acid", "Vitamin B1", "Vitamin B2", "Vitamin B3", "Vitamin B6"
        ],
        BiomarkerCategory.MINERAL_STATUS.value: [
            "Iron", "Ferritin", "Calcium", "Magnesium", "Zinc", 
            "Selenium", "Iodine", "Copper"
        ],
        BiomarkerCategory.HORMONAL.value: [
            "Estrogen", "Testosterone", "Cortisol", "Thyroid Hormones", "PTH"
        ],
    }


# Export main components
__all__ = [
    'COMPOUND_CLASS_TO_BIOMARKERS',
    'SPECIFIC_COMPOUND_EFFECTS',
    'FooDBMapper',
    'CompoundBiomarkerEffect',
    'BiomarkerCategory',
    'get_biomarker_categories',
]
