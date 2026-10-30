from pathlib import Path
import json
import numpy as np
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, accuracy_score

ROOT = Path(__file__).parent
df = pd.read_csv(ROOT / "data" / "housing_data.csv")
features = ["city", "area_sqft", "bedrooms", "bathrooms", "property_age_years",
            "location_score", "amenities_count", "annual_rent_yield_pct"]
numeric = features[1:]
categorical = ["city"]
X = df[features]
y = df["price_inr"].astype(float)
y_class = (y >= y.median()).astype(int)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=.2, random_state=42)
Xctr, Xcte, yctr, ycte = train_test_split(X, y_class, test_size=.2, random_state=42, stratify=y_class)

def make_preprocessor():
    return ColumnTransformer([
        ("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), numeric),
        ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                          ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical)
    ])

reg = Pipeline([("prep", make_preprocessor()), ("model", RandomForestRegressor(n_estimators=180, random_state=42, min_samples_leaf=2))])
clf = Pipeline([("prep", make_preprocessor()), ("model", RandomForestClassifier(n_estimators=160, random_state=42, min_samples_leaf=2, class_weight="balanced"))])
reg.fit(Xtr, ytr)
clf.fit(Xctr, yctr)
rp = reg.predict(Xte)
cp = clf.predict(Xcte)
metrics = {"mae": float(mean_absolute_error(yte, rp)),
           "rmse": float(np.sqrt(mean_squared_error(yte, rp))),
           "r2": float(r2_score(yte, rp)),
           "classification_accuracy": float(accuracy_score(ycte, cp))}
(ROOT / "models").mkdir(exist_ok=True)
import joblib
joblib.dump(reg, ROOT / "models" / "price_regressor.joblib")
joblib.dump(clf, ROOT / "models" / "value_classifier.joblib")
(ROOT / "models" / "metrics.json").write_text(json.dumps(metrics, indent=2))
mlflow.set_experiment("Real-Estate-Investment-Advisor")
with mlflow.start_run():
    mlflow.log_params({"regressor": "RandomForestRegressor", "classifier": "RandomForestClassifier",
                       "test_size": 0.2, "random_state": 42, "dataset_rows": len(df)})
    mlflow.log_metrics(metrics)
    mlflow.sklearn.log_model(reg, "price_regressor")
    mlflow.sklearn.log_model(clf, "value_classifier")
    mlflow.log_artifact(str(ROOT / "data" / "housing_data.csv"))
print("Training complete.")
print(json.dumps(metrics, indent=2))
print("Models saved in models/ and experiment logged to MLflow.")
