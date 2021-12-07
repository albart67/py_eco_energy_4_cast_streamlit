import streamlit as st
import pandas as pd
import numpy as np
import json
from prophet import Prophet
from prophet.serialize import model_to_json, model_from_json
from prophet.diagnostics import performance_metrics
from prophet.plot import plot_cross_validation_metric
from prophet.diagnostics import cross_validation


title = "Energy consumption forecast with adding a temperature regressor"
sidebar_name = "Consumption with T° regressor"


def run():

    st.title(title)


    st.markdown(
        """
        Because consumption is seasonal we can assume that temperature is an important factor for predicting consumption. 
        We acquired temperature data "temperature-quotidienne-regionale.csv" from the Eco2mix website and merged it with our dataset.
        This allows us to include temperature data as regressor in our Facebook Prophet model. The period of daily temperature data starts on January 
        2016, so we have to reduce our dataset (starting in 2013) accordingly.
        
        We want to evaluate if adding temperature data can compensate for the shorter time horizon of the adjusted dataset.
        """
    )

    st.subheader("Original dataframe merged with temperature-quotidienne-regionale ")

    df_day = pd.read_csv('df_t_dly.csv', sep =',', index_col='Unnamed: 0')
    df_day['Date'] = pd.to_datetime(df_day['Date']).dt.date
    df_day[['Consommation (MW)', 'Thermique (MW)','Nucléaire (MW)','Eolien (MW)','Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)']] = df_day[['Consommation (MW)','Thermique (MW)','Nucléaire (MW)','Eolien (MW)','Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)']].apply(pd.to_numeric, errors='coerce')
    df_day[['tmin', 'tmax', 'tmoy']] = df_day[['tmin', 'tmax', 'tmoy']].apply(pd.to_numeric, errors='coerce')
    df_day = df_day.sort_values(by=['Date'], ignore_index=True)
    st.write(df_day.head(10))

    st.header( "Comparison of the model efficiency with regressor and without regressor")

    st.subheader("Regional Consumption accuracy with regressor")
    """
    prod_type = st.selectbox(
        'Which energy production do you want to display?', ('Thermique (MW)','Nucléaire (MW)','Eolien (MW)', 'Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)'))
    st.write('You selected the energy:', prod_type)
    """
    region = st.selectbox(
        'Which region do you want to display?', ('Pays de la Loire',
                                                                 'Normandie',
                                                                 'Grand Est',
                                                                 'Centre-Val de Loire',
                                                                 'Bourgogne-Franche-Comté',
                                                                 'Île-de-France',
                                                                 'Auvergne-Rhône-Alpes',
                                                                 'Bretagne',
                                                                 'Occitanie',
                                                                 'Hauts-de-France',
                                                                 "Provence-Alpes-Côte d'Azur",  'Nouvelle-Aquitaine'))

    st.write('You selected the region:', region)

    def cons_reg(region):
        df_reg = df_day[df_day['region']== region]
        prophet_df = df_reg.rename(columns = {'Date' : 'ds', 'Consommation (MW)': 'y'})
        m = Prophet()
        m.add_regressor('tmoy')
        m.add_regressor('tmin')
        m.add_regressor('tmax')
        #Model training
        m.fit(prophet_df)
        #future = m.make_future_dataframe(periods = -1)
        #forecast = m.predict(future)
        df_cv = cross_validation(m, initial='1582 days', horizon = '395 days')
        df_p = performance_metrics(df_cv)
        fig = plot_cross_validation_metric(df_cv, metric='mape')
        #fig1 = m.plot(forecast)
        st.write('Mean absolute percentage error :', (round(df_p.mean().mape, 2)*100), " %")
        st.write(fig)
        #st.write(fig1)


    cons_reg(region)

    st.subheader("Regional Consumption accuracy without regressor")

    def cons_reg2(region):
        df_reg = df_day[df_day['region']== region]
        prophet_df = df_reg.rename(columns = {'Date' : 'ds', 'Consommation (MW)': 'y'})
        m = Prophet()
        #m.add_regressor('tmoy')
        #m.add_regressor('tmin')
        #m.add_regressor('tmax')
        #Model training
        m.fit(prophet_df)
        #future = m.make_future_dataframe(periods = -1)
        #forecast = m.predict(future)
        df_cv = cross_validation(m, initial='1582 days', horizon = '395 days')
        df_p = performance_metrics(df_cv)
        fig = plot_cross_validation_metric(df_cv, metric='mape')
        #fig1 = m.plot(forecast)
        st.write('Mean absolute percentage error :', (round(df_p.mean().mape, 2)*100), " %")
        st.write(fig)
        #st.write(fig1)


    cons_reg2(region)

    st.markdown(
        """
        The MAPE improved for all regions. The gain of precision goes from 2 to 6% with an average of 3.8%.
        
        We can deduce that adding a temperature regressor is a good way to improve our model.
        """
    )
