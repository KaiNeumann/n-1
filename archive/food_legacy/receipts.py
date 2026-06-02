from Food import *
from food_naehrwertdaten_ch import *
from food_openfoodfacts_manual import *
from food_yazio_manual import *
from food_other_manual import *


mispelsche = Food().add(
    mispel_frisch * gramm(10),
    calvados * ml(20),
    wasser * ml(10)
)
ofenkartoffeln = Food().add(
    Kartoffel_geschält_roh * gramm(1000),
    Olivenöl * ml(50),
    Paprika_Gewürz * gramm(2),
    Food({'salt':100}) * gramm(1)
)
ofenkartoffeln.portion(stück,50)

chinesische_nudelsuppe = Food().add(
    yum_yum_chicken_flavour * packung
)
chinesische_nudelsuppe_mit_ei = Food().add(
    yum_yum_chicken_flavour * packung,
    egg * eins,
    cholula_hot_sauce * ml(0.05)
)
nutella_toast = Food().add( 
    golden_toast * scheibe, 
    butter * gramm(4),
    rewe_bio_nuss_nougat_creme * gramm(5)
)
gefüllte_grilltomate = Food().add(
    Tomate_roh * gramm(75),
    patros_feta_aus_griechischer_schafsmilch * gramm(50),
    Olivenöl * ml(5),
    Knoblauch_roh * gramm(2)
)
gefüllte_grillpilze = Food().add(
    kulturchampignion_braun * gramm(10),
    rewe_bio_frischkäse * gramm(5),
    haselnusskerne_gehackt * gramm(5)
)