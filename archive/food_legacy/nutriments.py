from typing import Union, List, Dict
from health import default_body_parameters, lifestyles, diets

_nutriments_data : Dict[str,dict] = {}

#TODO define category of macronutirents

def get_all_rdis(options={}) -> Dict[str,dict] :
    return {name: get_rdi(name,options) for name in all_nutriments() if _nutriments_data[name].get("rdi",None)}

def get_rdis_by_category(category : str = None, options={}) -> Dict[str,dict] :
    if not category:
        return get_all_rdis()
    return {name: get_rdi(name,options) for name in names_by_category(category) if _nutriments_data[name].get("rdi",None)}

def get_rdi(name : str, options={}) -> dict :
    if _nutriments_data[ name ].get("rdi",None):
        return _nutriments_data[ name ]["rdi"](options)
    else: 
        return None

#list all nutriments names
def all_nutriments() -> List[str] :
    names = list(_nutriments_data.keys())
    names.sort()
    return names

#list all names within a category
def names_by_category(category : str = None) -> List[str] :
    if not category:
        return all()
    return [name for name, obj in _nutriments_data.items() if category in obj["categories"]]

#get canonical name from list of synonyms
def get_name(term : str) -> str :
    term = term.lower().strip()
    for name, obj in _nutriments_data.items():
        if term == name or term in obj["synonyms"]:
            return name
    return None

def get_summands(name : str) -> List[str] :
    name = get_name(name)
    return [name for name, obj in _nutriments_data.items() if name == obj["sum_to"]]

def get_parent(name: str) -> str :
    name = get_name(name)
    return _nutriments_data[name].get("sum_to",None)

def get_kcal_per_gramm(name: str) -> Union[int,float] :
    name = get_name(name)
    val = _nutriments_data[name].get("kcal_per_gramm",None)
    if val:
        return val
    parent = get_parent(name)
    return get_kcal_per_gramm(parent) if parent else 0

def get_categories() -> List[str] :
    categories = set()
    for name, obj in _nutriments_data.items():
        categories.update(obj["categories"])
    return list(categories)


#helper class for easy and chained entering of attributes
class _RDI:
    def __init__(self,val={}):
        self.minimum : Union[int,float] =   val.get("minimum", None)
        self.reference : Union[int,float] = val.get("reference", None)
        self.maximum : Union[int,float]=    val.get("maximum", None)
        self.unit : str =                   val.get("unit", "g/day")
        self.comments : List[str] =         val.get("comments", [])
        self.sources : List[str] =          val.get("source", ["https://www.dge.de/wissenschaft/referenzwerte/"]) # default source
    def __str__(self):
        return str( {k: v for k, v in vars(self).items() if v and k in ['minimum', 'reference', 'maximum']} )
    #division and multiplication with a number usefule for example for beta-carotene, where rdi is defined in relation to vitamin a
    def __truediv__(self,divisor : Union[int,float]) -> '_RDI':
        return _RDI({
            "minimum": self.minimum/divisor if self.minimum else None,
            "maximum": self.maximum/divisor if self.maximum else None,
            "reference": self.reference/divisor if self.reference else None,
            "unit": self.unit,
            "comments": self.comments,
            "sources": self.sources
        })
    def __mul__(self,value: Union[int,float]) -> '_RDI' :
        return _RDI({
            "minimum": self.minimum*value if self.minimum else None,
            "maximum": self.maximum*value if self.maximum else None,
            "reference": self.reference*value if self.reference else None,
            "unit": self.unit,
            "comments": self.comments,
            "sources": self.sources
        })
    def set_unit(self,s : str) -> '_RDI' :
        self.unit = s
        return self
    def comment(self,s : str) -> '_RDI' :
        self.comments.append(s)
        return self
    def source(self,s : str) -> '_RDI' :
        self.sources.append(s)
        return self
    def ref(self,val : Union[int,float]) -> '_RDI' :
        self.reference = val
        return self
    def min(self,val : Union[int,float]) -> '_RDI' :
        self.minimum = val
        return self
    def max(self,val : Union[int,float]) -> '_RDI' :
        self.maximum = val
        return self

################# Nutriment details ###################

def _rdi_calories(options={}):
    options = default_body_parameters | options
    #FIXME Extremely active lifestyle missing
    val = _RDI({"unit":"kcal/day"})
    if options["sex"] == "male":
        if options["age"] < 19:
            add_by_lifestyle = [0,0,400,800]
            return val.ref(2600 + add_by_lifestyle[lifestyles[options["lifestyle"]]])
        elif options["age"] < 25:
            add_by_lifestyle = [0,0,400,700]
            return val.ref(2400 + add_by_lifestyle[lifestyles[options["lifestyle"]]])
        elif options["age"] < 51:
            add_by_lifestyle = [0,0,300,600]
            return val.ref(2300 + add_by_lifestyle[lifestyles[options["lifestyle"]]])
        elif options["age"] < 65:
            add_by_lifestyle = [0,0,300,600]
            return val.ref(2200 + add_by_lifestyle[lifestyles[options["lifestyle"]]])
        else:
            add_by_lifestyle = [0,0,400,700]
            return val.ref(2100 + add_by_lifestyle[lifestyles[options["lifestyle"]]])
    else:
        add = 0
        if options["is_pregnant"] and options["trimester"] == 2:
            add = 250
        if options["is_pregnant"] and options["trimester"] == 3:
            add = 500
        if options["is_lactating"]:
            add = 500
        if options["age"] < 19:
            add_by_lifestyle = [0,0,300,600]
            return val.ref(2000 + add + add_by_lifestyle[lifestyles[options["lifestyle"]]])
        elif options["age"] < 25:
            add_by_lifestyle = [0,0,300,600]
            return val.ref(1900 + add + add_by_lifestyle[lifestyles[options["lifestyle"]]])
        elif options["age"] < 51:
            add_by_lifestyle = [0,0,300,600]
            return val.ref(1800 + add + add_by_lifestyle[lifestyles[options["lifestyle"]]])
        elif options["age"] < 65:
            add_by_lifestyle = [0,0,300,500]
            return val.ref(1700 + add + add_by_lifestyle[lifestyles[options["lifestyle"]]])
        else:
            add_by_lifestyle = [0,0,200,400]
            return val.ref(1700 + add + add_by_lifestyle[lifestyles[options["lifestyle"]]])
