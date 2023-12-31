# -*- coding: utf-8 -*-
"""olympic data analyzer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Hs2QZBiNV1fX4cIY08Hraxvxy7BGhCUe
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

athletes=pd.read_csv('/content/athlete_events.csv')
noc_region=pd.read_csv('/content/noc_regions.csv')

athletes.tail()

athletes.shape

# but i need only according to the summer olympic so what i will do
athletes=athletes[athletes['Season']=='Summer']

athletes.shape

# no only data of summer seasons only
athletes.tail()

noc_region.tail()

# now we have to merge both the datasets on the basis of NOC
athletes=athletes.merge(noc_region,on='NOC',how='left')

athletes.head()

# this helps that NOC short form in athletes table gets full form in NOC_region table so that
# is

## if we want to know how many regions participated in the olympics so we do
athletes['region'].unique()
# here if we see there is a historical mistake  russia here has two names like soviet union and russiaetc
# but there is no issue at all

athletes['region'].unique().shape

# here check the null value
athletes.isnull().sum()

# at this point of time hold on this

# checking any duplicate row
athletes.duplicated().sum()

athletes.drop_duplicates(inplace=True)

athletes.duplicated().sum()

# here counts the medal
athletes['Medal'].value_counts()

pd.get_dummies(athletes['Medal'])

# what this function did
# here where there is player got gold it makes it 1 there and rest makes it 0
# and where there is no medal won by any player there written is 0,0,0
# so what we do we put this table with athletes table

athletes=pd.concat([athletes,pd.get_dummies(athletes['Medal'])],axis=1)

athletes.head()

athletes.groupby('region').sum()[['Bronze','Gold','Silver']].sort_values('Gold',ascending=False).reset_index()

# when we tally with google this gives wrong data as real is upto 2016 summer olympics USA
# has won 1022 Gold medals and here showing 2472
# again if we looking for india here they are showing 131 gold medals but actually india won only 9 gold medals



# after so much research i got to know that it is calculating individual atheltes medals
# for ex- ina hockey india won 8 gold medals but it is calculating 8*11 and some extra players medals
# so it is calculating individuals atheletes medals that is why india got 131 medals

athletes[(athletes['NOC']=='IND') & (athletes['Medal']=='Gold')]


# here the examples of above written description


# so this data has to be removed as this is totally a wrong data

# we have to remove the duplicate data on the basis of team,noc,year,season,games,city

medal_tally=athletes.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])

medal_tally=medal_tally.groupby('region').sum()[['Bronze','Gold','Silver']].sort_values('Gold',ascending=False).reset_index()

medal_tally

medal_tally['total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']

medal_tally

# still medals are coming slightly wrong numbers

medal_tally[medal_tally['region']=='IND']

# this is right for india
# so this could be enough for the data

years=athletes['Year'].unique().tolist()

years

years.insert(0,'overall')

years

country=athletes['region'].unique().tolist()

country

# to remove nan value from here
country = np.unique(athletes['region'].dropna().values).tolist()

country.sort()

country.insert(0,'overall')

country

def fetch_medal_tally(year,country):
  if year=='overall' & country=='overall':
    temp_athletes=medal_athletes
  if year=='overall' & country!='overall':
    temp_athletes=medal_athletes[medal_athletes['region']=='country']
  if year!='overall' & country=='overall':
    temp_athletes=medal_athletes[medal_athletes['Year']==int(year)]
  if year!='overall' & country!='overall':
    temp_athletes=medal_athletes[(medal_athletes['Year']==int(year)) & (medal_athletes['region']=='country')]

  x=temp_athletes.groupby('region').sum()[['Bronze','Gold','Silver']].sort_values('Gold',ascending=False).reset_index()
  x['total']=x['Gold'] + x['Silver'] + x['Bronze']

  print(x)

medal_athletes=athletes.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])

medal_athletes



medal_athletes[(medal_athletes['Year']==2016) & (medal_athletes['region']=='India')]

def fetch_medal_tally(athletes,year, country):
    medal_athletes=athletes.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag=0
    if year == 'overall' and country == 'overall':
        temp_athletes = medal_athletes
    elif year == 'overall' and country != 'overall':
        flag=1
        temp_athletes = medal_athletes[medal_athletes['region'] == country]
    elif year != 'overall' and country == 'overall':
        temp_athletes = medal_athletes[medal_athletes['Year'] == year]
    else:
        temp_athletes = medal_athletes[(medal_athletes['Year'] == year) & (medal_athletes['region'] == country)]

    if flag==1:
      x=temp_athletes.groupby('Year').sum()[['Bronze','Gold','Silver']].sort_values('Year').reset_index()
    else:
      x=temp_athletes.groupby('region').sum()[['Bronze','Gold','Silver']].sort_values('Gold',ascending=False).reset_index()

    medal_tally = temp_athletes.groupby('region')['Medal'].value_counts().unstack().fillna(0)
    return medal_tally

fetch_medal_tally(athletes,year='overall',country='India')

"""# time for the overall analysis so far we have done it is for medal_tally
*   number of editions
*   number of cities
*   number of ahletes/events
*   number of sports
*   participating nations







