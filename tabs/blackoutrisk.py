import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly_express as px


title = "Blackout risk"
sidebar_name = "Blackout risk"


def run():

    st.title(title)

    st.markdown("---")

    # Read the csv file
    daily_shortage = pd.read_csv('daily_shortage.csv', 
                                 sep = ',')
     
    daily_shortage = daily_shortage[daily_shortage['Shortage'] > 0]

    daily_shortage['Shortage'] /= 2

    fig1 = px.line(daily_shortage,
                   x = 'Date', y = 'Shortage',
                   #range_y = [-10,10], 
                   title = 'National electricity shortage', 
                   labels = {'Shortage': 'MWh', 'Date':'Date'})

    fig1.update_layout(showlegend=False)
    st.write(fig1)

    max_val = daily_shortage['Shortage'].max()
    max_date = daily_shortage[daily_shortage['Shortage'] == max_val]['Date']
    max_2_person_households = int(round(max_val*1000 / 5.5,0))

    st.markdown(
    '''
    * Energy shortage is the difference between energy supply and energy consumption.
    * The maximum value is '''+str(max_val)+''' MWh on '''+str(pd.to_datetime(max_date[1655]).month_name())+''' '''+str(pd.to_datetime(max_date[1655]).day)+str(', ')+str(pd.to_datetime(max_date[1655]).year)+str('.')+'''
    * On this date, '''+str(max_2_person_households)+''' two-person households would theoretically suffer from energy shortage.
    '''
     )
   
   
    ##############################
    # Read a file for second chart
    df_blackout = pd.read_csv('df_blackout.csv', sep = ',', index_col='Unnamed: 0')

    # Select one region
    regions = ['Bretagne', 'Nouvelle-Aquitaine', 'Île-de-France',
       'Auvergne-Rhône-Alpes', 'Normandie', 'Bourgogne-Franche-Comté',
       'Centre-Val de Loire', 'Grand Est', 'Hauts-de-France',
       'Pays de la Loire', 'Occitanie', "Provence-Alpes-Côte d'Azur"]
    region = regions[6]

    # Compute the data
    df_blackout_region = df_blackout[(df_blackout['Région'] == region) & (df_blackout['Person Blackout'] > 0) & (pd.to_datetime(df_blackout['Date']).dt.year > 2013)]
    
    # Plot the data
    fig2 = px.scatter(df_blackout_region, 
                      x = df_blackout_region['Consommation (MW)']/1000/2, 
                      y = 'Person Blackout', 
                      color = 'warm month', 
                      range_color = [0,1], 
                      labels = {'Person Blackout': 'Persons affected', \
                                'x': 'Electricity consumption (GWh)'}, 
                      title = 'Regional blackout risk for '+ region)
    fig2.update_layout(coloraxis_showscale=False)
    st.write(fig2)