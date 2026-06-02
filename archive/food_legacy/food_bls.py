"""
German Food Database (BLS 4.0) - Curated Selection

Bundeslebensmittelschlüssel Version 4.0 - Popular Foods
Source: https://blsdb.de/download

License: CC BY 4.0 (Creative Commons Attribution 4.0 International)
Citation: Max Rubner-Institut (2025): Bundeslebensmittelschlüssel (BLS),
          Version 4.0 - Deutsche Nährstoffdatenbank. Karlsruhe.
          DOI: 10.25826/Data20251217-134202-0

This file contains a curated selection of popular/common foods from the 
German BLS database. For the full database (7,140 foods), use the importer:
    from importers import get_importer
    bls = get_importer("bls")
"""

from Food import *

##########
# Getreide und Getreideprodukte
##########

Hafer_ganzes_Korn_roh = Food({'calories': 343.0, 'water': 11.45, 'protein': 11.5, 'fat': 7.09, 'carbohydrate': 57.8, 'sugar': 1.08, 'starch': 52.6, 'fiber': 9.8, 'sodium': 0.008, 'potassium': 0.412, 'calcium': 0.056, 'magnesium': 0.116, 'phosphorus': 0.342, 'iron': 0.005, 'zinc': 0.004, 'manganese': 6.16, 'copper': 0.484, 'selenium': 0.000008, 'vitamin_e': 0.001342, 'vitamin_b1': 0.0007, 'vitamin_b3': 0.00237, 'vitamin_b5': 0.00071, 'vitamin_b6': 0.00096, 'vitamin_b7': 0.000013, 'vitamin_k': 0.0000021})
Hafer_ganzes_Korn_roh.set_category('cereal')

Hafer_Flocken = Food({'calories': 348.0, 'water': 10.07, 'protein': 11.2, 'fat': 6.65, 'carbohydrate': 58.9, 'sugar': 0.74, 'starch': 52.6, 'fiber': 8.3, 'sodium': 0.002, 'potassium': 0.382, 'calcium': 0.044, 'magnesium': 0.121, 'phosphorus': 0.325, 'iron': 0.004, 'zinc': 0.004, 'manganese': 4.934, 'copper': 0.41, 'selenium': 0.000009, 'vitamin_e': 0.0008, 'vitamin_b1': 0.00065, 'vitamin_b3': 0.001, 'vitamin_b5': 0.00109, 'vitamin_b6': 0.000098, 'vitamin_b7': 0.00002, 'vitamin_k': 0.0000021})
Hafer_Flocken.set_category('cereal')
Hafer_Flocken.portion(becher, 50)

Gerste_ganzes_Korn_roh = Food({'calories': 332.0, 'water': 12.7, 'protein': 10.5, 'fat': 2.1, 'carbohydrate': 67.2, 'sugar': 1.71, 'starch': 60.9, 'fiber': 14.5, 'sodium': 0.018, 'potassium': 0.51, 'calcium': 0.035, 'magnesium': 0.114, 'phosphorus': 0.342, 'iron': 0.006, 'zinc': 0.003, 'manganese': 1.68, 'copper': 0.524, 'vitamin_e': 0.00031, 'vitamin_b1': 0.0004, 'vitamin_b3': 0.0048, 'vitamin_b5': 0.00068, 'vitamin_b6': 0.00056, 'vitamin_b7': 0.000009, 'vitamin_k': 0.0000022})
Gerste_ganzes_Korn_roh.set_category('cereal')

Reis_poliert_roh = Food({'calories': 351.0, 'water': 11.88, 'protein': 7.0, 'fat': 0.62, 'carbohydrate': 77.0, 'sugar': 0.28, 'starch': 76.8, 'fiber': 1.3, 'sodium': 0.016, 'potassium': 0.107, 'calcium': 0.005, 'magnesium': 0.04, 'phosphorus': 0.114, 'iron': 0.0003, 'zinc': 0.003, 'manganese': 0.702, 'copper': 0.251, 'vitamin_b3': 0.0013, 'vitamin_b5': 0.00063, 'vitamin_b6': 0.000048, 'vitamin_b7': 0.000003})
Reis_poliert_roh.set_category('cereal')

Vollkornbrot = Food({'calories': 209.0, 'water': 41.3, 'protein': 7.0, 'fat': 1.4, 'carbohydrate': 39.7, 'sugar': 2.1, 'starch': 33.6, 'fiber': 6.3, 'sodium': 0.46, 'potassium': 0.24, 'calcium': 0.041, 'magnesium': 0.045, 'phosphorus': 0.11, 'iron': 0.0017, 'zinc': 0.001, 'vitamin_e': 0.00036, 'vitamin_b1': 0.00018, 'vitamin_b2': 0.00007, 'vitamin_b3': 0.00144, 'vitamin_b6': 0.000085, 'vitamin_b9': 0.000025, 'vitamin_b5': 0.0004})
Vollkornbrot.set_category('bread')
Vollkornbrot.portion(scheibe, 30)

Roggenbrot = Food({'calories': 204.0, 'water': 42.4, 'protein': 6.1, 'fat': 1.3, 'carbohydrate': 39.0, 'sugar': 2.2, 'starch': 33.6, 'fiber': 5.5, 'sodium': 0.53, 'potassium': 0.23, 'calcium': 0.037, 'magnesium': 0.044, 'phosphorus': 0.095, 'iron': 0.0016, 'zinc': 0.001, 'vitamin_b1': 0.00021, 'vitamin_b2': 0.00007, 'vitamin_b3': 0.001, 'vitamin_b6': 0.00009})
Roggenbrot.set_category('bread')
Roggenbrot.portion(scheibe, 30)

Toastbrot_weiss = Food({'calories': 265.0, 'water': 33.0, 'protein': 8.2, 'fat': 3.8, 'carbohydrate': 48.0, 'sugar': 4.0, 'starch': 43.0, 'fiber': 2.8, 'sodium': 0.45, 'potassium': 0.1, 'calcium': 0.026, 'magnesium': 0.021, 'phosphorus': 0.077, 'iron': 0.001, 'zinc': 0.0006, 'vitamin_b1': 0.00023, 'vitamin_b2': 0.00008, 'vitamin_b3': 0.00178, 'vitamin_b9': 0.000027})
Toastbrot_weiss.set_category('bread')
Toastbrot_weiss.portion(scheibe, 25)

##########
# Milch und Milchprodukte
##########

Milch_voll = Food({'calories': 64.0, 'water': 87.8, 'protein': 3.3, 'fat': 3.5, 'carbohydrate': 4.8, 'sugar': 4.8, 'fiber': 0.0, 'sodium': 0.05, 'potassium': 0.15, 'calcium': 0.12, 'magnesium': 0.011, 'phosphorus': 0.095, 'iron': 0.00003, 'zinc': 0.0004, 'iodine': 0.000011, 'vitamin_a': 0.000052, 'vitamin_d': 0.000001, 'vitamin_e': 0.0001, 'vitamin_b1': 0.000038, 'vitamin_b2': 0.00018, 'vitamin_b12': 0.00000038, 'vitamin_b3': 0.0001, 'vitamin_b5': 0.00032, 'cholesterol': 0.014})
Milch_voll.set_category('milk')
Milch_voll.portion(glas, 200)

