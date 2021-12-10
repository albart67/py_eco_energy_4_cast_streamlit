import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import plotly_express as px


title = "Data analysis"
sidebar_name = "Data analysis"



def run():


    st.title(title)

    st.markdown("---")

    st.markdown(
        """
        Let's start with exploring the dataset!
        """
    )

    df_day = pd.read_csv('df_day.csv', sep =',', index_col='Unnamed: 0')
    df_day['Date'] = pd.to_datetime(df_day['Date']).dt.date
    df_day[['Consommation (MW)', 'Thermique (MW)','Nucléaire (MW)','Eolien (MW)','Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)','Ech. physiques (MW)']] = df_day[['Consommation (MW)','Thermique (MW)','Nucléaire (MW)','Eolien (MW)','Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)','Ech. physiques (MW)']].apply(pd.to_numeric, errors='coerce')
    df_day[['month', 'year']] = df_day[['month', 'year']].apply(pd.to_numeric, errors='coerce')
    df_cons_day = df_day.groupby(['Date'], as_index= False)['Consommation (MW)'].sum()
    #st.write(df_day)

    st.header("Consumption")
    st.markdown("---")


    #Plot of the the global consumption
    fig2 = px.line(df_cons_day, x='Date', y='Consommation (MW)', width=850, height=500)
    fig2.update_xaxes(showgrid=False, zeroline= False)
    fig2.update_yaxes(showgrid=False)
    fig2.update_layout(title_text='National consumption from 2013 to 2021')
    ts_chart = st.plotly_chart(fig2)

    st.markdown(
        """
        * Electricity consumption is clearly seasonal with peaks at the turn of the year.
        """
    )
    
    
    #ANALYSE AND BAX PLOT OF THE GLOBAL CONSUMPTION INTO ONE WEEK
    df_cons_day2 = df_day.groupby(['Date','weekday'],as_index=False)['Consommation (MW)'].sum()
    fig3 = px.box(df_cons_day2, x='weekday', y = 'Consommation (MW)', width = 800, height= 500)
    fig3.update_traces(marker_color='darkblue')
    fig3.update_xaxes(title_text='', showgrid=False, zeroline= False)
    fig3.update_yaxes(showgrid=False)
    fig3.update_layout(title_text='National weekly consumption range')
    #fig3.update_xaxes(type='category')
    st.write(fig3)
    st.markdown(
        """
        * Consumption is about 10% lower on weekends.
        """
    )

    #COMPARISON OF THE DAILY CONSUMPTION RANGE BY REGION
    #We group the consumption by region and by date and make the daily sum
    df_cons_day3 = df_day.groupby(['Région', 'Date'],as_index=False)['Consommation (MW)'].sum()
    #consumption range plot
    fig_plot2 = px.box(df_cons_day3, x="Région", y="Consommation (MW)", width=850, height= 600)
    fig_plot2.update_traces(marker_color='green')
    fig_plot2.update_xaxes(title_text='', showgrid=False, zeroline= False)
    fig_plot2.update_yaxes(showgrid=False)
    fig_plot2.update_layout(title_text='Regional consumption range')
    st.write(fig_plot2)
    st.markdown(
        """
        * Île-de-France and Auvergne-Rhône-Alpes comsume the most electricity, Bourgogne-Franche-Conté and Centre-Val de Loire
         the least.
        """
    )

    
    #COMPARISON OF THE DAILY EXCHANGE RANGE BY REGION
    #We group the exchange by region and by date and make the daily sum
    df_cons_day3 = df_day.groupby(['Région', 'Date'],as_index=False)['Ech. physiques (MW)'].sum()
    #consumption range plot
    fig_plot2 = px.box(df_cons_day3, x="Région", y="Ech. physiques (MW)", width=850, height= 600)
    fig_plot2.update_traces(marker_color='blue')
    fig_plot2.update_xaxes(title_text='', showgrid=False, zeroline= False)
    fig_plot2.update_yaxes(showgrid=False, zeroline= False)
    fig_plot2.update_layout(title_text='Electricity exchange variability by regions')
    st.write(fig_plot2)
    st.markdown(
    """
    - Île-de-France is the region, which imports the most electricity.
    - Auvergne-Rhône-Alpes, Centre-Val de Loire and Grand-Est are the main electricity providers for other regions.
    - The variability of exchange expressed as the difference between the minimum and maximum value is quite different for each region: e.g. energy exporters (left below zero) have higher variability than other regions. 
    """
)


    st.header("Production")
    st.markdown('---')
    #st.subheader("National electricity production from 2013 to 2021")

    st.markdown(
        """
        With the menu below, choose which national electricity production you want to display.
        """
    )

    prod_type = st.selectbox(
        'Which electricity production do you want to display ?', ('Thermique (MW)','Nucléaire (MW)','Eolien (MW)', 'Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)', 'Ech. physiques (MW)'))
    st.write('You selected:', prod_type)

    def prod_plot(prod):
        df_cons_day = df_day.groupby(['Date'], as_index= False)[prod].sum()
        #st.write(df_day)

        fig = px.line(df_cons_day, x='Date', y= prod, width = 850, height=500 )
        fig.update_xaxes(showgrid=False, zeroline= False)
        fig.update_yaxes(showgrid=False, zeroline= False)
        fig.update_layout(title_text='National electricity production from 2013 to 2021')
        ts_chart = st.plotly_chart(fig)

    prod_plot(prod_type)

    st.markdown(
        """
        - Stable evolution for thermal energy production.
        - Annual increase for wind, sun and bio energy, our green energies.
        - Annual decrease for nuclear energy.
        - The amplitude of energy exchange is increasing over time. The reason could be a changing energy balance between regions, i.e. some regions needed more energy than others. This could also indicate a trend in the energy production mix, e.g. closing of a nuclear factory.
        """
    )

    st.header("Regional comparison of energy production, consumption and exchange")
    st.markdown('---')

    #st.subheader("Regional electricity production mix")

    #Energy production repartition by region
    #We group the different columns of electricity productions by region and make the sum
    df_rep_reg = df_day.groupby(['Région'],as_index=False)['Thermique (MW)','Nucléaire (MW)','Eolien (MW)', 'Solaire (MW)','Hydraulique (MW)','Pompage (MW)','Bioénergies (MW)'].sum()
    pd.DataFrame(df_rep_reg).head()

    fig5 = px.bar(df_rep_reg, x="Région", y=['Thermique (MW)','Nucléaire (MW)','Eolien (MW)', 'Solaire (MW)','Hydraulique (MW)','Bioénergies (MW)'], width=850, height=720)

    fig5.update_layout(
        title_text='Regional electricity production mix',
        legend=dict(
            orientation="v",
            x=.8,
            y=.98,
            title_font_family="arial",
            font=dict(
                family="arial",
                size=10,
                color="white"
            ),
            bgcolor=None,
            #bordercolor=None,
            title=''
            )
    )
    fig5.update_xaxes(title_text="", showgrid=False, zeroline= False)
    fig5.update_yaxes(title_text="MW", showgrid=False)

    st.write(fig5)

    #st.subheader("Regional electricity consumption")
    #Energy consumption by region
    #We group the different columns of electricity consumption by region and make the sum
    df_reg_cons = df_day.groupby(['Région'], as_index = False)['Consommation (MW)'].sum()
    fig6 = px.bar(df_reg_cons, x = 'Région', y='Consommation (MW)', width=850, height=700);
    fig6.update_xaxes(title_text='', showgrid=False, zeroline= False)
    fig6.update_yaxes(showgrid=False)
    fig6.update_layout(title_text='Regional electricity consumption')
    st.write(fig6)

    #st.subheader("Regional electricity exchange")
    #Energy exchange by region
    #We group the different columns of electricity exchange by region and make the sum
    df_ech = df_day.groupby(['Région'],as_index=False)['Ech. physiques (MW)'].sum()
    fig7 = px.bar(df_ech, x = 'Région', y='Ech. physiques (MW)', width=850, height=700)
    fig7.update_traces(marker_color='green')
    fig7.update_xaxes(title_text='', showgrid=False, zeroline= False)
    fig7.update_yaxes(showgrid=False, zeroline= False)
    fig7.update_layout(title_text='Regional electricity exchange')

    st.write(fig7)

    st.markdown(
        """
        - Regions with high consumption and low production like Île-de-France need to import electricity from 
          other regions.
        - Regions, which produce more electricity than they consume have the capacity to export 
        (Centre-Val de Loire, Grand-Est, Auvergne-Rhône Alpes). 
        These regions have nuclear operations.
        - Consumption and production in Hauts-de-France are nearly balanced.
        """
    )



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