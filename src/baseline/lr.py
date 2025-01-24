import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 1. 加载数据
file_path = 'olympic_data.csv'
data = pd.read_csv(file_path)

# 2. 数据预处理
# 筛选训练集和测试集
train_data = data[data['Year'] < 2024]  # 2016 和 2020 数据作为训练集
test_data = data[data['Year'] == 2024]  # 2024 数据作为测试集

# 删除包含缺失值的行
train_data = train_data.dropna()
test_data = test_data.dropna()

# 分离特征和目标变量
X_train = train_data.drop(columns=['#Gold', '#Total Medals', 'Year'])
y_gold_train = train_data['#Gold']
y_total_train = train_data['#Total Medals']

X_test = test_data.drop(columns=['#Gold', '#Total Medals', 'Year'])
y_gold_test = test_data['#Gold']
y_total_test = test_data['#Total Medals']

# 3. 独热编码国家特征
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')

# 对训练集和测试集分别进行独热编码
X_train_encoded = pd.DataFrame(encoder.fit_transform(X_train[['Country']])) # 对训练集中的 'Country' 列进行独热编码，并将结果转换为 DataFrame
X_train_encoded.columns = encoder.get_feature_names_out(['Country']) # 设置独热编码后的列名（基于国家名称），便于后续操作
X_train = pd.concat([X_train_encoded, X_train.drop(columns=['Country'])], axis=1) # 将独热编码后的列与训练集的其他特征合并，同时移除原始的 'Country' 列

X_test_encoded = pd.DataFrame(encoder.transform(X_test[['Country']])) # 对测试集中的 'Country' 列进行独热编码，使用与训练集一致的编码规则（transform 而非 fit_transform）
X_test_encoded.columns = encoder.get_feature_names_out(['Country']) # 设置独热编码后的列名（基于国家名称），与训练集保持一致
X_test = pd.concat([X_test_encoded, X_test.drop(columns=['Country'])], axis=1) # 将独热编码后的列与测试集的其他特征合并，同时移除原始的 'Country' 列

# 再次检查并删除所有残留的 NaN 值
X_train = X_train.dropna()
X_test = X_test.dropna()

# 确保目标变量与特征对齐
y_gold_train = y_gold_train[X_train.index]
y_total_train = y_total_train[X_train.index]
y_gold_test = y_gold_test[X_test.index]
y_total_test = y_total_test[X_test.index]

# 4. 训练模型
# 模型1：预测金牌数
model_gold = LinearRegression()
model_gold.fit(X_train, y_gold_train)

# 模型2：预测总奖牌数
model_total = LinearRegression()
model_total.fit(X_train, y_total_train)

# 5. 模型预测
gold_pred = model_gold.predict(X_test)
total_pred = model_total.predict(X_test)

# 6. 模型评估
print("Gold Prediction (2024 Test Data):")
print("Mean Squared Error (MSE):", mean_squared_error(y_gold_test, gold_pred))
print("R-squared (R2):", r2_score(y_gold_test, gold_pred))

print("\nTotal Medals Prediction (2024 Test Data):")
print("Mean Squared Error (MSE):", mean_squared_error(y_total_test, total_pred))
print("R-squared (R2):", r2_score(y_total_test, total_pred))

"""
# 7. 测试 2028 年某国家数据
new_country_data = pd.DataFrame({
    'Country': ['United States'],  # 替换为你要预测的国家
    'Host': [0],  # 是否是东道主
    '#Participants': [850],  # 预计参赛人数
    '#Events': [250],  # 预计参赛项目
    'Medal Efficiency': [0.14],  # 奖牌效率
    'Gold Medal Focus': [0.36]  # 金牌集中度
})

# 对新数据进行独热编码
new_country_encoded = pd.DataFrame(encoder.transform(new_country_data[['Country']]))
new_country_encoded.columns = encoder.get_feature_names_out(['Country'])
new_country_data = pd.concat([new_country_encoded, new_country_data.drop(columns=['Country'])], axis=1)

# 预测2028年的金牌数和总奖牌数
gold_2028_pred = model_gold.predict(new_country_data)
total_2028_pred = model_total.predict(new_country_data)

print("\nPredicted Gold Medals (2028):", gold_2028_pred[0])
print("Predicted Total Medals (2028):", total_2028_pred[0])
"""
