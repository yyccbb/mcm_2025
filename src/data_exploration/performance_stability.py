
# X Feature Explaination: 
# Those with advantage in certain sports will have 
# higher stability in winning medals

import pandas as pd
from tqdm import tqdm
import numpy as np
import time
from pathlib import Path
base_dir = Path(__file__).parents[2]
athletes = pd.read_csv(base_dir / './Data/summerOly_athletes.csv')
medal_counts = pd.read_csv(base_dir / './Data/summerOly_medal_counts.csv')
hosts = pd.read_csv(base_dir/'./Data/summerOly_hosts.csv')

athletes['Sport'] = athletes['Sport'].str.strip() 
athletes_df=pd.DataFrame(athletes)
# print(athletes.columns)
#国家的优势项目

#count events in each sport
events_per_sport = athletes_df.groupby('Sport')['Event'].nunique().reset_index()
print(events_per_sport)
#rank country by medal count per sport
medals_per_sport = athletes_df.groupby(['Team', 'Sport'])['Medal'].count().reset_index()
# print(medals_per_sport)

#find list of teams with top 5 medal counts in for each event
top_teams = medals_per_sport.groupby('Sport').apply(lambda x: x.nlargest(5, 'Medal')).reset_index(drop=True)
# print(top_teams)

#{Sport1,[NOC1,NOC2,NOC3]}
sport_advantage_countries={}
for sport in top_teams['Sport'].unique():
    teams=list(top_teams[top_teams['Sport']==sport]['Team'].unique())
    sport_advantage_countries[sport]=teams

#convert to dataframe
temp={"Sport":[],"Countries":[]}

for s in sport_advantage_countries.keys():
    temp["Sport"].append(s)
    temp["Countries"].append(sport_advantage_countries[s])

sport_advantage_countries_df=pd.DataFrame(temp)
    
print(sport_advantage_countries_df)

#定义historical NOC SPORT优势系数

country_scores = {}

# Iterate through each row in sport_advantage_countries_df

# 加权event per sport

for index, row in sport_advantage_countries_df.iterrows():
    countries = row['Countries']
    sport=row['Sport']
    sport_weight = events_per_sport.loc[events_per_sport["Sport"] == sport, "Event"].values[0]
    # print(sport_weight.info)
    for i, country in enumerate(countries):
        score = sport_weight*(5 - i)
        if score > 0:  # Only add positive scores
            if country in country_scores:
                country_scores[country] += score
            else:
                country_scores[country] = score

# Convert the dictionary to a DataFrame
score_df = pd.DataFrame(list(country_scores.items()), columns=['Country', 'Score'])
score_df = score_df.sort_values('Score', ascending=False)
# add zero rows to historical data
list_of_zero_countries=list(athletes_df["Team"].unique())
zero_scores_df = pd.DataFrame({'Country': list_of_zero_countries, 'Score': 0})
score_df = pd.concat([score_df, zero_scores_df[~zero_scores_df['Country'].isin(score_df['Country'])]], ignore_index=True)

#take log of score
score_df['log Score'] = score_df['Score'].apply(lambda x: np.log(x))
#Take Standarized score
score_df['Standardized Score'] = (score_df['Score'] - score_df['Score'].mean()) / score_df['Score'].std()
#take e to the standarized score power
score_df['e^Standardized Score'] = np.exp(score_df['Standardized Score'])
#take the min max standarized score
score_df['Min-Max Standardized Score'] = (score_df['Score'] - score_df['Score'].min()) / (score_df['Score'].max() - score_df['Score'].min())


# print(score_df)



#create dataframe of all countries' score, if country not in score_df, score is 0




#Task: 优势系数乘以time sensitive 优势值
#Subtask: time sensitive 优势值
def subset_df(df,year,interval=2):
    return df[df['Year'].isin([year-4*interval,year,4])]

sub_athletes_df=subset_df(athletes,2024)



def get_time_sensitive_advantage(year):
    #count events in each sport
    events_per_sport = sub_athletes_df.groupby('Sport')['Event'].nunique().reset_index()
    # print(events_per_sport)
    #rank country by medal count per sport
    medals_per_sport = sub_athletes_df.groupby(['Team', 'Sport'])['Medal'].count().reset_index()
    # print(medals_per_sport)

    #find list of teams with top 5 medal counts in for each event
    top_teams = medals_per_sport.groupby('Sport').apply(lambda x: x.nlargest(5, 'Medal')).reset_index(drop=True)
    # print(top_teams)

    #{Sport1,[NOC1,NOC2,NOC3]}
    sport_advantage_countries={}

    for sport in top_teams['Sport'].unique():
        teams=list(top_teams[top_teams['Sport']==sport]['Team'].unique())
        sport_advantage_countries[sport]=teams

    #convert to dataframe
    temp={"Sport":[],"Countries":[]}

    for s in sport_advantage_countries.keys():
        temp["Sport"].append(s)
        temp["Countries"].append(sport_advantage_countries[s])

    sport_advantage_countries_df=pd.DataFrame(temp)
    
    # print(sport_advantage_countries_df)

    country_scores = {}
    score_df = pd.DataFrame(list(country_scores.items()), columns=['Country', 'Score'])
    score_df = score_df.sort_values('Score', ascending=False)

    # Iterate through each row in sport_advantage_countries_df
    for index, row in sport_advantage_countries_df.iterrows():
        countries = row['Countries']
        sport=row['Sport']
        sport_weight = events_per_sport.loc[events_per_sport["Sport"] == sport, "Event"].values[0]
    # print(sport_weight.info)
        for i, country in enumerate(countries):
            score = sport_weight*(5 - i)
            if score > 0:  # Only add positive scores
                if country in country_scores:
                    country_scores[country] += score
                else:
                    country_scores[country] = score

    score_df = pd.DataFrame(list(country_scores.items()), columns=['Country', 'Score'])

    #insert 0 scores:for countries not in score_df, their score should be 0
    list_of_zero_countries_in_year=list(athletes_df["Team"].unique())
    zero_scores_df = pd.DataFrame({'Country': list_of_zero_countries_in_year, 'Score': 0})
    score_df = pd.concat([score_df, zero_scores_df[~zero_scores_df['Country'].isin(score_df['Country'])]], ignore_index=True)

    score_df = score_df.sort_values('Score', ascending=False)

    return score_df

print(score_df)
advantage_scores_2024=get_time_sensitive_advantage(2024)
print(advantage_scores_2024)


#Task: 组合加权：

#KL divergence 

