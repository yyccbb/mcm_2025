import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
base_dir = Path(__file__).parents[2]
athletes = pd.read_csv(base_dir / './data/summerOly_athletes.csv')
print(athletes.head())
print(athletes.columns)

unique_names_count_year_noc_sport = athletes.groupby(['Year', 'Team', 'Sport'])['Name'].nunique().reset_index()

# Rename the columns for clarity
unique_names_count_year_noc_sport.columns = ['Year', 'Team', 'Sport', 'UniqueNameCount']

print(unique_names_count_year_noc_sport.head())



# Assuming 'athletes' DataFrame is already loaded
unique_names_count_year_sport = athletes.groupby(['Year', 'Sport'])['Name'].nunique().reset_index()

# Rename the columns for clarity
unique_names_count_year_sport.columns = ['Year', 'Sport', 'UniqueNameCount']

# print(unique_names_count_year_sport.head())

## Plot the data
# plt.figure(figsize=(14, 8))
# for sport in unique_names_count_year_sport['Sport'].unique():
#     sport_data = unique_names_count_year_sport[unique_names_count_year_sport['Sport'] == sport]
#     plt.plot(sport_data['Year'], sport_data['UniqueNameCount'], label=sport)
#
# plt.xlabel('Year')
# plt.ylabel('Unique Name Count')
# plt.title('Unique Name Counts Each Year by Sport')
# plt.legend(title='Sport', bbox_to_anchor=(1.05, 1), loc='upper left')
# # plt.tight_layout()  # Adjust layout to fit everything
# plt.show()


#find sports which are declining in participation
# Define the number of recent years to consider for the trend analysis
recent_years = 5

# Get the most recent years
most_recent_years = unique_names_count_year_sport['Year'].unique()[-recent_years:]

# Filter the data for the most recent years
recent_data = unique_names_count_year_sport[unique_names_count_year_sport['Year'].isin(most_recent_years)]

# Calculate the trend for each sport
from scipy.stats import linregress
declining_sports = []
for sport in recent_data['Sport'].unique():
    sport_data = recent_data[recent_data['Sport'] == sport]
    slope, _, _, _, _ = linregress(sport_data['Year'], sport_data['UniqueNameCount'])
    if slope < 0:
        declining_sports.append(sport)

print(declining_sports)
#countries which are emerging winners per year

medals = pd.read_csv(base_dir / './Data/summerOly_medal_counts.csv')
# print(medals.head())

#create new dataframe year_first_medal against NOC
noc_year_total = medals.groupby(['NOC', 'Year'])['Total'].sum().reset_index()

# Find the smallest year for each NOC where the total is greater than 0
first_years = noc_year_total[noc_year_total['Total'] > 0].groupby('NOC')['Year'].min().reset_index()

# Create a pivot table with NOCs as rows and years as columns
years = sorted(noc_year_total['Year'].unique())
nocs = sorted(noc_year_total['NOC'].unique())
first_years_pivot = pd.DataFrame(False, index=nocs, columns=years)

# Set the value to True for the identified years
for _, row in first_years.iterrows():
    first_years_pivot.at[row['NOC'], row['Year']] = True

print(first_years_pivot.head())
#athletes who's country is emerging winner



#count athletes participating in declining sports per country per year
# Filter athletes DataFrame for declining sports
declining_sports_athletes = athletes[athletes['Sport'].isin(declining_sports)]

# # Create a list to store the filtered rows
filtered_rows = []

# Iterate over the rows of declining_sports_athletes
for _, row in declining_sports_athletes.iterrows():
    team = row['Team']
    year = row['Year']
    if first_years_pivot.at[team, year]:
        filtered_rows.append(row)

# # Create a new DataFrame from the filtered rows
# filtered_df = pd.DataFrame(filtered_rows, columns=['Team', 'Sport', 'Year', 'Name'])
#
# print(filtered_df.head())
#
# #sport kind which emerging winners are participating in

