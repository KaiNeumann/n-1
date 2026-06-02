import re
from typing import Union, List, Dict

from health import Activity_profile, default_body_parameters
import nutriments

class Amount:
    def __init__(self, value):
        self.value = value

    def __call__(self, amount):
        return Amount(self.value * amount)

# Example usage:
# gram = Amount(1)
# apple = Food()
# portion = apple * gram(250)

gramm = Amount(1)
kilo = Amount(1000)
ml = Amount(1)
liter = Amount(1000)

class Portion:
    # Initializes a new portion with the given name and an optional default weight
    # The sizes of each individual food instance are stored in a dictionary called "sizes"
    def __init__(self, name: str, weight : Union[int,float] = 100, sizes : Dict[int,Union[int,float]] = {} ):
        self.name : str = name
        self.sizes : Dict[int,Union[int,float]] = sizes
        self.weight : Union[int,float] = weight

    def __call__(self, amount: Union[int,float] = 1, custom_weight: Union[int,float] = None) -> 'Portion':
        """Create a modified portion.
        
        Args:
            amount: Number of portions (default 1)
            custom_weight: Override the base weight (default None = use standard weight)
        
        Returns:
            New Portion with calculated weight
        
        Examples:
            scheibe(2)        # 2 standard slices (2 x 25g = 50g)
            scheibe(2, 100)   # 2 big slices (2 x 100g = 200g)
            scheibe(1, 100)   # 1 big slice (100g)
        """
        if custom_weight is not None:
            # Using custom weight - ignore sizes and use weight directly
            base_weight = custom_weight
            new_sizes = {}
        else:
            # Using standard weight - scale sizes dict
            base_weight = self.weight if self.weight is not None else 100
            new_sizes = {}
            if self.sizes:
                for id, val in self.sizes.items():
                    new_sizes[id] = val * amount
        
        return Portion(self.name, base_weight * amount, new_sizes)

    # Adds a new size for a specific food instance to the "sizes" dictionary
    # If no amount is provided, it defaults to the standard quantity
    # Returns the portion instance itself for method chaining
    def add(self, instance_id : int, amount: Union[int,float] = None ) -> 'Portion':
        self.sizes[instance_id] = amount or self.weight
        return self

    # Retrieves the size of a specific food instance from the "sizes" dictionary
    # If there's no size defined for the food instance, it returns the standard quantity instead
    def get(self, instance_id : int ) -> Union[int,float] :
        return self.sizes.get(instance_id, self.weight)

class CategoryPortionDefaults:
    """Manages default portion sizes for food categories.
    
    Allows setting category-wide defaults that apply when a food doesn't have
    an explicit portion size defined.
    
    Example:
        # Set defaults
        CategoryPortionDefaults.set("beer", flasche, 500)
        CategoryPortionDefaults.set("bread", scheibe, 25)
        
        # Now all "beer" foods will use 500ml for flasche unless overridden
    """
    
    _defaults: Dict[str, Dict[str, Union[int, float]]] = {}
    
    @classmethod
    def set(cls, category: str, portion: Portion, amount: Union[int, float]):
        """Set a default portion size for a category.
        
        Args:
            category: Food category name (e.g., 'beer', 'bread', 'yogurt')
            portion: The Portion type (e.g., flasche, scheibe)
            amount: Default amount in grams/ml for this portion
        """
        if category not in cls._defaults:
            cls._defaults[category] = {}
        cls._defaults[category][portion.name] = amount
    
    @classmethod
    def get(cls, category: str, portion_name: str) -> Union[int, float, None]:
        """Get default portion size for a category.
        
        Args:
            category: Food category name
            portion_name: Name of the portion type
            
        Returns:
            Default amount or None if not set
        """
        if category in cls._defaults:
            return cls._defaults[category].get(portion_name)
        return None
    
    @classmethod
    def list_categories(cls) -> List[str]:
        """List all categories with defaults defined."""
        return list(cls._defaults.keys())
    
    @classmethod
    def get_category_defaults(cls, category: str) -> Dict[str, Union[int, float]]:
        """Get all default portions for a category."""
        return cls._defaults.get(category, {}).copy()


class Portion_Registry:
    # Initializes a new portion registry with an empty dictionary of portions
    def __init__(self):
        self.portions : Dict[str, Portion] = {}

    # Creates a new portion with the given name and optional standard quantity
    # Adds it to the dictionary of portions in the registry
    # Returns the newly created portion
    def create_portion(self, name : str, weight : Union[int,float] = None) -> Portion:
        portion = Portion(name, weight)
        self.portions[name] = portion
        return portion

    # Retrieves a portion by its name from the dictionary of portions in the registry
    # If there's no portion with that name, it returns None
    def get_portion_by_name(self, name : str) -> Union[Portion, None]:
        return self.portions.get(name)

    # Retrieves a portion from the dictionary of portions in the registry based on its ID
    # This is useful when dealing with multiple references to the same object in memory
    # If there's no portion with that ID, it returns None
    def get_portion_by_id(self, portion_id : int) -> Union[Portion, None]:
        for portion in self.portions.values():
            if id(portion) == portion_id:
                return portion
        return None

    # Retrieves a list of portion names for a specific food instance
    # This is done by checking which portions have a size defined for the given food instance
    def get_portions_for_food_instance(self, food_instance : 'Food') -> List[str]:
        return [
            portion_name for portion_name, portion in self.portions.items()
            if id(food_instance) in portion.sizes
        ]


