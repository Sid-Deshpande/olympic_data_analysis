import pandas as pd




def preprocess(athletes,noc_region):

    # filtering for the summer olympics
    athletes = athletes[athletes['Season'] == 'Summer']
    # merge with noc_region
    athletes = athletes.merge(noc_region, on='NOC', how='left')
    # dropping duplicate values
    athletes.drop_duplicates(inplace=True)
    # one hot encoding for the medals
    athletes = pd.concat([athletes, pd.get_dummies(athletes['Medal'])], axis=1)

    return athletes

