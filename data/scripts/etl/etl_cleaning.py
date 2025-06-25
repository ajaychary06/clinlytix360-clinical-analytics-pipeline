import pandas as pd
import numpy as np
import os

# Define file paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
DATA_PATH = os.path.join(BASE_DIR, 'data')

# Load datasets
ehr = pd.read_csv(os.path.join(DATA_PATH, 'ehr_oncology.csv'))
trial = pd.read_csv(os.path.join(DATA_PATH, 'trial_protocol.csv'))
pro = pd.read_csv(os.path.join(DATA_PATH, 'pro_scores.csv'))

### 🩺 EHR Cleaning ###
print("\n🩺 Cleaning ehr_oncology.csv...")

# Convert date columns
ehr['diagnosis_date'] = pd.to_datetime(ehr['diagnosis_date'])
ehr['last_followup_date'] = pd.to_datetime(ehr['last_followup_date'])

# Check for invalid survival values
ehr['calculated_days'] = (ehr['last_followup_date'] - ehr['diagnosis_date']).dt.days
ehr['survival_mismatch'] = ehr['calculated_days'] != ehr['days_survived']
mismatch_count = ehr['survival_mismatch'].sum()
if mismatch_count > 0:
    print(f"⚠️ {mismatch_count} rows have mismatched survival days.")
else:
    print("✅ Survival days match follow-up correctly.")

# Drop helper columns
ehr.drop(columns=['calculated_days', 'survival_mismatch'], inplace=True)

### 📋 Trial Protocol Cleaning ###
print("\n📋 Cleaning trial_protocol.csv...")

# Ensure numeric types
trial['eligibility_age_min'] = pd.to_numeric(trial['eligibility_age_min'], errors='coerce')
trial['eligibility_age_max'] = pd.to_numeric(trial['eligibility_age_max'], errors='coerce')
trial['target_enrollment'] = pd.to_numeric(trial['target_enrollment'], errors='coerce')

# Standardize string columns
trial['eligibility_stage'] = trial['eligibility_stage'].str.upper().str.strip()
trial['allowed_sex'] = trial['allowed_sex'].str.capitalize().str.strip()

# Check missing values
if trial.isnull().sum().any():
    print("⚠️ Missing values detected in trial_protocol.csv:")
    print(trial.isnull().sum())
else:
    print("✅ Trial protocol cleaned successfully.")

### 🧠 PRO Scores Cleaning ###
print("\n🧠 Cleaning pro_scores.csv...")

score_cols = ['fatigue_score', 'pain_score', 'mobility_score', 'emotional_score']
pro[score_cols] = pro[score_cols].clip(lower=1, upper=5)

# Recalculate total score
pro['total_score'] = pro[score_cols].sum(axis=1)

# Drop rows with invalid or missing scores
before = len(pro)
pro.dropna(subset=score_cols, inplace=True)
after = len(pro)
if before != after:
    print(f"⚠️ Dropped {before - after} rows with missing scores.")
else:
    print("✅ PRO scores clean.")

### 💾 Optional: Save cleaned versions (overwrite or save new)
ehr.to_csv(os.path.join(DATA_PATH, 'ehr_oncology_cleaned.csv'), index=False)
trial.to_csv(os.path.join(DATA_PATH, 'trial_protocol_cleaned.csv'), index=False)
pro.to_csv(os.path.join(DATA_PATH, 'pro_scores_cleaned.csv'), index=False)

print("\n✅ All datasets cleaned and saved successfully.")