_nutriments_data["calories"] = {
    "synonyms": ['kcal', 'energy-kcal', 'calorific value', 'caloric value', 'kalorien', 'brennwert'],
    "categories": ['main'],
    "to_kJ": lambda kcal: kcal * 0.23885,
    "rdi": _rdi_calories
}
    

def _rdi_alcohol(options={}):
    options = default_body_parameters | options
    val = _RDI().comment("Diese Werte sind nicht als Aufforderung zu täglichem Alkoholgenuss anzusehen - keine regelmäßig konsumierte Alkoholmenge kann als gesundheitlich unbedenklich bezeichnet werden.")
    if options["age"] < 19 or options["is_pregnant"] or options["is_lactating"]:
        return val.max(0)
    elif options["sex"] == "female":
        return val.max(10)
    else:
        return val.max(20)
_nutriments_data["alcohol"] = {
    #Bad
    "is_fluid": True,
    "synonyms": ["alkohol"],
    "categories": ['main'],
    "kcal_per_gramm": 6.93,
    "kcal_per_ml": 5.47,
    "rdi": _rdi_alcohol
}

def _rdi_alpha_carotene(options={}):
    options = default_body_parameters | options
    return _rdi_vitamin_a(options) / 24
_nutriments_data["alpha carotene"] = {
    "synonyms": ["alpha-carotene", "alpha karotin"],
    "categories": ["micronutrients","vitamins&provitamins","provitamins"],
    "sum_to": "provitamin a",
    "rdi": _rdi_alpha_carotene
}

_nutriments_data["alpha-linoleic acid"] = {
    "synonyms": ["α-linolensäure", "α-linoleic acid"],
    "categories": ["fat","essential fat", "unsaturated fat", "polyunsaturated fat", "micronutrients"],
    "sum_to": "omega 3"
}

def _rdi_beta_caroten(options={}):
    options = default_body_parameters | options
    return _rdi_vitamin_a(options) / 12
_nutriments_data["beta carotene"] = {
    "synonyms": ["beta-carotene", "β-carotene", "beta karotin", "betacarotin"],
    "categories": ["micronutrients","vitamins&provitamins","provitamins","antioxidants"],
    "sum_to": "provitamin a",
    "rdi": _rdi_beta_caroten
}

def _rdi_beta_cryptoxanthin(options={}):
    options = default_body_parameters | options
    return _rdi_vitamin_a(options) / 24
_nutriments_data["beta cryptoxanthin"] = {
    "synonyms": ["beta-cryptoxanthin"],
    "categories": ["micronutrients","vitamins&provitamins","provitamins"],
    "sum_to": "provitamin a",
    "rdi": _rdi_beta_cryptoxanthin
}

_nutriments_data["caffeine"] = {
    "synonyms": ["koffein","theine"], # yes, theine is the same molecule as caffeine
    "categories": ["antioxidants","stimulants"] # however only to a very small degree. other compornents in coffee are stronger antioxidants
}

def _rdi_calcium(options={}):
    options = default_body_parameters | options
    val = _RDI()
    if options["is_lactating"] or options["is_pregnant"] or options["age"] < 19:
        return val.ref(1.2)
    else:
        return val.ref(1)
_nutriments_data["calcium"] = {
    "synonyms": ["kalzium"],
    "categories": ["micronutrients","ash","minerals"],
    "rdi": _rdi_calcium
}

def _rdi_carbohydrate(options={}):
    #usually net carbs excluding fiber
    options = default_body_parameters | options
    val = _RDI()
    kcal = _rdi_calories(options).reference
    # 45 - 65%
    val.min( 45/100 * kcal / get_kcal_per_gramm("carbohydrate") )
    val.max( 65/100 * kcal / get_kcal_per_gramm("carbohydrate") )
    return val
_nutriments_data["carbohydrate"] = {
    "synonyms": ["total carbohydrates", "carbohydrates", "carbs", 'kohlenhydrate'],
    "categories": ["main","macronutrient"],
    "kcal_per_gramm": 4,
    "to_BE": lambda carbs: carbs / 12, # "broteinheiten" 1BE = 12g carbohydrates! 
    "rdi": _rdi_carbohydrate
}

_nutriments_data["carbonic acid"] = {
    "synonyms": ["kohlensäure", "hydrogencarbonat"], # hydrocarbonate is not the same but sometimes used instead
    "categories": [] 
}

def _rdi_chloride(options={}):
    options = default_body_parameters | options
    return _RDI().ref(2.3)
_nutriments_data["chloride"] = {
    "synonyms": ["chlorid"],
    "categories": ["micronutrients","minerals"],
    "rdi": _rdi_chloride
}

_nutriments_data["cholesterol"] = {
    #Limit it, as food with cholesterol also contains a lot of saturated fats
    "synonyms": ["cholesterin"],
    "categories": ["fat"],
}

def _rdi_choline(options={}):
    options = default_body_parameters | options
    val = _RDI()
    val.sources = ["Source: https://s3.amazonaws.com/public-inspection.federalregister.gov/2016-11867.pdf (pages 903-904)"]
    return val.ref(550/1000)
_nutriments_data["choline"] = {
    "synonyms": [],
    "categories": [],
    "rdi": _rdi_choline
}

def _rdi_chromium(options={}):
    options = default_body_parameters | options
    return _RDI().min(30/1000000).max(100/1000000)
_nutriments_data["chromium"] = {
    "synonyms": ["chrom"],
    "categories": ["micronutrients","minerals","trace elements"],
    "rdi": _rdi_chromium
}

def _rdi_copper(options={}):
    options = default_body_parameters | options
    return _RDI().min(1/1000).max(1.5/1000)
_nutriments_data["copper"] = {
    "synonyms": ["kupfer"],
    "categories": ["micronutrients","minerals","trace elements","antioxidants"],
    "rdi": _rdi_copper
}

