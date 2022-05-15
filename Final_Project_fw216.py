#!/usr/bin/env python
# coding: utf-8

# In[1]:

pip install -U scikit-learn
import sklearn
import streamlit as st
from sklearn import datasets
import numpy as np
import pandas as pd
import requests
from plotnine import *
import altair as alt
import datetime
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go



# requests.get()
    # accepts string of URL
    # accepts query parameters as dict
r = requests.get("https://api.census.gov/data/timeseries/idb/5year",
                params = {
                    "get":"NAME,E0_F,E0_M,IMR_F,IMR_M,FMR0_4,ASFR15_19,ASFR20_24,ASFR25_29,ASFR30_34,ASFR35_39,ASFR40_44,ASFR45_49,SRB",
                    "YR":"2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021",
                })


# In[132]:


# Examine response in formatted JSON
r.json()


# In[129]:


r.status_code


# In[134]:


census_df = pd.DataFrame(columns=["country_name", "Female life expectancy at birth", "Male life expectancy at birth",
                                 "Female infant mortality rate (infant deaths per 1,000 population)","Male infant mortality rate (infant deaths per 1,000 population)",
                                 "Mortality rates for females under 5 years of age","Age specific fertility rate for women age 15-19 (births per 1,000 population)",
                                  "Age specific fertility rate for women age 20-24 (births per 1,000 population)",
                                  "Age specific fertility rate for women age 25-29 (births per 1,000 population)",
                                  "Age specific fertility rate for women age 30-34 (births per 1,000 population)",
                                  "Age specific fertility rate for women age 35-39 (births per 1,000 population)",
                                  "Age specific fertility rate for women age 40-44 (births per 1,000 population)",
                                  "Age specific fertility rate for women age 45-49 (births per 1,000 population)",
                                  "Sex ratio at birth (males per female)","Year"],
                        data=r.json()[1:])

census_df['country_name']=census_df['country_name'].replace({'Congo (Kinshasa)':'Democratic Republic of the Congo'})
census_df['country_name']=census_df['country_name'].replace({'Congo (Brazzaville)':'Republic of the Congo'})
census_df['country_name']=census_df['country_name'].replace({"Côte d'Ivoire":"Côte d'Ivoire"})


census_df["Year"]=census_df["Year"].astype(int)
census_df["Female life expectancy at birth"]=census_df["Female life expectancy at birth"].astype(float)
census_df["Female infant mortality rate (infant deaths per 1,000 population)"]=census_df["Female infant mortality rate (infant deaths per 1,000 population)"].astype(float)
census_df["Mortality rates for females under 5 years of age"]=census_df["Mortality rates for females under 5 years of age"].astype(float)
census_df["Age specific fertility rate for women age 15-19 (births per 1,000 population)"]=census_df["Age specific fertility rate for women age 15-19 (births per 1,000 population)"].astype(float)
census_df["Age specific fertility rate for women age 20-24 (births per 1,000 population)"]=census_df["Age specific fertility rate for women age 20-24 (births per 1,000 population)"].astype(float)
census_df["Age specific fertility rate for women age 25-29 (births per 1,000 population)"]=census_df["Age specific fertility rate for women age 25-29 (births per 1,000 population)"].astype(float)
census_df["Age specific fertility rate for women age 30-34 (births per 1,000 population)"]=census_df["Age specific fertility rate for women age 30-34 (births per 1,000 population)"].astype(float)
census_df["Age specific fertility rate for women age 35-39 (births per 1,000 population)"]=census_df["Age specific fertility rate for women age 35-39 (births per 1,000 population)"].astype(float)
census_df["Age specific fertility rate for women age 40-44 (births per 1,000 population)"]=census_df["Age specific fertility rate for women age 40-44 (births per 1,000 population)"].astype(float)
census_df["Age specific fertility rate for women age 45-49 (births per 1,000 population)"]=census_df["Age specific fertility rate for women age 45-49 (births per 1,000 population)"].astype(float)
census_df["Sex ratio at birth (males per female)"]=census_df["Sex ratio at birth (males per female)"].astype(float)
census_df["Male life expectancy at birth"]=census_df["Male life expectancy at birth"].astype(float)
census_df["Male infant mortality rate (infant deaths per 1,000 population)"]=census_df["Male infant mortality rate (infant deaths per 1,000 population)"].astype(float)