Milch_fettarm = Food({'calories': 48.0, 'water': 89.0, 'protein': 3.4, 'fat': 1.5, 'carbohydrate': 4.9, 'sugar': 4.9, 'fiber': 0.0, 'sodium': 0.05, 'potassium': 0.16, 'calcium': 0.12, 'magnesium': 0.011, 'phosphorus': 0.1, 'iron': 0.00003, 'zinc': 0.0004, 'iodine': 0.000011, 'vitamin_a': 0.000024, 'vitamin_d': 0.000001, 'vitamin_e': 0.00005, 'vitamin_b1': 0.00004, 'vitamin_b2': 0.00018, 'vitamin_b12': 0.00000044, 'vitamin_b3': 0.0001, 'vitamin_b5': 0.00035, 'cholesterol': 0.007})
Milch_fettarm.set_category('milk')
Milch_fettarm.portion(glas, 200)

Joghurt_natur = Food({'calories': 62.0, 'water': 85.5, 'protein': 3.5, 'fat': 3.0, 'carbohydrate': 4.7, 'sugar': 4.7, 'fiber': 0.0, 'sodium': 0.06, 'potassium': 0.17, 'calcium': 0.12, 'magnesium': 0.012, 'phosphorus': 0.1, 'iron': 0.00005, 'zinc': 0.0004, 'iodine': 0.000011, 'vitamin_a': 0.000032, 'vitamin_d': 0.0000008, 'vitamin_e': 0.00009, 'vitamin_b1': 0.00003, 'vitamin_b2': 0.00014, 'vitamin_b12': 0.00000024, 'vitamin_b3': 0.00008, 'vitamin_b5': 0.00035, 'cholesterol': 0.009})
Joghurt_natur.set_category('yogurt')
Joghurt_natur.portion(becher, 150)

Joghurt_griechisch = Food({'calories': 114.0, 'water': 77.8, 'protein': 3.3, 'fat': 9.4, 'carbohydrate': 4.0, 'sugar': 4.0, 'fiber': 0.13, 'sodium': 0.04, 'potassium': 0.14, 'calcium': 0.11, 'magnesium': 0.011, 'phosphorus': 0.091, 'iron': 0.00003, 'zinc': 0.0004, 'vitamin_a': 0.000089, 'vitamin_e': 0.00015, 'vitamin_b1': 0.00003, 'vitamin_b2': 0.00013, 'vitamin_b12': 0.00000018, 'vitamin_b3': 0.00009, 'cholesterol': 0.036})
Joghurt_griechisch.set_category('yogurt')
Joghurt_griechisch.portion(becher, 150)

Quark_mager = Food({'calories': 67.0, 'water': 82.5, 'protein': 12.0, 'fat': 0.3, 'carbohydrate': 3.8, 'sugar': 3.8, 'fiber': 0.0, 'sodium': 0.05, 'potassium': 0.13, 'calcium': 0.09, 'magnesium': 0.009, 'phosphorus': 0.14, 'iron': 0.0001, 'zinc': 0.0004, 'vitamin_a': 0.000009, 'vitamin_b1': 0.00004, 'vitamin_b2': 0.00028, 'vitamin_b12': 0.0000007, 'vitamin_b3': 0.00012, 'cholesterol': 0.003})
Quark_mager.set_category('yogurt')
Quark_mager.portion(becher, 150)

Quark_20 = Food({'calories': 107.0, 'water': 76.0, 'protein': 10.0, 'fat': 6.0, 'carbohydrate': 3.5, 'sugar': 3.5, 'fiber': 0.0, 'sodium': 0.07, 'potassium': 0.14, 'calcium': 0.1, 'magnesium': 0.009, 'phosphorus': 0.15, 'iron': 0.00005, 'zinc': 0.0004, 'vitamin_a': 0.00007, 'vitamin_b1': 0.00003, 'vitamin_b2': 0.00024, 'vitamin_b12': 0.00000065, 'vitamin_b3': 0.0001, 'cholesterol': 0.02})
Quark_20.set_category('yogurt')
Quark_20.portion(becher, 150)

Butter = Food({'calories': 741.0, 'water': 15.3, 'protein': 0.7, 'fat': 83.2, 'carbohydrate': 0.6, 'sugar': 0.6, 'fiber': 0.0, 'sodium': 0.01, 'potassium': 0.024, 'calcium': 0.015, 'magnesium': 0.002, 'phosphorus': 0.024, 'iron': 0.00002, 'vitamin_a': 0.000683, 'vitamin_d': 0.0000015, 'vitamin_e': 0.002, 'vitamin_k': 0.000007, 'vitamin_b2': 0.00004, 'cholesterol': 0.215, 'saturated_fat': 53.8})
Butter.set_category('spread')
Butter.portion(scheibe, 10)

Sahne = Food({'calories': 204.0, 'water': 72.0, 'protein': 2.1, 'fat': 19.3, 'carbohydrate': 3.2, 'sugar': 3.2, 'fiber': 0.0, 'sodium': 0.04, 'potassium': 0.077, 'calcium': 0.065, 'magnesium': 0.004, 'phosphorus': 0.06, 'iron': 0.00002, 'vitamin_a': 0.000155, 'vitamin_d': 0.0000006, 'vitamin_e': 0.0004, 'vitamin_b2': 0.00009, 'cholesterol': 0.065, 'saturated_fat': 12.3})
Sahne.set_category('milk')
Sahne.portion(esslöffel, 15)

##########
# Käse
##########

Gouda = Food({'calories': 356.0, 'water': 38.2, 'protein': 25.0, 'fat': 27.4, 'carbohydrate': 2.2, 'sugar': 0.0, 'fiber': 0.0, 'sodium': 0.82, 'potassium': 0.12, 'calcium': 0.7, 'magnesium': 0.027, 'phosphorus': 0.55, 'iron': 0.0001, 'zinc': 0.0037, 'vitamin_a': 0.00027, 'vitamin_b2': 0.00034, 'vitamin_b12': 0.0000016, 'cholesterol': 0.115, 'saturated_fat': 17.6})
Gouda.set_category('cheese')
Gouda.portion(scheibe, 20)

Edamer = Food({'calories': 327.0, 'water': 43.0, 'protein': 25.0, 'fat': 24.3, 'carbohydrate': 1.4, 'sugar': 0.0, 'fiber': 0.0, 'sodium': 0.96, 'potassium': 0.12, 'calcium': 0.73, 'magnesium': 0.029, 'phosphorus': 0.54, 'iron': 0.0001, 'zinc': 0.0039, 'vitamin_a': 0.00026, 'vitamin_b2': 0.00038, 'vitamin_b12': 0.0000017, 'cholesterol': 0.1, 'saturated_fat': 15.6})
Edamer.set_category('cheese')
Edamer.portion(scheibe, 20)

