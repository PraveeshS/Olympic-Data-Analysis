import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd


df=pd.read_csv('athlete_events.csv')
df1=pd.read_csv('noc_regions.csv')

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby(['NOC','region']).sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['total'] = medal_tally[['Gold', 'Silver', 'Bronze']].sum(axis=1)
    return medal_tally





def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country


import matplotlib.cm as cm

import plotly.express as px
import geopandas as gpd
import streamlit as st


def geoplot(medal_tally):
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    world = world.merge(medal_tally, how='left', left_on='iso_a3', right_on='NOC')

   
    fig = px.choropleth_mapbox(
        world,
        geojson=world.geometry,
        locations=world.index,
        color='total',
        hover_name='region',
        color_continuous_scale='Viridis',  
        mapbox_style='carto-positron',
        center={'lat': 0, 'lon': 0},
        zoom=1,
        opacity=0.7,  
        labels={'total': 'Total Medals'}, width=800 

    )

   
    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0),  
        coloraxis_colorbar=dict(
            title='Total Medals',
            tickvals=[0, medal_tally['total'].max()],
            ticktext=['0', str(medal_tally['total'].max())],
        ),
    )

  
    fig.update_geos(
        showcoastlines=False,  
        showland=True,  
        showcountries=True,  
        showocean=True,  
    )


    st.plotly_chart(fig)

import plotly.express as px
import streamlit as st

def top_10(medal_tally):
    medal_tally = medal_tally.sort_values(by='total', ascending=False)

    top_10 = medal_tally.head(10)
    color_discrete_map = {'Gold': '#6DA7E5', 'Silver': '#FFA500', 'Bronze': '#79C978'}
    fig = px.bar(
        top_10,
        x='region',
        y=['Gold', 'Silver', 'Bronze'],
        color_discrete_map=color_discrete_map,
        labels={'region': 'Country', 'value': 'Number of Medals', 'variable': 'Medal'},
        height=500,width=800
    )

    # Customize plot labels and title
    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0),
        xaxis_title='Country',
        yaxis_title='Number of Medals',
    )

    # Show the plot using Streamlit
    st.plotly_chart(fig)

# Example usage
# top_10(medal_tally)


def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year': 'Edition', 'count': col}, inplace=True)
    return nations_over_time

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df




def get_top_athletes(merged_df, selected_sport):
    # Filter data for the selected sport if it is provided
    merged_df = df.merge(df1, on='NOC', how='left')
    if selected_sport and selected_sport != 'Overall':
        temp_df_sport = merged_df[merged_df['Sport'] == selected_sport]
    else:
        temp_df_sport = merged_df[merged_df['Sport'] != 'Art Competitions']


    # Get the top athletes for the selected sport or overall
    top_athletes = temp_df_sport['Name'].value_counts().reset_index().head(15).merge(
        temp_df_sport[['Name', 'region', 'Sport']].drop_duplicates('Name'),
        left_on='Name',
        right_on='Name',
        how='left'
    ).drop_duplicates('Name')

    # Rename the 'count' column to 'Medal'
    top_athletes = top_athletes.rename(columns={'index': 'Name', 'count': 'Medal'})

    return top_athletes




    



    
def most_successful(merged_df, sport):
    merged_df = df.merge(df1, on='NOC', how='left')
    temp_df = merged_df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(merged_df, left_on='Name', right_on='Name', how='left')[
        ['Name', 'count', 'Sport', 'region']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals','region':'Country'}, inplace=True)
    x = x.sort_values(by='Medals', ascending=False)
    return x


def most_successful_countrywise(merged_df, country):
    merged_df = df.merge(df1, on='NOC', how='left')
    temp_df = merged_df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, left_on='Name', right_on='Name', how='left')[
        ['Name', 'count', 'Sport']].drop_duplicates('Name')
    x.rename(columns={'Name': 'Name', 'count': 'Medals'}, inplace=True)
    return x


def most_successful_yearwise(merged_df, year):
    temp_df = merged_df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['Year'] == year]

    # Count the number of medals for each athlete
    athlete_counts = temp_df['Name'].value_counts().reset_index()
    athlete_counts.columns = ['Name', 'Medals']

    # Merge with the original DataFrame to get additional information like 'Sport'
    top_athletes = pd.merge(athlete_counts.head(10), df, on='Name', how='left')[['Name', 'Medals', 'Sport']].drop_duplicates('Name')

    return top_athletes

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
 

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def male_female_participants_yearwise(df, year):
    temp_df = df[df['Year'] == year]

    temp_df = temp_df.drop_duplicates(subset='Name')

    # Group by gender and count the number of participants
    gender_counts = temp_df['Sex'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']

    return gender_counts