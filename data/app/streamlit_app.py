import streamlit as st
import pandas as pd
from PIL import Image
import os
import time

# Optional auto-refresh (every 30 seconds)
refresh_interval = st.sidebar.slider("Refresh interval (seconds)", 5, 60, 30)
st.sidebar.button("Refresh Now")
time.sleep(refresh_interval)

# Set page config
st.set_page_config(page_title="Clinlytix360 – Survival Dashboard", layout="centered")

st.title("🧬 Clinlytix360 – Survival Analysis Dashboard")
st.markdown("Visualize survival trends across cancer stages and treatment types.")

# Load dataset for filters
data_path = os.path.join("..", "data", "ehr_oncology_cleaned.csv")
if os.path.exists(data_path):
    df = pd.read_csv(data_path)
    stage_options = sorted(df['stage'].dropna().unique())
    treatment_options = sorted(df['treatment'].dropna().unique())

    # Filters
    stage_filter = st.selectbox("Filter by Cancer Stage", options=["All"] + stage_options)
    treatment_filter = st.selectbox("Filter by Treatment Type", options=["All"] + treatment_options)
else:
    st.error("EHR data file not found.")
    stage_filter = "All"
    treatment_filter = "All"

# Load and display Kaplan-Meier plot
km_path = os.path.join("..", "data", "outputs", "km_plot.png")
if os.path.exists(km_path):
    st.image(Image.open(km_path), caption="Kaplan-Meier Survival Curves", use_column_width=True)
else:
    st.warning("Kaplan-Meier plot not found.")

# Display Cox model summary
st.subheader("🧠 Cox Model Summary")
summary_path = os.path.join("..", "data", "outputs", "cox_summary.txt")

try:
    with open(summary_path, 'r') as f:
        summary = f.read()
        st.text(summary)
except FileNotFoundError:
    st.warning("Cox model summary not available. Please run the DAG or script.")

# Display Cox hazard ratio plot
st.subheader("📊 Hazard Ratios (Cox Regression)")
cox_plot_path = os.path.join("..", "data", "outputs", "cox_plot.png")

if os.path.exists(cox_plot_path):
    st.image(Image.open(cox_plot_path), caption="Hazard Ratios from Cox Model", use_column_width=True)
else:
    st.warning("Cox plot not found. Please run the DAG or script.")

# Optional: Show filtered dataset
if st.checkbox("🔍 Show filtered data"):
    if stage_filter != "All":
        df = df[df['stage'] == stage_filter]
    if treatment_filter != "All":
        df = df[df['treatment'] == treatment_filter]
    st.dataframe(df.head())