_nutriments_data["essential fat"] = {
    #Good
    "synonyms": ["essential fats", "essential fatty acids", "essentielle fettsäuren"],
    "categories": ["fat","unsaturated fat"]
}

def _rdi_fat(options={}):
    options = default_body_parameters | options
    val = _RDI()
    kcal = _rdi_calories(options).reference
    # 20 - 35%
    val.min( 20/100 * kcal / get_kcal_per_gramm("fat") )
    val.max( 35/100 * kcal / get_kcal_per_gramm("fat") )
    return val
_nutriments_data["fat"] = {
    "synonyms": ['total fat', 'fats', 'fatty acids', 'lipids', 'total lipid', 'fett', 'fette', 'fettsäuren'],
    "categories": ["main","macronutrient"],
    "kcal_per_gramm": 9,
    "rdi": _rdi_fat
}

def _rdi_fiber(options={}):
    options = default_body_parameters | options
    val = _RDI().comment("Der Richtwert für die Ballaststoffzufuhr gilt für Frauen und Männer gleichermaßen; die Ableitung eines geschlechtsspezifischen Richtwerts ist derzeit nicht möglich. Frauen und Männer sollten dieselbe Ballaststoffzufuhr pro 1000 kcal (Ballaststoffdichte) anstreben. Bei einer mittleren Energiezufuhr von 2050 kcal/Tag – dem Mittel aus Zufuhrwerten für Energie für 25–50-jährige Männer (2300 kcal/Tag) und Frauen (1800 kcal/Tag) mit einem PAL-Wert von 1,4 – entspricht dies einer anzustrebenden Ballaststoffdichte von etwa 14,6 g/1000 kcal bzw. 3,5 g/MJ.")
    kcal = _rdi_calories(options).reference
    return val.ref( 14.6 * kcal/1000 )
_nutriments_data["fiber"] = {
    "synonyms": ["dietary fiber", 'fibre', 'ballaststoffe'],
    "categories": ['main'], #TODO dietary fibers are technically carbohydrates, but it seems its calory value is not summarized to carbs for the sources I used
    "kcal_per_gramm": 2.2,
    "rdi": _rdi_fiber
}

def _rdi_flouride(options={}):
    options = default_body_parameters | options
    val = _RDI()
    val.comment("Sicherheitshinweis: Ab einem Trinkwasserfluoridgehalt von 0,7 mg/l sind weder Fluoridtabletten noch -speisesalz zulässig.")
    val.comment("Fluoridzufuhr aus fester Nahrung, Trinkwasser, Getränken und Nahrungsergänzungen. Bei einer längeren Überschreitung der tolerierbaren Gesamtzufuhrmenge (etwa 0,1 mg/kg/Tag), besonders im Alter von 1 bis 8 Jahren, ist mit einem zunehmenden Vorkommen von Zahnschmelzflecken (Zahnfluorose) zu rechnen.")
    if options["sex"] == "male":
        if options["age"] < 19:
            return val.ref(3.2/1000)
        else:
            return val.ref(3.8/1000)
    else:
        if options["is_lactating"] or options["is_pregnant"]:
            return val.ref(3.1/1000)
        elif options["age"] < 19:
            return val.ref(2.9/1000)
        else:
            return val.ref(3.1/1000)
_nutriments_data["flouride"] = {
    "synonyms": ["flourid","flour"],
    "categories": ["micronutrients","minerals"],
    "rdi": _rdi_flouride
}

_nutriments_data["fructose"] = {
    "synonyms": ["fruktose"],
    "categories": ["carbohydrate","sugar","monosaccharides"],
    "sum_to": "sugar",
    "kcal_per_gramm": 3.75
}

_nutriments_data["galactose"] = {
    "synonyms": [],
    "categories": ["carbohydrate","sugar","monosaccharides"],
    "sum_to": "sugar",
    "kcal_per_gramm": 3.75
}

_nutriments_data["glucose"] = {
    "synonyms": ["glukose","dextrose"],
    "categories": ["carbohydrate","sugar","monosaccharides"],
    "sum_to": "sugar",
    "kcal_per_gramm": 3.75
}

_nutriments_data["glutamate"] = {
    "synonyms": ["glutamic acid", "glutamat", "glutaminsäure", "natriumglutamat", "monosodium glutamate"],
    "categories": ["protein"],
    "sum_to": "protein"
}

def _rdi_iodine(options={}):
    options = default_body_parameters | options
    val = _RDI()
    val.comment("Zusätzlich zu einer ausgewogenen Ernährung sollen Schwangere täglich ein Supplement mit 100 (bis 150) µg Jod einnehmen. Bei Schilddrüsenerkrankungen soll vor der Supplementierung eine Rücksprache mit dem behandelnden Arzt erfolgen. Quelle: https://www.gesund-ins-leben.de/fuer-fachkreise/familien-vor-und-in-der-schwangerschaft/handlungsempfehlungen/supplemente/supplement-jod/")
    val.comment("Während der Stillzeit sollten zusätzlich zur Verwendung von Jodsalz (mit Jod angereichertem Kochsalz) Jodtabletten (100 μg Jod/Tag) eingenommen werden. Quelle: https://www.gesund-ins-leben.de/fuer-fachkreise/bestens-unterstuetzt-durchs-1-lebensjahr/handlungsempfehlungen/empfehlungen-fuer-die-mutter/naehrstoffsupplemente-in-der-stillzeit/")
    if options["is_lactating"]:
        return val.ref(260/1000000)
    elif options["is_pregnant"]:
        return val.ref(230/1000000)
    elif options["age"] > 50:
        return val.ref(180/1000000)
    else:
        return val.ref(200/1000000)
_nutriments_data["iodine"] = {
    "synonyms": ["jod"],
    "categories": ["micronutrients","minerals","trace elements"],
    "rdi": _rdi_iodine
}