Emmentaler = Food({'calories': 382.0, 'water': 35.0, 'protein': 28.5, 'fat': 29.2, 'carbohydrate': 0.0, 'sugar': 0.0, 'fiber': 0.0, 'sodium': 0.4, 'potassium': 0.09, 'calcium': 1.04, 'magnesium': 0.035, 'phosphorus': 0.76, 'iron': 0.0002, 'zinc': 0.0048, 'vitamin_a': 0.0003, 'vitamin_b2': 0.0003, 'vitamin_b12': 0.000002, 'cholesterol': 0.11, 'saturated_fat': 19.2})
Emmentaler.set_category('cheese')
Emmentaler.portion(scheibe, 20)

Camembert = Food({'calories': 297.0, 'water': 51.0, 'protein': 19.8, 'fat': 24.3, 'carbohydrate': 0.5, 'sugar': 0.0, 'fiber': 0.0, 'sodium': 0.8, 'potassium': 0.1, 'calcium': 0.35, 'magnesium': 0.02, 'phosphorus': 0.38, 'iron': 0.0002, 'zinc': 0.0027, 'vitamin_a': 0.00024, 'vitamin_b2': 0.0005, 'vitamin_b12': 0.0000015, 'cholesterol': 0.09, 'saturated_fat': 15.5})
Camembert.set_category('cheese')
Camembert.portion(stück, 30)

Frischkäse = Food({'calories': 264.0, 'water': 57.8, 'protein': 6.5, 'fat': 25.0, 'carbohydrate': 3.2, 'sugar': 3.2, 'fiber': 0.0, 'sodium': 0.4, 'potassium': 0.13, 'calcium': 0.065, 'magnesium': 0.005, 'phosphorus': 0.1, 'iron': 0.0001, 'zinc': 0.0004, 'vitamin_a': 0.00025, 'vitamin_b2': 0.00022, 'vitamin_b12': 0.0000005, 'cholesterol': 0.085, 'saturated_fat': 16.2})
Frischkäse.set_category('cheese')
Frischkäse.portion(esslöffel, 20)

Mozzarella = Food({'calories': 256.0, 'water': 58.8, 'protein': 19.5, 'fat': 19.5, 'carbohydrate': 0.7, 'sugar': 0.7, 'fiber': 0.0, 'sodium': 0.14, 'potassium': 0.008, 'calcium': 0.34, 'magnesium': 0.01, 'phosphorus': 0.35, 'iron': 0.0001, 'zinc': 0.0026, 'vitamin_a': 0.000183, 'vitamin_d': 0.0000003, 'vitamin_b2': 0.00027, 'vitamin_b12': 0.0000014, 'cholesterol': 0.046, 'saturated_fat': 11.4})
Mozzarella.set_category('cheese')
Mozzarella.portion(kugel, 50)

Feta = Food({'calories': 264.0, 'water': 55.2, 'protein': 14.2, 'fat': 21.3, 'carbohydrate': 4.1, 'sugar': 4.1, 'fiber': 0.0, 'sodium': 1.11, 'potassium': 0.06, 'calcium': 0.49, 'magnesium': 0.019, 'phosphorus': 0.34, 'iron': 0.0002, 'zinc': 0.0022, 'vitamin_a': 0.00013, 'vitamin_b2': 0.00024, 'vitamin_b12': 0.000001, 'cholesterol': 0.089, 'saturated_fat': 13.3})
Feta.set_category('cheese')
Feta.portion(stück, 30)

##########
# Fleisch und Wurst
##########

Rindfleisch_roh = Food({'calories': 113.0, 'water': 75.0, 'protein': 22.0, 'fat': 2.5, 'carbohydrate': 0.0, 'sugar': 0.0, 'fiber': 0.0, 'sodium': 0.06, 'potassium': 0.32, 'calcium': 0.005, 'magnesium': 0.022, 'phosphorus': 0.2, 'iron': 0.0023, 'zinc': 0.0042, 'vitamin_b1': 0.00009, 'vitamin_b2': 0.00022, 'vitamin_b3': 0.005, 'vitamin_b6': 0.00035, 'vitamin_b12': 0.000002, 'cholesterol': 0.055, 'saturated_fat': 1.0})
Rindfleisch_roh.set_category('meat')
Rindfleisch_roh.portion(portion, 150)

Schweinefleisch_roh = Food({'calories': 143.0, 'water': 72.0, 'protein': 20.5, 'fat': 6.3, 'carbohydrate': 0.0, 'sugar': 0.0, 'fiber': 0.0, 'sodium': 0.06, 'potassium': 0.35, 'calcium': 0.006, 'magnesium': 0.023, 'phosphorus': 0.21, 'iron': 0.001, 'zinc': 0.002, 'vitamin_b1': 0.0009, 'vitamin_b2': 0.00019, 'vitamin_b3': 0.0045, 'vitamin_b6': 0.0004, 'vitamin_b12': 0.0000007, 'cholesterol': 0.06, 'saturated_fat': 2.3})
Schweinefleisch_roh.set_category('meat')
Schweinefleisch_roh.portion(portion, 150)

Hähnchenbrust_roh = Food({'calories': 114.0, 'water': 75.5, 'protein': 21.2, 'fat': 2.6, 'carbohydrate': 0.0, 'sugar': 0.0, 'fiber': 0.0, 'sodium': 0.07, 'potassium': 0.25, 'calcium': 0.006, 'magnesium': 0.027, 'phosphorus': 0.21, 'iron': 0.0005, 'zinc': 0.0009, 'vitamin_b3': 0.007, 'vitamin_b6': 0.00055, 'vitamin_b12': 0.0000004, 'cholesterol': 0.065, 'saturated_fat': 0.7})
Hähnchenbrust_roh.set_category('meat')
Hähnchenbrust_roh.portion(portion, 150)

Wiener_Würstchen = Food({'calories': 296.0, 'water': 56.0, 'protein': 11.5, 'fat': 27.0, 'carbohydrate': 1.0, 'sugar': 0.0, 'fiber': 0.0, 'sodium': 1.0, 'potassium': 0.15, 'calcium': 0.01, 'magnesium': 0.015, 'phosphorus': 0.1, 'iron': 0.0015, 'zinc': 0.002, 'vitamin_b1': 0.00025, 'vitamin_b2': 0.00012, 'vitamin_b3': 0.003, 'vitamin_b12': 0.000001, 'cholesterol': 0.055, 'saturated_fat': 10.0})
Wiener_Würstchen.set_category('sausage')
Wiener_Würstchen.portion(stück, 50)

Bratwurst = Food({'calories': 313.0, 'water': 53.0, 'protein': 13.5, 'fat': 28.0, 'carbohydrate': 1.0, 'sugar': 0.0, 'fiber': 0.0, 'sodium': 0.9, 'potassium': 0.22, 'calcium': 0.009, 'magnesium': 0.018, 'phosphorus': 0.13, 'iron': 0.0013, 'zinc': 0.0025, 'vitamin_b1': 0.00035, 'vitamin_b2': 0.00018, 'vitamin_b3': 0.0035, 'vitamin_b12': 0.000001, 'cholesterol': 0.07, 'saturated_fat': 10.5})
Bratwurst.set_category('sausage')
Bratwurst.portion(stück, 100)