Registry = Portion_Registry()

becher = Registry.create_portion("becher")
beutel = Registry.create_portion("beutel")
dose = Registry.create_portion("dose")
eins = Registry.create_portion("eins")
esslöffel = Registry.create_portion("esslöffel",15)
flasche = Registry.create_portion("flasche",1000)
glas = Registry.create_portion("glas",200)
handvoll = Registry.create_portion("handvoll")
kleine_flasche = Registry.create_portion("kleine_flasche",330)
kugel = Registry.create_portion("kugel")
packung = Registry.create_portion("packung")
pad = Registry.create_portion("pad")
portion = Registry.create_portion("portion")
pott = Registry.create_portion("pott",200)
prise = Registry.create_portion("prise")
scheibe = Registry.create_portion("scheibe")
schnapsglas = Registry.create_portion("glas",20)
schüssel = Registry.create_portion("schüssel")
stück = Registry.create_portion("stück")
tablette = Registry.create_portion("tablette")
tafel = Registry.create_portion("tafel")
tasse = Registry.create_portion("tasse",150)
teelöffel = Registry.create_portion("teelöffel",5)
teller = Registry.create_portion("teller")
topf = Registry.create_portion("topf")
tüte = Registry.create_portion("tüte")
zehe = Registry.create_portion("zehe")


class Food:
    def __init__(self, nutrition_data : Union[Dict[str,Union[int,float]],'Food'] = {}, weight : Union[int,float] = 0, category: str = None):
        #Nutrition dat is per 100g. Always per 100g!
        self.nutrition_data : Dict[str,Union[int,float]] = {}
        self.weight = weight
        self.category = category  # Food category for default portion sizes
        if isinstance(nutrition_data, dict):
            self.nutrition_data = {}
            for key, value in nutrition_data.items():
                name = nutriments.get_name(key)
                if name:
                    self.nutrition_data[name] = value
        elif isinstance(nutrition_data, Food):
            self.nutrition_data = dict(nutrition_data.nutrition_data)
            self.weight = nutrition_data.weight
            self.category = nutrition_data.category
    
    def __str__(self) -> str :
        sums = {nutriments.get_name(key) : self.nutrition_data[key] * self.weight / 100 for key in sorted(self.nutrition_data) }
        #sums = {nutriments.get_name(key) : value * self.weight / 100 for key, value in self.nutrition_data.items() }
        return f"Food({sums},{self.weight})"

    def __mul__(self, quantity: Union[Portion,Amount,int,float]) -> 'Food':
        weight = self.weight
        if isinstance(quantity, Portion):
            # First check if this specific food has a custom portion size
            amount = quantity.sizes.get(id(self))
            if amount is None:
                # No specific size set, check for category default
                if self.category:
                    amount = CategoryPortionDefaults.get(self.category, quantity.name)
                # If still no amount, use the portion's default
                if amount is None:
                    amount = quantity.weight
            weight = amount
        # multiplying with an Amount, e.g. gramm(200) means we have a total weight of 200g of the current food. This doesn't change the nutrition per 100g
        elif isinstance(quantity, Amount):
            weight = quantity.value
        # multiplying with a number
        else:
            weight *= quantity
        
        return Food(self.nutrition_data, weight)

    def __truediv__(self, quantity : Union[int,float]) -> 'Food':
        # allows direct division of the instances, e.g. Ingredient_instance / 3. dividing by a Amount, e.g. gramm(200) makes no sense
        if quantity == 0:
            raise ValueError("Cannot divide by zero")
        return Food(self.nutrition_data, self.weight / quantity )

    def __add__(self, other : 'Food') -> 'Food':
        total_weight = self.weight + other.weight
        if total_weight == 0:
            return Food({}, 0)
        weighted_nutrition = {k: (self.nutrition_data.get(k, 0) * self.weight + other.nutrition_data.get(k, 0) * other.weight)/total_weight for k in set(self.nutrition_data) | set(other.nutrition_data)}
        return Food(weighted_nutrition, total_weight)

    def __sub__(self, other : 'Food') -> 'Food':
        #FIXME check that we don't subtract more than there is
        total_weight = self.weight - other.weight
        if total_weight <= 0:
            return Food({}, 0)
        weighted_nutrition = {k: (self.nutrition_data.get(k, 0) * self.weight - other.nutrition_data.get(k, 0) * other.weight)/total_weight for k in set(self.nutrition_data) | set(other.nutrition_data)}
        return Food(weighted_nutrition, total_weight)

    def add(self, *others : Union[Dict[str,Union[int,float]],'Food']) -> 'Food':
        new_food = self
        for other in others:
            if isinstance(other,dict):
                other = Food(other)
            new_food = new_food + other
        return new_food

    def compare_with_activity_profile(self, profile : Activity_profile, options={}) -> str:
        intake = self.nutrition_data.get('calories') * self.weight / 100 #remember nutrition_data is per 100g!
        outtake = profile.get_kcal(options)
        if outtake == 0:
            return "N/A (no activity)"
        return "{:.2f}%".format(round(intake / outtake * 100, 2))

    def compare_with_rdi(self,category : str = None, options : dict = {}, days : Union[int,float] = 1) -> dict :
        rdis = nutriments.get_rdis_by_category(category,options)
        diff = {}
        for nutriment, rdi_obj in rdis.items():
            value = self.nutrition_data.get(nutriment, 0) * self.weight / 100 #remember nutrition_data is per 100g!
            if rdi_obj.minimum and value < rdi_obj.minimum * days:
                diff[nutriment] = "{:.2f}%".format(round(value / (rdi_obj.minimum * days) * 100, 2))
            elif rdi_obj.maximum and value > rdi_obj.maximum * days:
                diff[nutriment] = "Not OK"
            elif rdi_obj.reference and value != rdi_obj.reference * days:
                diff[nutriment] = "{:.2f}%".format(round(value / (rdi_obj.reference * days) * 100, 2))
            else:
                diff[nutriment] = "OK"
        return diff

    def portion(self,portion_instance : Portion, ammount : Union[int,float] = None) -> 'Food':
        portion_instance.add(id(self), ammount)
        return self

    def set_category(self, category: str) -> 'Food':
        """Set the food category for default portion sizes.
        
        Args:
            category: Category name (e.g., 'beer', 'bread', 'yogurt')
            
        Returns:
            Self for method chaining
            
        Example:
            beer = Food({'calories': 40, ...}).set_category('beer')
            # Now beer * flasche will use the 'beer' category default if set
        """
        self.category = category
        return self

    @staticmethod
    def valid_name(string : str) -> str :
        # Remove all non-alphanumeric characters and replace spaces with underscores
        valid_name = re.sub('[^0-9a-zA-ZäöüÄÖÜßéêè]+', '_', string).strip('_')
        # Ensure the name does not start with a digit
        if valid_name[0].isdigit():
            valid_name = '_' + valid_name
        return valid_name

