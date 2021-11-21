"""" This module was created to show a dashboard on streamlit according to House Rocket project
premises.

Author: Joao Renato Freitas Mendes <joaorenatomendes@gmail.com>

Created on Nov 10th, 2021.
"""

###---IMPORTS---###
import pandas as pd   #to handle csv files and DataFrame structures
import numpy as np
import folium         #to handle the map with price density
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import geopandas
import plotly.express as px #to plot graphic results of the metrics
#import seaborn as sns     #to plot graphic results of the metrics given
import streamlit as st  #to create the dashboard page
import Functions  #functions created to modularize the code
pd.set_option('display.float_format', lambda x: '%.2f' % x)  #limits the quantity of float numbers (decimal)

st.set_page_config(layout = 'wide')
@st.cache(allow_output_mutation=True)
def get_data(path):
    data = pd.read_csv(path) #loads the archive
    return data

def get_geofile(path): #change to url
   geofile = geopandas.read_file(path)
   return geofile

def data_overview(data):
    st.title('House Rocket Exploratory Data Analysis')
    f_attributes = st.sidebar.multiselect('Enter columns', data.columns)
    f_zipcode = st.sidebar.multiselect('Enter zipcode', sorted(set(data['zipcode'].unique())))
    st.title('Data Overview')
    # attributes + zipcode = Select columns and rows
    # atributes = select colunmns
    # zipcode = select lines
    # 0 + 0 = returns original dataset

    if (f_zipcode != []) & (f_attributes != []):
        data = data.loc[data['zipcode'].isin(f_zipcode), f_attributes]

    elif (f_zipcode != []) & (f_attributes == []):
        data = data.loc[data['zipcode'].isin(f_zipcode), :]

    elif (f_zipcode == []) & (f_attributes != []):
        data = data.loc[:, f_attributes]

    else:
        data = data.copy()

    st.dataframe(data)

    return None

def portfolio_density(data, geofile):
    st.title('Region Overview')
    c1, c2 = st.beta_columns(2)
    c1.header('Portfolio Density')

    df = data.sample(10)

    # -----------
    # MAP CONSTRUCTION - folium
    # --------------

    density_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()],
                             default_zoom_start=15)

    # st.write(density_map)
    marker_cluster = MarkerCluster().add_to(density_map)

    for name, row in df.iterrows():
        folium.Marker(([row['lat'], row['long']]),
                      popup='Price {0}, Sold on: {1}, with sqft: {2} m2'.format(row['price'],
                                                                                row['date'],
                                                                                row['sqft_living'])).add_to(marker_cluster)

    with c1:
        folium_static(density_map)

    # -------
    # Region Price Map
    # -------

    c2.header("Price Density")

    df = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()

    df.columns = ['ZIP', 'PRICE']
    df.sample(10)
    geofile = geofile[geofile['ZIP'].isin(df['ZIP'].tolist())]

    region_price_map = folium.Map(location=[data['lat'].mean(), data['long'].mean()],
                                  default_zoom_start=15)

    region_price_map.choropleth(data=df,
                                geo_data=geofile,
                                columns=['ZIP', 'PRICE'],
                                key_on='feature.properties.ZIP',
                                fill_color='YlOrRd',
                                fill_opacity=0.7,
                                line_opacity=0.2,
                                legend_name='AVG PRICE')

    with c2:
        folium_static(region_price_map)

    return None


