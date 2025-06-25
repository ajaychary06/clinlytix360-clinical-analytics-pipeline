import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
import plotly.express as px
import os

# Set paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
DATA_PATH = os.path.join(BASE_DIR, 'data')

# Load datasets
ehr = pd.read_csv(os.path.join(DATA_PATH, 'ehr_oncology_cleaned.csv'))
feasibility = pd.read_csv(os.path.join(DATA_PATH, 'site_feasibility_report.csv'))
pro = pd.read_csv(os.path.join(DATA_PATH, 'pro_scores_cleaned.csv'))

# ---------- Dashboard ----------
st.set_page_config(page_title="Clinlytix360 Dashboard", layout="wide")

st.title("🩺 Clinlytix360 – Clinical & Real-World Outcomes Analytics")

# Sidebar
st.sidebar.header("Filters")
selected_stage = st.sidebar.selectbox("Select Cancer Stage", sorted(ehr['stage'].unique()))
selected_site = st.sidebar.selectbox("Select Site", sorted(feasibility['site_id'].unique()))

# --------- Section 1: Survival Analysis ---------
st.header("📈 Kaplan-Meier Survival Curve")

kmf = KaplanMeierFitter()
fig, ax = plt.subplots(figsize=(10, 5))

for stage in ehr['stage'].unique():
    mask = ehr['stage'] == stage
    kmf.fit(durations=ehr[mask]['days_survived'], event_observed=ehr[mask]['event_status'], label=f"Stage {stage}")
    kmf.plot_survival_function(ax=ax)

ax.set_title("Survival by Cancer Stage")
ax.set_xlabel("Days")
ax.set_ylabel("Survival Probability")
st.pyplot(fig)

# --------- Section 2: Trial Feasibility ---------
st.header("🧪 Site-Level Trial Feasibility")

site_data = feasibility[feasibility['site_id'] == selected_site].iloc[0]

st.metric(label="Eligible Patients", value=site_data['eligible_patients'])
st.metric(label="Target Enrollment", value=site_data['target_enrollment'])
st.metric(label="Projected Fill Rate", value=f"{100 * site_data['projected_fill_rate']:.1f}%")

bar_fig = px.bar(feasibility, x='site_id', y='projected_fill_rate', color='country',
                 title="Projected Enrollment Fill Rate by Site", labels={'projected_fill_rate': 'Fill Rate'})
st.plotly_chart(bar_fig, use_container_width=True)

# --------- Section 3: PRO/COA Scores ---------
st.header("🧠 PRO/COA Score Trends")

score_avg = pro.groupby('visit_day')[['fatigue_score', 'pain_score', 'mobility_score', 'emotional_score']].mean().reset_index()

line_fig = px.line(score_avg, x='visit_day', y=['fatigue_score', 'pain_score', 'mobility_score', 'emotional_score'],
                   title="Average PRO Scores Over Time", labels={'value': 'Score', 'variable': 'Domain'})
st.plotly_chart(line_fig, use_container_width=True)

st.markdown("---")
st.caption("📊 Built with Streamlit · Data simulated for Clinlytix360")

