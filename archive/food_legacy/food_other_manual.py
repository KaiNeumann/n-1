from Food import *

wasser = Food({'water':100})
kaffee = Food({'calories': 2,'carbohydrates': 0.3,'protein': 0.2,'water': 99.4})
altenmünster_landbier = Food({'calories': 43,'carbohydrates': 2.9, 'sugar':0.5, 'protein': 0.5, 'fat': 0.5, 'saturated fat': 0.1, 'water': 97, 'alcohol':4.9})
altenmünster_landbier.portion(flasche,500)
schmucker_bio_bier_alkoholfrei = Food({'calories': 12,'carbohydrates': 2.3, 'sugar':0.5, 'protein': 0.5,'water': 97})
schmucker_bio_bier_alkoholfrei.portion(flasche,500)
schmucker_bio_landbier = Food({'carbohydrate': 3.2, 'calories': 42, 'fat': 0, 'fiber': 0, 'protein': 0.5, 'saturated fat': 0, 'sugar': 0.5, 'alcohol': 5 })
schmucker_bio_landbier.portion(flasche,500)

dennree_bio_hartweizen_linguine = Food({'carbohydrate': 62, 'calories': 335, 'fat': 2.1, 'protein': 12.5, 'salt': 0.01, 'saturated fat': 0.4, 'sugar': 3}) #https://www.dennree.de/dennree-produkte/uebersicht/hartweizen-vollkorn/vollkorn-hartweizen-linguine
dennree_bio_hartweizen_linguine.portion(teller,300)
kulturchampignion_braun = Food({'calories': 26, 'fat': 0.3, 'carbohydrates': 2.7, 'sugar':2.3, 'protein': 1.9})
baguette =  Food({'calories': 242.0, 'protein': 7.9, 'carbohydrate': 55.4, 'sugar': 1.0, 'fat': 0.7, 'fiber': 3.2, 'water': 30.0, 'vitamin e': 0.0003, 'vitamin b1': 5.9999999999999995e-05, 'vitamin b2': 5e-05, 'vitamin b6': 8.999999999999999e-05, 'salt': 1.3716, 'iron': 0.0012, 'zinc': 0.0007, 'magnesium': 0.019, 'manganese': 0.0006, 'potassium': 0.13, 'calcium': 0.018, 'phospohorus': 0.105, 'copper': 0.0002, 'iodine': 7e-06}) #https://fddb.info/db/de/lebensmittel/baecker_baguette/index.html
baguettebrötchen = Food({'calories': 305, 'fat': 1.8, 'carbohydrates': 60.2, 'sugar':1.1, 'protein': 9.7, 'fiber':3.5, 'salt':1.7})
bio_hackfleisch = Food({'calories': 243, 'fat': 19, 'saturated_fatty_acids': 6.4, 'carbohydrates': 0, 'sugar':0, 'protein': 18, 'salt':0.1})
bio_hackfleisch.portion(packung,250)
bio_inside_ratatouille_mix = Food({'calories': 26.0, 'protein': 1.3, 'carbohydrate': 3.2, 'fat': 0.4})
bio_inside_ratatouille_mix.portion(packung,400)
bratwurst_mit_senf_und_brötchen = Food({'calories': 250, 'fat': 18.2, 'carbohydrates': 9.2, 'sugar':0.2, 'protein': 12.6, 'fiber':.5, 'water':41, 'salt':.365}) #https://fddb.info/db/de/lebensmittel/imbiss_bratwurst_mit_senf_und_broetchen/index.html 
bratwurst_mit_senf_und_brötchen.portion(eins,197)
calvados = Food({'calories':248,'alcohol':32, 'water':68})
mispel_frisch = Food({'calories': 49, 'fat': 0.2, 'carbohydrates': 10.6, 'sugar': 10.6, 'fiber': 2.1, 'water': 87, 'protein': 0.55, 'iron': 0.5 / 1000, 'zinc': 0.1/1000, 'vitamin_c': 2/1000, 'vitamin_a': 0.01/1000})
hähnchenbrustfilet = Food({'calories':107,'protein':23,'carbohydrate':0.5,'sugar':0,'fat':1.7,'salt':0.13})
honig = Food({"calories": 306.0, "carbohydrates": 76.0, "sugar": 76.0, "protein": 0.4, "water": 20.0, "vitamin_b2": 5e-05, "vitamin_b6": 0.0003, "vitamin_b3": 0.0002, "provitamin_b9": 5.3e-06, "provitamin_b5": 0.0001, "vitamin_c": 0.0017, "potassium": 0.047, "sodium": 0.007, "chloride": 0.018, "calcium": 0.005, "magnesium": 0.003, "phosphorus": 0.017, "iron": 0.0005, "iodine": 5e-07, "zinc": 0.0004})
egg = Food({'protein': 12.56, 'fat': 9.51, 'carbohydrate': 0.72, 'calories': 143.0, 'glucose': 0.37, 'water': 76.15, 'sugar': 0.37, 'calcium': 56.0/1000, 'iron': 1.75/1000, 'magnesium': 12.0/1000, 'phosphorus': 198.0/1000, 'potassium': 138.0/1000, 'sodium': 142.0/1000, 'zinc': 1.29/1000, 'copper': 0.072/1000, 'fluoride': 1.1/1000, 'manganese': 0.028/1000, 'selenium': 30.7/1000000, 'vitamin_a': 160.0/1000000, 'vitamin_e': 1.05/1000, 'vitamin_d': 82.0/1000000, 'vitamin_d3': 2.0/1000000, 'vitamin_b1': 0.04/1000, 'vitamin_b2': 0.457/1000, 'vitamin_b3': 0.075/1000, 'vitamin_b5': 1.533/1000, 'vitamin_b6': 0.17/1000, 'vitamin_b12': 0.89/1000000, 'vitamin_k': 0.3/1000000, 'glutamate': 1.673/1000, 'cholesterol': 372.0/1000000, 'trans_fat': 0.038, 'saturated_fatty_acids': 3.1259999999999994, 'monounsaturated_fatty_acids': 3.658, 'polyunsaturated_fatty_acids': 1.911})
egg.portion(eins,30)
cholula_hot_sauce = Food({'kcal':19,'fat':1,'protein':1,'salt':5,'water':90}) #water estimated. https://www.scovilla.com/de/hot-sauces/111/cholula-hot-sauce-mexico-148ml
creme_fraiche = Food({'calories':294,'protein':2.4,'carbohydrate':3,'sugar':3,'fat':30})
tabasco_habanero = Food({'kcal':121,'carbohydrate':21,'sugar':21,'protein':1.5,'salt':6.1}) #https://shop.rewe.de/p/tabasco-habanero-60ml/2235797?source=mc
landprimus_pfefferbeisser = Food({'calories': 300,'fat': 25,'saturated_fatty_acids': 10,'carbohydrates': 0.5,'sugar': 0.5, 'protein': 19,'salt': 2.1}) #https://www.tegut.com/angebote-produkte/produkte/eigenmarken/produkt/pfefferbeisser.html
landprimus_pfefferbeisser.portion(packung,250)
landprimus_pfefferbeisser.portion(stück,50)
ökostern_bio_dijon_senf = Food({'calories': 220,'fat': 13.3,'saturated_fatty_acids': 0.4,'carbohydrates': 8.9,'sugar': 1, 'protein': 14.6,'salt': 7.1})
walnüsse =  Food({'calories': 687,'fat': 63.8,'carbohydrates': 10.5,'sugar': 3.4, 'protein': 14.5,'fiber': 6.4})
schnitzel = Food({'protein': 21.554650945161892, 'fat': 14.683932247800861, 'carbohydrate': 6.947454613513007, 'calories': 251.54739846528165, 'starch': 5.652863559797867, 'glucose': 0.21588994946659182, 'fructose': 0.23324911098633727, 'maltose': 0.18192026951151036, 'water': 55.278167696050915, 'sugar': 0.6311529103499905, 'fiber': 0.443383866741531, 'calcium': 41.904314055773916, 'iron': 1.2514037057832679, 'magnesium': 23.96195957327344, 'potassium': 288.34386112670785, 'sodium': 264.29150290099193, 'zinc': 1.8615010293842411, 'copper': 0.09086655437020401, 'manganese': 0.10588620625116975, 'selenium': 38.01179112857945, 'vitamin a': 20.18552311435523, 'beta carotene': 0.20849709900804791, 'alpha carotene': 0.008094703350177803, 'vitamin e': 0.667087778401647, 'vitamin d': 31.63054463784391, 'vitamin d3': 0.8216357851394348, 'vitamin b1': 0.5364027699794124, 'vitamin b2': 0.26366273629047354, 'vitamin b3': 6.623011416807038, 'vitamin b5': 0.7159367396593673, 'vitamin b6': 0.5230207748455923, 'vitamin b12': 0.5706999812839229, 'vitamin k': 10.536496350364963, 'vitamin b9': 7.769605090772974, 'glutamate': 3.5911472955268575, 'cholesterol': 105.22300205876847, 'trans fat': 0.21041549691184727, 'saturated fat': 3.432107430282613, 'monounsaturated fat': 4.748783454987835, 'polyunsaturated fat': 4.637048474639715})
zigeuner_schnitzel = Food({'carbohydrate': 16.2, 'calories': 165, 'fat': 2.2, 'fiber': 4.1, 'protein': 18, 'salt': 1.5, 'saturated fat': 0.3, 'sodium': 0.6, 'sugar': 1.3})
haselnusskerne_gehackt = Food({'carbohydrate': 5.4, 'calories': 695, 'sugar':5.4, 'fat': 67, 'fiber': 8.2, 'protein': 15})
leicht_und_cross_goldweizen = Food({'carbohydrate': 73, 'calories': 391, 'fat': 4, 'fiber': 5.4, 'protein': 13, 'saturated fat': 0.5, 'salt': 1.2, 'sugar': 3.5})
leicht_und_cross_goldweizen.portion(scheibe,125/17)
palatum_grüne_oliven_mit_frischkäse_creme = Food({'carbohydrate': 4, 'calories': 217, 'fat': 19.4, 'fiber': 1.9, 'protein': 4.6, 'saturated fat': 5.2, 'salt': 2.1, 'sugar': 0.4})
palatum_grüne_oliven_mit_frischkäse_creme.portion(packung,80)
palatum_grüne_oliven_mit_frischkäse_creme.portion(eins,80/7)
palatum_naturschwarze_kalamata_oliven = Food({'carbohydrate': 1.1, 'calories': 224, 'fat': 22.5, 'fiber': 6.4, 'protein': 1.1, 'salt': 1.94, 'saturated fat': 2.5, 'sodium': 0.776, 'sugar': 0.1})
palatum_naturschwarze_kalamata_oliven.portion(packung,80)
palatum_naturschwarze_kalamata_oliven.portion(eins,80/20)
rettich = Food({'carbohydrate': 2, 'calories': 14, 'fat': 0, 'fiber': 1.9, 'protein': 1, 'vitamin c':27/1000, 'vitamin k':50/1000000, 'iron':800/1000000})
spaghetti_bolognese = Food({'calories':166,'protein':7,'carbohydrate':10,'sugar':1,'fat':9,'fiber':1,'cholesterol':32/1000,'water':68}) #https://fddb.info/db/de/lebensmittel/cuisine_spaghetti_alla_bolognese/index.html
spinat_dinkel_pfannkuchen = Food({'calories':123,'protein':12.5,'carbohydrate':12.7,'fat':2.4,'fiber':0})
hackfleisch = Food({'carbohydrate': 0.1, 'calories': 234, 'fat': 18, 'fiber': 0, 'protein': 18, 'cholesterol':63/1000, 'water':63, 'vitamin a':0.01/1000, 'vitamin e':.42/1000, 'vitamin b1':.32/1000, 'vitamin b2':.21/1000, 'vitamin b6':.29/1000, 'vitamin b12':3/1000000, 'salt':.1676, 'iron':1.7/1000, 'zinc':3.8/1000, 'magnesium':23/1000, 'chloride':59/1000, 'sulfate':.182, 'potassium':.346, 'calcium':6/1000, 'phosphorous':.178,'copper':0.1/1000, 'fluoride':.01/1000, 'iodine':5/1000000})

