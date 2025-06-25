# Load libraries
library(psych)
library(tidyverse)

# Set working directory to data folder
setwd("C:/Users/ajayc/clinlytix360_airflow/data")

# Load cleaned PRO data
pro <- read_csv("pro_scores_cleaned.csv")

# View structure
glimpse(pro)

# Subset only Likert item scores
items <- pro %>% select(fatigue_score, pain_score, mobility_score, emotional_score)

### ✅ 1. Cronbach’s Alpha
cat("\n🧪 Cronbach's Alpha:\n")
alpha(items)

### ✅ 2. Correlation Matrix
cat("\n📈 Correlation Matrix:\n")
print(cor(items))

### ✅ 3. Exploratory Factor Analysis (1-factor model)
cat("\n🔍 Factor Analysis (EFA, 1 factor):\n")
fa_result <- fa(items, nfactors = 1, rotate = "none", fm = "ml")
print(fa_result)

### ✅ 4. Optional: 2-Factor Solution (if structure is unclear)
cat("\n🔍 Factor Analysis (EFA, 2 factors):\n")
fa2 <- fa(items, nfactors = 2, rotate = "varimax", fm = "ml")
print(fa2)

# Visualize factor loadings
fa.diagram(fa2)
