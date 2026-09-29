import pandas as pd
import xgboost as xgb

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix

# -----------------------------------
# 1. Load dataset
# -----------------------------------

df = pd.read_csv("cumulative_copy.csv")

# -----------------------------------
# 2. Features
# -----------------------------------

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

target = "koi_disposition"

# -----------------------------------
# 3. Remove missing values
# -----------------------------------

data = df[features + [target]].dropna()

X = data[features]
y = data[target]

# -----------------------------------
# 4. Encode labels
# -----------------------------------

encoder = LabelEncoder()

y_encoded = encoder.fit_transform(y)

print("Classes:")
print(encoder.classes_)

# -----------------------------------
# 5. Train/test split
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)

# -----------------------------------
# 6. XGBoost
# -----------------------------------

model = xgb.XGBClassifier(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,

    objective="multi:softprob",

    eval_metric="mlogloss",

    random_state=42
)

# -----------------------------------
# 7. Train
# -----------------------------------

model.fit(
    X_train,
    y_train
)

# -----------------------------------
# 8. Evaluate
# -----------------------------------

predictions = model.predict(X_test)

print(
    classification_report(
        y_test,
        predictions,
        target_names=encoder.classes_
    )
)

print("Confusion matrix:")
print(
    confusion_matrix(
        y_test,
        predictions
    )
)

model.save_model("exoplanet_xgboost.json")