def _rdi_iron(options={}):
    options = default_body_parameters | options
    val = _RDI()
    if options["sex"] == "male":
        if options["age"] < 19:
            return val.ref(12/1000)
        else:
            return val.ref(10/1000)
    elif options["is_pregnant"]:
        return val.ref(30/1000)
    elif options["is_lactating"]:
        return val.ref(20/1000)
    elif options["age"] < 51:
        return val.ref(15/1000)
    else:
        return val.ref(10/1000)
_nutriments_data["iron"] = {
    "synonyms": ["eisen"],
    "categories": ["micronutrients","minerals"],
    "rdi": _rdi_iron
}

_nutriments_data["lactose"] = {
    "synonyms": ["galactose", "laktose"],
    "categories": ["carbohydrate","sugar","disaccharides"],
    "sum_to": "sugar",
    "kcal_per_gramm": 4
}

_nutriments_data["lecithin"] = {
    "synonyms": [],
    "categories": ["fat"],
}

_nutriments_data["linoleic acid"] = {
    "synonyms": ["linolsäure"],
    "categories": ["fat","essential fat", "unsaturated fat","micronutrients"],
    "sum_to": "omega 6"
}

def _rdi_magnesium(options={}):
    options = default_body_parameters | options
    val = _RDI()
    #https://pubmed.ncbi.nlm.nih.gov/22051430/ Magnesium intake of 500 mg/d to 1000 mg/d may reduce blood pressure (BP) as much as 5.6/2.8 mm Hg
    #https://www.health.harvard.edu/heart-health/magnesium-and-blood-pressure-whats-the-evidence claims pills are not needed. Rather eat nuts, black beans and spinach, and reduce salt.
    if options["sex"] == "female":
        if options["age"] < 19:
            return val.ref(260/1000)
        else:
            return val.ref(300/1000)
    else:
        if options["age"] < 19:
            return val.ref(330/1000)
        else:
            return val.ref(350/1000)
_nutriments_data["magnesium"] = {
    "synonyms": [],
    "categories": ["micronutrients","ash","minerals"],
    "rdi": _rdi_magnesium
}            

_nutriments_data["maltose"] = {
    "synonyms": ["malzzucker"],
    "categories": ["carbohydrate","sugar","disaccharides"],
    "sum_to": "sugar",
    "kcal_per_gramm": 3.87
}

def _rdi_manganese(options={}):
    options = default_body_parameters | options
    return _RDI().min(2/1000).max(5/1000)
_nutriments_data["manganese"] = {
    "synonyms": ["mangan"],
    "categories": ["micronutrients","minerals","trace elements"],
    "rdi": _rdi_manganese
}

_nutriments_data["mannitol"] = {
    "synonyms": [],
    "categories": ["carbohydrate","sugar","sugar alcohols","sweeteners"],
    "kcal_per_gramm": 1.6
}

def _rdi_molybdenum(options={}):
    options = default_body_parameters | options
    return _RDI().min(50/1000000).max(100/1000000)
_nutriments_data["molybdenum"] = {
    "synonyms": ["molybdän"],
    "categories": ["micronutrients","minerals","trace elements"],
    "rdi": _rdi_molybdenum
}

_nutriments_data["monounsaturated fat"] = {
    #Good except for trans fats
    "synonyms": ["unsaturated fatty acids", "monounsaturates", "einfach ungesättigte fettsäuren"],
    "categories": ["fat","unsaturated fat"],
    "sum_to": "unsaturated fat"
}

_nutriments_data["nicotine"] = {
    "synonyms": ["nikotin"],
    "categories": ["stimulants"]
}

def _rdi_omega_3(options={}):
    options = default_body_parameters | options
    val = _RDI()
    kcal = _rdi_calories(options).reference
    val.ref( 2.5/100 * kcal / get_kcal_per_gramm("fat") )
    return val
_nutriments_data["omega 3"] = {
    "synonyms": ["omega-3", "omega-3 fatty acids", "omega 3 fettsäuren", "omega-3 fettsäuren"],
    "categories": ["fat","essential fat", "unsaturated fat", "polyunsaturated fat","micronutrients"],
    "sum_to": "essential fat",
    "rdi": _rdi_omega_3
}

def _rdi_omega_6(options={}):
    options = default_body_parameters | options
    val = _RDI()
    kcal = _rdi_calories(options).reference
    val.ref( 0.5/100 * kcal / get_kcal_per_gramm("fat") )
    return val
_nutriments_data["omega 6"] = {
    "synonyms": ["omega-6", "omega-6 fatty acids", "omega 6 fettsäuren", "omega-6 fettsäuren"],
    "categories": ["fat","essential fat", "unsaturated fat","micronutrients"],
    "sum_to": "essential fat",
    "rdi": _rdi_omega_6
}

def _rdi_phosphorus(options={}):
    options = default_body_parameters | options
    val = _RDI().comment("Schwangere und Stillende < 19 Jahre 1250 mg")
    if options["age"] < 19:   
        return val.ref(1250/1000)
    elif options["is_lactating"]:
        return val.ref(900/1000)
    elif options["is_pregnant"]:
        return val.ref(800/1000)
    else: 
        return val.ref(700/1000)
_nutriments_data["phosphorus"] = {
    "synonyms": ["phosphor"],
    "categories": ["micronutrients","minerals"],
    "rdi": _rdi_phosphorus
}

_nutriments_data["polyunsaturated fat"] = {
    #Good except for trans fats
    "synonyms": ["polyunsaturates", "polyunsaturated fatty acids", "mehrfach ungesättigte fettsäuren"],
    "categories": ["fat","unsaturated fat"],
    "sum_to": "unsaturated fat"
}

def _rdi_potassium(options={}):
    options = default_body_parameters | options
    #TODO higher recommendation for high blood pressure
    val = _RDI()
    if options["is_lactating"]:
        return val.ref(4.4)
    else:
        return val.ref(4)
_nutriments_data["potassium"] = {
    "synonyms": ["potash", "kalium"],
    "categories": ["micronutrients","ash","minerals"],
    "rdi": _rdi_potassium
}