Schinken_gekocht = Food({'calories': 122.0, 'water': 72.0, 'protein': 20.0, 'fat': 4.5, 'carbohydrate': 0.5, 'sugar': 0.0, 'fiber': 0.0, 'sodium': 1.2, 'potassium': 0.3, 'calcium': 0.006, 'magnesium': 0.02, 'phosphorus': 0.2, 'iron': 0.0009, 'zinc': 0.0018, 'vitamin_b1': 0.0006, 'vitamin_b2': 0.00015, 'vitamin_b3': 0.0045, 'vitamin_b6': 0.00035, 'vitamin_b12': 0.0000008, 'cholesterol': 0.04, 'saturated_fat': 1.5})
Schinken_gekocht.set_category('sausage')
Schinken_gekocht.portion(scheibe, 20)

##########
# Fisch
##########

Lachs_roh = Food({'calories': 208.0, 'water': 67.0, 'protein': 20.0, 'fat': 14.0, 'carbohydrate': 0.0, 'sugar': 0.0, 'fiber': 0.0, 'sodium': 0.05, 'potassium': 0.36, 'calcium': 0.009, 'magnesium': 0.027, 'phosphorus': 0.24, 'iron': 0.0003, 'zinc': 0.0004, 'iodine': 0.000012, 'vitamin_d': 0.000008, 'vitamin_e': 0.003, 'vitamin_b3': 0.007, 'vitamin_b6': 0.0006, 'vitamin_b12': 0.000003, 'cholesterol': 0.055, 'saturated_fat': 3.0, 'omega_3': 2.3})
Lachs_roh.set_category('fish')
Lachs_roh.portion(portion, 120)

Thunfisch_Dose = Food({'calories': 116.0, 'water': 70.0, 'protein': 26.0, 'fat': 1.0, 'carbohydrate': 0.0, 'sugar': 0.0, 'fiber': 0.0, 'sodium': 0.4, 'potassium': 0.3, 'calcium': 0.01, 'magnesium': 0.035, 'phosphorus': 0.22, 'iron': 0.0008, 'zinc': 0.0005, 'iodine': 0.000015, 'vitamin_d': 0.000001, 'vitamin_b3': 0.012, 'vitamin_b6': 0.0004, 'vitamin_b12': 0.000002, 'cholesterol': 0.04, 'saturated_fat': 0.3, 'omega_3': 0.3})
Thunfisch_Dose.set_category('fish')
Thunfisch_Dose.portion(dose, 120)

##########
# Gemüse
##########

Kartoffel_roh = Food({'calories': 71.0, 'water': 79.0, 'protein': 1.8, 'fat': 0.1, 'carbohydrate': 15.2, 'sugar': 0.8, 'starch': 13.5, 'fiber': 1.7, 'sodium': 0.008, 'potassium': 0.41, 'calcium': 0.009, 'magnesium': 0.022, 'phosphorus': 0.055, 'iron': 0.0005, 'zinc': 0.0003, 'vitamin_c': 0.011, 'vitamin_b3': 0.0014, 'vitamin_b6': 0.00024, 'vitamin_b9': 0.000018})
Kartoffel_roh.set_category('vegetable')
Kartoffel_roh.portion(stück, 100)

Möhre_roh = Food({'calories': 35.0, 'water': 88.0, 'protein': 0.9, 'fat': 0.2, 'carbohydrate': 6.8, 'sugar': 4.7, 'fiber': 2.4, 'sodium': 0.06, 'potassium': 0.32, 'calcium': 0.033, 'magnesium': 0.012, 'phosphorus': 0.035, 'iron': 0.0004, 'zinc': 0.0002, 'provitamin_a': 0.00835, 'vitamin_c': 0.004, 'vitamin_b3': 0.0006, 'vitamin_b6': 0.00012, 'vitamin_b9': 0.000024})
Möhre_roh.set_category('vegetable')
Möhre_roh.portion(stück, 80)

Broccoli_roh = Food({'calories': 35.0, 'water': 89.0, 'protein': 2.8, 'fat': 0.4, 'carbohydrate': 3.0, 'sugar': 1.7, 'fiber': 2.6, 'sodium': 0.03, 'potassium': 0.38, 'calcium': 0.047, 'magnesium': 0.021, 'phosphorus': 0.066, 'iron': 0.0007, 'zinc': 0.0004, 'provitamin_a': 0.000361, 'vitamin_c': 0.089, 'vitamin_b3': 0.00064, 'vitamin_b5': 0.00057, 'vitamin_b6': 0.0002, 'vitamin_b9': 0.000063, 'vitamin_e': 0.00078, 'vitamin_k': 0.000102})
Broccoli_roh.set_category('vegetable')
Broccoli_roh.portion(portion, 100)

Tomate_roh = Food({'calories': 18.0, 'water': 94.0, 'protein': 0.9, 'fat': 0.2, 'carbohydrate': 2.8, 'sugar': 2.6, 'fiber': 1.2, 'sodium': 0.005, 'potassium': 0.24, 'calcium': 0.01, 'magnesium': 0.011, 'phosphorus': 0.024, 'iron': 0.0003, 'zinc': 0.0001, 'provitamin_a': 0.00045, 'vitamin_c': 0.014, 'vitamin_b3': 0.0006, 'vitamin_b5': 0.0002, 'vitamin_b6': 0.00006, 'vitamin_b9': 0.000015, 'vitamin_e': 0.00054, 'vitamin_k': 0.000079})
Tomate_roh.set_category('vegetable')
Tomate_roh.portion(stück, 120)

Gurke_roh = Food({'calories': 13.0, 'water': 96.0, 'protein': 0.6, 'fat': 0.1, 'carbohydrate': 2.2, 'sugar': 1.7, 'fiber': 0.8, 'sodium': 0.002, 'potassium': 0.15, 'calcium': 0.016, 'magnesium': 0.013, 'phosphorus': 0.024, 'iron': 0.0003, 'zinc': 0.0002, 'vitamin_c': 0.004, 'vitamin_b3': 0.0001, 'vitamin_b5': 0.00026, 'vitamin_b9': 0.000007, 'vitamin_k': 0.000016})
Gurke_roh.set_category('vegetable')
Gurke_roh.portion(stück, 150)

Paprika_rot_roh = Food({'calories': 26.0, 'water': 92.0, 'protein': 1.0, 'fat': 0.3, 'carbohydrate': 4.6, 'sugar': 4.2, 'fiber': 1.9, 'sodium': 0.003, 'potassium': 0.21, 'calcium': 0.01, 'magnesium': 0.012, 'phosphorus': 0.026, 'iron': 0.0004, 'zinc': 0.0002, 'provitamin_a': 0.00162, 'vitamin_c': 0.128, 'vitamin_b3': 0.0005, 'vitamin_b5': 0.0003, 'vitamin_b6': 0.00029, 'vitamin_b9': 0.000046, 'vitamin_e': 0.0014, 'vitamin_k': 0.000043})
Paprika_rot_roh.set_category('vegetable')
Paprika_rot_roh.portion(stück, 120)

