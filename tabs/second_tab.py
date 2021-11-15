import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import plotly_express as px


title = "Data analyse"
sidebar_name = "Data analyse"



def run():


    st.title(title)

    st.markdown(
        """
        On this page we show the different analyses we made for this project
        """
    )

    df_day = pd.read_csv('df_day.csv', sep =',', index_col='Unnamed: 0')
    df_day['Date'] = pd.to_datetime(df_day['Date']).dt.date
    df_day[['Consommation (MW)', 'Thermique (MW)','Nucléaire (MW)','Eolien (MW)','Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)','Ech. physiques (MW)']] = df_day[['Consommation (MW)','Thermique (MW)','Nucléaire (MW)','Eolien (MW)','Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)','Ech. physiques (MW)']].apply(pd.to_numeric, errors='coerce')
    df_day[['month', 'year']] = df_day[['month', 'year']].apply(pd.to_numeric, errors='coerce')
    df_cons_day = df_day.groupby(['Date'], as_index= False)['Consommation (MW)'].sum()
    #st.write(df_day)

    st.header("Consumption")
    st.markdown(
        """
        Analyse of the consumption
        """
    )

    st.subheader("National consumption evolution from 2013 to 2021")

    #Plot of the the global consumption
    fig2 = px.line(df_cons_day, x='Date', y='Consommation (MW)', width=850, height=500)
    ts_chart = st.plotly_chart(fig2)

    st.subheader("Global consumption range for one week")
    #ANALYSE AND BAX PLOT OF THE GLOBAL CONSUMPTION INTO ONE WEEK
    df_cons_day2 = df_day.groupby(['Date','weekday'],as_index=False)['Consommation (MW)'].sum()
    fig3 = px.box(df_cons_day2, x='weekday', y = 'Consommation (MW)', width = 800, height= 500)
    fig3.update_traces(marker_color='darkblue')
    #fig3.update_xaxes(type='category')
    st.write(fig3)

    st.subheader("Consumption range for the different regions")
    #COMPARISON OF THE DAILY CONSUMPTION RANGE BY REGION
    #We group the consumption by region and by date and make the daily sum
    df_cons_day3 = df_day.groupby(['Région', 'Date'],as_index=False)['Consommation (MW)'].sum()
    #consumption range plot
    fig_plot2 = px.box(df_cons_day3, x="Région", y="Consommation (MW)", width=850, height= 600)
    fig_plot2.update_traces(marker_color='green')
    st.write(fig_plot2)

    st.header("Analyse of the production")
    st.subheader("National electricity production from 2013 to 2021")

    st.markdown(
        """
        With the menu below, choose which national energy production you want to display
        """
    )

    prod_type = st.selectbox(
        'Which energy production did you want to display ?', ('Thermique (MW)','Nucléaire (MW)','Eolien (MW)', 'Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)'))
    st.write('You selected the energy:', prod_type)

    def prod_plot(prod):
        df_cons_day = df_day.groupby(['Date'], as_index= False)[prod].sum()
        #st.write(df_day)

        fig = px.line(df_cons_day, x='Date', y= prod, width = 850, height=500 )
        ts_chart = st.plotly_chart(fig)

    prod_plot(prod_type)

    st.subheader("Regional electricity production")

    st.markdown(
        """
        With the menu below, choose which regional energy production you want to display
        """
    )

    prod_type2 = st.selectbox(
        'Which energy production did you want to display ?', ('Nucléaire (MW)', 'Thermique (MW)','Eolien (MW)', 'Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)'))
    st.write('You selected the energy:', prod_type2)

    st.markdown(
        """
        With the menu below, choose which region you want to display
        """
    )
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
                                                              "Provence-Alpes-Côte d'Azur",
                                                              'Nouvelle-Aquitaine'))

    st.write('You selected the region:', region)

    def prod_plot_reg(prod, reg):
        df_day_reg = df_day[df_day['Région'] == reg]
        df_cons_day = df_day_reg.groupby(['Date'], as_index= False)[prod].sum()
        #st.write(df_day)

        fig = px.line(df_cons_day, x='Date', y= prod, width = 850, height=500 )
        ts_chart = st.plotly_chart(fig)

    prod_plot_reg(prod_type2, region)


    st.header("Regional comparison of energy production, consumption and exchange")

    st.subheader("Regional electricity production mix")

    #Energy production repartition by region
    #We group the different columns of electricity productions by region and make the sum
    df_rep_reg = df_day.groupby(['Région'],as_index=False)['Thermique (MW)','Nucléaire (MW)','Eolien (MW)', 'Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)'].sum()
    pd.DataFrame(df_rep_reg).head()

    fig5 = px.bar(df_rep_reg, x="Région", y=['Thermique (MW)','Nucléaire (MW)','Eolien (MW)', 'Solaire (MW)','Hydraulique (MW)','Bioénergies (MW)'], width=850, height=720)

    fig5.update_layout(
        legend=dict(
            orientation="h",
            x=0,
            y=1.1,
            title_font_family="arial",
            font=dict(
                family="arial",
                size=10,
                color="black"
            ),
            #bgcolor="LightSteelBlue",
            bordercolor="Black",
            )
    )

    st.write(fig5)

    st.subheader("Regional electricity consumption")
    #Energy consumption by region
    #We group the different columns of electricity consumption by region and make the sum
    df_reg_cons = df_day.groupby(['Région'], as_index = False)['Consommation (MW)'].sum()
    fig6 = px.bar(df_reg_cons, x = 'Région', y='Consommation (MW)', width=850, height=700);
    st.write(fig6)

    st.subheader("Regional electricity exchange")
    #Energy exchange by region
    #We group the different columns of electricity exchange by region and make the sum
    df_ech = df_day.groupby(['Région'],as_index=False)['Ech. physiques (MW)'].sum()
    fig7 = px.bar(df_ech, x = 'Région', y='Ech. physiques (MW)', width=850, height=700)
    fig7.update_traces(marker_color='green')

    st.write(fig7)



