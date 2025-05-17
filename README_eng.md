# The Project Overview

  The project aims to develop a system for hydrological analysis and forecasting based on meteorological and hydrological data from the open data repository of the Institute of Meteorology and Water Management – National Research Institute (IMGW-PIB). The system is designed to support the analysis of hydrological and meteorological phenomena, such as water levels, precipitation, and river flows, taking into account the geographical variability across Poland

A key strength of the project is the implementation of a model based on the XGBoost algorithm, which enables:

🔵 Prediction of future water levels based on input hydrological conditions (e.g., precipitation, water flow rates)

🔵 Visual evaluation of model performance (comparison of actual vs. predicted data, model quality metrics, visualizations, and correlation matrices between variables)

🔵 Data filtering by station, voivodeship, and region, which improves model quality by accounting for significant geographic and environmental variability

# Repository Content


# How to run the app
  The project has been deployed to the Streamlit cloud service to prevent source code and data issues. The app is available at the following address: https://hydrological-analysis-system-app.streamlit.app/

# The Project sections
The "Hydrological Analysis System" project consists of six main modules: **Home Page, Historical Analysis, Spatial Analysis, XGBoost Model Evaluation, Forecasting**

Statistics
  ![image](https://github.com/user-attachments/assets/2c2a1693-a9c4-4739-a201-fe81e101e4b8)


# Used technologies and libraries
**1. streamlit (1.44.1)
2. pandas (2.2.3)
numpy (2.2.5)
matplotlib (3.10.1)
seaborn (0.13.2)
scipy (1.15.2)
xgboost (3.0.0)
plotly (6.0.1)
folium
streamlit_folium
qrcode (8.1)
scikit-learn**