Zwiebel_roh = Food({'calories': 38.0, 'water': 89.0, 'protein': 1.1, 'fat': 0.1, 'carbohydrate': 7.9, 'sugar': 4.2, 'fiber': 1.5, 'sodium': 0.004, 'potassium': 0.15, 'calcium': 0.023, 'magnesium': 0.01, 'phosphorus': 0.03, 'iron': 0.0002, 'zinc': 0.0002, 'vitamin_c': 0.007, 'vitamin_b3': 0.00012, 'vitamin_b5': 0.00012, 'vitamin_b6': 0.00012, 'vitamin_b9': 0.000016})
Zwiebel_roh.set_category('vegetable')
Zwiebel_roh.portion(stück, 80)

Knoblauch_roh = Food({'calories': 141.0, 'water': 60.0, 'protein': 6.4, 'fat': 0.5, 'carbohydrate': 28.2, 'sugar': 1.0, 'fiber': 1.9, 'sodium': 0.017, 'potassium': 0.4, 'calcium': 0.181, 'magnesium': 0.025, 'phosphorus': 0.153, 'iron': 0.0017, 'zinc': 0.0016, 'manganese': 0.167, 'vitamin_c': 0.031, 'vitamin_b3': 0.0006, 'vitamin_b5': 0.0003, 'vitamin_b6': 0.0012, 'vitamin_b9': 0.000003})
Knoblauch_roh.set_category('vegetable')
Knoblauch_roh.portion(zehe, 5)

Salat_grün_roh = Food({'calories': 14.0, 'water': 95.0, 'protein': 1.3, 'fat': 0.2, 'carbohydrate': 1.4, 'sugar': 0.8, 'fiber': 1.3, 'sodium': 0.03, 'potassium': 0.25, 'calcium': 0.036, 'magnesium': 0.013, 'phosphorus': 0.029, 'iron': 0.0009, 'zinc': 0.0002, 'provitamin_a': 0.00188, 'vitamin_c': 0.009, 'vitamin_b3': 0.0003, 'vitamin_b5': 0.00015, 'vitamin_b6': 0.00007, 'vitamin_b9': 0.000073, 'vitamin_e': 0.00018, 'vitamin_k': 0.000126})
Salat_grün_roh.set_category('vegetable')
Salat_grün_roh.portion(teller, 100)

##########
# Obst
##########

Apfel_roh = Food({'calories': 52.0, 'water': 85.0, 'protein': 0.3, 'fat': 0.2, 'carbohydrate': 11.8, 'sugar': 10.4, 'fiber': 2.0, 'sodium': 0.001, 'potassium': 0.12, 'calcium': 0.007, 'magnesium': 0.005, 'phosphorus': 0.012, 'iron': 0.0002, 'zinc': 0.00005, 'vitamin_c': 0.005, 'vitamin_b3': 0.0001, 'vitamin_b5': 0.00006, 'vitamin_b6': 0.00004, 'vitamin_b9': 0.000003, 'vitamin_e': 0.00018, 'vitamin_k': 0.000002})
Apfel_roh.set_category('fruit')
Apfel_roh.portion(stück, 150)

Banane_roh = Food({'calories': 89.0, 'water': 75.0, 'protein': 1.1, 'fat': 0.3, 'carbohydrate': 20.2, 'sugar': 12.0, 'starch': 6.0, 'fiber': 2.1, 'sodium': 0.001, 'potassium': 0.36, 'calcium': 0.005, 'magnesium': 0.027, 'phosphorus': 0.022, 'iron': 0.0003, 'zinc': 0.00015, 'provitamin_a': 0.000026, 'vitamin_c': 0.009, 'vitamin_b3': 0.0007, 'vitamin_b5': 0.00033, 'vitamin_b6': 0.00037, 'vitamin_b9': 0.00002, 'vitamin_e': 0.0001})
Banane_roh.set_category('fruit')
Banane_roh.portion(stück, 120)

Orange_roh = Food({'calories': 47.0, 'water': 87.0, 'protein': 0.9, 'fat': 0.1, 'carbohydrate': 9.6, 'sugar': 8.5, 'fiber': 2.0, 'sodium': 0.001, 'potassium': 0.18, 'calcium': 0.04, 'magnesium': 0.01, 'phosphorus': 0.018, 'iron': 0.0001, 'zinc': 0.00005, 'provitamin_a': 0.000071, 'vitamin_c': 0.053, 'vitamin_b1': 0.00009, 'vitamin_b3': 0.0003, 'vitamin_b5': 0.00025, 'vitamin_b9': 0.00003, 'vitamin_b6': 0.00006})
Orange_roh.set_category('fruit')
Orange_roh.portion(stück, 130)

Birne_roh = Food({'calories': 57.0, 'water': 84.0, 'protein': 0.4, 'fat': 0.1, 'carbohydrate': 13.5, 'sugar': 10.0, 'fiber': 2.6, 'sodium': 0.001, 'potassium': 0.12, 'calcium': 0.009, 'magnesium': 0.006, 'phosphorus': 0.012, 'iron': 0.0002, 'zinc': 0.00007, 'provitamin_a': 0.000012, 'vitamin_c': 0.004, 'vitamin_b3': 0.0001, 'vitamin_b5': 0.00005, 'vitamin_b9': 0.000007, 'vitamin_e': 0.00012, 'vitamin_k': 0.000004})
Birne_roh.set_category('fruit')
Birne_roh.portion(stück, 150)

Trauben_roh = Food({'calories': 69.0, 'water': 81.0, 'protein': 0.7, 'fat': 0.2, 'carbohydrate': 16.5, 'sugar': 15.5, 'fiber': 1.0, 'sodium': 0.002, 'potassium': 0.19, 'calcium': 0.01, 'magnesium': 0.007, 'phosphorus': 0.02, 'iron': 0.0004, 'zinc': 0.00007, 'vitamin_c': 0.004, 'vitamin_b3': 0.0002, 'vitamin_b5': 0.00005, 'vitamin_b6': 0.00009, 'vitamin_b9': 0.000002, 'vitamin_k': 0.000015})
Trauben_roh.set_category('fruit')
Trauben_roh.portion(portion, 150)

Erdbeeren_roh = Food({'calories': 32.0, 'water': 91.0, 'protein': 0.7, 'fat': 0.3, 'carbohydrate': 5.7, 'sugar': 4.9, 'fiber': 2.0, 'sodium': 0.001, 'potassium': 0.15, 'calcium': 0.016, 'magnesium': 0.013, 'phosphorus': 0.024, 'iron': 0.0004, 'zinc': 0.0001, 'provitamin_a': 0.000008, 'vitamin_c': 0.059, 'vitamin_b3': 0.0004, 'vitamin_b5': 0.00013, 'vitamin_b6': 0.00005, 'vitamin_b9': 0.000024, 'vitamin_e': 0.00029, 'vitamin_k': 0.000003})
Erdbeeren_roh.set_category('fruit')
Erdbeeren_roh.portion(portion, 150)

