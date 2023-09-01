import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import scipy
from plotly.figure_factory import create_distplot

athletes = pd.read_csv('athlete_events.csv')
noc_region = pd.read_csv('noc_regions.csv')

athletes = preprocessor.preprocess(athletes, noc_region)

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://cdn.pixabay.com/photo/2013/02/15/10/58/blue-81847_1280.jpg')


user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-Wise Analysis', 'Athlete-Wise Analysis')
)

st.dataframe(athletes)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(athletes)
    selected_year=st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    medal_tally = helper.fetch_medal_tally(athletes,selected_year,selected_country)

    if selected_year=='overall' and selected_country=='overall':
        st.title("Overall Tally")
    if selected_year!='overall' and selected_country=='overall':
        st.title("Medal_tally in" + str(selected_year))
    if selected_year == 'overall' and selected_country != 'overall':
        st.title("Selected_country" + "overall performance")
    if selected_year != 'overall' and selected_country != 'overall':
        st.title(selected_country + "performance in" + str(selected_year))

    st.dataframe(medal_tally)

if user_menu == 'Overall Analysis':
    editions=athletes['Year'].unique().shape[0]-1
    cities=athletes['City'].unique().shape[0]
    sports=athletes['Sport'].unique().shape[0]
    events=athletes['Event'].unique().shape[0]
    athlete=athletes['Name'].unique().shape[0]
    nations=athletes['region'].unique().shape[0]
    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)

    with col2:
        st.header("Hosts")
        st.title(cities)

    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)

    with col2:
        st.header("Nations")
        st.title(nations)

    with col3:
        st.header("Athletes")
        st.title(athlete)

    nations_over_time = helper.participating_nations_over_time(athletes)
    fig = px.line(nations_over_time, x="No of Countries", y="count")
    st.title("participating nations over a time")
    st.plotly_chart(fig)

    nations_over_time = helper.events_occur_over_time(athletes)
    fig = px.line(nations_over_time, x="Event", y="count")
    st.title("events occur over a time")
    st.plotly_chart(fig)

    nations_over_time = helper.Athlete_over_time(athletes)
    fig = px.line(nations_over_time, x="Name", y="count")
    st.title("Athletes over a time")
    st.plotly_chart(fig)

    st.title("No of Sports over time(every sports)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = athletes.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),
                annot=True)
    st.pyplot(fig)


    st.title("Most successful Athletes")
    sport_list= athletes['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(athletes, selected_sport)
    st.table(x)


if user_menu == 'Country-Wise Analysis':

    st.title('Country-Wise Analysis')
    country_list=athletes['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.selectbox('select a country',country_list)
    country_athletes = helper.year_wise_medal_tally(athletes,selected_country)
    fig = px.line(country_athletes, x="Year", y="Medal")
    st.title(selected_country + " " + "Medal Tally Over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " " + "excels in the following sports")
    pt = helper.country_event_heatmap(athletes,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes" + " " + selected_country)
    top10_athletes = helper.most_successful_country_wise(athletes,selected_country)
    st.table(top10_athletes)


if user_menu == 'Athlete-Wise Analysis':
    player_athletes = athletes.drop_duplicates(subset=['Name', 'region'])
    x1 = player_athletes['Age'].dropna()
    x2 = player_athletes[player_athletes['Medal'] == 'Gold']['Age'].dropna()
    x3 = player_athletes[player_athletes['Medal'] == 'Silver']['Age'].dropna()
    x4 = player_athletes[player_athletes['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                             show_hist=False, show_rug=False)

    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution Of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-of-war', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'taekwondo', 'Cycling', 'Diving', 'Canoeing'
        , 'Tennis', 'Golf', 'Softball', 'Archery', 'Volleyball',
                     'Synchronized Swimming', 'Baseball', 'Table Tennis',
                     'Rhythmic Gymnastics', 'Rugby Sevens', 'Beach Volleyball', 'Polo',
                     'Rugby', 'Triathlon', 'Ice Hockey']
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    # Initialize subplots
    num_sports = len(famous_sports)
    fig = make_subplots(rows=num_sports, cols=1, subplot_titles=famous_sports)

    # Create distribution plots for each sport
    for i, sport in enumerate(famous_sports):
        temp_athletes = player_athletes[(player_athletes['Sport'] == sport) & (player_athletes['Medal'] == 'Gold')]
        ages = temp_athletes['Age'].dropna()

        trace = go.Histogram(x=ages, showlegend=False)
        fig.add_trace(trace, row=i + 1, col=1)

        fig.update_yaxes(title_text="Frequency", row=i + 1, col=1)
        fig.update_xaxes(title_text="Age", row=i + 1, col=1)

    fig.update_layout(title="Distribution of Ages for Gold Medalists in Different Sports")
    fig.show()

    sport_list = athletes['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    st.title("Height vs Weight")
    selected_sport = st.selectbox('Select a Sport', sport_list)

    temp_athletes = helper.weight_v_height(athletes, selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(x=temp_athletes['Weight'], y=temp_athletes['Height'],hue=temp_athletes['Medal'],style=temp_athletes['Sex'],s=60)

    st.pyplot(fig)

    st.title("Men vs Women Participation Over the Years")
    final = helper.men_vs_women(athletes)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)






