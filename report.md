# Real Estate Investment Advisor: Predicting Property Profitability & Future Value

## Abstract
This project demonstrates a machine-learning workflow for estimating property prices and exploring investment scenarios through a Streamlit dashboard. The application uses property attributes such as city, area, bedrooms, bathrooms, property age, location score, amenities and rent yield. A Random Forest regression model predicts sample property price; a Random Forest classifier identifies whether a property is at or above the sample dataset median. The dashboard also calculates a user-defined future-value scenario.

## Problem statement
Property buyers and students often need a structured way to compare property attributes and understand the possible effect of price growth and rent yield. The project demonstrates how data preprocessing, machine learning, visual analytics and a web interface can support exploratory analysis.

## Objectives
1. Prepare a structured housing dataset.
2. Explore city and area-related price patterns.
3. Build a regression model for estimated price.
4. Build a classification model for the dataset's above-median price class.
5. Evaluate model results using appropriate metrics.
6. Provide a Streamlit interface for user inputs and scenario calculations.
7. Track training runs and metrics with MLflow.

## Technology stack
Python, Pandas, NumPy, scikit-learn, Matplotlib, Streamlit, MLflow and CSV.

## Dataset and features
The included dataset contains 1,200 synthetic records. Features: city, area_sqft, bedrooms, bathrooms, property_age_years, location_score, amenities_count and annual_rent_yield_pct. Target: price_inr. The dataset is generated for demonstration only and is not verified market data.

## Methodology
1. Load and inspect the dataset.
2. Perform exploratory analysis with city-level median price and area-price plots.
3. Split data into training and test partitions (80/20; random state 42).
4. Impute missing numeric values with median and scale numeric features.
5. Impute categorical values with most-frequent value and one-hot encode city.
6. Train Random Forest Regressor for price prediction.
7. Train Random Forest Classifier for above-median price class.
8. Evaluate with MAE, RMSE, R² and classification accuracy.
9. Present predictions and scenario outputs in Streamlit.
10. Record model parameters and metrics using MLflow training script.

## Future value and profitability scenario
The dashboard calculates future value as:

**Future Value = Predicted Current Value × (1 + Annual Growth Rate) ^ Number of Years**

Projected gain is future value minus the user-entered purchase price. ROI is projected gain divided by purchase price, multiplied by 100. This simplified scenario excludes taxes, stamp duty, registration, maintenance, financing costs, vacancy, liquidity and other transaction costs. It is not a guarantee or professional investment advice.

## Evaluation metrics
- **MAE:** mean absolute difference between actual and predicted prices.
- **RMSE:** square root of mean squared error; more sensitive to large errors.
- **R²:** variance explained by the model on the held-out test data.
- **Accuracy:** fraction of correct predictions for the above-median class.

Actual metric values are calculated when the application or training script runs. Since the data is synthetic, metrics reflect this educational dataset and do not prove real-market performance.

## Results and discussion
The app provides a property input panel, estimated price, future value scenario, illustrative annual rent, EDA visualizations and a model evaluation tab. It clearly identifies the dataset as synthetic. Model quality should be re-evaluated after replacing the data with verified local market observations.

## Limitations
- Synthetic dataset is not representative of actual prices.
- Location score is a simplified proxy and not a real geospatial feature.
- Future value assumes a constant user-selected growth rate.
- No taxes, loans, repairs, transaction costs, rent vacancy or regulatory due diligence are modeled.
- Classification target is based on dataset median, not investment suitability.

## Future scope
Integrate reliable verified listings or transaction records, add locality and geospatial attributes, include EMI and ownership costs, test gradient boosting models, use time-aware validation for dated market data, and add explainability and model monitoring.

## Conclusion
The project demonstrates an end-to-end beginner-friendly real-estate ML application: data preparation, EDA, feature engineering, regression, classification, model evaluation, MLflow tracking and an interactive Streamlit dashboard. It is a learning prototype and must be trained on verified real-world data before any real investment use.