##########
# Hülsenfrüchte und Nüsse
##########

Bohnen_weiss_gekocht = Food({'calories': 114.0, 'water': 69.0, 'protein': 7.0, 'fat': 0.5, 'carbohydrate': 17.0, 'sugar': 0.3, 'starch': 14.0, 'fiber': 7.0, 'sodium': 0.02, 'potassium': 0.4, 'calcium': 0.05, 'magnesium': 0.04, 'phosphorus': 0.12, 'iron': 0.002, 'zinc': 0.001, 'vitamin_b1': 0.0001, 'vitamin_b3': 0.0005, 'vitamin_b5': 0.0002, 'vitamin_b6': 0.0001, 'vitamin_b9': 0.000035})
Bohnen_weiss_gekocht.set_category('legume')
Bohnen_weiss_gekocht.portion(becher, 80)

Linsen_gekocht = Food({'calories': 116.0, 'water': 69.0, 'protein': 9.0, 'fat': 0.4, 'carbohydrate': 16.0, 'sugar': 0.5, 'starch': 13.0, 'fiber': 8.0, 'sodium': 0.02, 'potassium': 0.37, 'calcium': 0.019, 'magnesium': 0.036, 'phosphorus': 0.18, 'iron': 0.0033, 'zinc': 0.0013, 'vitamin_b1': 0.00017, 'vitamin_b3': 0.001, 'vitamin_b5': 0.0004, 'vitamin_b6': 0.00018, 'vitamin_b9': 0.000181})
Linsen_gekocht.set_category('legume')
Linsen_gekocht.portion(becher, 80)

Mandeln = Food({'calories': 579.0, 'water': 4.4, 'protein': 21.2, 'fat': 49.9, 'carbohydrate': 6.0, 'sugar': 4.4, 'fiber': 12.5, 'sodium': 0.001, 'potassium': 0.73, 'calcium': 0.269, 'magnesium': 0.27, 'phosphorus': 0.481, 'iron': 0.0037, 'zinc': 0.0031, 'manganese': 0.00217, 'vitamin_e': 0.0256, 'vitamin_b2': 0.001, 'vitamin_b3': 0.0035, 'vitamin_b5': 0.0003, 'vitamin_b6': 0.00014, 'vitamin_b9': 0.000044, 'saturated_fat': 3.8, 'omega_6': 12.3})
Mandeln.set_category('snack')
Mandeln.portion(handvoll, 30)

Walnüsse = Food({'calories': 654.0, 'water': 3.0, 'protein': 15.2, 'fat': 65.2, 'carbohydrate': 6.0, 'sugar': 2.6, 'fiber': 6.7, 'sodium': 0.002, 'potassium': 0.44, 'calcium': 0.098, 'magnesium': 0.158, 'phosphorus': 0.346, 'iron': 0.0029, 'zinc': 0.0031, 'vitamin_b6': 0.00054, 'vitamin_b9': 0.000098, 'vitamin_e': 0.0007, 'saturated_fat': 6.1, 'omega_3': 9.1, 'omega_6': 38.1})
Walnüsse.set_category('snack')
Walnüsse.portion(handvoll, 30)

##########
# Fette und Öle
##########

Olivenöl = Food({'calories': 884.0, 'water': 0.0, 'protein': 0.0, 'fat': 100.0, 'carbohydrate': 0.0, 'sugar': 0.0, 'fiber': 0.0, 'vitamin_e': 0.0144, 'vitamin_k': 0.00006, 'saturated_fat': 13.8, 'monounsaturated_fat': 73.0, 'polyunsaturated_fat': 10.5, 'omega_3': 0.8, 'omega_6': 9.8})
Olivenöl.set_category('oil')
Olivenöl.portion(esslöffel, 10)

Rapsöl = Food({'calories': 884.0, 'water': 0.0, 'protein': 0.0, 'fat': 100.0, 'carbohydrate': 0.0, 'sugar': 0.0, 'fiber': 0.0, 'vitamin_e': 0.0173, 'vitamin_k': 0.000071, 'saturated_fat': 7.4, 'monounsaturated_fat': 63.3, 'polyunsaturated_fat': 28.1, 'omega_3': 9.1, 'omega_6': 19.0})
Rapsöl.set_category('oil')
Rapsöl.portion(esslöffel, 10)

Sonnenblumenöl = Food({'calories': 884.0, 'water': 0.0, 'protein': 0.0, 'fat': 100.0, 'carbohydrate': 0.0, 'sugar': 0.0, 'fiber': 0.0, 'vitamin_e': 0.0411, 'vitamin_k': 0.000005, 'saturated_fat': 10.3, 'monounsaturated_fat': 19.5, 'polyunsaturated_fat': 65.7, 'omega_3': 0.0, 'omega_6': 65.7})
Sonnenblumenöl.set_category('oil')
Sonnenblumenöl.portion(esslöffel, 10)

Butterschmalz = Food({'calories': 900.0, 'water': 0.0, 'protein': 0.0, 'fat': 100.0, 'carbohydrate': 0.0, 'sugar': 0.0, 'fiber': 0.0, 'vitamin_a': 0.00084, 'vitamin_d': 0.000001, 'vitamin_e': 0.003, 'vitamin_k': 0.000009, 'cholesterol': 0.285, 'saturated_fat': 65.0, 'omega_3': 1.0, 'omega_6': 3.0})
Butterschmalz.set_category('oil')
Butterschmalz.portion(esslöffel, 10)

##########
# Süßwaren
##########

Schokolade_vollmilch = Food({'calories': 546.0, 'water': 1.0, 'protein': 7.3, 'fat': 31.0, 'carbohydrate': 56.0, 'sugar': 55.0, 'fiber': 3.4, 'sodium': 0.09, 'potassium': 0.37, 'calcium': 0.19, 'magnesium': 0.063, 'phosphorus': 0.21, 'iron': 0.001, 'zinc': 0.0012, 'vitamin_a': 0.0002, 'vitamin_b2': 0.0003, 'vitamin_b12': 0.0000005, 'vitamin_d': 0.000002, 'vitamin_e': 0.001, 'cholesterol': 0.023, 'saturated_fat': 19.0})
Schokolade_vollmilch.set_category('sweet')
Schokolade_vollmilch.portion(tafel, 100)

Schokolade_zartbitter = Food({'calories': 598.0, 'water': 1.0, 'protein': 7.8, 'fat': 42.6, 'carbohydrate': 45.4, 'sugar': 24.0, 'fiber': 10.9, 'sodium': 0.02, 'potassium': 0.72, 'calcium': 0.031, 'magnesium': 0.23, 'phosphorus': 0.31, 'iron': 0.017, 'zinc': 0.003, 'manganese': 0.019, 'copper': 0.0014, 'vitamin_b3': 0.0012, 'vitamin_b6': 0.00004, 'vitamin_b12': 0.0000003, 'vitamin_e': 0.001, 'saturated_fat': 24.5})
Schokolade_zartbitter.set_category('sweet')
Schokolade_zartbitter.portion(tafel, 100)

