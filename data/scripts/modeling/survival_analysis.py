import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter, CoxPHFitter
import os

# Set up paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
DATA_PATH = os.path.join(BASE_DIR, 'data')
OUTPUT_PATH = os.path.join(DATA_PATH, 'outputs')
os.makedirs(OUTPUT_PATH, exist_ok=True)

# Load the cleaned EHR data
df = pd.read_csv(os.path.join(DATA_PATH, 'ehr_oncology_cleaned.csv'))

# Convert stage and treatment to categorical
df['stage'] = df['stage'].astype('category')
df['treatment'] = df['treatment'].astype('category')

### 📈 Kaplan-Meier Survival Analysis ###
print("📈 Kaplan-Meier Survival Curve by Cancer Stage")
kmf = KaplanMeierFitter()

plt.figure(figsize=(10, 6))
for stage in df['stage'].unique():
    mask = df['stage'] == stage
    kmf.fit(durations=df[mask]['days_survived'], event_observed=df[mask]['event_status'], label=f"Stage {stage}")
    kmf.plot_survival_function()

plt.title("Kaplan-Meier Survival Curves by Cancer Stage")
plt.xlabel("Days Survived")
plt.ylabel("Survival Probability")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_PATH, 'km_plot.png'))
plt.close()

### ⚙️ Cox Proportional Hazards Model ###
print("⚙️ Running Cox Proportional Hazards Regression")

# One-hot encode categorical variables
df_encoded = pd.get_dummies(df[['age', 'sex', 'stage', 'treatment', 'days_survived', 'event_status']], drop_first=True)

# Fit model
cph = CoxPHFitter()
cph.fit(df_encoded, duration_col='days_survived', event_col='event_status')

# Print and save summary
print("\n🧠 Cox Model Summary:")
cph.print_summary()

cox_summary_path = os.path.join(OUTPUT_PATH, 'cox_summary.txt')
with open(cox_summary_path, 'w') as f:
    cph.print_summary(stream=f)

# 📊 Save hazard ratio plot
plt.figure(figsize=(8, 5))
cph.plot()
plt.title("Hazard Ratios (Cox Regression)")
plt.tight_layout()
cox_plot_path = os.path.join(OUTPUT_PATH, 'cox_plot.png')
plt.savefig(cox_plot_path)
plt.close()