# In[ ]
# In[ ]:
life_expectancy=census_df[["country_name","Year","Female life expectancy at birth","Male life expectancy at birth"]]
infant_mortality=census_df[["country_name","Year","Female infant mortality rate (infant deaths per 1,000 population)","Male infant mortality rate (infant deaths per 1,000 population)"]]
life_expectancy=pd.melt(life_expectancy,id_vars=['country_name','Year'],var_name='type', value_name='life expectancy at birth')
infant_mortality=pd.melt(infant_mortality,id_vars=['country_name','Year'],var_name='type', value_name='infant mortality rate')

#Geo Data
geo = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')
geo.rename(columns = {'COUNTRY':'country_name'}, inplace = True)
geo['country_name']=geo['country_name'].replace({'Congo, Democratic Republic of the':'Democratic Republic of the Congo'})
geo['country_name']=geo['country_name'].replace({'Congo, Republic of the':'Republic of the Congo'})
geo['country_name']=geo['country_name'].replace({"Cote d'Ivoire":"Côte d'Ivoire"})
geo['country_name']=geo['country_name'].replace({"Swaziland":"Eswatini"})


geo_dat = pd.merge(geo,census_df, on=['country_name'])
# In[ ]:




st.write("""
# Welcome to SDG 3 Indicators Data Visualization

This app provides data visualizations regarding indicators which are related to Sustainable Development Goals 3: Ensure healthy lives and promote well-being for all at all ages.

* Specifically, this app provides with insights to SDG 3 target 3.1, 3.2 and 3.4.
    * United Nations SDG 3 offical website: https://sdgs.un.org/goals/goal3

* Indicators available for visualization are life expectancy at birth, infant mortality rate, mortality rates for females under 5 years of age, age-specific fertility rate for women, and sex ratio at birth.

* Please select indicators, start year, end year, and countries on the left.
""")


ana_type = st.sidebar.selectbox(
        'Select Indicator',
        ('Life Expectancy at Birth', "Infant Mortality Rate", "Mortality Rates for Females Under 5 Years of Age","Age Specific Fertility Rate for Women","Sex Ratio at Birth"))
upper = st.sidebar.selectbox(
        'Choose Start Year',
        (2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021))
lower = st.sidebar.selectbox(
        'Choose End Year',
        (2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021))

if upper>=lower:
        st.error("Start year should be smaller than end year.")

clist = census_df['country_name'].unique()

countryA = st.sidebar.selectbox("Select a Country:",clist)

countryB = st.sidebar.selectbox("Select a Country for Comparison:",clist)



if ana_type == "Life Expectancy at Birth":
    df2=life_expectancy
    col1, col2 = st.columns(2)
    df2= df2[(df2.Year >= upper) & (df2.Year <= lower)]
    df2A= df2[df2.country_name == countryA]
    df2B= df2[df2.country_name == countryB]
    fig = px.line(df2A,x = "Year", y = "life expectancy at birth", color = "type", title = countryA)
    col1.plotly_chart(fig)
    fig = px.line(df2B,x = "Year", y = "life expectancy at birth", color = "type", title = countryB)
    col2.plotly_chart(fig)


    st.title('World Female Life Expectancy at Birth Choropleth Map By Year')

    geo_dat2 = geo_dat[(geo_dat.Year >= upper) & (geo_dat.Year <= lower)]
    ylist = geo_dat2["Year"].unique()
    year_option = st.selectbox(
     'Please Select A Year', ylist)

    oneyear = geo_dat2[geo_dat2.Year == year_option]

    fig1 = go.Figure(data=go.Choropleth(
    locations = oneyear['CODE'],
    z = oneyear['Female life expectancy at birth'],
    text = oneyear['country_name'],
    colorscale = 'Blues',
    autocolorscale=False,
    reversescale=True,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_tickprefix = '',
    colorbar_title = 'Female life expectancy at birth',))

    st.plotly_chart(fig1)



elif ana_type == "Infant Mortality Rate":
    df1=infant_mortality
    col1, col2 = st.columns(2)
    df1= df1[(df1.Year >= upper) & (df1.Year <= lower)]
    df1A= df1[df1.country_name == countryA]
    df1B= df1[df1.country_name == countryB]
    fig = px.line(df1A,x = "Year", y = "infant mortality rate", color = "type", title = countryA)
    col1.plotly_chart(fig)
    fig = px.line(df1B,x = "Year", y = "infant mortality rate", color = "type", title = countryB)
    col2.plotly_chart(fig)

    st.title('World Female Infant Mortality Rate Choropleth Map By Year')

    geo_dat2 = geo_dat[(geo_dat.Year >= upper) & (geo_dat.Year <= lower)]
    ylist = geo_dat2["Year"].unique()
    year_option = st.selectbox(
     'Please Select A Year', ylist)

    oneyear = geo_dat2[geo_dat2.Year == year_option]

    fig1 = go.Figure(data=go.Choropleth(
    locations = oneyear['CODE'],
    z = oneyear['Female infant mortality rate (infant deaths per 1,000 population)'],
    text = oneyear['country_name'],
    colorscale = 'sunset',
    autocolorscale=False,
    reversescale=True,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_tickprefix = '',
    colorbar_title = 'Female infant mortality rate',))

    st.plotly_chart(fig1)