def _rdi_protein(options={}):
    options = default_body_parameters | options
    val = _RDI().comment("KG = Körpergewicht; Die Angaben beziehen sich auf Normalgewicht; bei Übergewicht (BMI > 25 kg/m2 bei Erwachsenen) sollte das Normalgewicht für die Berechnung zugrunde gelegt werden.")
    if options["is_lactating"]:
        return val.ref(1.2 * options["weight"])
    elif options["is_pregnant"]: 
        return val.ref( (0.7 + options["trimester"]/10) * options["weight"])
    elif options["sex"] == "female":
        return val.ref(0.8 * options["weight"])
    else:
        if options["age"] < 19:
            return val.ref(0.9 * options["weight"])
        elif options["age"] < 65:
            return val.ref(0.8 * options["weight"])
        else:
            return val.ref(1.0 * options["weight"])
_nutriments_data["protein"] = {
    "synonyms": ["proteins", "proteine", "eiweiß", "eiweiss"],
    "categories": ["main","macronutrient"],
    "kcal_per_gramm": 4,
    "rdi": _rdi_protein
}

_nutriments_data["provitamin a"] = {
    "synonyms": [],
    "categories": ["vitamins&provitamins","provitamins"]
}

_nutriments_data["provitamin b5"] = {
    "synonyms": ["panthenol"],
    "categories": ["vitamins&provitamins","provitamins"]
}

_nutriments_data["provitamin d2"] = {
    "synonyms": ["ergosterol"],
    "categories": ["vitamins&provitamins","provitamins"]
}

_nutriments_data["provitamin d3"] = {
    "synonyms": ["7-dehydrocholesterol"],
    "categories": ["vitamins&provitamins","provitamins"]
}

_nutriments_data["provitamin k"] = {
    "synonyms": ["menadione"],
    "categories": ["vitamins&provitamins","provitamine"]
}

_nutriments_data["purine"] = {
    "synonyms": ["purines"],
    "categories": [] #TODO find category
}

_nutriments_data["resveratol"] = {
    "synonyms": [],
    "categories": ["antioxidants"] # anitoxidant found in red wine
}

def _rdi_salt(options={}):
    options = default_body_parameters | options
    val = _RDI().comment("One gram of salt contains approximately 0.4 grams of sodium")
    rdi_sodium = _rdi_sodium(options).reference
    return val.ref( rdi_sodium / 0.4 )
_nutriments_data["salt"] = {
    "synonyms": ["salz"],
    "categories": ["main"],
    "rdi": _rdi_salt
}

def _rdi_saturated_fat(options={}):
    options = default_body_parameters | options
    val = _RDI().comment("<10% der Energie")
    kcal = _rdi_calories(options).reference
    return val.max( 10/100 * kcal / get_kcal_per_gramm("saturated fat") )
_nutriments_data["saturated fat"] = {
    #BAD because of cholesterol, but not realistic to completely avoid
    "synonyms": ["saturated fatty acids", "saturated fats", "saturated-fat", "gesättigte fettsäuren", "fettsäuren gesättigt"],
    "categories": ["fat"],
    "sum_to": "fat",
    "rdi": _rdi_saturated_fat
}

def _rdi_selenium(options={}):
    options = default_body_parameters | options
    val = _RDI()
    if options["is_lactating"]:
        return val.ref(75/1000000)
    elif options["sex"] == "female":
        return val.ref(60/1000000)
    else:
        return val.ref(70/1000000)
_nutriments_data["selenium"] = {
    "synonyms": ["selen"],
    "categories": ["micronutrients","minerals","trace elements","antioxidants"],
    "rdi": _rdi_selenium
}

def _rdi_sodium(options={}):
    options = default_body_parameters | options
    val = _RDI().source("ChatGPT 2023-05-12")
    if options["hypertension"]:
        return val.ref(1.5) #  the American Heart Association recommends an even lower daily limit of 1,500 mg of sodium for most adults, especially those with high blood pressure
    else:
        return val.ref(2.3) # the 2015-2020 Dietary Guidelines for Americans recommend that adults consume less than 2,300 milligrams (mg) of sodium per day
_nutriments_data["sodium"] = {
    "synonyms": ["natrium"],
    "categories": ["micronutrients","ash","minerals"],
    "rdi": _rdi_sodium
}

_nutriments_data["sorbitol"] = {
    "synonyms": [],
    "categories": ["carbohydrate","sugar","sugar alcohols","sweeteners"],
    "kcal_per_gramm": 2.6
}

_nutriments_data["starch"] = {
    "synonyms": ["stärke", "polysaccharides"],
    "categories": ["carbohydrate"],
    "sum_to": "carbohydrate",
    "kcal_per_gramm": 4
}

_nutriments_data["sucrose"] = {
    "synonyms": ["saccharose","table sugar"],
    "categories": ["carbohydrate","sugar","disaccharides"],
    "sum_to": "sugar",
    "kcal_per_gramm": 3.87
}

_nutriments_data["sugar"] = {
    "synonyms": ["sugars", "zucker"],
    "categories": ["carbohydrate"],
    "sum_to": "carbohydrate",
    "kcal_per_gramm": 4.2
}

_nutriments_data["sulfate"] = {
    "synonyms": ["sulfat","schwefel"],
    "categories": ["micronutrients","minerals"]
}

_nutriments_data["taurine"] = {
    "synonyms": ["taurin"],
    "categories": ["antioxidants","stimulants"] # however only to a very small degree antioxidant
}

_nutriments_data["theobromine"] = {
    "synonyms": [],
    "categories": ["stimulants"] #  natural stimulant found in chocolate that affects the central nervous system and has similar effects to caffeine.
}

_nutriments_data["trans fat"] = {
    #VERY BAD, wikipedia quote: "resulting in hundreds of thousands of deaths each year"
    "synonyms": ["trans fats", "trans fatty acids","trans fette"],
    "categories": ["fat","unsaturated fat"],
    #don't sum, as the more common categorisation is mon and polyunsaturated
}

_nutriments_data["unsaturated fat"] = {
    #Good except for trans fats
    "synonyms": ["unsaturated fatty acids", "unsaturated-fat", "ungesättigte fettsäuren", "fettsäuren ungesättigt"],
    "categories": ["fat"],
    "sum_to": "fat"
}