### What are the estates that House Rocket should buy and for how much? ###
### COLOCAR MAPA DE DENSIDADE EM CIMA OU EMBAIXO
def buy_estates(data):

    st.header('1. How many estates should House Rocket buy?')
    c1, c2 = st.beta_columns(2)

    #st.header('1. What are the estates that House Rocket should buy and for how much?')
    #c1.header('Dataset overview')
    data['zipcode'] = data['zipcode'].astype(str) # Transforms "ZIPCODE" feature data type from INT - STRING
    df = data[['id', 'date', 'price', 'condition', 'zipcode', 'waterfront']].copy()
    df_group_median = df[['price', 'zipcode']].groupby('zipcode').median().reset_index()  # calculating the average price per region

    buy_estate_result = pd.merge(df, df_group_median, on='zipcode', how='inner')         #merges into a single dataframe with all data of interest
    buy_estate_result.rename(columns= {'price_x': 'price', 'price_y': 'median_price'}, inplace = True)
    buy_estate_result.sort_values('zipcode')    #organizes the dataframe by zipcode order

    buy_estate_result['buy_estate']=buy_estate_result.apply(Functions.buy_estate, axis = 1) #for more details, check Functions archive
    buy_estate_result.sort_values('condition', inplace = True)
    #c1.dataframe(buy_estate_result.head(15))

    #c1.header('Quantity of estates to buy')
    st.header('Quantity of estates to buy')
    fig = px.histogram(
        data_frame=buy_estate_result,
        x="buy_estate",
        y="id",
        color = "condition",
        histfunc="count",
        barmode = "group",
        color_discrete_sequence = px.colors.sequential.Viridis
        #title = 'Number of houses to buy'

        )
    #fig.update_layout(font_family = "Times New Roman",
                      #font_color = "black",
    #                  title_font_family = "Times New Roman",
     #                 legend_title_font_color = "black"
      #
       #               )


    #fig.update_xaxes(title_font_family = "Arial")

    st.plotly_chart(fig, use_container_width=True)  #creates a minor plot with a description of how many estates HR should buy

#----SET SEASONS ON DATAFRAME----#
    st.header('2. What is/are the best season(s) to buy a estate?')
    c1, c2 = st.beta_columns(2)
    c1.subheader('Estates per region x Sales Percentual')
    c2.subheader('Mean price sell per region')



    data_pivot = buy_estate_result[buy_estate_result['buy_estate'] == 'yes'].copy()  #collecting only the dataframe estates that House Rocket will probably buy. that will help to create a final dataframe
    data_pivot.rename(columns = {'price': 'price_buy'}, inplace = True) #renaming
    data_pivot['date'] = pd.to_datetime(data_pivot['date'])

    data_pivot['season'] = (data_pivot['date'].dt.month%12 + 3)//3   #Calculating respective seasons according to date column on data frame

    seasons = {
           1: 'Winter',
           2: 'Spring',
           3: 'Summer',
           4: 'Autumn'
            }

    data_pivot['season_name'] = data_pivot['season'].map(seasons)

    season_pivot = data_pivot[['price_buy', 'season_name', 'zipcode']].groupby(['season_name', 'zipcode']).median().reset_index()
    data_seasons = pd.merge(data_pivot, season_pivot, on=['zipcode', 'season_name'], how='inner')        #merges the dataframe we used to help us gettting the info we wanted
    data_seasons.rename(columns={"price_buy_x": "price_buy", "price_buy_y": "season_median"}, inplace=True)
    data_seasons = data_seasons[['id', 'zipcode', 'season_name', 'price_buy', 'season_median']].sort_values('zipcode', ascending=True)

    data_seasons['sale_price'] = data_seasons.apply(Functions.price_sale, axis=1)
    data_seasons['percentual'] = data_seasons.apply(Functions.percentual_sale, axis=1)

    #st.dataframe(data_seasons)
    fig2 = px.histogram(data_seasons,
                       x="zipcode",
                       y="id",
                       color="percentual",
                       barmode="stack",
                       histfunc = "count",
                       labels = {
                         "percentual": "Percentual Profit", "zipcode": "Zipcode"
                       },
                       color_discrete_sequence = px.colors.cyclical.Edge
                       )

    c1.plotly_chart(fig2, use_container_width=True)

    mean_price_sell_by_zipcode = data_seasons[['zipcode', 'sale_price']].groupby('zipcode').mean().reset_index()
    fig3 = px.line(mean_price_sell_by_zipcode,
                   x = "zipcode",
                   y = "sale_price",
                   color_discrete_sequence=px.colors.cyclical.Edge
                   )
    c2.plotly_chart(fig3, use_container_width=True)

    return None

