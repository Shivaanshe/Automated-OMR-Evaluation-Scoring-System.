# app.py - Streamlit frontend for Theme 1 OMR system
import streamlit as st
import os
import pandas as pd
import json
from theme_1_omr_system import evaluate_image_path

st.set_page_config(page_title="Automated OMR Evaluation", layout="centered")

st.title("📄 Automated OMR Evaluation & Scoring")

st.markdown(
    "Upload an OMR sheet image (photo or scan). The backend will evaluate and return per-question, "
    "subject-wise and total scores. Toggle debug to get annotated overlay."
)

uploaded_file = st.file_uploader("Upload OMR sheet (jpg/png)", type=["jpg", "jpeg", "png"])
version = st.selectbox("Answer key version", ("A", "B"))
debug = st.checkbox("Save debug overlay image", value=True)

if uploaded_file:
    # create uploads folder
    UPLOAD_DIR = "uploads"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    tmp_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

    # save uploaded file
    with open(tmp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("Evaluating OMR sheet..."):
        try:
            out = evaluate_image_path(tmp_path, version=version, debug=debug)
        except Exception as e:
            st.error(f"Evaluation failed: {e}")
            raise

    result = out["result"]
    st.success(f"Done — Total Score: {result['total']}/100 ({result['percentage']:.2f}%)")

    st.subheader("Subject-wise Scores")
    subj_df = pd.DataFrame.from_dict(result["subject_scores"], orient="index", columns=["score"])
    subj_df.index.name = "Subject"
    st.table(subj_df)

    st.subheader("Per-question (first 50 rows preview)")
    pq_df = pd.DataFrame(result["per_question"])
    st.dataframe(pq_df.head(50))

    # Download JSON
    if os.path.exists(out["json_path"]):
        with open(out["json_path"], "r", encoding="utf-8") as jf:
            json_bytes = jf.read().encode("utf-8")
        st.download_button("Download JSON", json_bytes, file_name=os.path.basename(out["json_path"]), mime="application/json")

    # Download CSV
    if os.path.exists(out["csv_path"]):
        with open(out["csv_path"], "rb") as cf:
            csv_bytes = cf.read()
        st.download_button("Download CSV", csv_bytes, file_name=os.path.basename(out["csv_path"]), mime="text/csv")

    # Show debug image
    if debug and out.get("debug_path") and os.path.exists(out["debug_path"]):
        st.subheader("Debug Overlay")
        st.image(out["debug_path"], use_column_width=True)