_nutriments_data["uric acid"] = {
    "synonyms": ["harnsäure"],
    "categories": [] 
}

def _rdi_vitamin_a(options={}):
    options = default_body_parameters | options
    val = _RDI()
    val.comment("Berechnungsgrundlage: 1 μg Retinolaktivitätsäquivalent (retinol activity equivalent, RAE) = 1 μg Retinol = 12 μg β-Carotin = 24 μg andere Provitamin-A-Carotinoide.")
    if options["is_lactating"]:
        return val.ref(1300/1000000)
    elif options["is_pregnant"]:
        return val.ref(800/1000000)
    elif options["sex"] == "female":
        if options["age"] < 19:
            return val.ref(800/1000000)
        else:
            return val.ref(700/1000000)
    else:
        if options["age"] < 19:
            return val.ref(950/1000000)
        elif options["age"] < 65:
            return val.ref(850/1000000)
        else:
            return val.ref(800/1000000)
_nutriments_data["vitamin a"] = {
    "synonyms": ["retinol"],
    "categories": ["vitamins","vitamins&provitamins"],
    "rdi": _rdi_vitamin_a
}

def _rdi_vitamin_b1(options={}):
    options = default_body_parameters | options
    val = _RDI().comment("Defined for thiamin")
    val.comment("Zugrunde gelegt wurden die alters- und geschlechtsspezifischen Richtwerte für die Energiezufuhr (PAL-Wert 1,4).")
    val.comment("Unter Berücksichtigung des Richtwerts für Frauen von 19 bis unter 25 Jahren (PAL-Wert 1,4) und Zulage von 250 kcal/Tag während des 2. Trimesters und von 500 kcal/Tag während des 3. Trimesters der Schwangerschaft.")
    val.comment("Unter Berücksichtigung des Richtwerts für Frauen von 19 bis unter 25 Jahren (PAL-Wert 1,4) und Zulage von 500 kcal/Tag für ausschließliches Stillen während der ersten 4 bis 6 Monate.")
    if options["is_lactating"]:
        return val.ref(1.3/1000)
    elif options["is_pregnant"]:
        trimester_data = [None, 1.0, 1.2, 1.3]
        return val.ref( trimester_data[options["trimester"]]/1000 )
    elif options["sex"] == "female":
        if options["age"] < 19:
            return val.ref(1.1/1000)
        else:
            return val.ref(1/1000)
    else:
        if options["age"] < 19:
            return val.ref(1.4/1000)
        elif options["age"] < 25:
            return val.ref(1.3/1000)
        elif options["age"] < 65:
            return val.ref(1.2/1000)
        else:
            return val.ref(1.1/1000)
_nutriments_data["vitamin b1"] = {
    "synonyms": ["thiamin"],
    "categories": ["vitamins","vitamins&provitamins","vitamin b complex"],
    "rdi": _rdi_vitamin_b1
}

def _rdi_vitamin_b2(options={}):
    options = default_body_parameters | options
    val = _RDI().comment("Defined for riboflavin")
    val.comment("Zugrunde gelegt wurden die alters- und geschlechtsspezifischen Richtwerte für die Energiezufuhr (PAL-Wert 1,4).")
    val.comment("Unter Berücksichtigung des Richtwerts für Frauen von 19 bis unter 25 Jahren (PAL-Wert 1,4) und Zulage von 250 kcal/Tag während des 2. Trimesters und von 500 kcal/Tag während des 3. Trimesters der Schwangerschaft.")
    val.comment("Unter Berücksichtigung des Richtwerts für Frauen von 19 bis unter 25 Jahren (PAL-Wert 1,4) und Zulage von 500 kcal/Tag für ausschließliches Stillen während der ersten 4 bis 6 Monate.")
    if options["is_lactating"]:
        return val.ref(1.4/1000)
    elif options["is_pregnant"]:
        trimester_data = [None, 1.1, 1.3, 1.4]
        return val.ref( trimester_data[options["trimester"]]/1000 )
    elif options["sex"] == "female":
        if options["age"] < 19:
            return val.ref(1.2/1000)
        elif options["age"] < 51:
            return val.ref(1.1/1000)
        else:
            return val.ref(1/1000)
    else:
        if options["age"] < 25:
            return val.ref(1.3/1000)
        elif options["age"] < 65:
            return val.ref(1.2/1000)
        else:
            return val.ref(1.1/1000)
_nutriments_data["vitamin b2"] = {
    "synonyms": ["riboflavin"],
    "categories": ["vitamins","vitamins&provitamins","vitamin b complex"],
    "rdi": _rdi_vitamin_b2
}

def _rdi_vitamin_b3(options={}):
    options = default_body_parameters | options
    val = _RDI()
    val.comment("Defined for Niacin")
    val.comment("1 mg Niacin-Äquivalent = 1 mg Niacin = 60 mg Tryptophan")
    val.comment("Zugrunde gelegt wurden die alters- und geschlechtsspezifischen Richtwerte für die Energiezufuhr (PAL-Wert 1,4).")
    val.comment("Unter Berücksichtigung des Richtwerts für Frauen von 19 bis unter 25 Jahren (PAL-Wert 1,4) und Zulage von 250 kcal/Tag während des 2. Trimesters und von 500 kcal/Tag während des 3. Trimesters der Schwangerschaft.")
    if options["is_lactating"]:
        return val.ref(16/1000)
    elif options["is_pregnant"]:
        if options["trimester"] == 3:
            return val.ref(16/1000)
        elif options["trimester"] == 2:
            return val.ref(14/1000)
        else:
            return val.ref(13/1000)
    elif options["sex"] == "female":
        if options["age"] < 25:
            return val.ref(13/1000)
        elif options["age"] < 51:
            return val.ref(12/1000)
        else:
            return val.ref(11/1000)
    else:
        if options["age"] < 19:
            return val.ref(17/1000)
        elif options["age"] < 25:
            return val.ref(16/1000)
        elif options["age"] < 65:
            return val.ref(15/1000)
        else:
            return val.ref(14/1000)
