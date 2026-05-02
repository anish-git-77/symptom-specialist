# ─────────────────────────────────────────────────────────────
#  specialist_map.py  —  disease → specialist knowledge base
# ─────────────────────────────────────────────────────────────

DISEASE_TO_SPECIALIST = {
    # Cardiologist
    "Heart attack":              "Cardiologist",
    "Hypertension":              "Cardiologist",
    "Varicose veins":            "Cardiologist",

    # Neurologist
    "Migraine":                  "Neurologist",
    "Paralysis (brain hemorrhage)": "Neurologist",
    "Cervical spondylosis":      "Neurologist",

    # Dermatologist
    "Psoriasis":                 "Dermatologist",
    "Acne":                      "Dermatologist",
    "Fungal infection":          "Dermatologist",
    "Ringworm":                  "Dermatologist",
    "Impetigo":                  "Dermatologist",
    "Chicken pox":               "Dermatologist",

    # Endocrinologist
    "Diabetes":                  "Endocrinologist",
    "Hypothyroidism":            "Endocrinologist",
    "Hyperthyroidism":           "Endocrinologist",
    "Hypoglycemia":              "Endocrinologist",

    # Pulmonologist
    "Pneumonia":                 "Pulmonologist",
    "Bronchial Asthma":          "Pulmonologist",
    "Tuberculosis":              "Pulmonologist",
    "Common Cold":               "Pulmonologist",

    # Rheumatologist
    "Arthritis":                 "Rheumatologist",

    # Gastroenterologist
    "GERD":                      "Gastroenterologist",
    "Peptic ulcer disease":      "Gastroenterologist",
    "Gastroenteritis":           "Gastroenterologist",
    "Chronic cholestasis":       "Gastroenterologist",
    "Alcoholic hepatitis":       "Gastroenterologist",
    "Hepatitis A":               "Gastroenterologist",
    "Hepatitis B":               "Gastroenterologist",
    "Hepatitis C":               "Gastroenterologist",
    "Hepatitis D":               "Gastroenterologist",
    "Hepatitis E":               "Gastroenterologist",
    "Jaundice":                  "Gastroenterologist",
    "Drug Reaction":             "Gastroenterologist",

    # Orthopedic
    "Osteoarthristis":           "Orthopedic Surgeon",
    "Back pain":                 "Orthopedic Surgeon",

    # Psychiatrist
    "Depression":                "Psychiatrist",

    # Urologist
    "Urinary tract infection":   "Urologist",
    "Kidney stones":             "Urologist",

    # General / Infectious Disease
    "Dengue":                    "General Physician",
    "Malaria":                   "General Physician",
    "Typhoid":                   "General Physician",
    "Influenza":                 "General Physician",
    "AIDS":                      "Infectious Disease Specialist",
    "Dimorphic hemmorhoids(piles)": "General Surgeon",
    "Allergy":                   "Allergist / Immunologist",
}

SPECIALIST_DESCRIPTIONS = {
    "Cardiologist":                   "Heart & blood vessel specialist. Treats hypertension, heart attacks, and vascular conditions.",
    "Neurologist":                    "Brain & nervous system specialist. Treats migraines, strokes, paralysis, and movement disorders.",
    "Dermatologist":                  "Skin, hair & nail specialist. Treats rashes, acne, fungal infections, and chronic skin conditions.",
    "Endocrinologist":                "Hormone & metabolism specialist. Treats diabetes, thyroid disorders, and hormonal imbalances.",
    "Pulmonologist":                  "Lung & respiratory specialist. Treats asthma, pneumonia, TB, and breathing difficulties.",
    "Rheumatologist":                 "Joint & autoimmune specialist. Treats arthritis, lupus, and inflammatory conditions.",
    "Gastroenterologist":             "Digestive system specialist. Treats stomach, liver, intestine, and hepatitis conditions.",
    "Orthopedic Surgeon":             "Bone, joint & muscle specialist. Treats fractures, back pain, and joint problems.",
    "Psychiatrist":                   "Mental health specialist. Treats depression, anxiety, and psychiatric disorders.",
    "Urologist":                      "Urinary tract specialist. Treats UTIs, kidney stones, and bladder conditions.",
    "General Physician":              "First-line doctor for infections, fever, and common illnesses.",
    "Allergist / Immunologist":       "Allergy & immune system specialist.",
    "Infectious Disease Specialist":  "Expert in complex infections, HIV/AIDS, and tropical diseases.",
    "General Surgeon":                "Surgical specialist for abdominal and general conditions.",
}

URGENCY = {
    "Heart attack":                  ("🚨 EMERGENCY", "error"),
    "Paralysis (brain hemorrhage)":  ("🚨 EMERGENCY", "error"),
    "Hepatitis A":                   ("⚠️ Seek care today", "warning"),
    "Hepatitis B":                   ("⚠️ Seek care today", "warning"),
    "Tuberculosis":                  ("⚠️ Seek care today", "warning"),
    "AIDS":                          ("⚠️ Seek care today", "warning"),
    "Dengue":                        ("⚠️ Seek care today", "warning"),
    "Malaria":                       ("⚠️ Seek care today", "warning"),
}

SPECIALIST_EMOJI = {
    "Cardiologist":                  "❤️",
    "Neurologist":                   "🧠",
    "Dermatologist":                 "🧴",
    "Endocrinologist":               "⚗️",
    "Pulmonologist":                 "🫁",
    "Rheumatologist":                "🦴",
    "Gastroenterologist":            "🫃",
    "Orthopedic Surgeon":            "🦵",
    "Psychiatrist":                  "🧘",
    "Urologist":                     "💧",
    "General Physician":             "🏥",
    "Allergist / Immunologist":      "🤧",
    "Infectious Disease Specialist": "🦠",
    "General Surgeon":               "🔬",
}
