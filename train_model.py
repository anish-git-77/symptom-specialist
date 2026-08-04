# ─────────────────────────────────────────────────────────────
#  train_model.py  —  train & save model from Kaggle dataset
# ─────────────────────────────────────────────────────────────
import os  
import pickle
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report

from load_data import load_kaggle_data
from specialist_map import DISEASE_TO_SPECIALIST, SPECIALIST_DESCRIPTIONS

os.makedirs("models", exist_ok=True)

# ── Load data ─────────────────────────────────────────────────
print("Loading Kaggle dataset...")
df, severity_map, description_map, precaution_map = load_kaggle_data("data")

texts  = df["text"].tolist()
labels = df["disease"].tolist()

# ── Train / test split ────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42, stratify=labels
)
print(f"Train: {len(X_train)}  |  Test: {len(X_test)}")

# ── Pipeline: TF-IDF + Logistic Regression ────────────────────
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=10000,
        sublinear_tf=True,
        min_df=2,
    )),
    ("clf", LogisticRegression(
        max_iter=2000,
        C=10.0,
        solver="lbfgs",
    )),
])

# ── Train ─────────────────────────────────────────────────────
print("\nTraining model...")
pipeline.fit(X_train, y_train)

# ── Evaluate ──────────────────────────────────────────────────
y_pred = pipeline.predict(X_test)
acc    = accuracy_score(y_test, y_pred)
print(f"\nTest accuracy  : {acc:.2%}")

cv = cross_val_score(pipeline, texts, labels, cv=5, scoring="accuracy", n_jobs=-1)
print(f"5-fold CV mean : {cv.mean():.2%} ± {cv.std():.2%}")

print("\nPer-class report (top diseases):")
print(classification_report(y_test, y_pred, zero_division=0))

# ── Save artifact ─────────────────────────────────────────────
artifact = {
    "pipeline":                pipeline,
    "disease_to_specialist":   DISEASE_TO_SPECIALIST,
    "specialist_descriptions": SPECIALIST_DESCRIPTIONS,
    "description_map":         description_map,
    "precaution_map":          precaution_map,
    "severity_map":            severity_map,
    "classes":                 pipeline.classes_.tolist(),
}

save_path = "models/specialist_model.pkl"
with open(save_path, "wb") as f:
    pickle.dump(artifact, f)

print(f"\n✅ Model saved → {save_path}")
print(f"   Diseases covered : {len(pipeline.classes_)}")
print(f"   Test accuracy    : {acc:.2%}")