def business_hypo_1(data):
    st.title('Business hypothesis')
    st.header('A. More than 10% of Estates with waterfront are cheaper than average')
    data['zipcode'] = data['zipcode'].astype(str)
    c1, c2 = st.beta_columns(2)
    c1.subheader('Estates with waterfront vs Price Avg')
    c2.subheader('Estates per region vs Price Avg')
    data_new = Functions.create_price_mean_col(data)  #Merges column price_mean on the current dataset

    data_new['percentual'] = data_new.apply(Functions.percentual_growth, axis=1)
    data_new['bigger_smaller'] = data_new.apply(Functions.bigger_smaller_than_avg, axis=1)
    data_new.sort_values('zipcode', inplace=True) #organizing dataframe by region order so that the plot is organized

    wf = data_new[data_new['waterfront'] == 1]
    wf = wf[['waterfront', 'bigger_smaller', 'zipcode']]

    #total_waterfront = wf.groupby(['zipcode','bigger_smaller']).count().reset_index()                    #IT TURNS OUT THAT IT WAS NOT LONGER NEEDED
    #total_estate = data_new[['id', 'bigger_smaller']].groupby('bigger_smaller').count().reset_index()

    ##### FIRST PLOT: Estates vs Price Avg
   # fig1 = px.pie(total_estate, values='id', names='bigger_smaller')
   # fig1.update_traces(textposition='inside')
    #fig1.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    #c1.plotly_chart(fig1, use_container_width=True)

    ##### SECOND PLOT: Estates with waterfront vs Price Avg
    fig1 = px.pie(wf, values='waterfront', names='bigger_smaller', color_discrete_sequence = px.colors.cyclical.Edge)
    fig1.update_traces(textposition='inside', textfont_size=15)
    #fig1.update_layout(uniformtext_minsize=14, uniformtext_mode='hide')
    c1.plotly_chart(fig1, use_container_width=True)

    ##### THIRD PLOT: Estates per region vs Price Avg
    fig2 = px.histogram(wf,
                       x="zipcode",
                       y="waterfront",
                       color="bigger_smaller",
                       histfunc="count",
                       barmode="stack",
                        labels={
                            "bigger_smaller": "Bigger/Smaller than Avg", "zipcode": "Zipcode"
                        },
                        color_discrete_sequence = px.colors.cyclical.Edge
                       )
    c2.plotly_chart(fig2, use_container_width=True)

    return None

def business_hypo_2(data):
    st.header('A. More than 10% of Estates with waterfront are cheaper than average')
    data['zipcode'] = data['zipcode'].astype(str)
    c1, c2 = st.beta_columns(2)

    c1.subheader('Price Avg of Estates with Year Built < 1955')
    c2.subheader('Estates per region vs Price Avg')

    data_new = Functions.create_price_mean_col(data)  # Merges column price_mean on the current dataset

    data_new['percentual'] = data_new.apply(Functions.percentual_growth, axis=1)
    data_new['bigger_smaller'] = data_new.apply(Functions.bigger_smaller_than_avg, axis=1)
    data_new.sort_values('zipcode', inplace=True)  # organizing dataframe by region order so that the plot is organized

    df_yrbuilt = data_new[data_new['yr_built'] < 1955].copy()
    df_yrbuilt.sort_values('zipcode', inplace=True)

    total_df_yrbuilt = df_yrbuilt[['id', 'bigger_smaller', 'zipcode']].groupby(['zipcode', 'bigger_smaller']).count().reset_index()

    fig1 = px.pie(total_df_yrbuilt, values= 'id', names='bigger_smaller', color_discrete_sequence = px.colors.cyclical.Edge)
    fig1.update_traces(textposition='inside', textfont_size=15)
    c1.plotly_chart(fig1, use_container_width=True)

    fig2 = px.histogram(df_yrbuilt,
                        y='id',
                        x='zipcode',
                        color='bigger_smaller',
                        histfunc='count',
                        barmode= 'stack',
                        color_discrete_sequence=px.colors.cyclical.Edge,
                        labels={
                            "bigger_smaller": "Bigger/Smaller than Avg", "zipcode": "Zipcode"
                        }
                        )

if __name__ == '__main__':
    # ETL
    # ---- Data Extraction
    path = 'kc_house_data.csv'
    url = 'Zip_Codes.geojson'
    data = get_data(path)
    geofile = get_geofile(url)

    # ---- Transformation
    data_overview(data)
    portfolio_density(data,geofile)
    buy_estates(data)
    business_hypo_1(data)