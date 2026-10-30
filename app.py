from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, accuracy_score, classification_report

ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "housing_data.csv"
FEATURES = ["city", "area_sqft", "bedrooms", "bathrooms", "property_age_years",
            "location_score", "amenities_count", "annual_rent_yield_pct"]
NUMERIC = ["area_sqft", "bedrooms", "bathrooms", "property_age_years",
           "location_score", "amenities_count", "annual_rent_yield_pct"]
CATEGORICAL = ["city"]

st.set_page_config(page_title="Real Estate Investment Advisor", page_icon="🏠", layout="wide")
st.title("🏠 Real Estate Investment Advisor")
st.caption("Educational ML demo • Synthetic sample data • Not a professional valuation or financial recommendation")

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

@st.cache_resource
def train_models(data):
    X = data[FEATURES].copy()
    y = data["price_inr"].astype(float)
    # Classification target: properties above the dataset median price are 'higher-value'.
    y_class = (y >= y.median()).astype(int)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    Xc_train, Xc_test, yc_train, yc_test = train_test_split(X, y_class, test_size=0.2, random_state=42, stratify=y_class)

    preprocessor = ColumnTransformer([
        ("num", Pipeline([("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]), NUMERIC),
        ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                          ("onehot", OneHotEncoder(handle_unknown="ignore"))]), CATEGORICAL)
    ])
    reg = Pipeline([("prep", preprocessor),
                    ("model", RandomForestRegressor(n_estimators=180, random_state=42, min_samples_leaf=2))])
    clf = Pipeline([("prep", preprocessor),
                    ("model", RandomForestClassifier(n_estimators=160, random_state=42, min_samples_leaf=2,
                                                     class_weight="balanced"))])
    reg.fit(X_train, y_train)
    clf.fit(Xc_train, yc_train)
    pred = reg.predict(X_test)
    class_pred = clf.predict(Xc_test)
    metrics = {
        "MAE (₹)": mean_absolute_error(y_test, pred),
        "RMSE (₹)": float(np.sqrt(mean_squared_error(y_test, pred))),
        "R²": r2_score(y_test, pred),
        "Classification accuracy": accuracy_score(yc_test, class_pred),
        "y_test": y_test, "pred": pred, "class_report": classification_report(yc_test, class_pred, output_dict=True)
    }
    return reg, clf, metrics, float(y.median())

data = load_data()
reg_model, clf_model, metrics, median_price = train_models(data)

with st.sidebar:
    st.header("Property details")
    selected_city = st.selectbox("City", sorted(data["city"].unique()))
    area = st.slider("Area (sq. ft.)", 350, 2600, 950, 50)
    bedrooms = st.selectbox("Bedrooms", [1,2,3,4,5], index=1)
    bathrooms = st.selectbox("Bathrooms", [1,2,3,4,5], index=1)
    age = st.slider("Property age (years)", 0, 35, 5)
    location_score = st.slider("Location score (1 = low, 10 = high)", 1, 10, 7)
    amenities = st.slider("Number of amenities", 0, 7, 3)
    rent_yield = st.slider("Expected annual rent yield (%)", 1.2, 7.5, 3.5, 0.1)
    purchase_price = st.number_input("Your expected purchase price (₹)", min_value=100000, value=7500000, step=100000)
    annual_growth = st.slider("Assumed annual price growth (%)", 0.0, 15.0, 6.0, 0.5)
    years = st.slider("Investment horizon (years)", 1, 20, 5)

input_df = pd.DataFrame([{
    "city": selected_city, "area_sqft": area, "bedrooms": bedrooms, "bathrooms": bathrooms,
    "property_age_years": age, "location_score": location_score,
    "amenities_count": amenities, "annual_rent_yield_pct": rent_yield
}])
predicted_price = float(reg_model.predict(input_df[FEATURES])[0])
class_probability = float(clf_model.predict_proba(input_df[FEATURES])[0][1])
future_value = predicted_price * ((1 + annual_growth / 100) ** years)
estimated_profit = future_value - purchase_price
roi = (estimated_profit / purchase_price) * 100 if purchase_price else 0
annual_rent = predicted_price * rent_yield / 100

tab1, tab2, tab3, tab4 = st.tabs(["🏡 Advisor", "📊 Explore data", "🤖 Model evaluation", "ℹ️ Methodology"])
with tab1:
    st.subheader("Your property estimate")
    c1,c2,c3 = st.columns(3)
    c1.metric("Predicted current value", f"₹{predicted_price:,.0f}")
    c2.metric(f"Estimated value in {years} years", f"₹{future_value:,.0f}")
    c3.metric("Projected gain vs purchase price", f"₹{estimated_profit:,.0f}", f"{roi:.1f}% projected ROI")
    st.progress(min(max(class_probability,0),1), text=f"Model probability of being in the dataset's higher-value class: {class_probability:.0%}")
    c4,c5 = st.columns(2)
    c4.metric("Illustrative annual rent", f"₹{annual_rent:,.0f}")
    c5.metric("Rent yield entered", f"{rent_yield:.1f}%")
    st.info("Future value uses your assumed constant annual growth rate. It is a scenario calculation, not a market forecast. Purchase costs, taxes, maintenance, vacancy and financing are not included.")
    st.write("**Selected inputs**")
    st.dataframe(input_df, use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Dataset overview")
    a,b,c = st.columns(3)
    a.metric("Properties in sample dataset", f"{len(data):,}")
    b.metric("Median sample price", f"₹{data['price_inr'].median():,.0f}")
    c.metric("Cities represented", data["city"].nunique())
    st.write("Preview")
    st.dataframe(data.head(15), use_container_width=True, hide_index=True)
    left,right = st.columns(2)
    with left:
        fig, ax = plt.subplots()
        data.groupby("city")["price_inr"].median().sort_values().plot(kind="barh", ax=ax)
        ax.set_title("Median sample price by city")
        ax.set_xlabel("Price (INR)")
        st.pyplot(fig)
        plt.close(fig)
    with right:
        fig, ax = plt.subplots()
        ax.scatter(data["area_sqft"], data["price_inr"], alpha=.35)
        ax.set_title("Area vs sample price")
        ax.set_xlabel("Area (sq. ft.)")
        ax.set_ylabel("Price (INR)")
        st.pyplot(fig)
        plt.close(fig)
    st.caption("This dataset is synthetically generated for learning and testing. It is not scraped or verified real market data.")

with tab3:
    st.subheader("Held-out test-set metrics")
    m1,m2,m3,m4 = st.columns(4)
    m1.metric("MAE", f"₹{metrics['MAE (₹)']:,.0f}")
    m2.metric("RMSE", f"₹{metrics['RMSE (₹)']:,.0f}")
    m3.metric("R²", f"{metrics['R²']:.3f}")
    m4.metric("Classification accuracy", f"{metrics['Classification accuracy']:.1%}")
    st.write("**How to interpret:** MAE is average absolute prediction error; RMSE penalizes large errors more; R² measures variance explained on this synthetic held-out test set. Classification predicts whether a sample is at/above the dataset median, not whether an investment is objectively good.")
    pred_plot = pd.DataFrame({"Actual": metrics["y_test"].to_numpy(), "Predicted": metrics["pred"]})
    fig, ax = plt.subplots()
    ax.scatter(pred_plot["Actual"], pred_plot["Predicted"], alpha=.45)
    low = min(pred_plot.min())
    high = max(pred_plot.max())
    ax.plot([low,high],[low,high], linestyle="--")
    ax.set_xlabel("Actual price (INR)")
    ax.set_ylabel("Predicted price (INR)")
    ax.set_title("Actual vs predicted on test set")
    st.pyplot(fig)
    plt.close(fig)

with tab4:
    st.subheader("Project methodology")
    st.markdown("""
    1. **EDA:** inspect distributions, city-level median prices and area-price relationship.
    2. **Preprocessing:** median imputation + standard scaling for numeric inputs; most-frequent imputation + one-hot encoding for city.
    3. **Regression:** Random Forest Regressor predicts the sample price.
    4. **Classification:** Random Forest Classifier predicts the synthetic dataset's above-median-price class.
    5. **Evaluation:** train/test split with fixed random seed; MAE, RMSE, R² and accuracy.
    6. **Future value scenario:** `predicted current value × (1 + assumed annual growth rate) ^ years`.
    7. **Limitations:** synthetic dataset; no live listings, location-level transaction data, legal checks, interest, taxes or transaction costs.
    """)
    st.warning("For a real investment decision, replace the synthetic data with verified recent transaction/listing data and consult qualified local professionals.")
