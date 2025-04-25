import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from xgboost import XGBRegressor
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from scipy.stats import uniform, randint
from sklearn.linear_model import LinearRegression

data = pd.read_csv("C:/Users/dzaja/OneDrive/Pulpit/Studia_DSAD/Projekt_zaliczeniowy/dane_hydrologiczne_msc/data_merged.csv", encoding='Windows-1250')
url = "https://github.com/DariuszZajaczkowski/Hydrological-analysis-system/raw/main/stations_full.csv"
stations = pd.read_csv(url, encoding="Windows-1250")
spatial_data = pd.merge(data, stations, on = ['station'], how = 'inner')

st.set_page_config(
    page_title="Predykcja za pomocą modelu XGBoost",
    layout="wide"
)
st.markdown("""
            <div style='text-align: left;'>
            <span style = "font-size: 20px; font-weight: bold;">
            SEKCJA IV - Predykcja za pomocą modelu XGBoost
            </span>
        </div>   
    """, unsafe_allow_html=True)


features = ["year", "month", "monthly_precip_sum", "snowfall_days", "max_precip", "water_flow"]
target = "water_level"
model_data = spatial_data.dropna(subset=features + [target])


#Podział na X (cechy) i y (target)
X = model_data[features]
y = model_data[target]

#Podział na zbiór treningowy i testowy (80/20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

#Tworzenie i trenowanie modelu
model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=70,
                         learning_rate=0.1,
                         max_depth=5,
                         min_child_weight=2,
                         random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
