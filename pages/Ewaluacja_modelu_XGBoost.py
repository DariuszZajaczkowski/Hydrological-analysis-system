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
from sklearn.model_selection import RandomizedSearchCV

url_data = "https://github.com/DariuszZajaczkowski/Hydrological-analysis-system/raw/main/dane_hydrologiczne_msc/data_merged.csv"
data = pd.read_csv(url_data, encoding="Windows-1250")

url = "https://github.com/DariuszZajaczkowski/Hydrological-analysis-system/raw/main/stations_full.csv"
stations = pd.read_csv(url, encoding="Windows-1250")
spatial_data = pd.merge(data, stations, on = ['station'], how = 'inner')

st.set_page_config(
    page_title="Wprowadzenie modelu XGBoost",
    layout="wide"
)
st.markdown("""
            <div style='text-align: left;'>
            <span style = "font-size: 20px; font-weight: bold;">
            SEKCJA III - Wprowadzenie modelu XGBoost
            </span>
        </div>   
    """, unsafe_allow_html=True)

st.markdown("Ewaluacja modelu")
st.write("Lepszym podejściem do analizy hydrologicznej jest filtrowanie i skupienie się na danych z poszczególnych stacji pomiarowych, ponieważ dane z różnych stacji mogą mieć zupełnie inne charakterystyki ze względu na lokalne warunki hydrologiczne, topografię, klimat regionalny czy zlewnie rzeczne.")
st.write("Mieszanie tych danych w jednym modelu może wprowadzać szum, który negatywnie wpływa na jakość wyników, obniżając skuteczność prognoz i zaburzając efektywność prognozowania modelu. Dlatego analiza na poziomie konkretnej stacji pozwala na bardziej precyzyjne modelowanie, które uwzględnia specyficzne warunki dla danego obszaru.")
st.write("Zmienne wykorzystane w modelu: Region geograficzny, Województwo, Stacja, Miesięczne sumy opadów [mm], Dni z opadem śniegu [n], Maskymalny zarejesdtrowany opad [mm], poziom wód [cm], przeływ wody [cm3/s], temperatura wody [oC]")
col1, col2 = st.columns([0.25,1])

with col1:
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

# Dynamiczna lista stacji na podstawie wyżej wybranych
    stacje = ['Wszystkie stacje'] + sorted(filtered_data['station'].dropna().unique().tolist())
    station_box = st.selectbox("Wybierz stację", stacje)
# Ostateczne filtrowanie po stacji
    if station_box != 'Wszystkie stacje':
        filtered_data = filtered_data[filtered_data['station'] == station_box]


features = ["year", "month", "monthly_precip_sum", "snowfall_days", "max_precip", "water_flow"]
target = "water_level"
model_data = filtered_data.dropna(subset=features + [target])


#Podział na X (cechy) i y (target)
X = model_data[features]
y = model_data[target]

#Podział na zbiór treningowy i testowy (80/20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

#Tworzenie i trenowanie modelu
model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=50,
                         learning_rate=0.1,
                         max_depth=4,
                         min_child_weight=2,
                         random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)



#print(f"Mean Squared Error: {mse:.2f}")
#print(f"R² Score: {r2:.2f}")

with col2:
    # Wykres: Rzeczywiste vs Przewidywane
    fig, ax = plt.subplots(figsize=(4, 1.5))
    ax.scatter(y_test, y_pred, color='skyblue', s=10, alpha=0.7, label='Dane')
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', label='Wymodelowane = rzeczywiste', linewidth = 0.5)
    ax.set_xlabel("Rzeczywisty poziom wody [cm]", fontsize=5)
    ax.set_ylabel("Przewidywany poziom wody [cm]", fontsize=5)
    ax.tick_params(axis='x', labelsize=6)
    ax.tick_params(axis='y', labelsize=6)
    ax.set_title("Porównanie zarejestrowanych i wymodelowanych poziomów wód [cm]", fontsize=6)
    ax.legend(fontsize=5)
    ax.grid(True)

    st.pyplot(fig)

# Oblicz dodatkowe metryki
#Ocena modelu
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
rmse = np.sqrt(mse)
mae = np.mean(np.abs(y_test - y_pred))
N = len(y_test)

# Tabela z metrykami
metrics_df = pd.DataFrame({
    "Metryka": ["Mean Squared Error (MSE) - Błąd średniokwadratowy", "Root Mean Squared Error (RMSE) - Pierwiastek z MSE", "Mean Absolute Error (MAE) - Średni bezwzględny błąd", "R² Score - Współczynnik determinacji", "Liczba obserwacji"],
    "Wartość": [f"{mse:.2f}", f"{rmse:.2f}", f"{mae:.2f}", f"{r2:.2f}", f"{N:.2f}"]
})

st.markdown("<h5 style='text-align: center;'>Wskaźniki efektywności modelu</h5>", unsafe_allow_html=True)
st.table(metrics_df)

st.markdown("<h5 style='text-align: center;'>Macierz korelacji między zmiennymi</h5>", unsafe_allow_html=True)

# Wybieranie tylko kolumn numerycznych - inaczej macierz korelacji się nie wygeneruje
numeric_data = filtered_data.select_dtypes(include=['float64', 'int64'])
numeric_data = numeric_data.drop(columns=['station_nr_x', 'year', 'month', 'lat', 'lon'])
# Obliczanie korelacji na danych numerycznych
correlation_matrix = numeric_data.corr()
# Rozmiar wykresu
plt.figure(figsize=(7, 2))  
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.01)
# Dostosowanie czcionek
#plt.title('Macierz korelacji', fontsize=14, fontweight='bold')  # Tytuł wykresu
plt.xlabel('Zmienne', fontsize=8)  # Etykieta osi X
plt.ylabel('Zmienne', fontsize=8)  # Etykieta osi Y
plt.xticks(fontsize=8, rotation = 45)  # Czcionka dla etykiet osi X
plt.yticks(fontsize=8)  # Czcionka dla etykiet osi Y

# Dostosowanie czcionki dla wartości w komórkach
st.pyplot(plt)
