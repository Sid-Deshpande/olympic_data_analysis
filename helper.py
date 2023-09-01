import numpy as np


def fetch_medal_tally(athletes, year, country):
    medal_athletes = athletes.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'overall' and country == 'overall':
        temp_athletes = medal_athletes
    elif year == 'overall' and country != 'overall':
        flag = 1
        temp_athletes = medal_athletes[medal_athletes['region'] == country]
    elif year != 'overall' and country == 'overall':
        temp_athletes = medal_athletes[medal_athletes['Year'] == year]
    else:
        temp_athletes = medal_athletes[(medal_athletes['Year'] == year) & (medal_athletes['region'] == country)]

    if flag == 1:
        x = temp_athletes.groupby('Year').sum()[['Bronze', 'Gold', 'Silver']].sort_values('Year').reset_index()
    else:
        x = temp_athletes.groupby('region').sum()[['Bronze', 'Gold', 'Silver']].sort_values('Gold',
                                                                                            ascending=False).reset_index()

    medal_tally = temp_athletes.groupby('region')['Medal'].value_counts().unstack().fillna(0)
    return medal_tally

def medal_tally(athletes):
    medal_tally = athletes.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City',
                                                   'Sport', 'Event', 'Medal'])

    medal_tally = medal_tally.groupby('region').sum()[['Bronze', 'Gold', 'Silver']].sort_values('Gold',
    ascending = False).reset_index()

    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['total'] = medal_tally['total'].astype('int')

    return medal_tally


def country_year_list(athletes):
    years = athletes['Year'].unique().tolist()
    years.insert(0, 'overall')
    country = np.unique(athletes['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'overall')

    return years, country


def participating_nations_over_time(athletes):
    nations_over_time = athletes.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index()
    nations_over_time = nations_over_time.sort_values(by='Year', ascending=True)

    nations_over_time.rename(columns={'index': 'Edition', 'Year': 'No of Countries'}, inplace=True)

    return nations_over_time

def events_occur_over_time(athletes):
    nations_over_time = athletes.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index()
    nations_over_time = nations_over_time.sort_values(by='Year', ascending=True)

    nations_over_time.rename(columns={'index': 'Edition', 'Year': 'Event'}, inplace=True)

    return nations_over_time

def Athlete_over_time(athletes):
    nations_over_time = athletes.drop_duplicates(['Year', 'Name'])['Year'].value_counts().reset_index()
    nations_over_time = nations_over_time.sort_values(by='Year', ascending=True)

    nations_over_time.rename(columns={'index': 'Edition', 'Year': 'Name'}, inplace=True)

    return nations_over_time


def most_successful(athletes, sport):
    temp_athletes = athletes.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_athletes = temp_athletes[temp_athletes['Sport'] == sport]

    x = temp_athletes['Name'].value_counts().reset_index()

    # Merge using the 'Name' column instead of 'index'
    x = x.merge(athletes, left_on='index', right_on='Name', how='left')
    [['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')


    # Rename columns after the merge
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)

    return x


def year_wise_medal_tally(athletes, country):
    temp_athletes = athletes.dropna(subset=['Medal'])
    temp_athletes.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'],
                                  inplace=True)

    new_athletes = temp_athletes[temp_athletes['region'] == country]
    final_athletes = new_athletes.groupby('Year').count()['Medal'].reset_index()

    return final_athletes


def country_event_heatmap(athletes, country):
    temp_athletes = athletes.dropna(subset=['Medal'])
    temp_athletes.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'],
                                  inplace=True)
    new_athletes = temp_athletes[temp_athletes['region'] == country]

    pt = new_athletes.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def most_successful_country_wise(athletes, country):
    temp_athletes = athletes.dropna(subset=['Medal'])

    temp_athletes = temp_athletes[temp_athletes['region'] == country]


    x = temp_athletes['Name'].value_counts().reset_index().head(15).merge(athletes, left_on='index', right_on='Name',
                                                                          how='left')[
            ['index', 'Name_x', 'Sport', ]].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)

    return x

def weight_v_height(athletes, sport):
    player_athletes = athletes.drop_duplicates(subset=['Name', 'region'])
    player_athletes['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':

        temp_athletes = player_athletes[player_athletes['Sport'] == 'sport']
        return temp_athletes

    else:
        return player_athletes


def men_vs_women(athletes):
    player_athletes = athletes.drop_duplicates(subset=['Name', 'region'])
    men = player_athletes[player_athletes['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = player_athletes[player_athletes['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    return final