"""
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=list("abc"))

    st.line_chart(chart_data)

    st.markdown(
        
        ## Test 2

        Proin malesuada diam blandit orci auctor, ac auctor lacus porttitor. Aenean id faucibus tortor. Morbi ac odio leo. Proin consequat facilisis magna eu elementum. Proin arcu sapien, venenatis placerat blandit vitae, pharetra ac ipsum. Proin interdum purus non eros condimentum, sit amet luctus quam iaculis. Quisque vitae sapien felis. Vivamus ut tortor accumsan, dictum mi a, semper libero. Morbi sed fermentum ligula, quis varius quam. Suspendisse rutrum, sapien at scelerisque vestibulum, ipsum nibh fermentum odio, vel pellentesque arcu erat at sapien. Maecenas aliquam eget metus ut interdum.
        
        ```python

        def my_awesome_function(a, b):
            return a + b
        ```

        Sed lacinia suscipit turpis sit amet gravida. Etiam quis purus in magna elementum malesuada. Nullam fermentum, sapien a maximus pharetra, mauris tortor maximus velit, a tempus dolor elit ut lectus. Cras ut nulla eget dolor malesuada congue. Quisque placerat, nulla in pharetra dapibus, nunc ligula semper massa, eu euismod dui risus non metus. Curabitur pretium lorem vel luctus dictum. Maecenas a dui in odio congue interdum. Sed massa est, rutrum eu risus et, pharetra pulvinar lorem.
    
    )

    st.area_chart(chart_data)

    st.markdown(
        
        ## Test 3

        You can also display images using [Pillow](https://pillow.readthedocs.io/en/stable/index.html).

        ```python
        import streamlit as st
        from PIL import Image

        st.image(Image.open("assets/sample-image.jpg"))

        ```

        
    )

    st.image(Image.open("assets/sample-image.jpg"))
"""