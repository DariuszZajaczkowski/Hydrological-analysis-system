import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import numpy as np
from scipy.stats import gaussian_kde

#Dodanie bazy danych (przetworzonej wczesniej w pliku Database.ipynb)--------------------------------------------------------------------------------------------------------

url_data = "https://github.com/DariuszZajaczkowski/Hydrological-analysis-system/raw/main/dane_hydrologiczne_msc/data_merged.csv"
data = pd.read_csv(url_data, encoding="Windows-1250")

# Sprawdzenie i usunięcie wartości NaN lub Inf w kolumnie 'water_level'
data = data[~data["water_level"].isna()]  # Usuwa NaN
data = data[~data["water_level"].isin([np.inf, -np.inf])]  # Usuwa Inf


st.set_page_config(
    page_title="Analiza statystyczna",
    layout="wide"
)

st.markdown("""
            <div style='text-align: left;'>
            <span style = "font-size: 20px; font-weight: bold;">
            SEKCJA VI - Analiza statystyczna
            </span>
        </div>   
    """, unsafe_allow_html=True)

st.write("Szczegółowa analiza kluczowych wskaźników statystycznych pozwala na wnikliwe rozpoznanie struktury danych, które wykorzystano w projekcie. Na pierwszy rzut oka wysuwają sie wartości odstające na wizualizacjach boxplotowych. ")
st.write("Charakter geograficzny analizy uniemożliwia ich wykluczenie ze względu na jakościową wartość pomiarową, która sugeruje występowanie anomali w środowisku naturalnym. Jak w statystyce teoretycznej takie wartości podlegają ekstrakcji, tak w analizie środowiskowej - dostarczają istotnych informacji o zjawiskach ekstremalnych.")
col1, col2 = st.columns([1,1])

with col1:
    st.markdown("""
        <div style= "border: 2px solid #000000; border-radius: 15px; padding: 15px; text-align: center; 
                    box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.2);">
                <span style=" font-weight: normal; color: #333333;">
            Statystyka stanów wód w Polsce
                </span>
        </div>
                
    """, unsafe_allow_html=True)

    fig = px.box(data, x=data["month"], y=data["water_level"])
    fig.update_traces(marker_color='skyblue')
    fig.update_layout(
        xaxis_title="Miesiąc",                     # Tytuł osi X
        yaxis_title="Miesięczne stany wód [m]"  # Tytuł osi Y
    )
    st.plotly_chart(fig)

    fig2 = px.histogram(data, x=data["water_level"])
    fig2.update_traces(marker_color='skyblue')
    fig2.update_layout(
        xaxis_title="Stany wód [m]",             # Tytuł osi X
        yaxis_title="Liczba wystąpień [n]"       # Tytuł osi Y
    )
    st.plotly_chart(fig2)

    st.markdown("""
        <div style= "border: 2px solid #000000; border-radius: 15px; padding: 15px; text-align: center; 
                    box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.2);">
                <span style=" font-weight: normal; color: #333333;">
            Statystyka danych przepływów wód w Polsce
                </span>
        </div>
                
    """, unsafe_allow_html=True)
    fig5 = px.box(data, x=data["month"], y=data["water_flow"])
    fig5.update_traces(marker_color='skyblue')
    fig5.update_layout(
        xaxis_title="Miesiąc",                     # Tytuł osi X
        yaxis_title="Miesięczne średnie przepływy wód [m]"  # Tytuł osi Y
    )
    st.plotly_chart(fig5)

    fig6 = px.histogram(data, x=data["water_flow"])
    fig6.update_traces(marker_color='skyblue')
    fig6.update_layout(
        xaxis_title="Przepływy wód [m]",             # Tytuł osi X
        yaxis_title="Liczba wystąpień [n]"       # Tytuł osi Y
    )
    st.plotly_chart(fig6)

with col2:
    st.markdown("""
        <div style= "border: 2px solid #000000; border-radius: 15px; padding: 15px; text-align: center; 
                    box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.2);">
                <span style=" font-weight: normal; color: #333333;">
            Statystyka danych opadów atmosferycznych
                </span>
        </div>
                
    """, unsafe_allow_html=True)

    fig3 = px.box(data, x=data["month"], y=data["monthly_precip_sum"])
    fig3.update_traces(marker_color='skyblue') #Ustawienie koloru wyświetlania danych
    fig3.update_layout(
        xaxis_title="Miesiąc", # Tytuł osi X
        yaxis_title="Średnie miesiećzne sumy opadów [mm]" # Tytuł osi Y
    )
    st.plotly_chart(fig3)

    fig4=px.histogram(data, x=data["monthly_precip_sum"])
    fig4.update_traces(marker_color='skyblue')
    fig4.update_layout(
        xaxis_title="Miesiąc", # Tytuł osi X
        yaxis_title="Liczba wystąpień [n]" # Tytuł osi Y
    )
    st.plotly_chart(fig4)

    st.markdown("""
        <div style= "border: 2px solid #000000; border-radius: 15px; padding: 15px; text-align: center; 
                    box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.2);">
                <span style=" font-weight: normal; color: #333333;">
            Statystyka najwyższych zanotowanych sum opadów w ciągu dnia
                </span>
        </div>
                
    """, unsafe_allow_html=True)

    fig7 = px.box(data, x=data["month"], y=data["max_precip"])
    fig7.update_traces(marker_color='skyblue') #Ustawienie koloru wyświetlania danych
    fig7.update_layout(
        xaxis_title="Miesiąc", # Tytuł osi X
        yaxis_title="Maksymalne opady atmosferyczne [mm]" # Tytuł osi Y
    )
    st.plotly_chart(fig7)

    fig8=px.histogram(data, x=data["max_precip"])
    fig8.update_traces(marker_color='skyblue')
    fig8.update_layout(
        xaxis_title="Miesiąc", # Tytuł osi X
        yaxis_title="Liczba wystąpień [n]" # Tytuł osi Y
    )
    st.plotly_chart(fig8)
