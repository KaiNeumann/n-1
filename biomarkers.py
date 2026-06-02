"""
Biomarkes DB built with the help of CSV files, the internet and Chat GPT

I used ChatGPT4 with Bing search and the following prompt:


I want to set up a dataset for biomarkers in python. Please help me completing this dataset for biomarkers for which I will provide you soon some already collected data. This collected data comes in two different formats:
1) Values from a test result csv that looks like this:
Wert,Laborident,Einheit,Normalwert
Albumin,ALBELK,%,55.8 - 66.1,,,,,67.4,64.8,,64.7
Albumin abs.,ALBEAK,g/l,35.2 - 50.4,,,,,,40.9,,45.0
Alkalische Phosphatase,A-AP,U/l,38.0 - 126,,,,,55,58,,68.0

2) Basic information on biomarkers in this format:
Test,Normal Range (Low),Normal Range (High),Ideal Range (Low),Ideal Range (High),Unit,Abreviation,Age Variance,Category,Wikipedia,Short Description,AwesomeList,Notes,Source1,Source1-URL,Source2,Source2-URL
Alkaline Phosphatase (ALP),20.0,125.0,,,,ALP,,Blood Chemistry,https://en.wikipedia.org/wiki/Alkaline_phosphatase,"An enzyme found in the liver, bone, kidneys, small intestine, and placenta. May be increased due to liver obstruction, cirrhosis, gastrointestinal issues, hyperphosphatemia, hyperparathyroidism. May be decreased due to nutrient deficiencies (zinc, magnesium, and/or Vit C).",Y,,,,,
Alanine amino transferase (ALT or SGPT),5.0,40.0,,,,,,Blood Chemistry,https://en.wikipedia.org/wiki/Alanine_transaminase,"An enzyme found in highest concentrations in the liver but also in smaller amounts in heart, muscle and kidney. May be elevated due to hepatocellular disease, biliary issues, pancreatitis.",Y,,,,,
Uric Acid,2.6,6.0,,,,,,Blood Chemistry,https://en.wikipedia.org/wiki/Uric_acid#Clinical_significance_and_research,"End product of DNA purine base metabolism and excretion in the kidneys; may indicate oxidative stress and elevated levels are associated with cardiovascular disease and diabetes. May be elevated due to gout, kidney dysfunction, excess alcohol intake, starvation, extreme calorie restriction, liver dysfunction, hemolytic anemia, excess fructose consumption, fungal infection, ketogenic diet, supplemental niacin, high protein diet, prolonged fasting, supplemental vitamin B3, excess acidity. May be decreased due to nutrient deficiencies (molybdenum, zinc, iron), oxidative stress, low purine intake (vegetarian or vegan), excess alkalinity.",Y,,,,,


This is an example of target structure for a biomarkers (with some values missing for brevity):

{
    "name": "Albumin",
    "synonyms":["ALBELK"],
    "catgeory": ["protein marker"],
    "range": {
        "%": [
            {
                "label": "normal",
                "min": 55.8,
                "max": 66.1,
                remark: []
            }
        ],
        "U/l": [
            { 
                "label": "normal",
                "min": 35.2,
                "max": 50.4,
                "remark": []
            }
        ]
    },
    "optimum": "range",
    "description": [
        Quote("Albumin ist ein Protein, das zur Gruppe der Plasmaproteine gehört. Menschliches Albumin nennt man Humanalbumin.", "https://flexikon.doccheck.com/de/Albumin"),
        Quote("The most abundant plasma protein in serum, synthesized in the liver, binds to other compounds in the blood and contributes to the plasma osmotic gradient.", "https://github.com/markwk/awesome-biomarkers")
    ],
    "interpretation": {
        "low": [
            Quote("May be decreased due to infection, inflammation, liver disease, kidney disease.", "https://github.com/markwk/awesome-biomarkers"),
            Quote("Zu kompensatorisch verminderten Werten kommt es bei signifikanten Immunglobulinvermehrungen , z.B. bei Infektionen, Tumoren oder Plasmozytom.", "https://flexikon.doccheck.com/de/Albumin")
        ],
        "high": [
            Quote("May be elevated due to dehydration.","https://en.wikipedia.org/wiki/Human_serum_albumin")
        ]
    },
    "organs": ["liver","kidney"],
    "diet": [
        Quote("A diet that includes an adequate intake of high-quality proteins, such as lean meats, poultry, fish, dairy products, legumes, and eggs, can support liver function and overall protein synthesis in the body","ChatGPT4 as of 2023-06-09")
    ]
}

Always keep this dict structure in your answer!

Here are some explanations about the structure:
- Make sure that both english and german names of the biomarker are present. As a rule, keep the english name as the "name" and put the german translation into the list of synonyms
- The synonyms value can be useful to collect english and german synonyms, abbreviations and the "Laborindent" value. 
- Quote(text,source) is a python class, that combines two strings, a text and a source. This source can be a url, a reference to the example csv or even "ChatGPT4 as of {date}". Please use Quote() whenever there is a longer text in a value. Keep the texts precise and short.
- "categories" is strictly one of "blood chemistry","blood count","bone health","coagulation","hormones","immunity","iron markers","lipids","protein markers","stress / inflammation","vitamins & minerals","misc"
- "optimum" should be "range" if staying in the value range is recommended. It should be "low" if the lower the better, and "high" vice versa
- if there is no dietary impact on the biomarker known, you can keep that value to the empty list []
- The range is a dict with units as key, in case I find different reference ranges for different units. It should group absolute values as well as percentages, and if risk levels are known, the following would be valid:
    "range": {
        "mg/L": [
            {
                "category": "low risk",
                "min": 0,
                "max": 1.0,
                "remark": [
                    Quote("CRP level less than 1.0 mg/L indicates low risk.", "source_url")
                ]
            },
            {
                "category": "intermediate risk",
                "min": 1.0,
                "max": 2.9,
                "remark": [
                    Quote("CRP level between 1.0 to 2.9 mg/L indicates intermediate risk.", "source_url")
                ]
            },
            {
                "category": "critical",
                "min": 2.9,
                "max": None,
                "remark": [
                    Quote("CRP level greater than 2.9 mg/L is critical.", "source_url")
                ]
            }
        ]
    }


You are free to complete the data according to your knowledge, but please keep web searches limited to wikipedia and pages from DocCheck such as https://flexikon.doccheck.com/de/Amylase.
Don't provide a verbose answer, but concentrate on the output of the data structure of the biomarker. Keep it to the facts only and stick to the given structure.

Please acknowledge that you understood the upcomming task.

"""