omni_biotic_10 = Food({'kcal':371,'fat':0.1,'unsaturated fat':0.02,'carbohydrate':90.4,'sugar':3.78,'proteine':2.2,'salt':0.66})
omni_biotic_10.portion(beutel,5)
bion3_energy = Food({'thiamin':3.3/1000*30*100/35.6,'riboflavin':4.2/1000*30*100/35.6,'niacin':20/1000*30*100/35.6,'pantothenic acid':15/1000*30*100/35.6,'vitamin b6':2/1000*30*100/35.6,'biotin':150/1000000*30*100/35.6,'folic acid':200/1000000*30*100/35.6,'vitamin b12':2.5/1000000*30*100/35.6,'vitamin c':180/1000*30*100/35.6,'vitamin d':5/1000000*30*100/35.6,'magnesium':57/1000*30*100/35.6,'iron':4.3/1000*30*100/35.6,'zinc':5/1000*30*100/35.6,'iodine':100/1000000*30*100/35.6}) #pro Tablette  30 Tabletten = 35.6g => 35.6/30 g    => 30*100/35.6 = Nährstoffe pro 100g
bion3_energy.portion(tablette,1)
buer_lecithin = Food({'calories':10, 'fat':1, 'protein':1, 'water': 20*5,'vitamin_b2': 0.755 / 1000*5,'vitamin_b3': 5 / 1000*5,'vitamin_b5': 3.683 / 1000*5,'vitamin_b6': 0.579 / 1000*5,'vitamin_b12': 0.5 / 1000000*5,'alcohol': 16.4 / 100, 'sugar':5/60*100})
buer_lecithin.portion(becher,20)
zinc = Food({'zinc':25/1000},1)

cheeseburger = Food({'kcal':261,'fat':11,'carbohydrate':27,'sugar':4.3,'proteine':12})
börek_mit_käse = Food({'kcal':300,'fat':13,'carbohydrate':39,'proteine':0})