"""

athletes.head(2)

athletes['Year'].unique()

# 1906 year is not considered as a olympic so we have to remove its shape
athletes['Year'].unique().shape[0]-1

athletes['City'].unique()

athletes['City'].unique().shape

athletes['Sport'].unique()

athletes['Sport'].unique().shape

athletes['Event'].unique()

athletes['Event'].unique().shape

athletes['Name'].unique()

athletes['Name'].unique().shape

athletes['region'].unique()

athletes['region'].unique().shape

# participating nations over a years
athletes.head()

athletes.drop_duplicates(['Year','region'])

nations_over_time=athletes.drop_duplicates(['Year','region'])['Year'].value_counts().reset_index().sort_values('index')

nations_over_time

nations_over_time.rename(columns={'index':'Edition','Year':'No of Countries'},inplace=True)

nations_over_time

import plotly.express as px

fig=px.line(nations_over_time,x="Edition",y="No of Countries")
fig.show()

nations_over_time = athletes.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index()
nations_over_time = nations_over_time.sort_values(by='Year', ascending=True)

nations_over_time

nations_over_time.rename(columns={'index':'Edition','Year':'No of Countries'},inplace=True)

nations_over_time

nations_over_time = athletes.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index()

nations_over_time = nations_over_time.sort_values(by='Year', ascending=True)

nations_over_time

plt.figure(figsize=(25,25))
sns.heatmap(athletes.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype
            ('int'),annot=True,cmap='YlGnBu')

# Create a pivot table and plot a heatmap
plt.figure(figsize=(25, 25))
heatmap_data = athletes.pivot_table(
    index='Sport', columns='Year', values='Event', aggfunc='count'
).fillna(0).astype(int)
sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu')
plt.title('Event Counts by Sport and Year')
plt.show()

x=athletes.drop_duplicates(['Year','Sport','Event'])

plt.figure(figsize=(25, 25))
sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype(int),annot=True)

athletes.dropna(subset='Medal')

"""Most succesful athletes in the olympics"""

def most_successful(athletes,sport):
  temp_athletes=athletes.dropna(subset=['Medal'])

  if sport !='Overall':
    temp_athletes=temp_athletes[temp_athletes['Sport'] == sport]

  x = temp_athletes['Name'].value_counts().reset_index().head(15).merge(athletes,left_on='index',right_on='Name',how='left')[
      ['index','Name_x','Sport','region']].drop_duplicates('index')
  x.rename(columns={'index':'Name','Name_x':'Medals'},inplace=True)

  return x

most_successful(athletes,'Overall')

"""country wise analysis

*  country-wise medal tally per year(line plot)
*  what countries are good at heat map
*  most succesful athlete top(10)




