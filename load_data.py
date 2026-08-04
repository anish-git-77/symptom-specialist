# ─────────────────────────────────────────────────────────────
#  load_data.py  —  reads Kaggle CSVs → training dataframe
# ─────────────────────────────────────────────────────────────
import os  
import pandas as pd
import numpy as np  


def load_kaggle_data(data_dir="data"):
    """
    Reads the 4 Kaggle CSVs and returns:
        df          — full dataframe with columns [text, disease, specialist]
        severity_map — {symptom: severity_score}
        description_map — {disease: description_text}
        precaution_map  — {disease: [precaution1, ..., precaution4]}
    """
    # ── 1. Main dataset ───────────────────────────────────────
    main_path = os.path.join(data_dir, "dataset.csv")
    if not os.path.exists(main_path):
        raise FileNotFoundError(
            f"\n\n❌  Could not find '{main_path}'.\n"
            "Please download the Kaggle dataset and place the CSVs inside the 'data/' folder.\n"
            "Dataset: https://www.kaggle.com/datasets/itachi9604/disease-symptom-description-dataset\n"
        )

    df_main = pd.read_csv(main_path)

    # Column names: Disease, Symptom_1 … Symptom_17
    symptom_cols = [c for c in df_main.columns if c.lower().startswith("symptom")]

    # ── 2. Severity map ───────────────────────────────────────
    sev_path = os.path.join(data_dir, "Symptom-severity.csv")
    severity_map = {}
    if os.path.exists(sev_path):
        df_sev = pd.read_csv(sev_path)
        df_sev.columns = df_sev.columns.str.strip()
        for _, row in df_sev.iterrows():
            symptom = str(row.iloc[0]).strip().lower().replace(" ", "_")
            weight  = int(row.iloc[1]) if not pd.isna(row.iloc[1]) else 1
            severity_map[symptom] = weight

    # ── 3. Description map ────────────────────────────────────
    desc_path = os.path.join(data_dir, "symptom_Description.csv")
    description_map = {}
    if os.path.exists(desc_path):
        df_desc = pd.read_csv(desc_path)
        df_desc.columns = df_desc.columns.str.strip()
        for _, row in df_desc.iterrows():
            disease = str(row.iloc[0]).strip()
            desc    = str(row.iloc[1]).strip() if len(row) > 1 else ""
            description_map[disease] = desc

    # ── 4. Precaution map ─────────────────────────────────────
    prec_path = os.path.join(data_dir, "symptom_precaution.csv")
    precaution_map = {}
    if os.path.exists(prec_path):
        df_prec = pd.read_csv(prec_path)
        df_prec.columns = df_prec.columns.str.strip()
        for _, row in df_prec.iterrows():
            disease = str(row.iloc[0]).strip()
            precs   = [str(row.iloc[i]).strip()
                       for i in range(1, len(row))
                       if not pd.isna(row.iloc[i]) and str(row.iloc[i]).strip()]
            precaution_map[disease] = precs

    # ── 5. Build text column ──────────────────────────────────
    def build_text(row):
        symptoms = []
        for col in symptom_cols:
            val = str(row[col]).strip().lower().replace("_", " ")
            if val and val not in ("nan", "none", ""):
                # repeat symptom proportional to severity for TF-IDF weighting
                raw_key = val.replace(" ", "_")
                weight  = severity_map.get(raw_key, 1)
                # repeat high-severity symptoms to boost their TF-IDF weight
                symptoms.extend([val] * max(1, weight // 2))
        return " ".join(symptoms)

    df_main["text"]    = df_main.apply(build_text, axis=1)
    df_main["disease"] = df_main["Disease"].str.strip()

    # Drop rows where text is empty
    df_main = df_main[df_main["text"].str.strip() != ""].reset_index(drop=True)

    print(f"Loaded {len(df_main)} rows | {df_main['disease'].nunique()} unique diseases")
    return df_main[["text", "disease"]], severity_map, description_map, precaution_map