class Quote:
    def __init__(str,source=""):
        self.str = str
        self.source = source
    def __str__(self):
        return self.str



Biomarkers = [
{
    "name": "Alpha-Amylase",
    "synonyms": ["a-Amylase", "α-Amylase", "A-AMYS"],
    "category": ["Blood Chemistry"],
    "range": {
        "U/l": [
            {
                "label": "normal",
                "min": 28.0,
                "max": 100.0,
                "remark": []
            }
        ]
    },
    "optimum": "range",
    "description": [
        Quote("Amylasen sind Enzyme, die alpha-1,4-glykosidische Bindungen der Stärke in Oligosaccharid- bzw. Disaccharid-Einheiten aufspalten können.", "https://flexikon.doccheck.com/de/Amylase"),
        Quote("Amylasen werden unter anderem in der Bauchspeicheldrüse (Pankreasamylase) und in den Speicheldrüsen der Mundhöhle (Speicheldrüsenamylase) produziert.", "https://flexikon.doccheck.com/de/Amylase")
    ],
    "interpretation": {
        "low": [
            Quote("Specific conditions leading to low Alpha-Amylase levels are not mentioned in the sources.", "ChatGPT4 as of 2023-06-09")
        ],
        "high": [
            Quote("Sind die Werte über die Norm erhöht, können folgende Krankheitsbilder ursächlich sein: akute Pankreatitis, Schub einer chronischen Pankreatitis, akute Ethanolintoxikation (in ca. 10% der Fälle), Zustand nach ERCP (2-3 Tage), Parotitis, Niereninsuffizienz, gastrointestinale Komplikationen, z.B. Perforation, Mesenterialinfarkt, akutes Abdomen (meist bei Pankreasbeteiligung), maligne Tumoren, auch paraneoplastisch, Virushepatitis, Herzinfarkt, Sarkoidose, Typhus abdominalis.", "https://flexikon.doccheck.com/de/Amylase")
        ]
    },
    "organs": ["pancreas", "salivary glands"],
    "diet": []
},
{
    "name": "Albumin",
    "synonyms": ["Albumin abs.", "ALB", "ALBELK"],
    "category": ["Protein Markers"],
    "range": {
        "%": [
            {
                "label": "normal",
                "min": 55.8,
                "max": 66.1,
                "remark": []
            }
        ],
        "g/l": [
            { 
                "label": "normal",
                "min": 35.2,
                "max": 50.4,
                "remark": []
            }
        ]
    },
    "optimum": "range",
    "description": [
        Quote("Albumin ist ein Protein, das zur Gruppe der Plasmaproteine gehört. Menschliches Albumin nennt man Humanalbumin.", "https://flexikon.doccheck.com/de/Albumin"),
        Quote("The most abundant plasma protein in serum, synthesized in the liver, binds to other compounds in the blood and contributes to the plasma osmotic gradient.", "https://en.wikipedia.org/wiki/Human_serum_albumin")
    ],
    "interpretation": {
        "low": [
            Quote("May be decreased due to infection, inflammation, liver disease, kidney disease.", "https://en.wikipedia.org/wiki/Human_serum_albumin"),
            Quote("Zu kompensatorisch verminderten Werten kommt es bei signifikanten Immunglobulinvermehrungen , z.B. bei Infektionen, Tumoren oder Plasmozytom.", "https://flexikon.doccheck.com/de/Albumin")
        ],
        "high": [
            Quote("May be elevated due to dehydration.","https://en.wikipedia.org/wiki/Human_serum_albumin")
        ]
    },
    "organs": ["liver","kidney"],
    "diet": [
        Quote("A diet that includes an adequate intake of high-quality proteins, such as lean meats, poultry, fish, dairy products, legumes, and eggs, can support liver function and overall protein synthesis in the body","ChatGPT4 as of 2023-06-09")
    ]
},
{
    "name": "Alkaline Phosphatase",
    "synonyms": ["Alkalische Phosphatase", "ALP", "A-AP"],
    "category": ["Blood Chemistry"],
    "range": {
        "U/l": [
            {
                "label": "normal",
                "min": 38.0,
                "max": 126.0,
                "remark": []
            }
        ]
    },
    "optimum": "range",
    "description": [
        Quote("Die Alkalischen Phosphatasen, kurz AP oder ALP, sind eine Gruppe von Enzymen, welche die Fähigkeit zur Spaltung von Phosphorsäuremonoestern haben. Die Bestimmung der alkalischen Phosphatase dient als Indikator für Erkrankungen der Leber und der Gallenwege sowie für Veränderungen des Knochenstoffwechsels.", "https://flexikon.doccheck.com/de/Alkalische_Phosphatase"),
        Quote("An enzyme found in the liver, bone, kidneys, small intestine, and placenta. May be increased due to liver obstruction, cirrhosis, gastrointestinal issues, hyperphosphatemia, hyperparathyroidism. May be decreased due to nutrient deficiencies (zinc, magnesium, and/or Vit C).", "https://en.wikipedia.org/wiki/Alkaline_phosphatase")
    ],
    "interpretation": {
        "low": [
            Quote("May be decreased due to nutrient deficiencies (zinc, magnesium, and/or Vit C).", "https://en.wikipedia.org/wiki/Alkaline_phosphatase"),
            Quote("Erniedrigte Werte: Hormonersatztherapie mit Östrogenen, Hypothyreose, Achondroplasie, Kinder mit schwerer Gastroenteritis, Morbus Wilson, Anämie, perniziöse Anämie, aplastische Anämie, CML, Zinkmangel, Hypophosphatasie (Rathbun-Syndrom).", "https://flexikon.doccheck.com/de/Alkalische_Phosphatase")
        ],
        "high": [
            Quote("May be increased due to liver obstruction, cirrhosis, gastrointestinal issues, hyperphosphatemia, hyperparathyroidism.", "https://en.wikipedia.org/wiki/Alkaline_phosphatase"),
            Quote("Erhöhte Werte: Erkrankungen mit hohem Knochenumsatz, Morbus Paget, Skelettmetastasen, Knochentumoren, Rachitis, Osteoporose, Osteomalazie, Erkrankungen von Leber und Gallenwegen, Cholestase, Lebermetastasen, Virushepatitis, Leberzirrhose, Endokrine Erkrankungen, Hyperparathyreoidismus, Hyperthyreose, Akromegalie, Cushing-Syndrom, Sonstige, Sarkoidose, Niereninsuffizienz, Multiples Myelom, Myokardinfarkt, Mononukleose.", "https://flexikon.doccheck.com/de/Alkalische_Phosphatase")
        ]
    },
    "organs": ["liver", "bone", "kidneys", "small intestine", "placenta"],
    "diet": [
        Quote("Dietary deficiencies in zinc, magnesium, and/or Vitamin C may lead to decreased levels of Alkaline Phosphatase.", "ChatGPT4 as of 2023-06-09")
    ]
},
{
    "name": "Alpha-1-Globulin",
    "synonyms": ["A1K", "A1AK"],
    "category": ["Protein Markers"],
    "range": {
        "%": [
            {
                "label": "normal",
                "min": 2.90,
                "max": 4.90,
                "remark": []
            }
        ],
        "g/l": [
            { 
                "label": "normal",
                "min": 1.30,
                "max": 3.90,
                "remark": []
            }
        ]
    },
    "optimum": "range",
    "description": [
        Quote("Alpha-1-Globuline sind ein Proteingemisch, das neben Albumin, Alpha-2-Globulinen, Beta-Globulinen und Gamma-Globulinen im Blutplasma vorkommt. Die Bezeichnung stammt aus der Serumelektrophorese, in der diese Proteine in der Alpha-1-Fraktion liegen.", "https://flexikon.doccheck.com/de/Alpha-1-Globulin")
    ],
    "interpretation": {
        "low": [
            Quote("Wichtig ist, bei einer Verminderung der Alpha-1-Globuline an einen möglichen erblichen Alpha-1-Antitrypsinmangel zu denken. Bei dieser nicht so seltenen Erbkrankheit kommt es zu Schädigung der Leber (Leberzirrhose) und der Lunge (Lungenüberblähung). Verminderungen kommen ferner bei Leberentzündungen, anderen akuten Leberschäden und bei Eiweißverlust (z.B. über die Nieren) vor.", "https://flexikon.doccheck.com/de/Alpha-1-Globulin")
        ],
        "high": [
            Quote("Zu den Alpha-1-Globulinen gehören die so genannten Akutphasenproteine, also Proteine, die in der akuten Phase einer Entzündung erhöht sind. Zu einer Erhöhung der alpha-1-Globuline kann es daher bei akuten Entzündungen verschiedener Ursache kommen, z.B. bei Akuten Infektionen (Beispiele Lungenentzündung, Wundrose), 'Rheumatischen' Erkrankungen bzw. Autoimmunerkrankungen, Entzündlichen Darmerkrankungen (Morbus Crohn, Colitis ulcerosa), Gewebsverletzungen (Traumata, Operationen), Gewebenekrosen (z.B. bei Myokardinfarkt, Pankreatitis), Tumoren.", "https://flexikon.doccheck.com/de/Alpha-1-Globulin")
        ]
    },
    "organs": ["liver", "lungs"],
    "diet": []
},
{
    "name": "Alpha-2-Globulin",
    "synonyms": ["A2K", "A2AK", "α-2-Globulin", "α2-Globulin"],
    "category": ["Protein Markers"],
    "range": {
        "%": [
            {
                "label": "normal",
                "min": 7.10,
                "max": 11.8,
                "remark": []
            }
        ],
        "g/l": [
            { 
                "label": "normal",
                "min": 5.40,
                "max": 9.30,
                "remark": []
            }
        ]
    },
    "optimum": "range",
    "description": [
        Quote("Als Alpha-2-Globuline werden Proteine bezeichnet, die bei der Serumeiweißelektrophorese in der Alpha-2-Fraktion dargestellt werden. Die Alpha-2-Fraktion ist bei Entzündungsreaktionen erhöht, aber nicht alle Alpha-2-Globuline sind Akute-Phase-Proteine.", "https://flexikon.doccheck.com/de/Alpha-2-Globulin")
    ],
    "interpretation": {
        "low": [
            Quote("Erniedrigte Werte findet man, z.B. bei Chronisch aktiver Hepatitis, Hämolysen, Haptoglobinmangel, Morbus Wilson, Leberschäden.", "https://flexikon.doccheck.com/de/Alpha-2-Globulin")
        ],
        "high": [
            Quote("Erhöhte Werte finden sich in der Akutphase einer Entzündung verschiedener Ursache, z.B. Gewebenekrosen, Akuten Infektionen, Autoimmunerkrankungen, Entzündlichen Darmerkrankungen (Colitis ulcerosa, Morbus Crohn), Tumoren. Beim Nephrotischen Syndrom sind die Alpha-2-Globuline charakteristischerweise erhöht, da es sich überwiegend um sehr große Proteine handelt, deren Verlust über die Niere relativ gering ist. Zudem werden sie reaktiv verstärkt synthetisiert.", "https://flexikon.doccheck.com/de/Alpha-2-Globulin")
        ]
    },
    "organs": ["liver", "kidneys"],
    "diet": []
},
{
    "name": "Antistreptolysin",
    "synonyms": [],
    "category": ["immunity"],
    "range": {
        "IU/ml": [
            {
                "label": "normal",
                "min": None,
                "max": 200,
                "remark": []
            }
        ]
    },
    "optimum": "range",
    "description": [],
    "interpretation": {
        "low": [],
        "high": []
    },
    "organs": [],
    "diet": []
},
{
    "name": "Basophils",
    "synonyms": ["Basophile", "Basophile abs.", "BASO", "BASOAB"],
    "category": ["immunity"],
    "range": {
        "%": [
            {
                "label": "normal",
                "min": 0.00,
                "max": 1.75,
                "remark": []
            },
            {
                "label": "normal",
                "min": 0.00,
                "max": 2.00,
                "remark": []
            }
        ],
        "10^9/l": [
            {
                "label": "normal",
                "min": 0.00,
                "max": 0.20,
                "remark": []
            }
        ]
    },
    "optimum": "range",
    "description": [
        Quote("Basophils are a type of white blood cell. They are part of the immune system and play a role in its functioning.", "ChatGPT4 as of 2023-06-09")
    ],
    "interpretation": {
        "low": [],
        "high": [
            Quote("May be elevated due to inflammation, allergies, hemolytic anemia, hypothyroidism.", "https://en.wikipedia.org/wiki/Basophil"),
            Quote("May be elevated due to hemochromatosis and other genetic conditions, inflammation, liver damage, hemolytic or sideroblastic anemia.")
        ]
    },
    "organs": ["blood", "liver"],
    "diet": []
},
{
    "name": "Beta Globulin",
    "synonyms": ["β-Globuline", "siderophilin", "transferrin"],
    "category": ["protein markers"],
    "range": {
        "%": [
            {
                "label": "normal",
                "min": 7.9,
                "max": 13.9,
                "remark": []
            }
        ]
    },
    "optimum": "range",
    "description": [
        Quote("Beta Globulins are a group of globular proteins that occur in blood plasma. They are formed in the liver.", "https://flexikon.doccheck.com/de/Beta-Globulin"),
        Quote("A globulin in blood plasma that carries iron", "https://www.wolframalpha.com/input?i=Beta+Globulin")
    ],
    "interpretation": {
        "low": [],
        "high": []
    },
    "organs": ["liver"],
    "diet": []
},
{
    "name": "Beta-1-Globulin",
    "synonyms": ["ß-1-Globulin", "BETA1K", "BET1AK"],
    "category": ["protein markers"],
    "range": {
        "%": [
            {
                "label": "normal",
                "min": 4.70,
                "max": 7.20,
                "remark": []
            }
        ],
        "g/l": [
            {
                "label": "normal",
                "min": 3.4,
                "max": 5.2,
                "remark": []
            }
        ]
    },
    "optimum": "range",
    "description": [],
    "interpretation": {
        "low": [],
        "high": []
    },
    "organs": [],
    "diet": []
},
{
    "name": "Beta-2-Globulin",
    "synonyms": ["ß-2-Globulin", "BETA2K", "BET2AK"],
    "category": ["protein markers"],
    "range": {
        "%": [
            {
                "label": "normal",
                "min": 3.20,
                "max": 6.50,
                "remark": []
            }
        ],
        "g/l": [
            {
                "label": "normal",
                "min": 2.3,
                "max": 4.7,
                "remark": []
            }
        ]
    },
    "optimum": "range",
    "description": [],
    "interpretation": {
        "low": [],
        "high": []
    },
    "organs": [],
    "diet": []
},
{
    "name": "Direct Bilirubin",
    "synonyms": ["Bilirubin direkt", "A-BILD"],
    "category": ["blood chemistry"],
    "range": {
        "mg/dl": [
            {
                "label": "normal",
                "min": 0,
                "max": 0.20,
                "remark": []
            },
            {
                "label": "normal",
                "min": 0,
                "max": 0.4,
                "remark": []
            }
        ]
    },
    "optimum": "range",
    "description": [
        Quote("Bilirubin is a breakdown product of hemoglobin and has a yellow-brown color. In serum, it is present as albumin-bound primary bilirubin.", "https://flexikon.doccheck.com/de/Bilirubin"),
        Quote("Bilirubin is a yellow compound that occurs in the normal catabolic pathway that breaks down heme in vertebrates.", "https://www.wolframalpha.com/input?i=Bilirubin")
    ],
    "interpretation": {
        "low": [],
        "high": [
            Quote("Increased serum concentration indicates enhanced hemolysis. Increased values can also occur in vitamin B12 deficiency.", "https://flexikon.doccheck.com/de/Bilirubin")
        ]
    },
    "organs": ["liver"],
    "diet": []
},
{
    "name": "Indirect Bilirubin",
    "synonyms": ["Bilirubin indirekt", "BILI", "Unkonjugiertes Bilirubin"],
    "category": ["blood chemistry"],
    "range": {
        "mg/dl": [
            {
                "label": "normal",
                "min": 0,
                "max": 0.80,
                "remark": []
            },
            {
                "label": "normal",
                "min": 0,
                "max": 1.1,
                "remark": []
            }
        ]
    },
    "optimum": "range",
    "description": [
        Quote("Indirect Bilirubin is the non-water soluble form of bilirubin that is transported in the serum bound to albumin. In the liver, it is converted into the water-soluble direct (conjugated) bilirubin by conjugation with glucuronic acid.", "https://flexikon.doccheck.com/de/Indirektes_Bilirubin")
    ],
    "interpretation": {
        "low": [],
        "high": [
            Quote("Indirect bilirubin is particularly increased in the context of prehepatic jaundice.", "https://flexikon.doccheck.com/de/Indirektes_Bilirubin")
        ]
    },
    "organs": ["liver"],
    "diet": []
},
{
    "name": "C-Reactive Protein",
    "synonyms": ["C-reaktives Protein", "C-reaktives Protein (hs)"],
    "category": ["stress / inflammation"],
    "range": {
        "mg/L": [
            {
                "label": "low risk",
                "min": 0.0,
                "max": 1.0,
                "remark": [
                    Quote("CRP level less than 1.0 mg/L indicates low risk.", "https://healthmatters.io/understand-blood-test-results/crp")
                ]
            },
            {
                "label": "intermediate risk",
                "min": 1.0,
                "max": 2.9,
                "remark": [
                    Quote("CRP level between 1.0 to 2.9 mg/L indicates intermediate risk.", "https://healthmatters.io/understand-blood-test-results/crp")
                ]
            },
            {
                "label": "critical",
                "min": 2.9,
                "max": None,
                "remark": [
                    Quote("CRP level greater than 2.9 mg/L is critical.", "https://healthmatters.io/understand-blood-test-results/crp")
                ]
            }
        ]
    },
    "optimum": "low",
    "description": [
        Quote("C-Reactive Protein (CRP) is a protein made by the liver. It is sent into the bloodstream in response to inflammation.", "https://en.wikipedia.org/wiki/C-reactive_protein"),
        Quote("C-reaktives Protein ist ein Akute-Phase-Protein der Leber und steigt bei Entzündungen, Infektionen und Gewebeschäden an.", "https://flexikon.doccheck.com/de/C-reaktives_Protein")
    ],
    "interpretation": {
        "low": [
            Quote("Low levels of CRP in the bloodstream are normally expected.", "ChatGPT4 as of 2023-06-09")
        ],
        "high": [
            Quote("High levels of CRP can be a sign of a serious infection or other disorder.", "https://en.wikipedia.org/wiki/C-reactive_protein"),
            Quote("Erhöhte Werte weisen auf eine Entzündung im Körper hin.", "https://flexikon.doccheck.com/de/C-reaktives_Protein")
        ]
    },
    "organs": ["liver"],
    "diet": []
},
{
    "name": "Calcium",
    "synonyms": ["A-CA"],
    "category": ["blood chemistry"],
    "range": {
        "mmol/l": [
            {
                "label": "normal",
                "min": 2.20,
                "max": 2.65,
                "remark": []
            }
        ]
    },
    "optimum": "range",
    "description": [
        Quote("Calcium is a mineral that is necessary for life. In addition to building bones and keeping them healthy, calcium enables our blood to clot, our muscles to contract, and our heart to beat.", "https://www.hsph.harvard.edu/nutritionsource/calcium/"),
        Quote("Calcium ist ein Mineralstoff, der im Körper für verschiedene Funktionen benötigt wird. Es spielt eine wichtige Rolle beim Aufbau und Erhalt von Knochen und Zähnen, ist aber auch für Muskelkontraktionen, Blutgerinnung und den Stoffwechsel von Hormonen und Enzymen wichtig.", "https://flexikon.doccheck.com/de/Calcium")
    ],
    "interpretation": {
        "low": [
            Quote("Low levels of calcium in the blood can indicate various health conditions, such as hypoparathyroidism, kidney disease, or vitamin D deficiency.", "https://www.mayoclinic.org/symptoms/hypercalcemia/basics/causes/sym-20050866")
        ],
        "high": [
            Quote("High levels of calcium in the blood can be caused by conditions such as hyperparathyroidism, certain cancers, or excessive intake of calcium or vitamin D supplements.", "https://www.mayoclinic.org/symptoms/hypercalcemia/basics/causes/sym-20050866")
        ]
    },
    "organs": ["bones"],
    "diet": [
        Quote("Calcium-rich foods include dairy products, leafy green vegetables (such as broccoli and spinach), tofu, almonds, and fortified plant-based milk alternatives.", "ChatGPT4 as of 2023-06-09")
    ]
},
{
    "name": "Carcinoembryonic Antigen",
    "synonyms": ["Carcinoembryonales Antigen","CEA"],
    "category": ["protein markers"],
    "range": {
        "ng/ml": [
            {
                "label": "normal",
                "min": 0,
                "max": 5,
                "remark": [
                    Quote("CEA levels below 5 ng/ml are considered normal.", "Example CSV provided")
                ]
            },
            {
                "label": "elevated",
                "min": 5,
                "max": 10,
                "remark": [
                    Quote("CEA levels between 5 and 10 ng/ml may indicate certain conditions. Further evaluation is recommended.", "Example CSV provided")
                ]
            },
            {
                "label": "critical",
                "min": 20,
                "max": None,
                "remark": [
                    Quote("Werte über 20 µg/L sind hochgradig verdächtig auf einen zugrundeliegenden malignen Progress. Hochpathologische Werte sind insbesondere bei großer Tumormasse oder Metastasierung zu erwarten.", "https://flexikon.doccheck.com/de/Carcinoembryonales_Antigen")
                ]
            }
        ]
    },
    "optimum": "low",
    "description": [
        Quote("Carcinoembryonic Antigen (CEA) is a protein that is normally produced during fetal development. In adults, elevated levels of CEA may be associated with certain types of cancer, particularly colorectal cancer.", "https://www.cancer.org/cancer/tumor-markers/tumor-marker-facts/cea.html"),
        Quote("Das Carcinoembryonale Antigen (CEA) ist ein Tumormarker, der bei bestimmten Tumorarten erhöht sein kann, insbesondere bei Dickdarmkrebs.", "https://flexikon.doccheck.com/de/Carcinoembryonales_Antigen")
    ],
    "interpretation": {
        "low": [
            Quote("Low levels of CEA in the blood are typically considered normal in adults.", "https://www.cancer.org/cancer/tumor-markers/tumor-marker-facts/cea.html")
        ],
        "high": [
            Quote("Elevated levels of CEA may indicate the presence of certain types of cancer, particularly colorectal cancer. However, CEA levels can also be elevated in non-cancerous conditions, such as inflammation or certain lung diseases.", "https://www.cancer.org/cancer/tumor-markers/tumor-marker-facts/cea.html"),
            Quote("Erhöhte CEA-Werte können auf verschiedene Krebsarten, insbesondere auf Dickdarmkrebs, hinweisen. Allerdings können auch nicht-krebsbedingte Erkrankungen wie Entzündungen oder bestimmte Lungenerkrankungen zu erhöhten CEA-Werten führen.", "https://flexikon.doccheck.com/de/Carcinoembryonales_Antigen")
        ]
    },
    "organs": [],
    "diet": []
}




]