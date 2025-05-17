import streamlit as st

st.set_page_config(
    page_title="Proces przetwarzania danych",
    layout="wide"
)
st.markdown("""
            <div style='text-align: left;'>
            <span style = "font-size: 20px; font-weight: bold;">
            SEKCJA I - Proces przetwarzania danych
            </span>
        </div>   
    """, unsafe_allow_html=True)
st.write("")
st.write("")
url = "https://github.com/DariuszZajaczkowski/Hydrological-analysis-system/raw/main/data_ETL.png"
st.image(url,  caption= "Ogólny proces przetwarzania danych w projekcie 'System Analiz Hydrologicznych")

st.markdown("<h5 style='text-align: left;'>Pierwszy etap przetwarzania danych</h5>", unsafe_allow_html=True)
url1 = "https://raw.githubusercontent.com/DariuszZajaczkowski/Hydrological-analysis-system/main/ETL_iamges/ETL_1.png"
with st.expander("Wyświetl fragment kodu:"):
    st.image(url1)
