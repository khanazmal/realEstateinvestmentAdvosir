# Real Estate Investment Advisor

A beginner-friendly BCA project using Python, Pandas, scikit-learn, Streamlit and MLflow.

## Important data note
`data/housing_data.csv` is a **synthetic educational dataset** generated for this project. It is not verified real-world property market data. Predictions demonstrate an ML workflow and should not be used for actual purchase decisions without validated data.

## Features
- Property price regression with Random Forest
- Above-median sample-price classification
- Feature preprocessing: imputation, scaling and one-hot encoding
- EDA charts and data preview
- Evaluation: MAE, RMSE, R² and classification accuracy
- Future value scenario calculator and illustrative rental estimate
- MLflow experiment tracking script
- Streamlit dashboard

## Windows 11 setup
Open this project folder in VS Code. In Terminal, use the full Python path if `python` command is not recognized:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" --version
```

Install dependencies:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" -m pip install -r requirements.txt
```

Run the dashboard:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" -m streamlit run app.py
```

Train and track models with MLflow:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" train_model.py
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" -m mlflow ui
```

Then open the local MLflow UI address shown in the terminal (usually http://127.0.0.1:5000).

## Project structure
- `app.py`: interactive Streamlit application
- `train_model.py`: model training, evaluation, model saving and MLflow tracking
- `data/housing_data.csv`: synthetic sample dataset (1,200 rows)
- `models/`: trained model outputs are created here when train_model.py runs
- `report.pdf`: college-style project report
- `report.md`: editable report source
- `requirements.txt`: Python dependencies

## Models and metrics
- Regression target: `price_inr`
- Classification target: price at or above dataset median
- Regression metrics: MAE, RMSE, R²
- Classification metric: accuracy
- Fixed random seed: 42, test split: 20%

## Limitations and future scope
Replace synthetic data with verified recent property listings/transactions; add locality-level coordinates, transport/school/hospital distances, price-per-sq-ft trends, taxes, fees, maintenance, loan EMI and rental vacancy. Consider time-series forecasting only after collecting sufficient dated historical prices.
