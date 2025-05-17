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
url1 = "https://raw.githubusercontent.com/DariuszZajaczkowski/Hydrological-analysis-system/main/ETL_images/ETL_1.png"
with st.expander("Wyświetl fragment kodu:"):
    st.image(url1)

st.markdown("<h5 style='text-align: left;'>Drugi etap przetwarzania danych</h5>", unsafe_allow_html=True)
url2 = "https://raw.githubusercontent.com/DariuszZajaczkowski/Hydrological-analysis-system/main/ETL_images/ETL_2.png"
with st.expander("Wyświetl fragment kodu:"):
    st.image(url2)

st.markdown("<h5 style='text-align: left;'>Trzeci etap przetwarzania danych</h5>", unsafe_allow_html=True)
url3 = "https://raw.githubusercontent.com/DariuszZajaczkowski/Hydrological-analysis-system/main/ETL_images/ETL_3.png"
url4 = "https://raw.githubusercontent.com/DariuszZajaczkowski/Hydrological-analysis-system/main/ETL_images/ETL_4.png"
url5 = "https://raw.githubusercontent.com/DariuszZajaczkowski/Hydrological-analysis-system/main/ETL_images/ETL_5.png"
with st.expander("Wyświetl fragment kodu:"):
    st.image(url3)
    st.image(url4)
    st.image(url5)
