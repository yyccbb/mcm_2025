import pandas as pd
from tqdm import tqdm
import time
import src.util.dataloader as dl
import matplotlib.pyplot as plt

athletes = dl.athletes_dataset()
medals = dl.medals_dataset()

athletes = athletes[athletes['Year'] >= 1972]

# athletes_series = athletes.groupby(['NOC'])['Name'].nunique()
# print(athletes_series.shape)
# medals_series = athletes[athletes['Medal'] != 'No medal'].groupby('NOC')['Name'].count()
# print(medals_series.shape)
#
# res_series = pd.concat([athletes_series, medals_series], axis=1).fillna(0, inplace=True)
# # res_series.columns = ['Athletes', 'Medals']
# # res_series.to_csv('medal_efficiency.csv')
# print(res_series)

unique_NOCs = athletes['NOC'].unique()
result = []
for NOC in unique_NOCs:
    participants_count = athletes[athletes['NOC'] == NOC]['Name'].nunique()
    medals_count = athletes[(athletes['NOC'] == NOC) & (athletes['Medal'] != 'No medal')]['Name'].count()
    result.append({'NOC': NOC, 'Participants': participants_count, 'Medals': medals_count})

result = pd.DataFrame(result)
result.to_csv(dl.get_base() / './data/medal_efficiency.csv')
print(result)

# User matplotlib to plot result['Medals'] against result['Participants']
plt.scatter(result['Participants'], result['Medals'])
plt.xlabel('Number of Participants')
plt.ylabel('Number of Medals')
plt.title('Number of Medals vs Number of Participants')
plt.show()
