# The Project Overview

  The project aims to develop a system for hydrological analysis and forecasting based on meteorological and hydrological data from the open data repository of the Institute of Meteorology and Water Management – National Research Institute (IMGW-PIB). The system is designed to support the analysis of hydrological and meteorological phenomena, such as water levels, precipitation, and river flows, taking into account the geographical variability across Poland

A key strength of the project is the implementation of a model based on the XGBoost algorithm, which enables:

🔵 Prediction of future water levels based on input hydrological conditions (e.g., precipitation, water flow rates)

🔵 Visual evaluation of model performance (comparison of actual vs. predicted data, model quality metrics, visualizations, and correlation matrices between variables)

🔵 Data filtering by station, voivodeship, and region — which improves model quality by accounting for significant geographic and environmental variability

  In order to prevent issues with the source code and data, the project has been deployed to the Streamlit cloud service. The app is available at the following address: https://hydrological-analysis-system-app.streamlit.app/