"""

athletes

# first we have to drop nan value of medal
temp_athletes = athletes.dropna(subset=['Medal'])

temp_athletes

temp_athletes.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace=True)

new_athletes = temp_athletes[temp_athletes['region']=='USA']
final_athletes = new_athletes.groupby('Year').count()['Medal'].reset_index()

final_athletes

fig=px.line(final_athletes,x="Year",y="Medal")
fig.show()

new_athletes = temp_athletes[temp_athletes['region']=='China']
plt.figure(figsize=(25,25))
sns.heatmap(new_athletes.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0),annot=True)

def most_successful(athletes,country):
  temp_athletes=athletes.dropna(subset=['Medal'])

  temp_athletes=temp_athletes[temp_athletes['region'] == country]

  x = temp_athletes['Name'].value_counts().reset_index().head(15).merge(athletes,left_on='index',right_on='Name',how='left')[
      ['index','Name_x','Sport',]].drop_duplicates('index')
  x.rename(columns={'index':'Name','Name_x':'Medals'},inplace=True)

  return x

most_successful(athletes,'Jamaica')

"""Athlete wise analysis starts"""

import plotly.figure_factory as ff

player_athletes = athletes.drop_duplicates(subset=['Name','region'])

player_athletes['Age'].dropna()

x1=player_athletes['Age'].dropna()
x2=player_athletes[player_athletes['Medal']=='Gold']['Age'].dropna()
x3=player_athletes[player_athletes['Medal']=='Silver']['Age'].dropna()
x4=player_athletes[player_athletes['Medal']=='Bronze']['Age'].dropna()

fig=ff.create_distplot([x1,x2,x3,x4],['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
fig.show()

famous_sports=['Basketball','Judo','Football','Tug-of-war','Athletics',
               'Swimming','Badminton','Sailing','Gymnastics',
               'Art Competitions','Handball','Weightlifting','Wrestling',
               'Water Polo','Hockey','Rowing','Fencing',
               'Shooting','Boxing','taekwondo','Cycling','Diving','Canoeing'
               ,'Tennis','Golf','Softball','Archery','Volleyball',
               'Synchronized Swimming','Baseball','Table Tennis',
               'Rhythmic Gymnastics','Rugby Sevens','Beach Volleyball','Polo',
               'Rugby','Triathlon','Ice Hockey']

famous_sports

x=[]
name=[]
for sport in famous_sports:
  temp_athletes=player_athletes[player_athletes['Sport']==sport]
  x.append(temp_athletes[temp_athletes['Medal']=='Gold']['Age'].dropna())
  name.append(sport)

x = []
name = []

for sport in famous_sports:
    temp_athletes = player_athletes[player_athletes['Sport'] == sport]
    gold_ages = temp_athletes[temp_athletes['Medal'] == 'Gold']['Age'].dropna()
    x.append(gold_ages)
    name.append(sport)
    print(f"Sport: {sport}, Gold Ages: {gold_ages}")

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
    fig.add_trace(trace, row=i+1, col=1)

    fig.update_yaxes(title_text="Frequency", row=i+1, col=1)
    fig.update_xaxes(title_text="Age", row=i+1, col=1)

fig.update_layout(title="Distribution of Ages for Gold Medalists in Different Sports")
fig.show()

player_athletes

player_athletes['Medal'].fillna('No Medal',inplace=True)

plt.figure(figsize=(10, 10))
temp_athletes=player_athletes[player_athletes['Sport']=='Athletics']
sns.scatterplot(x=temp_athletes['Weight'], y=temp_athletes['Height'],hue=temp_athletes['Medal'],style=temp_athletes['Sex'],s=100)
plt.show()

men=player_athletes[player_athletes['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
women=player_athletes[player_athletes['Sex']=='F'].groupby('Year').count()['Name'].reset_index()

men

women

final=men.merge(women,on='Year',how='left')

final

final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)

final.fillna(0,inplace=True)

final

fig = px.line(final,x="Year",y=["Male","Female"])
fig.show()

