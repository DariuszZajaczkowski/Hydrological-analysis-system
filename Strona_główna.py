import streamlit as st
import pandas as pd
from PIL import Image, ImageOps
import qrcode
from PIL import Image
import io
import folium
from streamlit_folium import st_folium

stations = pd.read_csv("C:/Users/dzaja/OneDrive/Pulpit/Studia_DSAD/Projekt_zaliczeniowy/stations_full.csv", encoding='Windows-1250')

#Określenie adresu url aplikacji aby móc wstawić wygenerowany wcześniej kod QR (Network URL Streamlit)-----------------------------------------------------------------------
url = "http://192.168.100.5:8501"

# Generowanie kodu QR--------------------------------------------------------------------------------------------------------------------------------------------------------
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=20,
    border=1,
)
qr.add_data(url)
qr.make(fit=True)

# Tworzenie obrazu kodu QR
img = qr.make_image(fill="black", back_color="white")

# Zapisanie obrazu QR do bufora w pamięci
buf = io.BytesIO()
img.save(buf)
buf.seek(0)

st.set_page_config(
    page_title="System analiz hydrologicznych",
    layout="wide"
)

# Wyświetl obraz QR w aplikacji Streamlit
st.image(buf, caption= "Analizuj mobilnie 🧐",width=110)

st.markdown("<h1 style='text-align: center;'>🌧️ System Analiz Hydrologicznych 🌊</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: left;'>Projekt zakłada stworzenie systemu do analizy i prognoz hydrologicznych w oparciu o dane meteorologiczne i hydrologiczne z otwartej bazy danych Instytutu Meteorologii i Gospodarki Wodnej - Państwowego Instytutu Badawczego. System został zaprojektowany z myślą o analizie zjawisk hydrologicznych i meteorologicznych, takich jak stany wód, opady atmosferyczne czy przepływy rzeczne, z uwzględnieniem zróżnicowania przestrzeni geograficznej w Polsce.</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: left;'>Mocną stroną projektu jest implemetnacja modelu opartego na algorytmie XGBoost, który umożliwia:</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: left;'>🔵 Predykcję przyszłych poziomów wód na podstawie wprowadzonych warunków hydrologicznych (np. opady atmosferyczne, przepływy wód)</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: left;'>🔵 Wizualną ocenę skuteczności modelu (porównanie danych rzeczywistych i przewidywanych, wskaźniki jakości modelu, wizuwalizacje oraz macierze korelacji między zmiennymi)</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: left;'>🔵 Filtrowanie danych po stacji, województwie i regionie - co zwiększa poziom jakości modelu mimo istotnego wpływu środowiska geograficznego</p>", unsafe_allow_html=True)

st.markdown("""
<div style='background-color: #3A506B; padding: 20px; border-radius: 10px; border-left: 5px solid #7289da;'>
    <h4 style='color: #ffffff;'>Główny powód rekomendacji pojedynczej stacji w modelowaniu</h4>
    <p style='color: #ffffff; font-size: 16px;'>
        Dane z różnych stacji pomiarowych mogą mieć zupełnie inne charakterystyki ze względu na lokalne warunki 
        hydrologiczne, topografię, klimat regionalny, czy zlewnie rzeczne. Mieszanie tych danych w jednym modelu 
        może wprowadzać szum i obniżać skuteczność prognoz.
    </p>
</div>
""", unsafe_allow_html=True)
st.write(" ")
st.write(" ")

st.write("Dane meteorologiczne dotyczące opadów atmosferycznych oraz hydrologii rzek:")

st.image("data_source.png",
         caption="Proces przepływu danych hydrologicznych i meteorologicznych w projeckie 'System Analiz Hydrologizcnych'")


st.write("Rozmieszczenie stacji pomiarowych na terenie Polski:")
m = folium.Map(location=[52.0, 19.0], zoom_start=6)


stations = pd.read_csv("C:/Users/dzaja/OneDrive/Pulpit/Studia_DSAD/Projekt_zaliczeniowy/stations_full.csv",
                       encoding="Windows-1250")

stations_m = stations.dropna(subset=['lat', 'lon'])
for i, row in stations_m.iterrows():
    popup_text = f"<b>Nazwa stacji:</b> {row['station']}<br><b>Region:</b> {row['obszar']}"
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=4,
        color='blue',
        popup=popup_text,
    ).add_to(m)

st_folium(m, width=700, height=500)

#Tabela podsumowująca ile stacji jest per województwo
st.write("Liczba stacji pomiarowych wykorzystanych w projekcie w podziale na województwa")
stations_per_state = stations.groupby("state")["station"].count().reset_index()
stations_per_state.columns = ["Województwo", "Liczba stacji"]
stations_per_state.index = stations_per_state.index + 1
st.table(stations_per_state)


