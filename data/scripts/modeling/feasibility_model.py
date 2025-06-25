import pandas as pd
import os

# Set paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
DATA_PATH = os.path.join(BASE_DIR, 'data')

# Load data
ehr = pd.read_csv(os.path.join(DATA_PATH, 'ehr_oncology_cleaned.csv'))
trial = pd.read_csv(os.path.join(DATA_PATH, 'trial_protocol_cleaned.csv'))

# Results container
site_eligibility = []

print("\n🧪 Trial Feasibility Matching per Site")

# Loop through each trial site to apply eligibility filters
for _, site in trial.iterrows():
    min_age = site['eligibility_age_min']
    max_age = site['eligibility_age_max']
    required_stage = site['eligibility_stage']
    allowed_sex = site['allowed_sex']
    
    # Apply inclusion/exclusion filters
    eligible = ehr.copy()
    eligible = eligible[(eligible['age'] >= min_age) & (eligible['age'] <= max_age)]
    eligible = eligible[eligible['stage'] == required_stage]
    
    if allowed_sex != 'Any':
        eligible = eligible[eligible['sex'] == allowed_sex]

    # Save result
    site_eligibility.append({
        'site_id': site['site_id'],
        'country': site['country'],
        'required_stage': required_stage,
        'allowed_sex': allowed_sex,
        'target_enrollment': site['target_enrollment'],
        'eligible_patients': len(eligible),
        'projected_fill_rate': round(len(eligible) / site['target_enrollment'], 2)
    })

# Create result DataFrame
feasibility_df = pd.DataFrame(site_eligibility)

# Save feasibility report
feasibility_df.to_csv(os.path.join(DATA_PATH, 'site_feasibility_report.csv'), index=False)

print("\n✅ Site-level feasibility report generated.")
print(feasibility_df.head())