Honig = Food({'calories': 304.0, 'water': 17.0, 'protein': 0.3, 'fat': 0.0, 'carbohydrate': 82.4, 'sugar': 82.1, 'fiber': 0.2, 'sodium': 0.004, 'potassium': 0.052, 'calcium': 0.006, 'magnesium': 0.002, 'phosphorus': 0.004, 'iron': 0.0004, 'zinc': 0.0002, 'vitamin_b2': 0.00004, 'vitamin_b3': 0.0001, 'vitamin_b5': 0.00006, 'vitamin_b6': 0.00001, 'vitamin_b9': 0.000002, 'vitamin_c': 0.0005})
Honig.set_category('spread')
Honig.portion(esslöffel, 15)

Zucker_weiss = Food({'calories': 400.0, 'water': 0.0, 'protein': 0.0, 'fat': 0.0, 'carbohydrate': 100.0, 'sugar': 100.0, 'fiber': 0.0, 'sodium': 0.0, 'potassium': 0.002, 'calcium': 0.001, 'magnesium': 0.0, 'phosphorus': 0.0, 'iron': 0.0001, 'zinc': 0.00001})
Zucker_weiss.set_category('spices')
Zucker_weiss.portion(esslöffel, 10)

Marmelade = Food({'calories': 250.0, 'water': 30.0, 'protein': 0.3, 'fat': 0.1, 'carbohydrate': 62.0, 'sugar': 59.0, 'fiber': 1.0, 'sodium': 0.03, 'potassium': 0.08, 'calcium': 0.02, 'magnesium': 0.003, 'phosphorus': 0.01, 'iron': 0.0004, 'zinc': 0.0001, 'vitamin_b3': 0.0001, 'vitamin_b9': 0.000002})
Marmelade.set_category('spread')
Marmelade.portion(esslöffel, 15)

Keks_Butter = Food({'calories': 502.0, 'water': 2.0, 'protein': 5.8, 'fat': 25.0, 'carbohydrate': 64.0, 'sugar': 20.0, 'fiber': 2.0, 'sodium': 0.38, 'potassium': 0.08, 'calcium': 0.02, 'magnesium': 0.01, 'phosphorus': 0.08, 'iron': 0.001, 'zinc': 0.0004, 'vitamin_b1': 0.00008, 'vitamin_b2': 0.00004, 'vitamin_b3': 0.0003, 'vitamin_b6': 0.00004, 'vitamin_b9': 0.000015, 'saturated_fat': 15.0})
Keks_Butter.set_category('sweet')
Keks_Butter.portion(stück, 10)

##########
# Gewürze und Kräuter
##########

Salz = Food({'calories': 0.0, 'water': 0.2, 'protein': 0.0, 'fat': 0.0, 'carbohydrate': 0.0, 'sugar': 0.0, 'fiber': 0.0, 'sodium': 38.76, 'chloride': 59.66, 'iodine': 0.0002})
Salz.set_category('spices')
Salz.portion(prise, 1)

Pfeffer_schwarz = Food({'calories': 255.0, 'water': 12.0, 'protein': 10.0, 'fat': 3.3, 'carbohydrate': 64.0, 'sugar': 0.6, 'fiber': 25.3, 'sodium': 0.044, 'potassium': 1.33, 'calcium': 0.443, 'magnesium': 0.194, 'phosphorus': 0.158, 'iron': 0.0286, 'zinc': 0.0013, 'manganese': 0.0059, 'copper': 0.001, 'vitamin_c': 0.0, 'vitamin_b3': 0.0011, 'vitamin_b5': 0.0003, 'vitamin_b6': 0.0003, 'vitamin_b9': 0.000017, 'vitamin_a': 0.000027, 'vitamin_e': 0.001, 'vitamin_k': 0.000163})
Pfeffer_schwarz.set_category('spices')
Pfeffer_schwarz.portion(prise, 1)

Zimt = Food({'calories': 247.0, 'water': 10.0, 'protein': 4.0, 'fat': 1.2, 'carbohydrate': 81.0, 'sugar': 2.2, 'fiber': 53.1, 'sodium': 0.01, 'potassium': 0.43, 'calcium': 1.002, 'magnesium': 0.06, 'phosphorus': 0.064, 'iron': 0.0083, 'zinc': 0.0018, 'manganese': 17.47, 'copper': 0.0004, 'vitamin_c': 0.004, 'vitamin_b3': 0.0013, 'vitamin_b6': 0.0002, 'vitamin_b9': 0.000006, 'vitamin_a': 0.000029, 'vitamin_e': 0.0023, 'vitamin_k': 0.000031})
Zimt.set_category('spices')
Zimt.portion(prise, 1)

Basilikum_frisch = Food({'calories': 23.0, 'water': 92.0, 'protein': 3.2, 'fat': 0.6, 'carbohydrate': 2.7, 'sugar': 0.3, 'fiber': 1.8, 'sodium': 0.004, 'potassium': 0.295, 'calcium': 0.177, 'magnesium': 0.064, 'phosphorus': 0.056, 'iron': 0.0032, 'zinc': 0.0008, 'manganese': 0.00115, 'vitamin_c': 0.018, 'vitamin_b3': 0.0009, 'vitamin_b5': 0.0003, 'vitamin_b6': 0.00016, 'vitamin_b9': 0.000068, 'vitamin_a': 0.000528, 'vitamin_e': 0.0008, 'vitamin_k': 0.000415})
Basilikum_frisch.set_category('vegetable')
Basilikum_frisch.portion(prise, 3)

Petersilie_frisch = Food({'calories': 36.0, 'water': 88.0, 'protein': 3.0, 'fat': 0.8, 'carbohydrate': 6.3, 'sugar': 0.9, 'fiber': 3.3, 'sodium': 0.056, 'potassium': 0.554, 'calcium': 0.138, 'magnesium': 0.05, 'phosphorus': 0.058, 'iron': 0.0062, 'zinc': 0.0011, 'manganese': 0.00016, 'copper': 0.00015, 'vitamin_c': 0.133, 'vitamin_b3': 0.0003, 'vitamin_b5': 0.0004, 'vitamin_b6': 0.00009, 'vitamin_b9': 0.000152, 'vitamin_a': 0.000842, 'vitamin_e': 0.00075, 'vitamin_k': 0.00164})
Petersilie_frisch.set_category('vegetable')
Petersilie_frisch.portion(prise, 5)

##########
# Getränke (Alkohol)
##########

Bier_Pils = Food({'calories': 43.0, 'water': 91.0, 'protein': 0.4, 'fat': 0.0, 'carbohydrate': 3.6, 'sugar': 0.1, 'fiber': 0.0, 'sodium': 0.003, 'potassium': 0.05, 'calcium': 0.005, 'magnesium': 0.006, 'phosphorus': 0.014, 'iron': 0.0001, 'zinc': 0.00004, 'vitamin_b3': 0.0004, 'vitamin_b6': 0.00004, 'vitamin_b9': 0.000006, 'alcohol': 4.9})
Bier_Pils.set_category('beer')
Bier_Pils.portion(flasche, 500)

