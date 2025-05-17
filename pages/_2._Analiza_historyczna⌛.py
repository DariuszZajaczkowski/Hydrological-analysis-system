import qrcode
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import io
import matplotlib.pyplot as plt
from scipy import stats

#Dodanie bazy danych (przetworzonej wczesniej w pliku Database.ipynb)--------------------------------------------------------------------------------------------------------

url = "https://github.com/DariuszZajaczkowski/Hydrological-analysis-system/raw/main/dane_hydrologiczne_msc/data_merged.csv"
data = pd.read_csv(url, encoding="Windows-1250")

st.set_page_config(page_title="System analiz powodziowych", layout="wide")

st.markdown("""
            <div style='text-align: left;'>
            <span style = "font-size: 20px; font-weight: bold;">
            SEKCJA II - Analiza historyczna dla Polski
            </span>
        </div>   
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.5, 1.5, 1.5])  # Tworzy 3 kolumny----------------------------------------------------------------------------------------------------------
# Stylizacja dla kolumny 1--------------------------------------------------------------------------------------------------------------------------------------------------
with col1:
    st.markdown("""
        <div style= "border: 2px solid #000000; border-radius: 15px; padding: 15px; text-align: center; 
                    box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.2);">
                <span style=" font-weight: normal; color: #333333;">
            Wybierz parametry analizy ⚙️
                </span>
        </div>
                
    """, unsafe_allow_html=True)

    #Dodanie przycisków rozwijanych z wyborem roku analizy
    data['year'] = data['year'].astype(int)
    year = sorted(data['year'].unique().tolist(), reverse=True)
    year.insert(0, 'Wszystkie lata') # Dodaję opcję "Wszystkie lata" na początek listy dlatego jako 0 aby było pierwsze na liście
    selected_year = st.selectbox("Wybierz rok:", year)


    if selected_year != "Wszystkie lata":
        filtered_data = data[data['year'] == selected_year]
    
    #Dodanie przycisku z wyborem rzeki
    #river = sorted(data['river'].unique().tolist())
    #river.insert(0, 'Wszystkie rzeki')
    #selected_river = st.selectbox("Wybierz rzekę:", river)

# month = sorted(data['month'].unique().tolist(), reverse=True)
# month.insert(0, 'Wszystkie miesiące') #Ta sama procedura co w przypadku możliwości wyboru wszystkich lat
# with col1:
#     selected_month = st.selectbox('Wybierz miesiąc', month, key ='month', label_visibility="visible")
# if month == 'Wszystkie miesiące':
#     selected_month = data
# else:
#     month = data[data['month'] == selected_month]

# Stylizacja dla kolumny 2--------------------------------------------------------------------------------------------------------------------------------------------------
with col2:
    st.markdown("""
        <div style="border: 2px solid #000000; border-radius: 15px; padding: 15px; text-align: center; 
                    box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.2);">
            Średnie miesięczne sumy opadów w wybranym roku 🌧️
        </div>
    """, unsafe_allow_html=True)

    if selected_year == "Wszystkie lata":
        # Obliczanie średnich sum opadów dla każdego miesiąca w całym zbiorze danych
        monthly_data = data.groupby("month")["monthly_precip_sum"].mean().reset_index()
    else:
        monthly_data = filtered_data.groupby("month")["monthly_precip_sum"].mean().reset_index()

    #Rysowanie wykresu z Matplotlib
    fig, ax = plt.subplots(figsize=(7,6.8))
    
    # Wykres kolumnowy, gdzie muszę określić ax.bar(): Używam teraz bezpośrednio kolumn monthly_data['month'] i monthly_data['monthly_precip_sum'] do narysowania wykresu. 
    # W poprzednim kodzie było monthly_data.index i monthly_data.values, ale index zawierał wartości od 0, co powodowało błąd.
    ax.bar(monthly_data['month'], monthly_data['monthly_precip_sum'], color="skyblue")

    # Dostosowanie tytułów, etykiet, osi
    ax.set_xlabel('Miesiąc', fontsize=9, fontweight='bold', color='gray')
    ax.set_ylabel('Średnia suma opadów (mm)', fontsize=9, fontweight='bold', color='gray')
    ax.tick_params(axis='x', labelsize=9, rotation=0)
    ax.tick_params(axis='y', labelsize=9)
    # Ustawienia przerywanej, szarej linii na osi X -> Nie wyglądało to najlepiej, ale zostawiam w komentarzu
    #ax.grid(axis='y', color='lightgray', linestyle='--', linewidth=0.7)  # Przerywana linia dla osi X

    st.pyplot(fig)

# Stylizacja dla kolumny 3--------------------------------------------------------------------------------------------------------------------------------------------------
with col3:
    st.markdown("""
        <div style="border: 2px solid #000000; border-radius: 15px; padding: 15px; text-align: center; 
                    box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.2);">
            Wieloletnie zmiany sum opadów 📉 oraz stanów wód 🌊
        </div>
    """, unsafe_allow_html=True)

    min_year = int(data['year'].min())
    max_year = int(data['year'].max())
  
    st.markdown(
    """
    <style>  
        /* Zmiana koloru kółka (uchwytu) suwaka */
        div[data-baseweb="slider"] > div > div > div {
            background: black !important; /* Czarny uchwyt */
            border: 2px solid white !important; /* Biała obwódka dla kontrastu */
        }
    </style>
    """,
    unsafe_allow_html=True
)
    
    years_range = st.slider(
        "Wybierz zakres lat:",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year),
        step=1
    )

    #Filtrowanie do wybranego zakresu dat
    selected_years_range = data[(data['year'] >= years_range[0]) & (data['year'] <= years_range[1])]

    # Obliczanie średnich sum opadów dla wszystkich lat
    #selected_years_range = data.groupby(['year', 'month'])['monthly_precip_sum'].mean().reset_index()
    fig, ax = plt.subplots()

    # Grupa danych - średnie miesięczne opady dla każdego roku
    avg_yearly_precip = selected_years_range.groupby('year')['monthly_precip_sum'].mean().reset_index()

    # Rysowanie wykresu
    ax.plot(avg_yearly_precip['year'], avg_yearly_precip['monthly_precip_sum'], color='skyblue', label='Średnie opady', marker='o')

    # Nałożenie linii trendu
    slope, intercept, r_value, p_value, std_err = stats.linregress(avg_yearly_precip['year'], avg_yearly_precip['monthly_precip_sum'])
    trend_line = slope * avg_yearly_precip['year'] + intercept
    ax.plot(avg_yearly_precip['year'], trend_line, color='black', linestyle='--', linewidth = 1, label='Linia trendu')

    # Dostosowanie tytułów i etykiet
    ax.set_xlabel('Rok', fontsize=9, color = 'gray', fontweight='bold')
    ax.set_ylabel('Średnia suma opadów (mm)', fontsize=9, color = 'gray', fontweight='bold')
    ax.tick_params(axis='x', labelsize=9, rotation=0)

    ax.tick_params(axis='y', labelsize=9)
    ax.legend(fontsize=9, loc='upper left')

    # Wyświetlanie wykresu
    st.pyplot(fig)
    
# Stylizacja dla kolumny 3--------------------------------------------------------------------------------------------------------------------------------------------------
with col3:
    
# Obliczanie średnich sum opadów dla wszystkich lat
    #selected_years_range = data.groupby(['year', 'month'])['monthly_precip_sum'].mean().reset_index()
    fig, ax = plt.subplots()

    # Grupa danych - średnie miesięczne opady dla każdego roku
    avg_yearly_water_level = selected_years_range.groupby('year')['water_level'].mean().reset_index()

    # Rysowanie wykresu
    ax.bar(avg_yearly_precip['year'], avg_yearly_water_level['water_level'], color='skyblue', label='Stany wód')

    # Nałożenie linii trendu
    slope, intercept, r_value, p_value, std_err = stats.linregress(avg_yearly_precip['year'], avg_yearly_water_level['water_level'])
    trend_line = slope * avg_yearly_precip['year'] + intercept
    ax.plot(avg_yearly_precip['year'], trend_line, color='black', linestyle='--', linewidth = 1, label='Linia trendu')

    # Dostosowanie tytułów i etykiet
    ax.set_xlabel('Rok', fontsize=9, color = 'gray', fontweight='bold')
    ax.set_ylabel('Średnie stany wód [cm]', fontsize=9, color = 'gray', fontweight='bold')
    ax.tick_params(axis='x', labelsize=9, rotation=0)
    ax.tick_params(axis='y', labelsize=9)
    ax.legend(fontsize=9, loc='upper left')

    # Wyświetlanie wykresu
    st.pyplot(fig)



   
