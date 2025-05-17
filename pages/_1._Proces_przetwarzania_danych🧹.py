import streamlit as st

st.set_page_config(
    page_title="Proces przetwarzania danych",
    layout="wide"
)
st.markdown("<h1 style='text-align: center;'>Proces przetwarzania danych</h1>", unsafe_allow_html=True)

url = "https://github.com/DariuszZajaczkowski/Hydrological-analysis-system/raw/main/data_ETL.png"
st.image(url,  caption= "Ogólny proces przetwarzania danych w projekcie 'System Analiz Hydrologicznych")
