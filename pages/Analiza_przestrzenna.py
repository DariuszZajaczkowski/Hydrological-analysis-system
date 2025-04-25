
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import plotly.express as px
import plotly.graph_objects as go

url_data = "https://github.com/DariuszZajaczkowski/Hydrological-analysis-system/raw/main/dane_hydrologiczne_msc/data_merged.csv"
data = pd.read_csv(url_data, encoding="Windows-1250")

url = "https://github.com/DariuszZajaczkowski/Hydrological-analysis-system/raw/main/stations_full.csv"
stations = pd.read_csv(url, encoding="Windows-1250")
spatial_data = pd.merge(data, stations, on = ['station'], how = 'inner')

st.set_page_config(
    page_title="Analiza przestrzenna",
    layout="wide"
)
st.markdown("""
            <div style='text-align: left;'>
            <span style = "font-size: 20px; font-weight: bold;">
            SEKCJA II - Analiza przestrzenna
            </span>
        </div>   
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.4,1,1])

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

# Dynamiczna lista stacji na podstawie wyżej wybranych
    stacje = ['Wszystkie stacje'] + sorted(filtered_data['station'].dropna().unique().tolist())
    station_box = st.selectbox("Wybierz stację", stacje)
# Ostateczne filtrowanie po stacji
    if station_box != 'Wszystkie stacje':
        filtered_data = filtered_data[filtered_data['station'] == station_box]


with col2:

    annual_precip = filtered_data.groupby(['station', 'year'])['monthly_precip_sum'].sum().reset_index()
    average_annual_precip = annual_precip.groupby('year')['monthly_precip_sum'].mean().reset_index()
    # Dane
    x = average_annual_precip['year']
    y = average_annual_precip['monthly_precip_sum']

    # Regresja liniowa (linia trendu)
    z = np.polyfit(x, y, 1)  # dopasowanie prostej (1 oznacza stopień wielomianu)
    p = np.poly1d(z)

    # Rysuj wykres
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o', linestyle='-', color='b', label='Średnie opady')
    plt.plot(x, p(x), linestyle='--', color='black', label='Linia trendu')  # linia trendu
    plt.title("Średnie roczne sumy opadów w latach 1989 - 2022", fontsize=19)
    plt.xlabel("Rok", fontsize=12)
    plt.ylabel("Średnia suma opadów (mm)", fontsize=12)
    plt.grid(True)
    plt.legend()
    plt.xticks(rotation=0)
    plt.tight_layout()
    st.pyplot(plt)

    annual_water_level = filtered_data.groupby(['station', 'year'])['water_level'].sum().reset_index()
    average_water_level = annual_water_level.groupby('year')['water_level'].mean().reset_index()
    x = average_water_level['year']
    y = average_water_level['water_level']
    # Regresja liniowa (linia trendu)
    z = np.polyfit(x, y, 1)  # dopasowanie prostej (1 oznacza stopień wielomianu)
    p = np.poly1d(z)
    plt.figure(figsize=(10, 6))
    plt.bar(average_water_level['year'], average_water_level['water_level'], color='skyblue')
    plt.plot(x, p(x), linestyle='--', color='black', label='Linia trendu')  # linia trendu
    plt.title("Średnie roczne stany wód w latach 1989 - 2022", fontsize=19)
    plt.xlabel("Rok", fontsize=12)
    plt.ylabel("Średnie stany wód [cm]", fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=0)
    plt.tight_layout()
    st.pyplot(plt)    

with col3:
    monthly_precip= filtered_data.groupby(['month'])['monthly_precip_sum'].mean().reset_index()
    monthly_precip_sum = monthly_precip.groupby('month')['monthly_precip_sum'].mean().reset_index()
    plt.figure(figsize=(10, 5.45))
    plt.plot(monthly_precip_sum['month'], monthly_precip_sum['monthly_precip_sum'], marker='o', linestyle='-', color='b')
    plt.title("Średnie miesięczne sumy opadów w latach 1989 - 2022", fontsize=16)
    plt.xlabel("Miesiąc")
    plt.ylabel("Średnia suma opadów [mm]]")
    plt.xticks(monthly_precip_sum['month'], labels=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
    plt.grid(True)
    st.pyplot(plt)

    monthly_water_level= filtered_data.groupby(['month'])['water_level'].mean().reset_index()
    monthly_water_level_sum = monthly_water_level.groupby('month')['water_level'].mean().reset_index()
    plt.figure(figsize=(10, 5.45))
    plt.bar(monthly_water_level_sum['month'], monthly_water_level_sum['water_level'], color='skyblue')
    plt.title("Średnie miesięczne stany wód w latach 1989 - 2022", fontsize=16)
    plt.xlabel("Miesiąc")
    plt.ylabel("Średnia suma opadów [mm]]")
    plt.xticks(monthly_water_level_sum['month'], labels=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(plt)

st.markdown("---")
st.markdown("""
<div style="font-size:16px; font-weight:bold; text-align:center; margin-top:25px;">
    Interkatywny wykres przebiegu wieloletniego miesięcznych sum opadów oraz stanów wód
</div>
""", unsafe_allow_html=True)

filtered_data['date'] = pd.to_datetime(filtered_data[['year', 'month']].assign(day=1))

# Średnie miesięczne wartości
monthly_avg_precip = (
    filtered_data.groupby('date')['monthly_precip_sum']
    .mean()
    .reset_index()
    .rename(columns={'monthly_precip_sum': 'Suma opadów [mm]'})
)

monthly_avg_water = (
    filtered_data.groupby('date')['water_level']
    .mean()
    .reset_index()
    .rename(columns={'water_level': 'Stan wód [cm]'})
)

# Tworzenie wykresu
fig = go.Figure()

# Linia – opady
fig.add_trace(go.Scatter(
    x=monthly_avg_precip['date'],
    y=monthly_avg_precip['Suma opadów [mm]'],
    mode='lines+markers',
    name='Suma opadów [mm]',
    line=dict(color='blue', width=2),
    marker=dict(size=4),
    yaxis='y1'
))

# Słupki – stany wód
fig.add_trace(go.Bar(
    x=monthly_avg_water['date'],
    y=monthly_avg_water['Stan wód [cm]'],
    name='Stan wód [cm]',
    marker_color='skyblue',
    opacity=0.6,
    yaxis='y2'
))
fig.update_layout(
    xaxis=dict(title='Data'),

    yaxis=dict(
        title=dict(text='Suma opadów [mm]', font=dict(color='black')),
        tickfont=dict(color='black')
    ),

    yaxis2=dict(
        title=dict(text='Stan wód [cm]', font=dict(color='black')),
        tickfont=dict(color='black'),
        overlaying='y',
        side='right',
        showgrid=False
    ),

    legend=dict(x=0.5, y=1.15, orientation='h', xanchor='center'),
    height=500
)

# Layout i suwak
fig.update_layout(
    xaxis=dict(
        title='Data',
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1R", step="year", stepmode="backward"),
                dict(count=5, label="5L", step="year", stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(visible=True),
        type="date"
    ),
    yaxis=dict(title='Wartości'),
    barmode='overlay',
    template='plotly_white',
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# Grupuje po regionach i miesiącach, oblicza średnie miesięczne sumy opadów, stany wód i przepływ
monthly_data = spatial_data.groupby(['obszar']).agg(
    avg_monthly_precip=('monthly_precip_sum', 'mean'),
    avg_water_level=('water_level', 'mean'),
    avg_water_flow=('water_flow', 'mean')
).reset_index()

monthly_data.columns = ['Region', 'Średnia suma opadów [mm]', 'Średni stan wód [cm]', 'Średni przepływ wód [m³/s]']

# Wyświetlenie tabeli w Streamlit
st.markdown("""
<div style="font-size:16px; font-weight:bold; text-align:center; margin-top:25px;">
    Średnie miesięczne sumy opadów, stany wód i przepływ wód dla regionów
</div>
""", unsafe_allow_html=True)
st.dataframe(monthly_data)
