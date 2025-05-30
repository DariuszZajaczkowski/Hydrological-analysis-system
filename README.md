# The Project Overview

  The project aims to develop a system for hydrological analysis and forecasting based on meteorological and hydrological data from the open data repository of the Institute of Meteorology and Water Management – National Research Institute (IMGW-PIB). The system is designed to support the analysis of hydrological and meteorological phenomena, such as water levels, precipitation, and river flows, taking into account the geographical variability across Poland

A key strength of the project is the implementation of a model based on the XGBoost algorithm, which enables:

🔵 Prediction of future water levels based on input hydrological conditions (e.g., precipitation, water flow rates)

🔵 Visual evaluation of model performance (comparison of actual vs. predicted data, model quality metrics, visualizations, and correlation matrices between variables)

🔵 Data filtering by station, voivodeship, and region, which improves model quality by accounting for significant geographic and environmental variability

# Repository Content
The repository for the "System Analiz Hydrologicznych" project consists of the following components:

**1.** Processed input data prepared from raw source data (**dane_hydrologiczne_msc/**)

**2.** Raw input data (**data/**)

**3.** A Jupyter Notebook containing the source data preprocessing code (**Database.ipynb**)

**4.** A diagram illustrating the data flow in the project (**data_source.png**)

**5.** A CSV file with installed required Python libraries (**libraries.csv**)

**6.** An interactive map showing the locations of measurement stations (**mapa_stacji.html**)

**7.** A requirements file listing the libraries needed to run the application (e.g., in the Streamlit Cloud environment) (**requirements.txt**)

**8.** A processed CSV file containing geographic and administrative metadata for measurement stations (**stations.full.csv**)

# How to run the app
  The project has been deployed to the Streamlit cloud service to prevent source code and data issues. The app is available at the following address: https://hydrological-analysis-system-app.streamlit.app/.
  Running the application via the Streamlit cloud service does not require the local installation of libraries or technologies used in the project's development.
  Sometimes users need to wake up the app by clicking the button presented below:
![image](https://github.com/user-attachments/assets/bd14d77a-4058-4dc6-bbb8-f77c7be51cb6)

  

# The Project sections
The "Hydrological Analysis System" project consists of six main modules: **Home Page, Historical Analysis, Spatial Analysis, XGBoost Model Evaluation, Forecasting, Statistics**
![image](https://github.com/user-attachments/assets/1b33ecde-3b0a-491b-bcbe-10ccd2be4035)

# Used technologies and libraries
![image](https://github.com/user-attachments/assets/dfd8242d-9791-4d17-a66e-b40b64cfbbf4)

# Data preparation process
The whole ETL data process is presented in a particular section of the Project. A brief presentation of the mentioned process is implemented below: 
![image](https://github.com/user-attachments/assets/33bff866-c825-4571-b730-94214b09796e)


