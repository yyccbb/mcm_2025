import pandas as pd
import numpy as np
#import tensorflow as tf
import matplotlib.pyplot as plt
#from matplotlib import pyplot as plt

import os

# Print the absolute path to verify
# print(os.getcwd())
# Load ../Data/summerOly_medal_counts.csv as a pandas DataFrame
medals = pd.read_csv('./Data/summerOly_medal_counts.csv')
athletes = pd.read_csv('./Data/summerOly_athletes.csv')

def first_participating_year_for_emerging_medal_winners(athletes, year=2024):
    df_year = athletes[athletes['Year'] <= year]
    df_before_year = athletes[athletes['Year'] < year]
    nocs_no_medals = df_before_year.groupby('NOC').filter(lambda group: (group['Medal'] == "No medal").all())
    nocs_no_medals_at_year = df_year.groupby('NOC').filter(lambda group: (group['Medal'] == "No medal").all())

    nocs_no_medals_at_year['Team'].unique()
    first_medals_at_year = np.setdiff1d(nocs_no_medals['Team'].unique(), nocs_no_medals_at_year['Team'].unique())

    no_medals_emerging = np.setdiff1d(nocs_no_medals_at_year['Team'].unique(), nocs_no_medals['Team'].unique())

    filtered_ds = df_year[df_year['Team'].isin(no_medals_emerging)]
    emerging_year = np.setdiff1d(df_year['Team'].unique(), df_before_year['Team'].unique())

    # Past participation records for countries that got their first medals in {year}
    NOCs_first_medal_year = df_year[df_year['Team'].isin(first_medals_at_year)]
    
    for noc in first_medals_at_year:
        participating_years = df_year[df_year['Team'] == noc]['Year'].unique()
        interval=year-participating_years.min()
        print(f"{noc} first participated in {participating_years.min()} and got their first medal in {year}")
        data.append({'Country': noc, 'Interval': interval, 'Year': year})
data=[]

for yr in range(2024, 1972, -4):
    print(f"\n\nYear: {yr}")
    first_participating_year_for_emerging_medal_winners(athletes, yr)

  

#create new dataframe with interval data
interval_df = pd.DataFrame(data) 
interval_df =  interval_df.sort_values(by='Interval', ascending=True)
print(f'The mean interval is {interval_df["Interval"].mean()}')

print(interval_df.head())

#number of emerging medal winners per year
emerging_medal_winners_per_year = interval_df['Year'].value_counts().sort_index()
plt.figure(figsize=(12, 8))
emerging_medal_winners_per_year.plot(kind='line', marker='o',color='skyblue')
plt.xlabel('Year')
plt.ylabel('Number of Emerging Medal Winners')
plt.title('Number of Emerging Medal Winners Each Year')
plt.xticks(ticks=emerging_medal_winners_per_year.index,rotation=90)  # Rotate year labels for better readability
plt.tight_layout()  # Adjust layout to fit everything
plt.show()

#bar plot of participating years for emerging medal winners
plt.figure(figsize=(12, 8))
plt.bar(interval_df['Country'], interval_df['Interval'], color='skyblue')
plt.xlabel('Country')
plt.ylabel('Interval (Years)')
plt.title('Interval Between First Participation and First Medal Year for Each Country')
plt.xticks(rotation=90)  # Rotate country names for better readability
plt.tight_layout()  # Adjust layout to fit everything
plt.show()

#boxplots of interval of countries geting their first medal that year
plt.figure(figsize=(12, 8))
interval_df.boxplot(column='Interval', by='Year', grid=False)
plt.xlabel('Year')
plt.ylabel('Interval (Years)')
plt.title('Number of participating years for emerging medal winners by year')
plt.suptitle('')  # Suppress the default title to avoid overlap
plt.xticks(rotation=90)  # Rotate year labels for better readability
plt.tight_layout()  # Adjust layout to fit everything
plt.show()





