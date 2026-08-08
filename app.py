# ─────────────────────────────────────────────────────────────
#  app.py  —  Streamlit web app for Symptom → Specialist
# ─────────────────────────────────────────────────────────────
import pickle  
import numpy as np
import streamlit as st
from specialist_map import SPECIALIST_EMOJI, URGENCY

st.set_page_config(    
    page_title="Symptom → Specialist",
    page_icon="🩺",
    layout="centered",
)

# ── Load model ────────────────────────────────────────────────
@st.cache_resource 
def load_model():
    try:
        with open("models/specialist_model.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None

artifact = load_model()

# ── CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
.big-title  { font-size:2rem; font-weight:700; margin-bottom:0; }
.subtitle   { color:gray; font-size:.95rem; margin-top:4px; margin-bottom:1.5rem; }
.rank-badge { display:inline-block; font-size:.7rem; font-weight:600;
              padding:2px 8px; border-radius:99px; margin-left:8px;
              background:#e8f5e9; color:#2e7d32; vertical-align:middle; }
.rank-2     { background:#e3f2fd; color:#1565c0; }
.rank-3     { background:#f3e5f5; color:#6a1b9a; }
.card       { border-radius:12px; padding:1rem 1.25rem; margin-bottom:.75rem;
              border-left:4px solid; }
.card-1     { background:#f8fdf8; border-color:#4CAF50; }
.card-2     { background:#f4f9ff; border-color:#2196F3; }
.card-3     { background:#fdf6ff; border-color:#9C27B0; }
.spec-name  { font-size:1.15rem; font-weight:600; }
.disease-lbl{ color:#555; font-size:.88rem; margin:.3rem 0; }
.conf-bar   { background:#e0e0e0; border-radius:6px; height:8px; margin:6px 0 4px; }
.conf-fill  { height:8px; border-radius:6px; }
.conf-lbl   { font-size:.78rem; color:#888; }
.desc-txt   { font-size:.88rem; color:#444; margin-top:6px; }
.prec-item  { font-size:.85rem; color:#333; margin:.2rem 0; }
.disclaimer { font-size:.73rem; color:#aaa; margin-top:2rem;
              border-top:1px solid #eee; padding-top:.75rem; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────
st.markdown('<p class="big-title">🩺 Symptom → Specialist</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Describe your symptoms in plain English. We\'ll tell you which specialist to see and why.</p>', unsafe_allow_html=True)

if artifact is None:
    st.error("⚠️  Model not found. Please run `python train_model.py` first.")
    st.stop()

pipeline             = artifact["pipeline"]
disease_to_specialist = artifact["disease_to_specialist"]
specialist_desc      = artifact["specialist_descriptions"]
description_map      = artifact.get("description_map", {})
precaution_map       = artifact.get("precaution_map", {})
classes              = artifact["classes"]

# ── Input ─────────────────────────────────────────────────────
symptom_input = st.text_area(
    "Describe your symptoms",
    placeholder="e.g.  I have a severe throbbing headache with nausea and light sensitivity...",
    height=110,
)

col_btn, col_clear = st.columns([2, 6])
with col_btn:
    analyse = st.button("🔍 Analyse Symptoms", type="primary", use_container_width=True)

# Quick example buttons
st.caption("Try an example:")
EXAMPLES = [
    ("🫀 Heart",    "chest pain shortness of breath sweating left arm pain"),
    ("🧠 Neuro",    "severe throbbing headache nausea light sensitivity vomiting"),
    ("🩸 Diabetes", "frequent urination excessive thirst fatigue blurred vision"),
    ("🦴 Joints",   "joint pain swelling stiffness morning fingers"),
    ("🧘 Mental",   "persistent sadness hopelessness loss of interest sleep problems"),
    ("🫁 Lungs",    "wheezing breathlessness chest tightness cough at night"),
]
cols = st.columns(len(EXAMPLES))
for i, (label, ex) in enumerate(EXAMPLES):
    if cols[i].button(label, key=f"ex{i}"):
        symptom_input = ex
        analyse = True

# ── Predict & display ─────────────────────────────────────────
if analyse:
    if not symptom_input.strip():
        st.warning("Please describe your symptoms first.")
        st.stop()

    probs     = pipeline.predict_proba([symptom_input])[0]
    top3_idx  = np.argsort(probs)[::-1][:3]
    top_disease = classes[top3_idx[0]]

    # Urgency banner
    if top_disease in URGENCY:
        label, level = URGENCY[top_disease]
        msg = f"{label} — **{top_disease}** detected. Seek immediate medical attention."
        if level == "error":
            st.error(msg)
        else:
            st.warning(msg)

    st.markdown("---")
    st.subheader("Recommended Specialists")

    card_styles  = ["card-1", "card-2", "card-3"]
    bar_colors   = ["#4CAF50", "#2196F3", "#9C27B0"]
    rank_labels  = ["Best match", "2nd option", "3rd option"]
    rank_classes = ["rank-badge", "rank-badge rank-2", "rank-badge rank-3"]

    for rank, idx in enumerate(top3_idx):
        disease    = classes[idx]
        specialist = disease_to_specialist.get(disease, "General Physician")
        emoji      = SPECIALIST_EMOJI.get(specialist, "🏥")
        conf       = probs[idx] * 100
        spec_desc  = specialist_desc.get(specialist, "")
        bar_w      = max(int(conf), 3)

        st.markdown(f"""
        <div class="card {card_styles[rank]}">
          <div class="spec-name">
            {emoji} {specialist}
            <span class="{rank_classes[rank]}">{rank_labels[rank]}</span>
          </div>
          <div class="disease-lbl">Likely condition: <strong>{disease}</strong></div>
          <div class="conf-bar">
            <div class="conf-fill" style="width:{bar_w}%;background:{bar_colors[rank]}"></div>
          </div>
          <div class="conf-lbl">Confidence: {conf:.1f}%</div>
          <div class="desc-txt">{spec_desc}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Disease description from Kaggle ──────────────────────
    if top_disease in description_map:
        st.markdown("---")
        st.subheader("📖 About this condition")
        st.info(description_map[top_disease])

    # ── Precautions from Kaggle ───────────────────────────────
    if top_disease in precaution_map:
        precs = precaution_map[top_disease]
        if precs:
            st.subheader("✅ Recommended Precautions")
            for p in precs:
                st.markdown(f'<div class="prec-item">• {p.capitalize()}</div>',
                            unsafe_allow_html=True)

    # ── What to tell the doctor ───────────────────────────────
    st.markdown("---")
    st.subheader("📋 What to tell the doctor")
    keywords = [w for w in symptom_input.replace(",", " ").split() if len(w) > 3]
    kw_str   = ", ".join(dict.fromkeys(keywords[:8]))
    st.markdown(f"""
- **Symptoms:** {kw_str if kw_str else symptom_input}
- **Duration** — how many days/weeks have you had these symptoms?
- **Severity** — rate your discomfort from 1 to 10
- **Triggers** — what makes it better or worse?
- **Medications** you are currently taking
- **Family history** of similar conditions
    """)

    # ── Highlighted keywords ──────────────────────────────────
    with st.expander("🔍 Symptom keywords detected"):
        highlighted = " ".join(
            f"**`{w}`**" if len(w) > 4 else w
            for w in symptom_input.split()
        )
        st.markdown(highlighted)

# ── Disclaimer ────────────────────────────────────────────────
st.markdown("""
<div class="disclaimer">
⚠️ <strong>Medical Disclaimer:</strong> This tool is for informational and educational purposes only.
It does not constitute medical advice, diagnosis, or treatment.
Always consult a qualified healthcare professional.
In emergencies, call your local emergency number immediately.
</div>
""", unsafe_allow_html=True)
