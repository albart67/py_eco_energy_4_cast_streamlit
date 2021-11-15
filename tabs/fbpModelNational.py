import streamlit as st
import pandas as pd
import numpy as np
import json
from prophet import Prophet
from prophet.serialize import model_to_json, model_from_json
from prophet.diagnostics import performance_metrics
from prophet.plot import plot_cross_validation_metric
from prophet.diagnostics import cross_validation


title = "FB Prophet National Models"
sidebar_name = "FB Prophet National Models"


def run():

    st.title(title)

    st.markdown(
        """
        On this page we will show the different models we have use on this project
        """
    )

    st.header("FB PROPHET MODELS")

    st.subheader('Consumption model')

    st.markdown(
        """
        We first want to check the performances from model. We train the model on 80% of the daily consumption data 
        and use 20% of the data (615 days called horizon in fb Prophet) to test it:'
        """
    )

    with open('serialized_model.json', 'r') as fin:
        m1 = model_from_json(json.load(fin))  # Load model

    #We use the cross validation method from fb prophet and take 80% (initial) of the datas for predict and 20% to test (horizon)
    df_cv = cross_validation(m1, initial='2457 days', horizon = '615 days')
    df_p = performance_metrics(df_cv)
    fig = plot_cross_validation_metric(df_cv, metric='mape')
    st.write('Mean MAPE value :', df_p.mape.mean())
    st.write(fig)

    st.markdown(
        """
        With the trained model we can display the predicted consumption for the next year and compare it with the last 
        years. The black points are the daily consumption values from dataset :
        """
    )

    #We want predict the consumption during one year after the end from our dataset. The make_future method create a dataframe
    future = m1.make_future_dataframe(periods = 365)
    forecast = m1.predict(future)
    fig1 = m1.plot(forecast)
    fig2 = m1.plot_components(forecast)
    st.write(fig1)

    st.markdown(
        """
        Fb Prophet can decompose the model with 3 trends: the general trend for the 8 years, a weekly trend and a yearly
         trend. The general trend is a decrease of the consumption, weekly and yearly trends show us the same tendency 
         we noticed in the data analyse.
        """
    )

    st.write(fig2)



    st.subheader('Electricity production model')

    st.markdown(
        """
        Like we do for the production, we generate models for electricity production. We are using the same proportion:
        80% of the data for training and 20% for test. We display the mean MAPE obtained with test set (Horizon) 
        compared to real values.
        
        We make also a 365 days future forecast.
        """
    )

    df_day = pd.read_csv('df_day.csv', sep =',', index_col='Unnamed: 0')
    df_day['Date'] = pd.to_datetime(df_day['Date']).dt.date
    df_day[['Consommation (MW)', 'Thermique (MW)','Nucléaire (MW)','Eolien (MW)','Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)','Ech. physiques (MW)']] = df_day[['Consommation (MW)','Thermique (MW)','Nucléaire (MW)','Eolien (MW)','Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)','Ech. physiques (MW)']].apply(pd.to_numeric, errors='coerce')
    df_day[['month', 'year']] = df_day[['month', 'year']].apply(pd.to_numeric, errors='coerce')




    with open('bioenergies_model.json', 'r') as fin:
        model_prod_bio = model_from_json(json.load(fin))  # Load model

    with open('ech_ physiques_model.json', 'r') as fin:
        model_ech = model_from_json(json.load(fin))  # Load model

    with open('eolien_model.json', 'r') as fin:
        model_prod_eol = model_from_json(json.load(fin))  # Load model

    with open('hydraulique_model.json', 'r') as fin:
        model_prod_hydr = model_from_json(json.load(fin))  # Load model

    with open('nucleaire_model.json', 'r') as fin:
        model_prod_nucl = model_from_json(json.load(fin))  # Load model

    with open('pompage_model.json', 'r') as fin:
        model_prod_pomp = model_from_json(json.load(fin))  # Load model

    with open('solaire_model.json', 'r') as fin:
        model_prod_sol = model_from_json(json.load(fin))  # Load model

    with open('thermique_model.json', 'r') as fin:
        model_prod_therm = model_from_json(json.load(fin))  # Load model



    prod_type = st.selectbox(
        'Which energy production did you want to display ?', ('Thermique (MW)','Nucléaire (MW)','Eolien (MW)', 'Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)'))
    st.write('You selected the energy:', prod_type)

    def prod_plot(prod):
        if prod == 'Thermique (MW)':
            m = model_prod_therm
        if prod_type == 'Nucléaire (MW)':
            m = model_prod_nucl
        if prod_type == 'Eolien (MW)':
            m = model_prod_eol
        if prod_type == 'Solaire (MW)':
            m = model_prod_sol
        if prod_type == 'Hydraulique (MW)':
            m = model_prod_hydr
        if prod_type == 'Pompage (MW)':
            m = model_prod_pomp
        if prod_type == 'Bioénergie (MW)':
            m = model_prod_bio
        future = m.make_future_dataframe(periods = 365)
        forecast = m.predict(future)
        fig1 = m.plot(forecast)
        #fig2 = m.plot_components(forecast)
        df_cv = cross_validation(m, initial='2457 days', horizon = '615 days')
        df_p = performance_metrics(df_cv)
        fig2 = plot_cross_validation_metric(df_cv, metric='mape')
        st.write('Mean MAPE value :', df_p.mape.mean())
        st.write(fig1)
        #st.write(fig2)

    prod_plot(prod_type)

