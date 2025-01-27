import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import src.util.dataloader as dl
from scipy.stats import linregress

athletes = dl.athletes_dataset()
athletes = athletes[athletes['Year'] >= 1972]  # Filter out data before 1972

# athletes['Team'] = athletes['Team'].str.strip()  # 去除 Team 字段中的空格
# athletes['Year'] = athletes['Year'].astype(int)  # 确保年份为整数
# athletes['Event'] = athletes['Event'].str.strip() 
# print(athletes.head())
# print(athletes.columns)


unique_names_count_year_noc_sport = athletes.groupby(['Year', 'Team', 'Sport'])['Name'].nunique().reset_index()
unique_names_count_year_noc_sport.columns = ['Year', 'Team', 'Sport', 'UniqueNameCount']
# print(unique_names_count_year_noc_sport.head(n=10))
# print("------------------------------------------------")

unique_names_count_year_sport = athletes.groupby(['Year', 'Sport'])['Name'].nunique().reset_index()
unique_names_count_year_sport.columns = ['Year', 'Sport', 'UniqueNameCount']
# print(unique_names_count_year_sport.head())
# print("------------------------------------------------")

# ## Plot the participation data
# # plt.figure(figsize=(14, 8))
# # for sport in unique_names_count_year_sport['Sport'].unique():
# #     sport_data = unique_names_count_year_sport[unique_names_count_year_sport['Sport'] == sport]
# #     plt.plot(sport_data['Year'], sport_data['UniqueNameCount'], label=sport)
# #
# # plt.xlabel('Year')
# # plt.ylabel('Unique Name Count')
# # plt.title('Unique Name Counts Each Year by Sport')
# # plt.legend(title='Sport', bbox_to_anchor=(1.05, 1), loc='upper left')
# # # plt.tight_layout()  # Adjust layout to fit everything
# # plt.show()


#Task: Find sports which are declining in participation
def find_declining_sports(year=2024):
    recent_games = 5
    most_recent_years = unique_names_count_year_sport['Year'].unique()[-recent_games:]
    recent_data = unique_names_count_year_sport[unique_names_count_year_sport['Year'].isin(most_recent_years)]


    declining_sports = []
    for sport in recent_data['Sport'].unique():
        sport_data = recent_data[recent_data['Sport'] == sport]
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            slope, _, _, _, _ = linregress(sport_data['Year'], sport_data['UniqueNameCount'])
        if slope < 0:
            declining_sports.append(sport)

    return declining_sports

# print(declining_sports)

#Task: Find countries which are emerging winners per year from the athletes file
# print(athletes.columns)
def first_participating_year_for_emerging_medal_winners(athletes, year=2024):
    df_year = athletes[athletes['Year'] <= year]
    df_before_year = athletes[athletes['Year'] < year]
    

    nocs_no_medals = df_before_year.groupby('Team').filter(lambda group: (group['Medal'] == "No medal").all())
    nocs_no_medals_at_year = df_year.groupby('Team').filter(lambda group: (group['Medal'] == "No medal").all())
    # print("checkpoint1")
    
    #list of teams:
    first_medals_at_year = np.setdiff1d( nocs_no_medals['Team'].unique(),nocs_no_medals_at_year['Team'].unique())
    # print(first_medals_at_year)
    # print("checkpoint2:generated list of emerging countries in current year.") 

    #athletes in emerging countries:
    df_this_year = athletes[athletes['Year'] == year]
    emerging_noc_athletes = df_this_year[df_this_year['Team'].isin(first_medals_at_year)]
    # print(emerging_noc_athletes)
    # print("checkpoint3:generated list of participants in emerging countries in current year")

    #winning athletes in emerging countries:
    emerging_medals_athletes = emerging_noc_athletes[emerging_noc_athletes['Medal'] != "No medal"]
    # print(emerging_medals_athletes)
    # print("checkpoint4:generated list of winning participants in emerging countries in current year")

    #medals in emerging countries:
    emerging_medals_count = emerging_noc_athletes[emerging_noc_athletes['Medal'] != "No medal"].shape[0]
    # print(f'Number of emerging medals is {emerging_medals_count}')

    # print(f'Final check point of {year}: generated number of emerging country medals and number of participants in emerging countries.')

    return first_medals_at_year, emerging_medals_count



# data=[]

# for yr in range(2024, 1972, -4):
#     print(f"\n\nYear: {yr}")
#     first_participating_year_for_emerging_medal_winners(athletes, yr)


# medals = pd.read_csv(base_dir / './Data/summerOly_medal_counts.csv')
# # print(medals.head())
# noc_year_total = medals.groupby(['NOC', 'Year'])['Total'].sum().reset_index()

# # Find the smallest year for each NOC where the total is greater than 0
# first_years = noc_year_total[noc_year_total['Total'] > 0].groupby('NOC')['Year'].min().reset_index()

# # Create a pivot table with NOCs as rows and years as columns
# years = sorted(noc_year_total['Year'].unique())
# nocs = sorted(noc_year_total['NOC'].unique())
# first_years_pivot = pd.DataFrame(False, index=nocs, columns=years)

# # Set the value to True for the identified years
# for _, row in first_years.iterrows():
#     first_years_pivot.at[row['NOC'], row['Year']] = True
# print(first_years_pivot.head())


