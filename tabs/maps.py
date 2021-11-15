import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly_express as px
import json

title = "Production and consumption Maps"
sidebar_name = "MAPS"


def run():

    # TODO: choose between one of these GIFs
    # st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/1.gif")
    st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/2.gif")
    # st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/3.gif")

    st.title(title)

    df_maps = pd.read_csv('df_map.csv', sep =',', index_col='Unnamed: 0')
    #df_maps['year'] = pd.to_datetime(df_maps['year']).dt.date
    df_maps[['Consommation (MW)', 'Thermique (MW)','Nucléaire (MW)','Eolien (MW)','Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)','Ech. physiques (MW)']] = df_maps[['Consommation (MW)','Thermique (MW)','Nucléaire (MW)','Eolien (MW)','Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)','Ech. physiques (MW)']].apply(pd.to_numeric, errors='coerce')
    df_maps[['year']] = df_maps[['year']].apply(pd.to_numeric, errors='coerce')
    df_maps.rename({'Code INSEE région': 'code'}, axis=1, inplace=True)
    #st.write(df_maps)
    st.markdown("---")

    france_reg = json.load(open("regions.geojson", "r"))
    sf = gpd.read_file('regions.geojson')
    df1 = sf[0:9]
    df2 = sf[14:17]
    gdf = pd.concat([df1, df2])
    gdf["code"] = pd.to_numeric(gdf["code"])
    jf = gdf.merge(df_maps, left_on='code', right_on='code')
    #st.write(jf)

    option = st.selectbox(
         'Which parameter do you want to display ?', ('Consommation (MW)', 'Thermique (MW)','Nucléaire (MW)','Eolien (MW)','Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)','Ech. physiques (MW)'))
    st.write('You selected:', option)

    year = st.selectbox(
        'Which year do you want to display ?', (2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021))
    st.write('You selected the year:', year)

    def plot_map(param):
            jf_year = jf[jf['year'] == year]
            fig = px.choropleth_mapbox(jf_year, geojson=france_reg, locations='code',
                        color= param,
                        color_continuous_scale ='YlOrRd',
                        #color_continuous_scale="Viridis",
                        #range_color=(0, 68e6),
                        #scope="europe",
                        featureidkey="properties.code",
                        #projection="mercator",
                        labels={ param, 'unemployment rate'},
                        #color_continuous_scale=px.colors.diverging.BrBG,
                        mapbox_style="carto-positron", zoom=3.8,
                        center={"lat": 47, "lon": 2},
                        #opacity = 0.8
                        )
            #48°52'N et 2°19'
            #46° 36′ 22″ N, 1° 52′ 31″

            #            projection="mercator")
            fig.update_geos(fitbounds="locations", visible=False)

            #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.write(fig)

    plot_map(option)