Weissbier = Food({'calories': 44.0, 'water': 90.0, 'protein': 0.5, 'fat': 0.0, 'carbohydrate': 4.0, 'sugar': 0.1, 'fiber': 0.0, 'sodium': 0.003, 'potassium': 0.04, 'calcium': 0.006, 'magnesium': 0.008, 'phosphorus': 0.015, 'iron': 0.0001, 'zinc': 0.00005, 'vitamin_b3': 0.0005, 'vitamin_b6': 0.00005, 'vitamin_b9': 0.000008, 'alcohol': 5.3})
Weissbier.set_category('beer')
Weissbier.portion(flasche, 500)

Rotwein = Food({'calories': 85.0, 'water': 87.0, 'protein': 0.1, 'fat': 0.0, 'carbohydrate': 2.6, 'sugar': 0.6, 'fiber': 0.0, 'sodium': 0.004, 'potassium': 0.12, 'calcium': 0.008, 'magnesium': 0.012, 'phosphorus': 0.02, 'iron': 0.0005, 'zinc': 0.0001, 'manganese': 0.00015, 'vitamin_b3': 0.0001, 'vitamin_b6': 0.00003, 'alcohol': 12.0})
Rotwein.set_category('alcohol')
Rotwein.portion(glas, 125)

Weisswein = Food({'calories': 82.0, 'water': 87.5, 'protein': 0.1, 'fat': 0.0, 'carbohydrate': 2.6, 'sugar': 1.2, 'fiber': 0.0, 'sodium': 0.005, 'potassium': 0.09, 'calcium': 0.009, 'magnesium': 0.01, 'phosphorus': 0.018, 'iron': 0.0003, 'zinc': 0.0001, 'vitamin_b3': 0.0001, 'alcohol': 11.5})
Weisswein.set_category('alcohol')
Weisswein.portion(glas, 125)

##########
# Brot und Brötchen
##########

Weizenbrötchen = Food({'calories': 261.0, 'water': 34.0, 'protein': 8.3, 'fat': 3.2, 'carbohydrate': 48.0, 'sugar': 2.6, 'starch': 43.0, 'fiber': 3.0, 'sodium': 0.47, 'potassium': 0.12, 'calcium': 0.029, 'magnesium': 0.023, 'phosphorus': 0.09, 'iron': 0.001, 'zinc': 0.0007, 'vitamin_b1': 0.00038, 'vitamin_b2': 0.00007, 'vitamin_b3': 0.002, 'vitamin_b6': 0.00005, 'vitamin_b9': 0.000037})
Weizenbrötchen.set_category('bread')
Weizenbrötchen.portion(stück, 60)

Roggenbrötchen = Food({'calories': 249.0, 'water': 36.0, 'protein': 7.5, 'fat': 2.3, 'carbohydrate': 47.0, 'sugar': 3.5, 'starch': 41.0, 'fiber': 5.5, 'sodium': 0.52, 'potassium': 0.18, 'calcium': 0.035, 'magnesium': 0.038, 'phosphorus': 0.1, 'iron': 0.0015, 'zinc': 0.001, 'vitamin_b1': 0.00023, 'vitamin_b2': 0.00009, 'vitamin_b3': 0.0012, 'vitamin_b6': 0.00012})
Roggenbrötchen.set_category('bread')
Roggenbrötchen.portion(stück, 70)

Baguette = Food({'calories': 261.0, 'water': 33.0, 'protein': 8.5, 'fat': 3.2, 'carbohydrate': 48.0, 'sugar': 2.5, 'starch': 43.0, 'fiber': 2.8, 'sodium': 0.58, 'potassium': 0.1, 'calcium': 0.03, 'magnesium': 0.02, 'phosphorus': 0.08, 'iron': 0.001, 'zinc': 0.0006, 'vitamin_b1': 0.0004, 'vitamin_b2': 0.00007, 'vitamin_b3': 0.002, 'vitamin_b6': 0.00005, 'vitamin_b9': 0.000032})
Baguette.set_category('bread')
Baguette.portion(stück, 30)

##########
# Pasta und Teigwaren
##########

Spaghetti_roh = Food({'calories': 357.0, 'water': 10.0, 'protein': 12.0, 'fat': 1.8, 'carbohydrate': 73.0, 'sugar': 2.5, 'starch': 67.0, 'fiber': 3.6, 'sodium': 0.005, 'potassium': 0.2, 'calcium': 0.025, 'magnesium': 0.045, 'phosphorus': 0.15, 'iron': 0.0014, 'zinc': 0.001, 'manganese': 0.54, 'selenium': 0.000026, 'vitamin_b1': 0.00025, 'vitamin_b2': 0.00006, 'vitamin_b3': 0.002, 'vitamin_b6': 0.00015, 'vitamin_b9': 0.000022, 'vitamin_e': 0.0002})
Spaghetti_roh.set_category('pasta')
Spaghetti_roh.portion(packung, 500)
Spaghetti_roh.portion(teller, 100)

Nudeln_Ei_roh = Food({'calories': 384.0, 'water': 9.0, 'protein': 13.0, 'fat': 5.5, 'carbohydrate': 71.0, 'sugar': 1.8, 'starch': 67.0, 'fiber': 3.0, 'sodium': 0.04, 'potassium': 0.15, 'calcium': 0.025, 'magnesium': 0.03, 'phosphorus': 0.16, 'iron': 0.0013, 'zinc': 0.001, 'vitamin_b1': 0.00025, 'vitamin_b2': 0.00012, 'vitamin_b3': 0.0018, 'vitamin_b6': 0.0001, 'vitamin_b9': 0.00004, 'vitamin_e': 0.0006, 'cholesterol': 0.07})
Nudeln_Ei_roh.set_category('pasta')
Nudeln_Ei_roh.portion(packung, 500)
Nudeln_Ei_roh.portion(teller, 100)

##########
# Fertiggerichte
##########

Pizza_Margherita = Food({'calories': 222.0, 'water': 51.0, 'protein': 9.5, 'fat': 7.8, 'carbohydrate': 28.0, 'sugar': 2.5, 'fiber': 2.0, 'sodium': 0.5, 'potassium': 0.18, 'calcium': 0.14, 'magnesium': 0.02, 'phosphorus': 0.16, 'iron': 0.0012, 'zinc': 0.001, 'vitamin_a': 0.00006, 'vitamin_b1': 0.0001, 'vitamin_b2': 0.0001, 'vitamin_b3': 0.001, 'vitamin_b12': 0.0000003, 'cholesterol': 0.015, 'saturated_fat': 3.5})
Pizza_Margherita.set_category('prepared')
Pizza_Margherita.portion(stück, 300)

##########
# Gesamtzahl
##########

# Total: ~100 populäre deutsche Lebensmittel aus der BLS 4.0 Datenbank
# Für die vollständige Datenbank (7.140 Lebensmittel) verwenden Sie:
#   from importers import get_importer
#   bls = get_importer("bls")