elif ana_type == "Mortality Rates for Females Under 5 Years of Age":
    df1=census_df
    col1, col2 = st.columns(2)
    df1= df1[(df1.Year >= upper) & (df1.Year <= lower)]
    fig = px.line(df1[df1.country_name == countryA],
     x = "Year", y = "Mortality rates for females under 5 years of age",title = countryA)
    col1.plotly_chart(fig)
    fig = px.line(df1[df1.country_name == countryB],
     x = "Year", y = "Mortality rates for females under 5 years of age",title = countryB)
    col2.plotly_chart(fig,use_container_width = True)

    st.title('World Mortality Rates for Females Under 5 Years of Age Choropleth Map By Year')

    geo_dat2 = geo_dat[(geo_dat.Year >= upper) & (geo_dat.Year <= lower)]
    ylist = geo_dat2["Year"].unique()
    year_option = st.selectbox(
     'Please Select A Year', ylist)

    oneyear = geo_dat2[geo_dat2.Year == year_option]

    fig1 = go.Figure(data=go.Choropleth(
    locations = oneyear['CODE'],
    z = oneyear['Mortality rates for females under 5 years of age'],
    text = oneyear['country_name'],
    colorscale = 'solar',
    autocolorscale=False,
    reversescale=True,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_tickprefix = '',
    colorbar_title = 'Mortality Rates for Females Under 5 Years of Age',))

    st.plotly_chart(fig1)