_nutriments_data["vitamin b3"] = {
    "synonyms": ["niacin", "nicotinic acid", "nikotinamid", "nikotinsäure"],
    "categories": ["vitamins","vitamins&provitamins","vitamin b complex"],
    "rdi": _rdi_vitamin_b3
}

def _rdi_vitamin_b5(options={}):
    options = default_body_parameters | options
    val = _RDI().comment("Defined for pantothenic acid")
    if options["is_lactating"]:
        return val.ref(7/1000)
    else:
        return val.ref(5/1000)
_nutriments_data["vitamin b5"] = {
    "synonyms": ["pantothenic acid", "pantothensäure"],
    "categories": ["vitamins&provitamins","vitamin b complex"],
    "rdi": _rdi_vitamin_b5
}

def _rdi_vitamin_b6(options={}):
    options = default_body_parameters | options
    val = _RDI()
    if options["is_lactating"] or options["sex"] == "male":
        return val.ref(1.6/1000)
    elif options["is_pregnant"]:
        trimester_data = [None, 1.5, 1.8, 1.8]
        return val.ref( trimester_data[options["trimester"]]/1000 )
    else:
        return val.ref(1.4/1000)
_nutriments_data["vitamin b6"] = {
    "synonyms": ["pyridoxine", "pyridoxin"],
    "categories": ["vitamins","vitamins&provitamins","vitamin b complex"],
    "rdi": _rdi_vitamin_b6
}

def _rdi_vitamin_b7(options={}):
    options = default_body_parameters | options
    val = _RDI().comment("Defined for Biotin")
    if options["is_lactating"]:
        return val.ref(45/1000000)
    else:
        return val.ref(40/1000000)
_nutriments_data["vitamin b7"] = {
    "synonyms": ["biotin"],
    "categories": ["vitamins","vitamins&provitamins","vitamin b complex"],
    "rdi": _rdi_vitamin_b7
}

def _rdi_vitamin_b9(options={}):
    options = default_body_parameters | options
    val = _RDI()
    val.comment("Originally for Folate")
    val.comment("Berechnet nach der Summe folatwirksamer Verbindungen in der üblichen Nahrung (Folat-Äquivalente): 1μg Folat-Äquivalent = 1μg Nahrungsfolat = 0,5 μg synthetische Folsäure")
    val.comment("Frauen, die schwanger werden wollen oder könnten, sollten zusätzlich zu einer folatreichen Ernährung 400 μg synthetische Folsäure/Tag oder äquivalente Dosen anderer Folate in Form eines Präparats einnehmen, um Neuralrohrdefekten vorzubeugen. Diese zusätzliche Einnahme eines Folsäure- oder Folatpräparats sollte mindestens 4 Wochen vor Beginn der Schwangerschaft anfangen und während des 1. Drittels der Schwangerschaft beibehalten werden.")
    if options["is_lactating"]:
        return val.ref(450/1000000)
    elif options["is_pregnant"]:
        return val.ref(550/1000000)
    else:
        return val.ref(300/1000000)
_nutriments_data["vitamin b9"] = {
    "synonyms": ["folate", "folic acid", "folsäure", "vitamin b11", "vitamin m"],
    "categories": ["vitamins","vitamins&provitamins","vitamin b complex"],
    "rdi": _rdi_vitamin_b9
}

def _rdi_vitamin_b12(options={}):
    options = default_body_parameters | options
    val = _RDI()
    if options["is_lactating"]:
        return val.ref(5.5/1000000)
    elif options["is_pregnant"]:
        return val.ref(4.5/1000000)
    else:
        return val.ref(4/1000000)
_nutriments_data["vitamin b12"] = {
    "synonyms": ["cyanocobalamin", "cobalamin"],
    "categories": ["vitamins","vitamins&provitamins","vitamin b complex"],
    "rdi": _rdi_vitamin_b12
}

def _rdi_vitamin_c(options={}):
    options = default_body_parameters | options
    val = _RDI()
    val.comment("Raucher 155 mg/Tag")
    val.comment("Raucherinnen 135 mg/Tag")
    if options["is_lactating"]:
        return val.ref(125/1000)
    elif options["is_pregnant"]:
        trimester_data = [None, 95, 105, 105]
        return val.ref( trimester_data[options["trimester"]]/1000 )
    elif options["is_smoker"]:
        if options["sex"] == "female":
            return val.ref(135/1000)
        else:
            return val.ref(155/1000)
    elif options["sex"] == "female":
        if options["age"] < 19:
            return val.ref(90/1000)
        else:
            return val.ref(95/1000)
    else:
        if options["age"] < 19:
            return val.ref(105/1000)
        else:
            return val.ref(110/1000)
_nutriments_data["vitamin c"] = {
    "synonyms": ["ascorbic acid", "ascorbinsäure"],
    "categories": ["vitamins","vitamins&provitamins","antioxidants"],
    "rdi": _rdi_vitamin_c
}

def _rdi_vitamin_d(options={}):
    options = default_body_parameters | options
    val = _RDI()
    #TODO sunlight exposure
    #TODO https://ods.od.nih.gov/factsheets/VitaminD-HealthProfessional/
    val = _RDI()
    val.comment("1 μg = 40 Internationale Einheiten (IE); 1 IE = 0,025 μg")
    val.comment("bei fehlender endogener Synthese")
    val.comment("Sicherheitshinweis: Bei Supplementation ist die tägliche tolerierbare Gesamtzufuhrmenge (Upper Intake Level) von 25 µg für Säuglinge, 50 µg für Kinder bis 10 Jahre sowie 100 µg für Kinder ab 11 Jahre, Jugendliche und Erwachsene zu beachten.")
    return val.ref(20/1000000)
_nutriments_data["vitamin d"] = {
    "synonyms": ["calciferol"],
    "categories": ["vitamins","vitamins&provitamins"],
    "rdi": _rdi_vitamin_d
}

_nutriments_data["vitamin d2"] = {
    "synonyms": ["ergocalciferol"],
    "categories": ["vitamins","vitamins&provitamins"],
    "sum_to": "vitamin d"
}

