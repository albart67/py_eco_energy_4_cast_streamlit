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
        The consumption is seasonal so we can suppose that the temperature is a important factor in consumption 
        forecast. We have not temperature information in our dataset so we use another dataframe,
        "temperature-quotidienne-regionale.csv" who is available on Eco2mix site and we merge it with our original dataset.
        Will will use this temperatures as regressors in the fb Prophet model. The daily temperatures start on january 
        2016, so we have less values than the original dataset who start in 2013.
        
        We want to check if the add of temperatures datas can compensate for the shorter duration of time datas.
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
        'Which energy production did you want to display ?', ('Thermique (MW)','Nucléaire (MW)','Eolien (MW)', 'Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)'))
    st.write('You selected the energy:', prod_type)
    """
    region = st.selectbox(
        'Which region did you want to display the production?', ('Pays de la Loire',
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
        The MAPE is improved for all regions. The gain of precision goes from 2 to 6% with an average of 3,8%.
        
        We can deduce that adding regressor is a good way to improve our model.
        """
    )
