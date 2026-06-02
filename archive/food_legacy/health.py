from typing import Union, List, Dict
from functools import reduce

from activities import activities

default_body_parameters : dict = {
    "age":              50,
    "sex":              "male",
    "height":           180,
    "weight":           90,
    "is_smoker":        False,
    "is_pregnant":      False,
    "trimester":        1,
    "is_lactating":     False,
    "hypertension":     True,
    "sun_exposure":     "low",
    "lifestyle":        "sedentary",
    "diet":             "balanced",
    "metabolic_method": "harris-benedict"   #optionally: "mifflin-st.jeor" see https://de.m.wikipedia.org/wiki/Grundumsatz
}

lifestyles : Dict[str,int] = { #                Example	                                                                    PAL
    "extremely inactive":   0,# Cerebral palsy patient	                                                    <1.40
    "sedentary":            1,# Office worker getting little or no exercise	                                1.40-1.69
    "moderately active":    2,# Construction worker or person running one hour daily	                    1.70-1.99
    "vigorously active":    3,#	Agricultural worker (non mechanized) or person swimming two hours daily	    2.00-2.40
    "extremely active":     4 # Competitive cyclist	                                                        >2.40
}
diets : Dict[str,int] = {
    "meat centric":         0, # low phytate intake of 330 mg/day results in higher zinc absorption
    "balanced":             1, # medium phytate intake of 660 mg/day results in moderate zinc absorption
    "vegan or vegetarian":  2  # high phytate intake of 990 mg/day results in lower zinc absorption
}

def get_normal_weight(options : dict = {}) -> Union[int,float]:
    #https://www.fettrechner.de/kalorienrechner/broca-index/broca-index.php
    options = default_body_parameters | options
    return options["height"] - 100

def get_BMI(options : dict ={}) -> float:
    options = default_body_parameters | options
    return options["weight"] / ( (options["height"]/100) ** 2 )

def get_basal_metabolic_rate(options : dict = {}) -> Union[int,float] :
    options = default_body_parameters | options
    if options["metabolic_method"] == "harris-benedict":
        if options["sex"] == "female":
            return 655.1 + (9.563 * options["weight"]) + (1.85 * options["height"]) - (4.676 * options["age"])
        else:
            return 66.47 + (13.75 * options["weight"]) + (5.003 * options["height"]) - (6.755 * options["age"])
    elif options["metabolic_method"] == "mifflin-st.jeor":
        if options["sex"] == "female":
            return (10 * options["weight"]) + (6.25 * options["height"]) - (5 * options["age"]) - 161
        else:
            return (10 * options["weight"]) + (6.25 * options["height"]) - (5 * options["age"]) + 5
    # other option: https://www.omnicalculator.com/health/bmr-katch-mcardle
    # other option: WHO formula, see https://www.cogap.de/wissen/formeln-zur-berechnung-des-grundumsatzes/
    else:
        raise ValueError(f"Unknown metabolic method: {options['metabolic_method']}")
def get_activation_metabolic_rate(options : dict = {}) -> Union[int,float] :
    options = default_body_parameters | options
    if options["sex"] == "female":
        return 1 * options["weight"] * 24
    else:
        return 1.1 * options["weight"] * 24

def kj_to_kcal(kj : float) -> float:
    return kj * 0.23885 #see https://de.m.wikipedia.org/wiki/Grundumsatz
def kcal_to_kj(kcal : float) -> float:
    return kcal * 4.1868


default_activity_profile : Dict[str,Union[int,float]] = {
    'sleeping':6,
    'eating, sitting':1,
    "walking (2.5 mph)":1,
    "sitting tasks , light effort (e.g., office work,...)":10
}

class Activity_profile:
    def __init__(self,profile : Dict[str,Union[int,float]] = {}):
        profile = default_activity_profile | profile
                
        self.hours = { activity: 0 for activity in activities.keys() }
        self.hours['sitting (inactive)'] = 24
        for activity, amount in profile.items():
            self.set(amount,activity,'sitting (inactive)')
        
    #set hours for an activity, per default taking it from sitting time
    def set(self, amount : Union[int,float], target : str, source : str ='sitting (inactive)'):
        if self.hours[source] >= amount:
            self.hours[source] -= amount
            self.hours[target] += amount

    def get_kcal(self, options : dict ={}) -> float:
        options = default_body_parameters | options
        #Method: hourly calory consumption is basal metabolic rate (e.g.with "harris-benedict") * metabolic equivalent of task MET per activity
        bmr = get_basal_metabolic_rate(options | {"metabolic_method": "harris-benedict"})
        if bmr is None:
            bmr = 2000  # Default fallback
        return reduce(lambda x, y: x + self.hours[y] * activities[y] * bmr / 24 , activities.keys(), 0) * 1.06


        