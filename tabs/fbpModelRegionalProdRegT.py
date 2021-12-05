import streamlit as st
import pandas as pd
import numpy as np
import json
from prophet import Prophet
from prophet.serialize import model_to_json, model_from_json
from prophet.diagnostics import performance_metrics
from prophet.plot import plot_cross_validation_metric
from prophet.diagnostics import cross_validation


title = "Energy production forecast with adding a temperature regressor"
sidebar_name = "Production with T° regressor"


def run():

    st.title(title)


    st.markdown(
        """
        We have seen that forecasting regional energy production is difficult.
        
        In our dataframe we have a kind of natural direct energies who are dependant on weather : sun and wind. We want
        now to control if we can have a better accuracy in production prediction with adding temperature regressors.
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



    prod_type = st.selectbox(
        'Which energy production did you want to display ?', ('Eolien (MW)', 'Solaire (MW)'))
    st.write('You selected the energy:', prod_type)

    region2 = st.selectbox(
        'Which region did you want to display the production ?', ('Pays de la Loire',
                                                                 'Normandie',
                                                                 'Grand Est',
                                                                 'Centre-Val de Loire',
                                                                 'Bourgogne-Franche-Comté',
                                                                 'Île-de-France',
                                                                 'Auvergne-Rhône-Alpes',
                                                                 'Bretagne',
                                                                 'Occitanie',
                                                                 'Hauts-de-France',
                                                                 "Provence-Alpes-Côte d'Azur",
                                                                 'Nouvelle-Aquitaine'))

    st.write('You selected the region:', region2)

    st.subheader("Regional Consumption accuracy with regressor")

    def pred_plot_reg(reg, prod):
        df_reg = df_day[df_day['region']== reg]
        prophet_df = df_reg.rename(columns = {'Date' : 'ds', prod: 'y'})
        m = Prophet()
        m.add_regressor('tmoy')
        m.add_regressor('tmin')
        m.add_regressor('tmax')
        #Model training
        m.fit(prophet_df)
        df_cv = cross_validation(m, initial='1582 days', horizon = '395 days')
        df_p = performance_metrics(df_cv)
        fig = plot_cross_validation_metric(df_cv, metric='mape')
        st.write('Mean absolute percentage error with regressor :', (round(df_p.mean().mape, 2)*100), " %")
        st.write(fig)


    pred_plot_reg(region2, prod_type)

    st.subheader("Regional Consumption accuracy without regressor")
    def pred_plot_reg2(reg, prod):
        df_reg = df_day[df_day['region']== reg]
        prophet_df = df_reg.rename(columns = {'Date' : 'ds', prod: 'y'})
        m = Prophet()
        #m.add_regressor('tmoy')
        #m.add_regressor('tmin')
        #m.add_regressor('tmax')
        #Model training
        m.fit(prophet_df)
        df_cv = cross_validation(m, initial='1582 days', horizon = '395 days')
        df_p = performance_metrics(df_cv)
        fig = plot_cross_validation_metric(df_cv, metric='mape')
        st.write('Mean absolute percentage error without regressor :', (round(df_p.mean().mape, 2)*100), " %")
        #st.write('Mean absolute percentage error :', df_p.mean())
        st.write(fig)


    pred_plot_reg2(region2, prod_type)

    st.markdown(
        """
        
        - The average MAPE for solar and wind energy is 15 % better by adding the temperature regressors to the model.
        
        - For wind energy production, the MAPE is better with original dataset who contain more values and no 
          temperature information. Teh seasonality of eolian electricity production is not as clear as for solar, this
          can explain why the number of data is more important than the temperature regressor for this model. 
                     
        - The results with regressor are the best in the sunniest regions like Provence-Alpes Côte d’Azur or Occitanie.
           These regions have mild winters and high production and there is clearly more correlation between solar 
           energy production and temperature.
           
        We can conclude that temperature data improves our Prophet model. With a larger weather dataset the prediction
        could even be better. The period of the dataset is also very important, especially since regions like 
        Île-de-France saw their production increase rapidly over the last few years. Given that the number of wind 
        turbines installed is not linked with temperature data, investment in wind energy could also be a good 
        regressor to boost the model.

           
        """

    )


"""
        df_pred = df_day[df_day['Région'] == reg].groupby(['Date'], as_index=False)[prod].sum()
        prophet_df = df_pred.rename(columns = {'Date' : 'ds', prod : 'y'})
        m = Prophet()
        m.fit(prophet_df)
        future = m.make_future_dataframe(periods = 365)
        forecast = m.predict(future)
        fig1 = m.plot(forecast)
        #fig2 = m.plot_components(forecast)
        df_cv = cross_validation(m, initial='2457 days', horizon = '615 days')
        df_p = performance_metrics(df_cv)
        st.write('mean performance values :', df_p.mean())
        st.write(fig1)


    
    """