_nutriments_data["vitamin d3"] = {
    "synonyms": ["cholecalciferol"],
    "categories": ["vitamins","vitamins&provitamins"],
    "sum_to": "vitamin d"
}

def _rdi_vitamin_e(options={}):
    options = default_body_parameters | options
    val = _RDI()
    val.comment("1 mg RRR-α-Tocopherol-Äquivalent = 1 mg RRR-α-Tocopherol = 1,49 IE; 1 IE = 0,67 mg RRR-α-Tocopherol = 1 mg all-rac-α-Tocopherylacetat")
    if options["is_lactating"]:
        return val.ref(17/1000)
    elif options["is_pregnant"]:
        return val.ref(13/1000)
    elif options["sex"] == "female":
        if options["age"] > 65:
            return val.ref(11/1000)
        else:
            return val.ref(12/1000)
    else:
        if options["age"] < 25:
            return val.ref(15/1000)
        elif options["age"] < 51:
            return val.ref(14/1000)
        elif options["age"] < 65:
            return val.ref(13/1000)
        else:
            return val.ref(12/1000)
_nutriments_data["vitamin e"] = {
    "synonyms": ["tocopherol","alpha-tocopherol"],
    "categories": ["vitamins","vitamins&provitamins","antioxidants"],
    "rdi": _rdi_vitamin_e
}

def _rdi_vitamin_k(options={}):
    options = default_body_parameters | options
    val = _RDI()
    if options["is_lactating"] or options["is_pregnant"]:
        return val.ref(60/1000000)
    elif options["sex"] == "female":
        if options["age"] < 51:
            return val.ref(60/1000000)
        else:
            return val.ref(65/1000000)
    else:
        if options["age"] < 51:
            return val.ref(70/1000000)
        else:
            return val.ref(80/1000000)
_nutriments_data["vitamin k"] = {
    "synonyms": [],
    "categories": ["vitamins","vitamins&provitamins"],
    "rdi": _rdi_vitamin_k
}

_nutriments_data["vitamin k1"] = {
    "synonyms": ["phylloquinone"],
    "categories": ["vitamins","vitamins&provitamins"],
    "sum_to": "vitamin k"
}

_nutriments_data["vitamin k2"] = {
    "synonyms": ["menaquinone"],
    "categories": ["vitamins","vitamins&provitamins"],
    "sum_to": "vitamin k"
}

def _rdi_water(options={}):
    options = default_body_parameters | options
    val = _RDI()
    val.comment("Hierbei handelt es sich um den Richtwert für die Wasserzufuhr durch Getränke.")
    if options["is_lactating"]:
        return val.ref(1710)
    elif options["is_pregnant"]:
        return val.ref(1470)
    elif options["age"] < 19:
        return val.ref(1530)
    elif options["age"] < 25:
        return val.ref(1470)
    elif options["age"] < 51:
        return val.ref(1410)
    elif options["age"] < 65:
        return val.ref(1230)
    else:
        return val.ref(1310)
_nutriments_data["water"] = {
    "is_fluid": True,
    "synonyms": ["wasser"],
    "categories": ['main'],
    "kcal_per_gramm": 0,
    "kcal_per_ml": 0,
    "rdi": _rdi_water
}

def _rdi_zinc(options={}):
    options = default_body_parameters | options
    val = _RDI()
    val.comment("Die Absorption von Zink wird bei Erwachsenen durch den Phytatgehalt der Nahrung beeinflusst. Daher wird die empfohlene Zufuhr für Zink in Abhängigkeit von der Phytatzufuhr angegeben.")
    val.comment("entspricht einer Phytatzufuhr von 330 mg/Tag (0,5 mmol/Tag); eine niedrige Phytatzufuhr und damit eine hohe Zinkabsorption liegt bei Ernährungsweisen vor, bei denen der Verzehr von Vollkornprodukten sowie Hülsenfrüchten gering ist und die Proteinquellen vorrangig tierischer Herkunft sind")
    val.comment("entspricht einer Phytatzufuhr von 660 mg/Tag (1,0 mmol/Tag); eine mittlere Phytatzufuhr und damit eine moderate Zinkabsorption liegt bei Ernährungsweisen vor, die Proteinquellen tierischer Herkunft, darunter auch Fleisch oder Fisch, sowie Vollkornprodukte und Hülsenfrüchte einschließen (entsprechend einer vollwertigen Ernährung) oder bei einer vegetarischen bzw. veganen Ernährung mit vorrangig hoch ausgemahlenen, gekeimten oder fermentierten Getreideprodukten")
    val.comment("entspricht einer Phytatzufuhr von 990 mg/Tag (1,5 mmol/Tag); eine hohe Phytatzufuhr und damit eine verringerte Zinkabsorption liegt bei Ernährungsweisen vor, bei denen der Verzehr von Vollkornprodukten (vor allem nicht gekeimte oder unfermentierte) und Hülsenfrüchten hoch ist und die Proteinquellen vorrangig oder ausschließlich pflanzlicher Herkunft sind (z. B. Soja)")
    if options["is_lactating"]:
        phytat_data = [None, 11,13,14]
        return val.ref( phytat_data[diets[options["diet"]]]/1000 )
    elif options["is_pregnant"]:
        if options["trimester"] == 1:
            phytat_data = [None, 7,9,11]
            return val.ref( phytat_data[diets[options["diet"]]]/1000 )
        else:
            phytat_data = [None, 9,11,13]
            return val.ref( phytat_data[diets[options["diet"]]]/1000 )
    elif options["sex"] == "female":
        if options["age"] < 19:
            return val.ref(11/1000)
        phytat_data = [None, 7,8,10]
        return val.ref( phytat_data[diets[options["diet"]]]/1000 )
    else:
        if options["age"] < 19:
            return val.ref(14/1000)
        phytat_data = [None, 11,14,16]
        return val.ref( phytat_data[diets[options["diet"]]]/1000 )
_nutriments_data["zinc"] = {
    "synonyms": ["zink"],
    "categories": ["micronutrients","minerals","antioxidants"],
    "rdi": _rdi_zinc
}
