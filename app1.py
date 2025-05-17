import base64
from tkinter import Image
import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff


df=pd.read_csv('athlete_events.csv')
df1=pd.read_csv('noc_regions.csv')

import streamlit as st

st.set_page_config(page_title="Olympics Analysis", page_icon="🏅")


import streamlit as st
import base64





st.sidebar.markdown(
    """
    <style>
        .sidebar-title {
            font-family: 'Arial', sans-serif;
            color: #FFD700;  
            font-size: 23px;
            font-weight: bold;
            text-align: center;
            padding: 20px 0;
            margin-bottom: 10px;
            border-bottom: 2px solid #FFD700;
            background-color:black;  
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown('<div class="sidebar-title">Olympics Data Analysis</div>', unsafe_allow_html=True)





st.sidebar.image('olympics.jpg')
df=preprocessor.preprocess(df,df1)
user_menu = st.sidebar.selectbox(
    'Select an Option',
    ('Overall Analysis', 'Athlete wise Analysis', 'Medal Tally', 'Country-Year wise Analysis')
)
st.markdown(
    """
    <style>
        div[data-testid="stSidebar"][aria-expanded="true"] > div {
            background-color: #f8f9fa !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)



if user_menu == 'Medal Tally':

    st.markdown("<p style='font-family: Arial; color: gold; font-size: 43px; font-weight: bold;'>Geoplot Visualization of Total medal Distribution</p>", unsafe_allow_html=True)
    medal_tally = helper.medal_tally(df)
    helper.geoplot(medal_tally)

    st.markdown("<p style='font-family: Arial; color: #FFD700; font-size: 43px; font-weight: bold;'>Top 10 countries</p>", unsafe_allow_html=True)
    helper.top_10(medal_tally)
   
 
if user_menu=='Overall Analysis':

    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]


    st.markdown("<p style='font-style:Arial; color: gold; font-size: 45px; font-weight: bold;'>Overall Statistics</p>", unsafe_allow_html=True)


    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("<p style='font-style:Arial;color: gold;font-size: 40px; font-weight: bold'>Editions</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-style:Arial;color: gold; font-size: 40px;font-weight: bold'>{editions}</p>", unsafe_allow_html=True)

    with col2:
        st.markdown("<p style='font-style:Arial ;color: gold;font-size: 40px; font-weight: bold'>Hosts</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-style:Arial; color: gold; font-size: 40px;font-weight: bold'>{cities}</p>", unsafe_allow_html=True)

    with col3: 
        st.markdown("<p style='font-style:Arial;  color: gold;font-size: 40px; font-weight: bold'>Sports</p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-style:Arial; color: gold; font-size: 40px;font-weight: bold'>{sports}</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
       st.markdown("<p style='font-style:Arial; color: gold;font-size: 40px; font-weight: bold'>Events</p>", unsafe_allow_html=True)
       st.markdown(f"<p style='font-style:Arial; color: gold; font-size:40px;font-weight: bold'>{events}</p>", unsafe_allow_html=True)

    with col2:
       st.markdown("<p style='font-style:Arial; color: gold;font-size: 40px; font-weight: bold'>Nations</p>", unsafe_allow_html=True)
       st.markdown(f"<p style='font-style:Arial; color: gold; font-size: 40px;font-weight: bold'>{nations}</p>", unsafe_allow_html=True)

    with col3:
       st.markdown("<p style='font-style:Arial; color: gold;font-size: 40px; font-weight: bold'>Athletes</p>", unsafe_allow_html=True)
       st.markdown(f"<p style='font-style:Arial; color: gold; font-size: 40px;font-weight: bold'>{athletes}</p>", unsafe_allow_html=True)

    

    st.markdown("<br>", unsafe_allow_html=True)
    # Participating Nations over the years
    st.markdown("<p style='font-style:Arial; color: gold;font-size: 43px; font-weight: bold'>Participating Nations over the years</p>", unsafe_allow_html=True)
    nations_time = helper.data_over_time(df, 'region')
    fig_nations = px.line(nations_time,x="Edition",y="region",
    markers=True, 
    line_shape='linear',  
    render_mode='svg',  
    hover_data={'region': True, 'Edition': True}, 
)
    st.plotly_chart(fig_nations)

    st.markdown("<p style='font-style:Arial; color: gold;font-size: 43px; font-weight: bold'>Event over the years</p>", unsafe_allow_html=True)
    nations_time = helper.data_over_time(df, 'Event')
    fig_nations = px.line(nations_time,x="Edition",y="Event",
    markers=True, 
    line_shape='linear',  
    render_mode='svg',  
    hover_data={'Event': True, 'Edition': True}, 
)
    
    st.plotly_chart(fig_nations)
    
    st.markdown("<p style='font-style:Arial; color: gold;font-size: 43px; font-weight: bold'>Participants over the years</p>", unsafe_allow_html=True)
    nations_time = helper.data_over_time(df, 'Name')
    fig_nations = px.line(nations_time,x="Edition",y="Name",
    markers=True, 
    line_shape='linear',  
    render_mode='svg',  
    hover_data={'Name': True, 'Edition': True}, 
)
    
    st.plotly_chart(fig_nations)


    
    st.markdown("<p style='font-style:Arial; color: gold;font-size: 43px; font-weight: bold'>No. of every sports Events</p>", unsafe_allow_html=True)
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event' ])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.markdown("<p style='font-family: Arial; color: #FFD700; font-size: 43px; font-weight: bold;'>Top 10 Successful Athletes</p>", unsafe_allow_html=True)
 
    sport_list = df[df['Sport'] != 'Art Competitions']['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox(
    'Select a Sport',
    sport_list
)


    x=helper.most_successful(df,selected_sport)
    
    x = x.sort_values(by='Medals', ascending=False)


    fig = px.bar(x, x='Name', y='Medals', color='Country', 
                 labels={'Medals':'Medals', 'Sport':'Sport', 'Country':'Country'},
                  height=800, category_orders={'Name': x['Name'].tolist()})

    fig.update_layout(xaxis_title='Athlete Name',
    yaxis_title='Number of Medals',
    barmode='stack', 
)
    fig.update_traces(
    hovertemplate='<b>%{x}</b><br>Sport: %{customdata[0]}<br>Country: %{customdata[1]}<br>Medals: %{y}<br>',
    customdata=x[['Sport', 'Country']].values.tolist(),  
)

    st.plotly_chart(fig)



   

   

if user_menu == 'Athlete wise Analysis':

    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()


    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    st.markdown("<p style='font-family: Arial; color: #FFD700; font-size: 43px; font-weight: bold;'>Men Vs Women Participation Over the Years</p>", unsafe_allow_html=True)
    final = helper.men_vs_women(df)
    fig = px.area(final, x='Year', y=['Male', 'Female'], 
              labels={'value': 'Number of Participants'},
              color_discrete_map={'Male': 'blue', 'Female': 'pink'})

    fig.update_layout(autosize=False, width=900, height=600)

    st.plotly_chart(fig)

    st.markdown("<p style='font-family: Arial; color: #FFD700; font-size: 43px; font-weight: bold;'>Height vs Weight</p>", unsafe_allow_html=True)
    sport_list = df[df['Sport'] != 'Art Competitions']['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list, key=f"select_{sport}")
    st.markdown(
    f"""
    <style>
    .st-bp {{
        max-width: 600px; /* Adjust the max-width as needed */
    }}
    </style>
    """,
    unsafe_allow_html=True
)
    temp_df = helper.weight_v_height(df, selected_sport)
    fig = px.scatter(temp_df, x='Weight', y='Height', color='Medal', symbol='Sex', size_max=12, labels={'Medal': 'Medal'}, hover_name='Name',width=900, height=700)

    
    
    fig.update_traces(marker=dict(size=15, line=dict(width=2, color='Black')))




# Display the Plotly figure in the Streamlit app
    st.plotly_chart(fig)
    

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=900,height=600)
    st.markdown("<p style='font-family: Arial; color: #FFD700; font-size:43px; font-weight: bold;'>Distribution of Age</p>", unsafe_allow_html=True)
    st.plotly_chart(fig)

    
    

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=900, height=600)
    st.markdown("<p style='font-family: Arial; color: #FFD700; font-size: 43px; font-weight: bold;'>Distribution of Age wrt Sports</p>", unsafe_allow_html=True)
    st.plotly_chart(fig)


  


    


if user_menu == 'Country-Year wise Analysis':
    st.sidebar.title('Country-Year wise Analysis')

    user_menu1 = st.sidebar.radio('Select a Type', ['Country-wise Analysis', 'Year-Wise Analysis'])

    if user_menu1=='Country-wise Analysis':

        country_list = df['region'].dropna().unique().tolist()
        country_list.sort()

        selected_country = st.sidebar.selectbox('Select a Country',country_list)

        country_df = helper.yearwise_medal_tally(df,selected_country)
        fig = px.line(country_df, x="Year", y="Medal")
        st.markdown("<p style='font-family: Arial; color: #FFD700; font-size: 43px; font-weight: bold;'>"+ selected_country + " Medal Tally over the years</p>", unsafe_allow_html=True)
        st.plotly_chart(fig)

        st.markdown("<p style='font-family: Arial; color: #FFD700; font-size: 43px; font-weight: bold;'>Top 10 athletes of " + selected_country+"</p>", unsafe_allow_html=True)
        top10_df = helper.most_successful_countrywise(df,selected_country)
        fig = px.scatter(top10_df, x='Name', y='Sport', size='Medals', color='Sport',
                 labels={'Name': 'Athlete Name', 'Sport': 'Sport', 'Medals': 'Number of Medals'})


        fig.update_layout(
    xaxis_title='Athlete Name',
    yaxis_title='Sport',
    showlegend=True,
    width=800
)

        st.plotly_chart(fig)


        st.markdown("<p style='font-family: Arial; color: #FFD700; font-size: 43px; font-weight: bold;'>"+selected_country + " excels in the following sports</p>", unsafe_allow_html=True)
        pt = helper.country_event_heatmap(df, selected_country)


        if not pt.empty:
            fig, ax = plt.subplots(figsize=(20, 20))
            ax = sns.heatmap(pt, annot=True)
            st.pyplot(fig)
        else:
            fig, ax = plt.subplots(figsize=(10, 10))
            ax.text(0.5, 0.5, "No data available for the selected country.", 
            horizontalalignment='center', verticalalignment='center', fontsize=14, color='gray')
            ax.axis('off')
            st.pyplot(fig)
        st.markdown("<br>", unsafe_allow_html=True)

        
    if user_menu1 == 'Year-Wise Analysis':
        year_list = df['Year'].dropna().astype(int).unique().tolist()
        year_list.sort()

        selected_year = st.sidebar.selectbox('Select a Year', year_list)

        st.markdown("<p style='font-family: Arial; color: #FFD700; font-size: 43px; font-weight: bold;'>Top 10 athletes of " + str(selected_year) + "</p>", unsafe_allow_html=True)
        top10_df = helper.most_successful_yearwise(df, selected_year)
        fig = px.scatter(top10_df, x='Name', y='Sport', size='Medals', color='Sport',
                 labels={'Name': 'Athlete Name', 'Sport': 'Sport', 'Medals': 'Number of Medals'})
    
        fig.update_layout(width=800,height=600)
        st.plotly_chart(fig)


    

        st.markdown("<p style='font-family: Arial; color: #FFD700; font-size: 43px; font-weight: bold;'> Male and Female Participants in " + str(selected_year)+"</p>", unsafe_allow_html=True)
        gender_counts_yearwise = helper.male_female_participants_yearwise(df, selected_year)

        fig = px.pie(gender_counts_yearwise, values='Count', names='Gender',
             labels={'Gender': 'Participant Gender','F':'Female'})
        st.plotly_chart(fig)