#Task:  Filter athlete rows who's country is emerging winner and participating in declining sports
year_ratio={"Year":[],"Ratio":[]}
year_all_ratio={"Year":[],"Ratio":[]}
compare_ratio={"Year":[],"Decline Ratio":[],"All Ratio":[],"Difference":[],"Ratio of Ratio":[]}
for yr in range(2024, 1992, -4):
    # print(f"\n\nYear: {yr}")
    declining_sports_year = find_declining_sports(yr)
    first_medals_at_year,emerging_medal_count=first_participating_year_for_emerging_medal_winners(athletes, yr)

    declining_sports_athletes = athletes[athletes['Sport'].isin(declining_sports_year)]
    declining_sports_emerging_noc_athletes = declining_sports_athletes[declining_sports_athletes['Team'].isin(first_medals_at_year)]

    #Task: count athletes participating in declining sports per country per year
    declining_emerging_athletes_count = declining_sports_emerging_noc_athletes.shape[0]
    ratio= emerging_medal_count/declining_emerging_athletes_count #ratio of medal/participation in declining sports
    year_ratio["Year"].append(yr)
    year_ratio["Ratio"].append(ratio)

    # print(f"Year: {yr}, Emerging Medals: {emerging_medal_count}, Declining Sports Participants: {declining_emerging_athletes_count}, Declining sport win Ratio: {ratio}")

    #Task: Find percentage of emerging athletes participating in all sports
    all_sports_emerging_noc_athletes = athletes[athletes['Team'].isin(first_medals_at_year)]
    all_sports_emerging_noc_athletes_count = athletes[athletes['Team'].isin(first_medals_at_year)].shape[0]
    ratio2=emerging_medal_count/all_sports_emerging_noc_athletes_count
    year_all_ratio["Year"].append(yr)
    year_all_ratio["Ratio"].append(ratio2)
    # print(f"Year: {yr}, Emerging Medals: {emerging_medal_count}, Declining Sports Participants: {all_sports_emerging_noc_athletes_count}, All sport win Ratio: {ratio2}")

    #Find ratio all sports emerging medals/all sports participation

    compare_ratio["Year"].append(yr)
    compare_ratio["Decline Ratio"].append(ratio)
    compare_ratio["All Ratio"].append(ratio2)
    compare_ratio["Difference"].append(ratio-ratio2)
    compare_ratio["Ratio of Ratio"].append(ratio/ratio2)


compare_ratio_df=pd.DataFrame(compare_ratio)
print('-------------------------------')
print('Win Ratio of emerging medal to participants in all sports is:')
print(compare_ratio_df.head())
print('-------------------------------')


#定义decline sport相关的score
print(type(athletes))

def subset_on_year_sport(year,sport):
    subset_df = athletes[(athletes["Year"] == year) & (athletes["Sport"] == sport)]
    return subset_df

print(subset_on_year_sport(2024, "Athletics").head())

# Given a year, find the list of sports for which the participation is declining
def athletes_in_declining_sports(year):
    recent_years = 5
    most_recent_years = unique_names_count_year_sport[unique_names_count_year_sport['Year']<=year]['Year'].unique()[-recent_years:]
    recent_data = unique_names_count_year_sport[unique_names_count_year_sport['Year'].isin(most_recent_years)]

    declining_sports = []
    for sport in recent_data['Sport'].unique():
        sport_data = recent_data[recent_data['Sport'] == sport]
        slope, _, _, _, _ = linregress(sport_data['Year'], sport_data['UniqueNameCount'])
        if slope < 0:
            declining_sports.append(sport)
    return declining_sports

#subset athlete declining sport, list of sports
def find_declining_sports_data(year):
    res={"Sport":[],"0Participants":[],"-1Participants":[],"-2Participants":[]}
    recent_years = 5
    most_recent_years = unique_names_count_year_sport['Year'].unique()[-recent_years:]
    recent_data = unique_names_count_year_sport[unique_names_count_year_sport['Year'].isin(most_recent_years)]

    #list of declining sports
    declining_sports_year = find_declining_sports(year)
    print(declining_sports_year)

    for s in declining_sports_year:
        df0 = subset_on_year_sport(year, s)
        df1 = subset_on_year_sport(year - 4, s)
        df2 = subset_on_year_sport(year - 8, s)

        count0 = df0[df0["Sport"] == s].shape[0]
        count1 = df1[df1["Sport"] == s].shape[0]
        count2 = df2[df2["Sport"] == s].shape[0]

        res["Sport"].append(s)
        res['0Participants'].append(count0)
        res['-1Participants'].append(count1)
        res['-2Participants'].append(count2)
    return pd.DataFrame(res)

print("---------------------------------------")
print(find_declining_sports_data(2024))
print("---------------------------------------")

# Given country, find participation in declining sports
def participation_in_declining_sports_by_NOC(NOC, year):
    declining_sports_year = find_declining_sports(year)
    athletes_participating_in_declining_sports = athletes[(athletes['NOC'] == NOC) & (athletes['Year'] == year) & (athletes['Sport'].isin(declining_sports_year))]
    return athletes_participating_in_declining_sports['Name'].nunique()

# print(participation_in_declining_sports_by_NOC("USA", 2016))

# Score for year 2024 = (Number of athletes participating in declining sports for the given NOC) / (Total number of participants in declining sports)
NOCs_2024 = athletes[athletes['Year'] == 2024]['NOC'].unique()
declining_sports_data_2024 = find_declining_sports_data(2024)
total_participants_2024 = declining_sports_data_2024['0Participants'].sum()
NOC_involvement_declining_sport_scores = []
for NOC in NOCs_2024:
    NOC_involvement_declining_sport_scores.append({"NOC": NOC, "Score": participation_in_declining_sports_by_NOC(NOC, 2024) / total_participants_2024})
    
print(pd.DataFrame(NOC_involvement_declining_sport_scores).head(n=10))
