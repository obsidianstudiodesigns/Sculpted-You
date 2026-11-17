"""Product catalogue and category content for Sculpted You.

Prices come from the client's price list (WhatsApp image, 16 Nov 2026).
Copy is informational: what each compound is, what it is studied or used for, known side effects
and who should avoid it. No dosing instructions on the website by design (see BUILD-PLAN.md, 2.3).
Edit here, then run: python tools/build.py
"""

CATEGORIES = [
    {
        "slug": "weight-loss",
        "name": "Weight Loss",
        "title": "Weight loss and metabolic support",
        "tagline": "Boost metabolism. Support fat loss. Improve overall health.",
        "blurb": "Appetite, blood sugar and metabolism peptides, from the GLP-1 family to gentler metabolic support.",
        "image": "cat-weight-loss",
        "icon": "scales",
    },
    {
        "slug": "recovery",
        "name": "Recovery",
        "title": "Recovery, healing and inflammation",
        "tagline": "Faster recovery. Support healing. Reduce inflammation.",
        "blurb": "Peptides studied for tissue repair, joints, gut lining and skin renewal.",
        "image": "cat-recovery",
        "icon": "first-aid",
    },
    {
        "slug": "hormones",
        "name": "Hormones",
        "title": "Hormone, energy and longevity",
        "tagline": "More energy. Hormonal balance. Long-term health.",
        "blurb": "Growth hormone support, cellular energy and the longevity compounds people ask about most.",
        "image": "cat-hormones",
        "icon": "lightning",
    },
    {
        "slug": "aesthetic",
        "name": "Aesthetic",
        "title": "Aesthetic and performance",
        "tagline": "Support skin health. Look and feel your best.",
        "blurb": "Tanning and appearance peptides.",
        "image": "cat-aesthetic",
        "icon": "sparkle",
    },
    {
        "slug": "brain-health",
        "name": "Brain Health",
        "title": "Cognitive and anxiety",
        "tagline": "Mental clarity. Focus. Calm and balanced.",
        "blurb": "Peptides researched for focus, stress resilience and a calmer mind.",
        "image": "cat-brain-health",
        "icon": "brain",
    },
]

# Applies to every product; shown under each product's own list.
GENERAL_AVOID = [
    "Pregnancy, trying to conceive or breastfeeding",
    "Anyone under 18",
    "Active cancer or a history of cancer, unless your oncologist agrees",
]

GLP1_AVOID = [
    "Personal or family history of medullary thyroid cancer or MEN2",
    "History of pancreatitis or gallbladder disease",
    "Type 1 diabetes, or insulin or sulphonylurea use without a doctor adjusting doses",
    "A history of an eating disorder",
]

GLP1_SIDE = [
    "Nausea, especially in the first weeks and after dose increases",
    "Diarrhoea or constipation",
    "Bloating, reflux and burping",
    "Fatigue, headaches or dizziness while appetite adjusts",
    "Low blood pressure in some people",
    "Rare but serious: pancreatitis and gallbladder problems. Severe stomach pain needs a doctor",
]