elif ana_type == "Age Specific Fertility Rate for Women":
    df1=census_df
    age_option = st.selectbox(
     'Please Select An Age Range',('15-19', '20-24', '25-29','30-34','35-39','40-44','45-49'))
    if age_option == '15-19':
        col1, col2 = st.columns(2)
        df1= df1[(df1.Year >= upper) & (df1.Year <= lower)]
        fig = px.line(df1[df1.country_name == countryA],
         x = "Year", y = "Age specific fertility rate for women age 15-19 (births per 1,000 population)",title = countryA)
        col1.plotly_chart(fig)
        fig = px.line(df1[df1.country_name == countryB],
         x = "Year", y = "Age specific fertility rate for women age 15-19 (births per 1,000 population)",title = countryB)
        col2.plotly_chart(fig,use_container_width = True)

        st.title('World Fertility Rate for Women Age 15-19 Choropleth Map By Year')

        geo_dat2 = geo_dat[(geo_dat.Year >= upper) & (geo_dat.Year <= lower)]
        ylist = geo_dat2["Year"].unique()
        year_option = st.selectbox(
         'Please Select A Year', ylist)

        oneyear = geo_dat2[geo_dat2.Year == year_option]

        fig1 = go.Figure(data=go.Choropleth(
        locations = oneyear['CODE'],
        z = oneyear['Age specific fertility rate for women age 15-19 (births per 1,000 population)'],
        text = oneyear['country_name'],
        colorscale = 'blugrn',
        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_tickprefix = '',
        colorbar_title = 'Fertility Rate for Women Age 15-19',))

        st.plotly_chart(fig1)

    elif age_option == '20-24':
        col1, col2 = st.columns(2)
        df1= df1[(df1.Year >= upper) & (df1.Year <= lower)]
        fig = px.line(df1[df1.country_name == countryA],
         x = "Year", y = "Age specific fertility rate for women age 20-24 (births per 1,000 population)",title = countryA)
        col1.plotly_chart(fig)
        fig = px.line(df1[df1.country_name == countryB],
         x = "Year", y = "Age specific fertility rate for women age 20-24 (births per 1,000 population)",title = countryB)
        col2.plotly_chart(fig,use_container_width = True)

        st.title('World Fertility Rate for Women Age 20-24 Choropleth Map By Year')

        geo_dat2 = geo_dat[(geo_dat.Year >= upper) & (geo_dat.Year <= lower)]
        ylist = geo_dat2["Year"].unique()
        year_option = st.selectbox(
         'Please Select A Year', ylist)

        oneyear = geo_dat2[geo_dat2.Year == year_option]

        fig1 = go.Figure(data=go.Choropleth(
        locations = oneyear['CODE'],
        z = oneyear['Age specific fertility rate for women age 20-24 (births per 1,000 population)'],
        text = oneyear['country_name'],
        colorscale = 'blugrn',
        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_tickprefix = '',
        colorbar_title = 'Fertility Rate for Women Age 20-24',))

        st.plotly_chart(fig1)
    elif age_option == '25-29':
        col1, col2 = st.columns(2)
        df1= df1[(df1.Year >= upper) & (df1.Year <= lower)]
        fig = px.line(df1[df1.country_name == countryA],
         x = "Year", y = "Age specific fertility rate for women age 25-29 (births per 1,000 population)",title = countryA)
        col1.plotly_chart(fig)
        fig = px.line(df1[df1.country_name == countryB],
         x = "Year", y = "Age specific fertility rate for women age 25-29 (births per 1,000 population)",title = countryB)
        col2.plotly_chart(fig,use_container_width = True)

        st.title('World Fertility Rate for Women Age 25-29 Choropleth Map By Year')

        geo_dat2 = geo_dat[(geo_dat.Year >= upper) & (geo_dat.Year <= lower)]
        ylist = geo_dat2["Year"].unique()
        year_option = st.selectbox(
         'Please Select A Year', ylist)

        oneyear = geo_dat2[geo_dat2.Year == year_option]

        fig1 = go.Figure(data=go.Choropleth(
        locations = oneyear['CODE'],
        z = oneyear['Age specific fertility rate for women age 25-29 (births per 1,000 population)'],
        text = oneyear['country_name'],
        colorscale = 'blugrn',
        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_tickprefix = '',
        colorbar_title = 'Fertility Rate for Women Age 25-29',))

        st.plotly_chart(fig1)
    elif age_option == '30-34':
        col1, col2 = st.columns(2)
        df1= df1[(df1.Year >= upper) & (df1.Year <= lower)]
        fig = px.line(df1[df1.country_name == countryA],
         x = "Year", y = "Age specific fertility rate for women age 30-34 (births per 1,000 population)",title = countryA)
        col1.plotly_chart(fig)
        fig = px.line(df1[df1.country_name == countryB],
         x = "Year", y = "Age specific fertility rate for women age 30-34 (births per 1,000 population)",title = countryB)
        col2.plotly_chart(fig,use_container_width = True)

        st.title('World Fertility Rate for Women Age 30-34 Choropleth Map By Year')

        geo_dat2 = geo_dat[(geo_dat.Year >= upper) & (geo_dat.Year <= lower)]
        ylist = geo_dat2["Year"].unique()
        year_option = st.selectbox(
         'Please Select A Year', ylist)

        oneyear = geo_dat2[geo_dat2.Year == year_option]

        fig1 = go.Figure(data=go.Choropleth(
        locations = oneyear['CODE'],
        z = oneyear['Age specific fertility rate for women age 30-34 (births per 1,000 population)'],
        text = oneyear['country_name'],
        colorscale = 'blugrn',
        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_tickprefix = '',
        colorbar_title = 'Fertility Rate for Women Age 30-34',))

        st.plotly_chart(fig1)


    elif age_option == '35-39':
        col1, col2 = st.columns(2)
        df1= df1[(df1.Year >= upper) & (df1.Year <= lower)]
        fig = px.line(df1[df1.country_name == countryA],
         x = "Year", y = "Age specific fertility rate for women age 35-39 (births per 1,000 population)",title = countryA)
        col1.plotly_chart(fig)
        fig = px.line(df1[df1.country_name == countryB],
         x = "Year", y = "Age specific fertility rate for women age 35-39 (births per 1,000 population)",title = countryB)
        col2.plotly_chart(fig,use_container_width = True)

        st.title('World Fertility Rate for Women Age 35-39 Choropleth Map By Year')

        geo_dat2 = geo_dat[(geo_dat.Year >= upper) & (geo_dat.Year <= lower)]
        ylist = geo_dat2["Year"].unique()
        year_option = st.selectbox(
         'Please Select A Year', ylist)

        oneyear = geo_dat2[geo_dat2.Year == year_option]

        fig1 = go.Figure(data=go.Choropleth(
        locations = oneyear['CODE'],
        z = oneyear['Age specific fertility rate for women age 35-39 (births per 1,000 population)'],
        text = oneyear['country_name'],
        colorscale = 'blugrn',
        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_tickprefix = '',
        colorbar_title = 'Fertility Rate for Women Age 35-39',))

        st.plotly_chart(fig1)
    elif age_option == '40-44':
        col1, col2 = st.columns(2)
        df1= df1[(df1.Year >= upper) & (df1.Year <= lower)]
        fig = px.line(df1[df1.country_name == countryA],
         x = "Year", y = "Age specific fertility rate for women age 40-44 (births per 1,000 population)",title = countryA)
        col1.plotly_chart(fig)
        fig = px.line(df1[df1.country_name == countryB],
         x = "Year", y = "Age specific fertility rate for women age 40-44 (births per 1,000 population)",title = countryB)
        col2.plotly_chart(fig,use_container_width = True)


        st.title('World Fertility Rate for Women Age 40-44 Choropleth Map By Year')

        geo_dat2 = geo_dat[(geo_dat.Year >= upper) & (geo_dat.Year <= lower)]
        ylist = geo_dat2["Year"].unique()
        year_option = st.selectbox(
         'Please Select A Year', ylist)

        oneyear = geo_dat2[geo_dat2.Year == year_option]

        fig1 = go.Figure(data=go.Choropleth(
        locations = oneyear['CODE'],
        z = oneyear['Age specific fertility rate for women age 40-44 (births per 1,000 population)'],
        text = oneyear['country_name'],
        colorscale = 'blugrn',
        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_tickprefix = '',
        colorbar_title = 'Fertility Rate for Women Age 40-44',))

        st.plotly_chart(fig1)
    elif age_option == '45-49':
        col1, col2 = st.columns(2)
        df1= df1[(df1.Year >= upper) & (df1.Year <= lower)]
        fig = px.line(df1[df1.country_name == countryA],
         x = "Year", y = "Age specific fertility rate for women age 45-49 (births per 1,000 population)",title = countryA)
        col1.plotly_chart(fig)
        fig = px.line(df1[df1.country_name == countryB],
         x = "Year", y = "Age specific fertility rate for women age 45-49 (births per 1,000 population)",title = countryB)
        col2.plotly_chart(fig,use_container_width = True)

        st.title('World Fertility Rate for Women Age 45-49 Choropleth Map By Year')

        geo_dat2 = geo_dat[(geo_dat.Year >= upper) & (geo_dat.Year <= lower)]
        ylist = geo_dat2["Year"].unique()
        year_option = st.selectbox(
         'Please Select A Year', ylist)

        oneyear = geo_dat2[geo_dat2.Year == year_option]

        fig1 = go.Figure(data=go.Choropleth(
        locations = oneyear['CODE'],
        z = oneyear['Age specific fertility rate for women age 45-49 (births per 1,000 population)'],
        text = oneyear['country_name'],
        colorscale = 'blugrn',
        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_tickprefix = '',
        colorbar_title = 'Fertility Rate for Women Age 45-49',))

        st.plotly_chart(fig1)

