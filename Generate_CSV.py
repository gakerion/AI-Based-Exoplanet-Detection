import pandas as pd
import xgboost as xgb
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig
)


results = []

# ============================================================
# 1. Load dataset
# ============================================================

df = pd.read_csv("data.csv")



# ============================================================
# 2. Features used by XGBoost
# ============================================================

features = [
    "koi_period",
    "koi_impact",
    "koi_duration",
    "koi_depth",
    "koi_prad",
    "koi_teq",
    "koi_insol",
    "koi_model_snr",
    "koi_steff",
    "koi_slogg",
    "koi_srad",
    "koi_kepmag",
]


# ============================================================
# 3. Load trained XGBoost model
# ============================================================

model = xgb.XGBClassifier()

model.load_model("exoplanet_xgboost.json")

print("XGBoost model loaded successfully!")


# ============================================================
# 4. Class mapping
# ============================================================

# If you trained the model using LabelEncoder,
# LabelEncoder sorts these alphabetically:
#
# 0 = CANDIDATE
# 1 = CONFIRMED
# 2 = FALSE POSITIVE

class_names = [
    "CANDIDATE",
    "CONFIRMED",
    "FALSE POSITIVE"
]


# ============================================================
# 5. Analyze each star
# ============================================================

for kepid, star_data in df.groupby("kepid"):

    print("\n" + "=" * 60)
    print(f"STAR: {kepid}")
    print(f"Number of candidates: {len(star_data)}")
    print("=" * 60)

    # ========================================================
    # Analyze each candidate around the star
    # ========================================================

    for _, row in star_data.iterrows():

        # --------------------------------------------
        # Create model input
        # --------------------------------------------

        candidate_data = pd.DataFrame([{
            feature: row[feature]
            for feature in features
        }])

        # --------------------------------------------
        # Handle missing values
        # --------------------------------------------

        candidate_data = candidate_data.fillna(
            df[features].median()
        )

        # --------------------------------------------
        # XGBoost prediction
        # --------------------------------------------

        prediction = model.predict(candidate_data)[0]

        predicted_class = class_names[int(prediction)]

        # --------------------------------------------
        # Save result
        # --------------------------------------------

        results.append({
            "kepid": kepid,
            "planet_status": predicted_class
        })

        # --------------------------------------------
        # Display
        # --------------------------------------------

        print("\nCandidate:", row["kepoi_name"])
        print("XGBoost prediction:", predicted_class)


# ========================================================
# Save predictions to CSV
# ========================================================

results_df = pd.DataFrame(results)

results_df.to_csv(
    "exoplanet_predictions.csv",
    index=False
)

print("\nPrediction CSV saved successfully!")
print(results_df.head())