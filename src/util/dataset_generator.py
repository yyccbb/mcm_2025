import pandas as pd
from tqdm import tqdm
import time
import dataloader as dl

medal_counts = dl.medals_dataset()
hosts = dl.hosts_dataset()
athletes = dl.athletes_dataset()

# medal_counts = pd.read_csv('summerOly_medal_counts.csv', encoding='ISO-8859-1')
# hosts = pd.read_csv('summerOly_hosts.csv', encoding='ISO-8859-1')
# athletes = pd.read_csv('summerOly_athletes.csv', encoding='ISO-8859-1')

latest_years = [2016, 2020, 2024]
filtered_medals = medal_counts[medal_counts['Year'].isin(latest_years)]

# 清理 athletes 表中的 Team、Year 和 Event 字段
athletes['Team'] = athletes['Team'].str.strip()  # 去除 Team 字段中的空格
athletes['Year'] = athletes['Year'].astype(int)  # 确保年份为整数
athletes['Event'] = athletes['Event'].str.strip()  # 去除 Event 字段中的空格

# 聚合 athletes 表，统计参赛人数
athlete_counts = (
    athletes[athletes['Year'].isin(latest_years)]  # 筛选出最近3届奥运会的数据
    .groupby(['Team', 'Year'])  # 按国家（Team）和年份分组
    .size()  # 统计每组的行数（即参赛人数）
    .reset_index(name='Participants')  # 重置索引，并将结果列命名为Participants
)

# 聚合 athletes 表，统计独立赛事数
event_counts = (
    athletes[athletes['Year'].isin(latest_years)]
    .groupby(['Team', 'Year'])['Event']
    .nunique()
    .reset_index(name='Event_Count')
)

# Debug: 打印预聚合结果
print("Aggregated athlete counts:")
print(athlete_counts.head(10))
print("Aggregated event counts:")
print(event_counts.head(10))

countries = filtered_medals['NOC'].unique()  # 获取所有参赛国家代码
data = []

total_iterations = len(countries) * len(latest_years)  # 总的循环次数，用于进度条
start_time = time.time()

with tqdm(total=total_iterations, desc="Processing", unit="iteration") as pbar:
    for country in countries:  # 遍历每个国家
        for year in latest_years:  # 遍历每个年份
            # Debug: 打印当前处理的国家和年份
            print(f"Processing Country: {country}, Year: {year}")

            # 查找当前国家和年份的金牌数和总奖牌数
            medal_row = filtered_medals[(filtered_medals['NOC'] == country) & (filtered_medals['Year'] == year)]
            gold = medal_row['Gold'].values[0] if not medal_row.empty else 0
            total_medals = medal_row['Total'].values[0] if not medal_row.empty else 0

            # 检查当前国家是否为该年份的主办国
            host_row = hosts[hosts['Year'] == year]  # 查找该年份的主办信息
            is_host = 1 if not host_row.empty and country in host_row['Host'].values[0] else 0

            # 从预聚合的athlete_counts表中获取参赛人数
            participant_row = athlete_counts[
                (athlete_counts['Team'] == country) & (athlete_counts['Year'] == year)
                ]
            participants = participant_row['Participants'].values[0] if not participant_row.empty else 0

            # 从预聚合的event_counts表中获取赛事数
            event_row = event_counts[
                (event_counts['Team'] == country) & (event_counts['Year'] == year)
                ]
            event_count = event_row['Event_Count'].values[0] if not event_row.empty else 0

            # 计算 Medal Efficiency 和 Gold Medal Focus
            medal_efficiency = total_medals / participants if participants > 0 else 0
            gold_medal_focus = gold / total_medals if total_medals > 0 else 0

            # 将当前国家、年份及相关信息追加到数据列表
            data.append({
                'Country': country,
                'Year': year,
                '#Gold': gold,
                '#Total Medals': total_medals,
                'Host': is_host,
                '#Participants': participants,
                '#Events': event_count,
                'Medal Efficiency': medal_efficiency,
                'Gold Medal Focus': gold_medal_focus
            })

            # 更新进度条
            pbar.update(1)

# 将数据列表转换为DataFrame
output_df = pd.DataFrame(data)

# 保存结果到CSV文件
output_df.to_csv(dl.get_base() / './data/olympic_data.csv', index=False)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"New CSV file 'olympic_data.csv' generated successfully in {elapsed_time:.2f} seconds!")