elif ana_type == "Sex Ratio at Birth":
    df1=census_df
    col1, col2 = st.columns(2)
    df1= df1[(df1.Year >= upper) & (df1.Year <= lower)]
    fig = px.line(df1[df1.country_name == countryA],
     x = "Year", y = "Sex ratio at birth (males per female)",title = countryA)
    col1.plotly_chart(fig)
    fig = px.line(df1[df1.country_name == countryB],
     x = "Year", y = "Sex ratio at birth (males per female)",title = countryB)
    col2.plotly_chart(fig,use_container_width = True)

    st.title('World Sex ratio at birth (males per female) Choropleth Map By Year')

    geo_dat2 = geo_dat[(geo_dat.Year >= upper) & (geo_dat.Year <= lower)]
    ylist = geo_dat2["Year"].unique()
    year_option = st.selectbox(
     'Please Select A Year', ylist)

    oneyear = geo_dat2[geo_dat2.Year == year_option]

    fig1 = go.Figure(data=go.Choropleth(
    locations = oneyear['CODE'],
    z = oneyear['Sex ratio at birth (males per female)'],
    text = oneyear['country_name'],
    colorscale = 'ice',
    autocolorscale=False,
    reversescale=True,
    marker_line_color='darkblue',
    marker_line_width=0.5,
    colorbar_tickprefix = '',
    colorbar_title = 'Sex ratio at birth',))

    st.plotly_chart(fig1)


st.write(""" API Data source:
U.S. Census Bureau's Time Series International Database by 5-Year Age Groups and Sex
Avaliable at https://www.census.gov/data/developers/data-sets/international-database.html
 * Please note data for United States is only avaliable from year 2020 to 2021.
""")
















# In[ ]:


# In[ ]:
