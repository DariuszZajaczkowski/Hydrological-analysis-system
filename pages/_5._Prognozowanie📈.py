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

url_data = "https://github.com/DariuszZajaczkowski/Hydrological-analysis-system/raw/main/dane_hydrologiczne_msc/data_merged.csv"
data = pd.read_csv(url_data, encoding="Windows-1250")

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
            SEKCJA V - Predykcja za pomocą modelu XGBoost
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
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Tworzenie i trenowanie modelu
model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=30,
                         learning_rate=0.9,
                         max_depth=2,
                         min_child_weight=1,
                         random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

st.write("Zaimplementowany model XGBoost pozwala na wykonanie analiz prognostycznych. Na potrzeby projeketu prognoza stanów wód jest ograniczona do końca 2024 roku. Ze względu na dynamiczny charakter środowiska i jego szybką responsywność, tak daleka prognoza powinna być traktowana jako duże uogólnienie przyszłej sytuacji hydrologicznej.")
st.write("Dane pochodzą z lat 1990-2023")
col1, col2 = st.columns([0.25,1])
with col1:
    st.markdown("""
        <div style= "border: 2px solid #000000; border-radius: 15px; padding: 15px; text-align: center; 
                    box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.2);">
                <span style=" font-weight: normal; color: #333333;">
            Wybierz parametry analizy ⚙️
                </span>
        </div>
                
    """, unsafe_allow_html=True)

    # Lista unikalnych regionów z uwzględnieniem 'Wszystkie'
    regiony = ['Wszystkie regiony'] + sorted(spatial_data['obszar'].dropna().unique().tolist())
    region_box = st.selectbox("Wybierz region", regiony)
# Filtruj dane po regionie, jeśli wybrano coś innego niż 'Wszystkie'
    filtered_data = spatial_data.copy()
    if region_box != 'Wszystkie regiony':
        filtered_data = filtered_data[filtered_data['obszar'] == region_box]
    
# Dynamiczna lista województw na podstawie regionu
    wojewodztwa = ['Wszystkie województwa'] + sorted(filtered_data['state'].dropna().unique().tolist())
    wojewodztwo_box = st.selectbox("Wybierz województwo", wojewodztwa)
# Filtruj dalej po województwie
    if wojewodztwo_box != 'Wszystkie województwa':
        filtered_data = filtered_data[filtered_data['state'] == wojewodztwo_box]

# Lista stacji na podstawie wyżej wybranych
    stacje = ['Wszystkie stacje'] + sorted(filtered_data['station'].dropna().unique().tolist())
    station_box = st.selectbox("Wybierz stację", stacje)
# Filtrowanie po stacji
    if station_box != 'Wszystkie stacje':
        filtered_data = filtered_data[filtered_data['station'] == station_box]


with col2:
    #Obliczanie średnich histroycznych zmiennych parametrów:
    avg_features = filtered_data.groupby(['month'])[["monthly_precip_sum", "snowfall_days", "max_precip", "water_flow"]].mean().reset_index()

# Generowanie danych wejściowych na 2023 rok
    future_years = [2023]
    future_data = []
    for year in future_years:
        for month in range(1, 13):
            row = avg_features[avg_features["month"] == month].iloc[0]
            future_data.append({
            "year": year,
            "month": month,
            "monthly_precip_sum": row["monthly_precip_sum"],
            "snowfall_days": row["snowfall_days"],
            "max_precip": row["max_precip"],
            "water_flow": row["water_flow"]
        })

    future_df = pd.DataFrame(future_data)

    # Przewidywanie poziomu wód
    future_df["water_level_pred"] = model.predict(future_df[features])

    # Łączenie z danymi historycznymi do wykresu
    history_plot = filtered_data[["year", "month", "water_level"]].copy()
    history_plot["source"] = "Zarejestrowane"
    future_plot = future_df[["year", "month", "water_level_pred"]].rename(columns={"water_level_pred": "water_level"})
    future_plot["source"] = "Prognoza"
    combined = pd.concat([history_plot, future_plot])

    # Tworzenie zmiennej czasu do wykresu
    combined["time"] = combined["year"] + (combined["month"] - 1) / 12
with col2:
    # Wykres
    fig, ax = plt.subplots(figsize=(10, 5))
    for source, group in combined.groupby("source"):
        ax.plot(group["time"], group["water_level"], label=source if source == "Prognoza" else "-", marker='o' if source == "Zarejestrowane" else None)

    ax.set_title("Zarejestrowane i prognozowane stany wód do 2023 roku", fontsize=14)
    ax.set_xlabel("Rok", fontsize=12)
    ax.set_ylabel("Stan wód (cm)", fontsize=12)
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

st.write("")
st.write("")

with st.form("predict_form"):
    st.write("Wprowadź dane do prognozy poziomu wód")

    # Wybór stacji (zakładając, że masz kolumnę 'station' w danych)
    stacja = st.selectbox("Wybierz stację", options=filtered_data['station'].unique())

    rok = st.number_input("Rok", min_value=1990, max_value=2030, value=2025)
    miesiac = st.number_input("Miesiąc", min_value=1, max_value=12, value=7)
    opady = st.number_input("Suma opadów (mm)", value=60.0)
    dni_snieg = st.number_input("Dni ze śniegiem", value=0)
    max_opad = st.number_input("Maksymalny opad (mm)", value=25.0)
    przeplyw = st.number_input("Przepływ (m³/s)", value=80.0)

    submit = st.form_submit_button("Prognozuj")

    if submit:
        # Filtrowanie danych stacji
        stacja_data = filtered_data[filtered_data['station'] == stacja]

        # Tworzenie danych wejściowych
        input_df = pd.DataFrame([{
            "year": rok,
            "month": miesiac,
            "monthly_precip_sum": opady,
            "snowfall_days": dni_snieg,
            "max_precip": max_opad,
            "water_flow": przeplyw
        }])

        # Prognoza na podstawie danych stacji i danych wejściowych
        # Zastosowanie modelu na podstawie stacji i danych wejściowych
        prognoza = model.predict(input_df)[0]

        st.success(f"Przewidywany poziom wody na stacji {stacja} na {rok}-{miesiac:02d}: {prognoza:.2f} cm")
