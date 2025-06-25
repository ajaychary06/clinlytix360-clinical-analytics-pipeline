import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
np.random.seed(42)

# Create data folder
os.makedirs("../../data", exist_ok=True)

### 1. Generate ehr_oncology.csv ###
n_patients = 200
patient_ids = [f"P{str(i).zfill(4)}" for i in range(1, n_patients + 1)]

cancer_types = ['Lung', 'Breast', 'Colon', 'Prostate']
stages = ['I', 'II', 'III', 'IV']
treatments = ['Chemo', 'Radiation', 'Surgery', 'Combo']

diagnosis_dates = [datetime(2018, 1, 1) + timedelta(days=random.randint(0, 1500)) for _ in range(n_patients)]

ehr_data = pd.DataFrame({
    'patient_id': patient_ids,
    'age': np.random.randint(35, 85, size=n_patients),
    'sex': np.random.choice(['Male', 'Female'], size=n_patients),
    'cancer_type': np.random.choice(cancer_types, size=n_patients),
    'stage': np.random.choice(stages, size=n_patients, p=[0.2, 0.3, 0.3, 0.2]),
    'treatment': np.random.choice(treatments, size=n_patients),
    'diagnosis_date': diagnosis_dates,
})

ehr_data['days_survived'] = [random.randint(180, 2000) for _ in range(n_patients)]
ehr_data['last_followup_date'] = ehr_data['diagnosis_date'] + ehr_data['days_survived'].apply(lambda x: timedelta(days=x))
ehr_data['event_status'] = np.random.choice([0, 1], size=n_patients, p=[0.6, 0.4])  # 0 = alive, 1 = died

ehr_data.to_csv("../../data/ehr_oncology.csv", index=False)

### 2. Generate trial_protocol.csv ###
n_sites = 15
site_ids = [f"S{str(i).zfill(3)}" for i in range(1, n_sites + 1)]
countries = ['US', 'UK', 'Germany', 'India', 'Brazil']

trial_data = pd.DataFrame({
    'trial_id': ['CT2025'] * n_sites,
    'site_id': site_ids,
    'country': np.random.choice(countries, size=n_sites),
    'eligibility_age_min': [18] * n_sites,
    'eligibility_age_max': [80] * n_sites,
    'eligibility_stage': np.random.choice(['III', 'IV'], size=n_sites),
    'allowed_sex': np.random.choice(['Male', 'Female', 'Any'], size=n_sites),
    'target_enrollment': np.random.randint(50, 150, size=n_sites),
    'protocol_date': [datetime(2023, 1, 1).strftime('%Y-%m-%d')] * n_sites
})

trial_data.to_csv("../../data/trial_protocol.csv", index=False)

### 3. Generate pro_scores.csv ###
pro_records = []

for pid in patient_ids:
    n_visits = np.random.randint(1, 4)
    for visit in range(n_visits):
        pro_records.append({
            'patient_id': pid,
            'visit_day': 30 * (visit + 1),
            'fatigue_score': np.random.randint(1, 6),
            'pain_score': np.random.randint(1, 6),
            'mobility_score': np.random.randint(1, 6),
            'emotional_score': np.random.randint(1, 6),
        })

pro_df = pd.DataFrame(pro_records)
pro_df['total_score'] = pro_df[['fatigue_score', 'pain_score', 'mobility_score', 'emotional_score']].sum(axis=1)

pro_df.to_csv("../../data/pro_scores.csv", index=False)

print("✅ All datasets generated successfully!")