PRODUCTS = [
    # ---------------------------------------------------------------- weight loss
    {
        "slug": "retatrutide-30mg", "name": "Retatrutide", "strength": "30mg", "price": 2100,
        "cat": "weight-loss", "feature": True, "guide": "Retatrutide Guide.pdf",
        "short": "Triple-action GLP-1, GIP and glucagon agonist. The newest and strongest of the three GLP-1 siblings.",
        "what": [
            "Retatrutide is a next-generation peptide that acts on three hormone receptors at once: GLP-1, GIP and glucagon. "
            "GLP-1 and GIP slow digestion and quieten hunger, while the glucagon action is thought to raise energy use and help the liver burn fat.",
            "It is still in clinical trials. In a 48-week phase 2 trial published in the New England Journal of Medicine (2023), "
            "people on the highest dose lost an average of about 24% of their body weight, the largest result seen in the GLP-1 family so far.",
        ],
        "benefits": [
            "Strong appetite control and fewer cravings",
            "Fat loss with a higher energy burn from the glucagon action",
            "Better blood sugar and insulin response",
            "Reduced liver fat in trial participants",
            "Improvements in blood pressure and cholesterol markers",
        ],
        "side": GLP1_SIDE + ["A slightly faster resting heart rate"],
        "who": "Adults with a BMI of 35 or higher, or people who reached a plateau on semaglutide or tirzepatide, working with a doctor who monitors them.",
        "avoid": GLP1_AVOID + ["Heart rhythm problems"],
        "related": ["tirzepatide-30mg", "semaglutide-10mg", "cagrilintide-10mg"],
    },
    {
        "slug": "semaglutide-10mg", "name": "Semaglutide", "strength": "10mg", "price": 1000,
        "cat": "weight-loss", "feature": True, "guide": "Semaglutide Guide.pdf",
        "short": "The original weekly GLP-1. The gentlest starting point of the GLP-1 family, with the longest track record.",
        "what": [
            "Semaglutide copies GLP-1, a gut hormone your body releases after eating. It tells your brain you are full, slows how quickly your stomach empties "
            "and helps your body release insulin when blood sugar rises.",
            "It was first developed for type 2 diabetes and is the active ingredient in medicines such as Ozempic and Wegovy. "
            "In the STEP 1 trial, adults lost an average of about 15% of their body weight over 68 weeks.",
        ],
        "benefits": [
            "Feeling full sooner and for longer",
            "Fewer cravings and less food noise",
            "Steadier blood sugar",
            "Gradual, sustained weight loss",
            "The most research and real-world experience of the three siblings",
        ],
        "side": GLP1_SIDE,
        "who": "Adults with a BMI of 30 or more, or 27 or more with a weight-related condition such as high blood pressure or prediabetes, who want to start with the most established option.",
        "avoid": GLP1_AVOID,
        "related": ["tirzepatide-30mg", "retatrutide-30mg", "5-amino-1mq"],
    },
    {
        "slug": "tirzepatide-30mg", "name": "Tirzepatide", "strength": "30mg", "price": 1800,
        "cat": "weight-loss", "feature": True, "guide": "Tirzepatide Guide.pdf",
        "short": "Dual GLP-1 and GIP agonist. Stronger than semaglutide, often with fewer stomach side effects at the same stage.",
        "what": [
            "Tirzepatide acts on two gut hormone receptors, GLP-1 and GIP. Together they reduce appetite, slow digestion and improve how your body handles sugar and fat.",
            "It is the active ingredient in Mounjaro and Zepbound. In the SURMOUNT-1 trial, adults on the highest dose lost an average of about 21% of their body weight over 72 weeks.",
        ],
        "benefits": [
            "Strong appetite control",
            "Greater average weight loss than semaglutide in trials",
            "Improved insulin sensitivity and blood sugar",
            "Improvements in waist size, blood pressure and cholesterol",
        ],
        "side": GLP1_SIDE,
        "who": "Adults with a BMI of 30 or more, people with insulin resistance, or people who stalled on semaglutide, under a doctor's guidance.",
        "avoid": GLP1_AVOID,
        "related": ["semaglutide-10mg", "retatrutide-30mg", "cagrilintide-10mg"],
    },
    {
        "slug": "cagrilintide-10mg", "name": "Cagrilintide", "strength": "10mg", "price": 1500,
        "cat": "weight-loss", "feature": False, "guide": None,
        "short": "Long-acting amylin analogue that adds a second fullness signal, often paired with a GLP-1.",
        "what": [
            "Cagrilintide is a long-acting version of amylin, a hormone released alongside insulin after meals. Amylin tells the brain you have eaten enough and slows stomach emptying, "
            "through a different pathway from GLP-1.",
            "It is being studied on its own and combined with semaglutide (a pairing known as CagriSema). It is not yet an approved medicine.",
        ],
        "benefits": [
            "Earlier fullness at meals",
            "Works alongside GLP-1 peptides through a separate pathway",
            "Weight loss in clinical trials, greater when combined with semaglutide",
        ],
        "side": ["Nausea", "Constipation or diarrhoea", "Reduced appetite that can be strong", "Injection site redness"],
        "who": "Adults already on a GLP-1 who want added appetite control, with a doctor overseeing the combination.",
        "avoid": ["Gastroparesis or other stomach-emptying problems", "Insulin use without a doctor adjusting doses"],
        "related": ["semaglutide-10mg", "tirzepatide-30mg", "retatrutide-30mg"],
    },
    {
        "slug": "5-amino-1mq", "name": "5-Amino-1MQ", "strength": "", "price": 400,
        "cat": "weight-loss", "feature": False, "guide": "5-Amino-1MQ Guide.pdf",
        "short": "Small-molecule NNMT blocker studied for stubborn fat and cellular energy, without stimulants.",
        "what": [
            "5-Amino-1MQ is a small molecule that blocks NNMT, an enzyme found in high amounts in fat cells. Blocking NNMT is thought to raise NAD+ levels inside fat cells, "
            "which pushes them to burn more energy instead of storing it.",
            "So far the evidence comes from laboratory and animal studies, where it reduced fat mass without changing food intake. Human studies are still lacking.",
        ],
        "benefits": [
            "Support for metabolism and fat loss",
            "Higher cellular energy through NAD+",
            "No stimulants, so no jitters",
            "May help with weight-loss plateaus",
        ],
        "side": ["Headaches", "Mild nausea", "Increased thirst", "Temporary change in appetite"],
        "who": "Adults with stubborn fat or a slow metabolism who want non-stimulant metabolic support alongside diet and training.",
        "avoid": ["Liver or kidney disease"],
        "related": ["semaglutide-10mg", "aod9604-2mg", "slu-pp-332-5mg"],
    },
    {
        "slug": "aod9604-2mg", "name": "AOD9604", "strength": "2mg", "price": 370,
        "cat": "weight-loss", "feature": False, "guide": None,
        "short": "Modified fragment of growth hormone researched for fat breakdown, without the effects on growth or blood sugar.",
        "what": [
            "AOD9604 is a modified piece of human growth hormone (fragment 176-191). It was designed to keep growth hormone's fat-burning signal without its effects on growth, blood sugar or insulin.",
            "Early studies looked promising, but larger human trials did not show significant weight loss compared with placebo. It has a good safety record in those trials.",
        ],
        "benefits": [
            "Supports fat breakdown",
            "Does not raise blood sugar",
            "Studied for cartilage and joint repair",
            "Well tolerated in human trials",
        ],
        "side": ["Injection site irritation", "Headache", "Mild fatigue"],
        "who": "Adults who want gentle fat-loss support with a strong safety record and realistic expectations.",
        "avoid": [],
        "related": ["5-amino-1mq", "slu-pp-332-5mg", "tesamorelin-10mg"],
    },
    {
        "slug": "slu-pp-332-5mg", "name": "SLU-PP-332", "strength": "5mg", "price": 910,
        "cat": "weight-loss", "feature": False, "guide": None,
        "short": "Experimental exercise mimetic that switches on the same muscle pathways as endurance training.",
        "what": [
            "SLU-PP-332 activates oestrogen-related receptors (ERRs), which control how muscles produce energy. In mice it mimicked the effects of endurance exercise: "
            "more fat burning, better endurance and less weight gain.",
            "It is at a very early research stage. There are no published human trials yet.",
        ],
        "benefits": [
            "Increased fat burning in research models",
            "Improved endurance in animal studies",
            "Support for metabolic health",
        ],
        "side": ["Unknown in humans. No clinical safety data yet", "Possible changes in heart rate or energy"],
        "who": "Experienced adults who understand that the evidence is preclinical only.",
        "avoid": ["Heart conditions"],
        "related": ["mots-c-10mg", "aicar-100mg", "5-amino-1mq"],
    },
    # ---------------------------------------------------------------- recovery
    {
        "slug": "tb500-10mg", "name": "TB500 (Thymosin Beta-4)", "strength": "10mg", "price": 1300,
        "cat": "recovery", "feature": True, "guide": None,
        "short": "Thymosin Beta-4 fragment researched for muscle, tendon and ligament recovery.",
        "what": [
            "TB500 is a synthetic version of the active part of thymosin beta-4, a protein found in almost every cell. It helps cells move to injured areas and supports new blood vessel growth.",
            "Research in animals shows faster healing of muscle, tendon, skin and heart tissue. Human data is limited.",
        ],
        "benefits": [
            "Faster recovery from muscle and soft-tissue injuries",
            "Improved flexibility and less stiffness",
            "Supports new blood vessel growth to injured areas",
            "Reduced inflammation",
        ],
        "side": ["Headache", "Tiredness", "Injection site redness"],
        "who": "Active adults and athletes recovering from injury or heavy training.",
        "avoid": [],
        "related": ["bpc-157-10mg", "glow-blend-70mg", "ghk-cu-100mg"],
    },
    {
        "slug": "bpc-157-10mg", "name": "BPC-157", "strength": "10mg", "price": 800,
        "cat": "recovery", "feature": True, "guide": None,
        "short": "Body Protection Compound. The most popular healing peptide, studied for tendons, joints and the gut.",
        "what": [
            "BPC-157 is a 15-amino-acid peptide based on a protective protein found in stomach juice. In animal studies it speeds up healing of tendons, ligaments, muscle, "
            "bone and the gut lining.",
            "It is widely used for recovery, but human trials are still small and few.",
        ],
        "benefits": [
            "Tendon, ligament and joint healing",
            "Gut lining repair and digestive comfort",
            "Reduced inflammation",
            "Faster recovery after training or surgery",
        ],
        "side": ["Nausea", "Dizziness", "Injection site irritation"],
        "who": "Adults recovering from tendon, joint or gut problems, or training hard.",
        "avoid": [],
        "related": ["tb500-10mg", "glow-blend-70mg", "ara-290-10mg"],
    },
    {
        "slug": "ghk-cu-100mg", "name": "GHK-Cu", "strength": "100mg", "price": 500,
        "cat": "recovery", "feature": True, "guide": "GHK-CU Guide (1).pdf",
        "short": "The copper peptide. Studied for collagen, firmer skin, thicker hair and faster healing.",
        "what": [
            "GHK-Cu is a small peptide that occurs naturally in your blood and binds copper. Levels drop as you age. It signals skin and tissue to repair, "
            "and helps your body make collagen and elastin.",
            "It is one of the best-studied peptides for skin, with evidence for firmer, smoother skin and wound healing. Most people notice skin or hair changes within 4 to 6 weeks.",
        ],
        "benefits": [
            "More collagen and elastin for firmer skin",
            "Fewer fine lines and more even tone",
            "Faster healing of cuts, scars and marks",
            "Thicker, stronger hair",
            "Calmer, less inflamed skin",
        ],
        "side": ["Injection site stinging or redness", "Temporary skin sensitivity"],
        "who": "Adults focused on skin quality, hair, healing or healthy ageing.",
        "avoid": ["Wilson's disease or any copper metabolism disorder"],
        "related": ["glow-blend-70mg", "bpc-157-10mg", "mt-2-10mg"],
    },
    {
        "slug": "ara-290-10mg", "name": "ARA-290 (Cibinetide)", "strength": "10mg", "price": 730,
        "cat": "recovery", "feature": False, "guide": None,
        "short": "Tissue-protective peptide studied for nerve pain and inflammation.",
        "what": [
            "ARA-290 (cibinetide) is a small peptide derived from erythropoietin. It activates the body's repair receptor without raising red blood cell counts.",
            "Small human trials have studied it for nerve pain in diabetes and sarcoidosis, with improvements in pain and small nerve fibre density.",
        ],
        "benefits": [
            "Nerve protection and repair",
            "Reduced neuropathic pain in trials",
            "Lower inflammation",
            "Support for blood sugar control in early studies",
        ],
        "side": ["Injection site reactions", "Mild headache"],
        "who": "Adults dealing with nerve pain or chronic inflammation, alongside their doctor.",
        "avoid": [],
        "related": ["bpc-157-10mg", "tb500-10mg", "vip-10mg"],
    },
    {
        "slug": "glow-blend-70mg", "name": "Glow Blend (BPC-157 + TB500 + GHK-Cu)", "strength": "70mg", "price": 1740,
        "cat": "recovery", "feature": True, "guide": None,
        "short": "BPC-157 10mg, TB500 10mg and GHK-Cu 50mg in one vial, for recovery and skin together.",
        "what": [
            "Glow combines the three most popular repair peptides: BPC-157 (10mg) for tendons, joints and the gut, TB500 (10mg) for muscle and tissue repair, "
            "and GHK-Cu (50mg) for collagen, skin and hair.",
            "Together they cover healing from the inside and visible skin quality on the outside, in one vial instead of three.",
        ],
        "benefits": [
            "Whole-body recovery support",
            "Firmer, more radiant skin",
            "Joint and soft-tissue repair",
            "Better value than buying all three separately",
        ],
        "side": ["Injection site redness or stinging", "Headache", "Mild nausea"],
        "who": "Adults who want recovery and skin results together.",
        "avoid": ["Wilson's disease or any copper metabolism disorder"],
        "related": ["bpc-157-10mg", "tb500-10mg", "ghk-cu-100mg"],
    },
    # ---------------------------------------------------------------- hormones
    {
        "slug": "tesamorelin-10mg", "name": "Tesamorelin", "strength": "10mg", "price": 1200,
        "cat": "hormones", "feature": False, "guide": None,
        "short": "Growth-hormone-releasing peptide best known for reducing deep belly fat.",
        "what": [
            "Tesamorelin is a GHRH analogue. It signals your pituitary gland to release more of your own growth hormone, in a natural pulse.",
            "It is approved in the United States (as Egrifta) to reduce visceral fat, the deep fat around the organs that drives metabolic risk.",
        ],
        "benefits": [
            "Reduced visceral (deep belly) fat",
            "Better body composition",
            "Improved sleep and recovery",
            "Support for skin and energy",
        ],
        "side": ["Injection site redness", "Joint pain", "Water retention", "Higher blood sugar in some people"],
        "who": "Adults carrying stubborn belly fat who want growth hormone support from their own pituitary.",
        "avoid": ["Diabetes without a doctor monitoring blood sugar"],
        "related": ["cjc-1295-ipa", "hgh-191aa-24iu", "mots-c-10mg"],
    },
    {
        "slug": "cjc-1295-ipa", "name": "CJC-1295 (No DAC) + Ipamorelin", "strength": "5mg + 5mg", "price": 900,
        "cat": "hormones", "feature": True, "guide": "CJC 1296 + IPA - Flyer (Growth Hormone).pdf",
        "short": "The classic growth hormone pair. Two signals that boost your body's own GH release.",
        "what": [
            "CJC-1295 (without DAC) is a GHRH analogue that stimulates growth hormone release. Ipamorelin is a gentle GH secretagogue that adds a second signal without "
            "raising cortisol or prolactin much.",
            "Combined, they follow your body's natural rhythm, supporting regeneration, recovery and body composition.",
        ],
        "benefits": [
            "Deeper sleep and waking refreshed",
            "Faster recovery from exercise and injury",
            "Steady fat loss with leaner muscle tone",
            "Healthier skin, hair and connective tissue",
            "More energy and vitality",
        ],
        "side": ["Injection site redness", "Temporary water retention", "Flushing", "Increased hunger", "Headaches (rare)"],
        "who": "Adults over 30 who want better sleep, recovery and body composition.",
        "avoid": ["Diabetes without a doctor monitoring blood sugar"],
        "related": ["tesamorelin-10mg", "hgh-191aa-24iu", "igf-1-lr3-1mg"],
    },
    {
        "slug": "mots-c-10mg", "name": "MOTS-c", "strength": "10mg", "price": 610,
        "cat": "hormones", "feature": False, "guide": None,
        "short": "Mitochondrial peptide researched for metabolism, insulin sensitivity and exercise capacity.",
        "what": [
            "MOTS-c is a peptide made by your mitochondria, the energy centres of your cells. It helps muscles use glucose and fat, and levels fall with age.",
            "Animal studies show better insulin sensitivity, exercise capacity and protection against diet-induced weight gain. Human research is early.",
        ],
        "benefits": [
            "Improved insulin sensitivity",
            "Better exercise capacity",
            "Support for healthy weight",
            "Cellular energy and healthy ageing",
        ],
        "side": ["Injection site reactions", "Mild fatigue", "Increased heart rate during exercise"],
        "who": "Active adults interested in metabolic health and longevity.",
        "avoid": [],
        "related": ["nad-500mg", "aicar-100mg", "slu-pp-332-5mg"],
    },
    {
        "slug": "nad-500mg", "name": "NAD+", "strength": "500mg", "price": 730,
        "cat": "hormones", "feature": True, "guide": None,
        "short": "The coenzyme in every cell. Popular for energy, recovery, mental clarity and healthy ageing.",
        "what": [
            "Nicotinamide adenine dinucleotide (NAD+) is a coenzyme found in every living cell. It is central to energy production and also takes part in DNA repair "
            "and cell stress responses through enzymes such as sirtuins.",
            "NAD+ levels decline with age. The biology is well established, but clinical evidence for injectable NAD+ as a routine wellness therapy is still limited.",
        ],
        "benefits": [
            "Energy support and less fatigue",
            "Recovery during stress, dieting or hard training",
            "Mental clarity",
            "Healthy ageing support",
        ],
        "side": ["Flushing or a warm feeling", "Nausea", "Chest tightness or cramping if given too fast", "Injection site discomfort"],
        "who": "Adults already working on sleep, nutrition and exercise who want NAD+ as an add-on, not a foundation.",
        "avoid": ["Significant kidney, liver or heart disease", "Recurrent nausea, vomiting or dehydration"],
        "related": ["mots-c-10mg", "5-amino-1mq", "semax-10mg"],
    },
    {
        "slug": "hgh-191aa-24iu", "name": "HGH 191AA (Somatropin)", "strength": "24IU", "price": 910,
        "cat": "hormones", "feature": False, "guide": None,
        "short": "Recombinant human growth hormone, identical to the 191-amino-acid hormone your pituitary makes.",
        "what": [
            "HGH 191AA is recombinant human growth hormone, made to be identical to the hormone your pituitary gland produces. Growth hormone drives tissue repair, "
            "muscle, bone density and fat metabolism.",
            "Unlike the releasing peptides, it replaces growth hormone directly, so the effects and the side effects are stronger. Medical supervision matters here.",
        ],
        "benefits": [
            "Leaner body composition",
            "Improved recovery and repair",
            "Better skin thickness and elasticity",
            "Bone density support",
        ],
        "side": ["Joint and muscle aches", "Water retention and swelling", "Tingling or numbness in the hands", "Raised blood sugar"],
        "who": "Adults with a confirmed low growth hormone level, under a doctor's supervision.",
        "avoid": ["Diabetes", "Uncontrolled high blood pressure"],
        "related": ["cjc-1295-ipa", "tesamorelin-10mg", "igf-1-lr3-1mg"],
    },
    {
        "slug": "igf-1-lr3-1mg", "name": "IGF-1 LR3", "strength": "1mg", "price": 1660,
        "cat": "hormones", "feature": False, "guide": None,
        "short": "Long-acting version of IGF-1, the hormone that carries out most of growth hormone's effects.",
        "what": [
            "IGF-1 LR3 is a modified, longer-lasting version of insulin-like growth factor 1. IGF-1 is the hormone the liver releases in response to growth hormone, "
            "and it drives muscle growth and repair.",
            "It is a research compound. Because it acts like insulin, it can lower blood sugar.",
        ],
        "benefits": [
            "Muscle growth and repair",
            "Recovery support",
            "Improved nutrient uptake into muscle",
        ],
        "side": ["Low blood sugar (shakiness, sweating, confusion)", "Joint pain", "Water retention", "Injection site reactions"],
        "who": "Experienced adults focused on muscle and recovery who understand the blood sugar risk.",
        "avoid": ["Diabetes or a history of low blood sugar"],
        "related": ["hgh-191aa-24iu", "cjc-1295-ipa", "tb500-10mg"],
    },
    {
        "slug": "aicar-100mg", "name": "AICAR", "strength": "100mg", "price": 730,
        "cat": "hormones", "feature": False, "guide": None,
        "short": "AMPK activator researched for endurance and fat metabolism. Banned in sport.",
        "what": [
            "AICAR activates AMPK, the cell's energy sensor that normally switches on during exercise. In mice it improved endurance and fat burning without training.",
            "It is on the World Anti-Doping Agency's prohibited list, so tested athletes should not use it.",
        ],
        "benefits": [
            "Endurance support in research models",
            "Fat metabolism and glucose uptake",
            "Metabolic health support",
        ],
        "side": ["Low blood sugar", "Raised uric acid", "Fatigue"],
        "who": "Non-competing adults interested in metabolic and endurance research.",
        "avoid": ["Competitive athletes subject to drug testing", "Gout or high uric acid"],
        "related": ["mots-c-10mg", "slu-pp-332-5mg", "nad-500mg"],
    },
    # ---------------------------------------------------------------- aesthetic
    {
        "slug": "mt-2-10mg", "name": "MT-2 (Melanotan II)", "strength": "10mg", "price": 400,
        "cat": "aesthetic", "feature": True, "guide": None,
        "short": "Melanocortin peptide that deepens your tan with less sun exposure.",
        "what": [
            "Melanotan II copies alpha-MSH, the hormone that tells skin cells to make melanin. It darkens skin with less UV exposure.",
            "It acts on several melanocortin receptors, which explains side effects such as reduced appetite and changes in libido. Dermatologists advise regular mole checks while using it.",
        ],
        "benefits": [
            "A deeper, longer-lasting tan",
            "Less time in the sun needed",
            "Reduced appetite in some people",
        ],
        "side": ["Nausea, mostly at the start", "Facial flushing", "New or darkening moles and freckles", "Increased libido or spontaneous erections", "Reduced appetite"],
        "who": "Adults with no history of skin cancer who will keep up regular mole checks.",
        "avoid": ["Personal or family history of melanoma or skin cancer", "Many or unusual moles", "Heart conditions or high blood pressure"],
        "related": ["ghk-cu-100mg", "glow-blend-70mg", "bpc-157-10mg"],
    },
    # ---------------------------------------------------------------- brain
    {
        "slug": "selank-5mg", "name": "Selank", "strength": "5mg", "price": 460,
        "cat": "brain-health", "feature": True, "guide": None,
        "short": "Calming peptide researched for anxiety and stress, without sedation or dependence.",
        "what": [
            "Selank is a synthetic version of tuftsin, a natural immune peptide, with added stability. It is used in Russia for anxiety.",
            "Studies suggest it calms anxiety by influencing GABA and serotonin systems, without the sedation, memory effects or dependence of common anti-anxiety medicines.",
        ],
        "benefits": [
            "Calmer mood and less anxiety",
            "Clear thinking under stress",
            "No sedation or dependence reported",
            "Possible immune support",
        ],
        "side": ["Mild fatigue", "Nasal irritation if used as a spray", "Headache"],
        "who": "Adults dealing with stress or anxious thoughts who want to stay sharp.",
        "avoid": ["Taking prescribed anxiety or depression medication without your doctor's input"],
        "related": ["semax-10mg", "vip-10mg", "nad-500mg"],
    },
    {
        "slug": "semax-10mg", "name": "Semax", "strength": "10mg", "price": 820,
        "cat": "brain-health", "feature": True, "guide": None,
        "short": "Nootropic peptide researched for focus, memory and mental energy.",
        "what": [
            "Semax is a synthetic peptide based on a fragment of ACTH, with no hormonal effect. It is used in Russia for stroke recovery and cognitive support.",
            "It raises BDNF, a protein that supports brain cell growth and connections, which is linked to sharper focus and memory.",
        ],
        "benefits": [
            "Sharper focus and attention",
            "Memory and learning support",
            "Mental energy without stimulants",
            "Support for brain cell resilience",
        ],
        "side": ["Nasal irritation if used as a spray", "Irritability or restlessness at higher amounts", "Headache"],
        "who": "Adults who want sharper focus and mental stamina for work or study.",
        "avoid": ["Seizure disorders", "Bipolar disorder or a history of mania"],
        "related": ["selank-5mg", "nad-500mg", "vip-10mg"],
    },
    {
        "slug": "vip-10mg", "name": "VIP", "strength": "10mg", "price": 1370,
        "cat": "brain-health", "feature": False, "guide": None,
        "short": "Vasoactive intestinal peptide, studied for inflammation, the gut-brain axis and mould-related illness.",
        "what": [
            "VIP (vasoactive intestinal peptide) is a natural neuropeptide found in the brain, gut and lungs. It relaxes blood vessels, calms inflammation and helps regulate the body clock.",
            "It is best known in functional medicine for chronic inflammatory response syndrome (CIRS), often linked to mould exposure, and is being studied for lung conditions.",
        ],
        "benefits": [
            "Calmer inflammation",
            "Support for the gut-brain axis",
            "Body clock and sleep regulation",
            "Lung and blood vessel support",
        ],
        "side": ["Low blood pressure and light-headedness", "Flushing", "Diarrhoea", "Nasal irritation if used as a spray"],
        "who": "Adults with chronic inflammation or CIRS, working with a practitioner.",
        "avoid": ["Low blood pressure"],
        "related": ["selank-5mg", "semax-10mg", "ara-290-10mg"],
    },
]


def by_slug():
    return {p["slug"]: p for p in PRODUCTS}


def label(p):
    return f'{p["name"]} {p["strength"]}'.strip()