class Day:
    def __init__(self,iso_date: str, *params):
        self.date = iso_date
        self.comments = []
        self.food = Food()
        self.activities = Activity_profile()
        self.body_parameters = default_body_parameters

        for item in params:
            self.add(item)    

    def add(self,item):
        if isinstance(item, Food):
            self.food = self.food.add(item)
        elif isinstance(item, Activity_profile):
            self.activities = item
        elif isinstance(item, dict):
            #FIXEM better check for body parameters
            self.body_parameters = item.copy()
        return self

    def calorie_balance(self):
        return self.food.compare_with_activity_profile(self.activities)
    
    def compare_with_rdi(self, category='main', options={}, days=1):
        options = self.body_parameters | options
        return self.food.compare_with_rdi(category,options,days)


# Predefined category defaults for common food types
# These can be customized or extended as needed
CategoryPortionDefaults.set("beer", flasche, 500)
CategoryPortionDefaults.set("beer", kleine_flasche, 330)
CategoryPortionDefaults.set("bread", scheibe, 25)
CategoryPortionDefaults.set("cheese", scheibe, 20)
CategoryPortionDefaults.set("yogurt", becher, 150)
CategoryPortionDefaults.set("soup", teller, 250)
CategoryPortionDefaults.set("pasta", teller, 210)
CategoryPortionDefaults.set("water", flasche, 750)
CategoryPortionDefaults.set("milk", glas, 200)

# New categories based on food file analysis
CategoryPortionDefaults.set("meat", portion, 100)
CategoryPortionDefaults.set("sausage", stück, 50)
CategoryPortionDefaults.set("beverage", flasche, 500)  # Soft drinks
CategoryPortionDefaults.set("snack", packung, 100)
CategoryPortionDefaults.set("spread", esslöffel, 15)
CategoryPortionDefaults.set("supplement", tablette, 1)

# Additional categories for Swiss database (1000+ foods)
CategoryPortionDefaults.set("fruit", portion, 150)  # Apple, banana, etc.
CategoryPortionDefaults.set("vegetable", portion, 100)  # Carrots, broccoli, etc.
CategoryPortionDefaults.set("fish", portion, 120)  # Salmon, tuna, etc.
CategoryPortionDefaults.set("cereal", becher, 50)  # Oats, muesli
CategoryPortionDefaults.set("rice", teller, 180)  # Rice dishes
CategoryPortionDefaults.set("oil", esslöffel, 10)  # Cooking oils
CategoryPortionDefaults.set("sweet", stück, 80)  # Cakes, pastries
CategoryPortionDefaults.set("prepared", packung, 400)  # Ready meals
CategoryPortionDefaults.set("alcohol", glas, 40)  # Wine, spirits
CategoryPortionDefaults.set("legume", becher, 80)  # Beans, lentils, peas
CategoryPortionDefaults.set("spices", teelöffel, 5)  # Salt, pepper, spices
CategoryPortionDefaults.set("seafood", portion, 100)  # Shrimp, squid, mussels