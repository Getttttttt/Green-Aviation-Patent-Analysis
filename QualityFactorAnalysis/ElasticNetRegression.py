import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import ElasticNetCV
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import seaborn as sns

# 加载数据集
data_path = './Dataset/Dataset.xlsx'
data = pd.read_excel(data_path)

# 选取数值型变量作为特征，除了目标变量外
X = data.select_dtypes(include=[np.number]).drop(columns=["INPADOC同族专利申请数量","INPADOC同族被引用专利总数"])
y = data["INPADOC同族专利申请数量"]

# 分割数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 标准化特征
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ElasticNetCV模型，使用交叉验证确定正则化参数
elastic_net_cv = ElasticNetCV(cv=5, random_state=42)
elastic_net_cv.fit(X_train_scaled, y_train)

# 预测测试集
y_pred = elastic_net_cv.predict(X_test_scaled)

# 计算模型的评价指标
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"mse:{mse}\n r2:{r2}\n elastic_net_cv.alpha_:{elastic_net_cv.alpha_}\n elastic_net_cv.l1_ratio_:{elastic_net_cv.l1_ratio_}")

feature_coef = pd.DataFrame({
    'Feature': X.columns,
    'Coefficients (B)': elastic_net_cv.coef_
})
    
feature_coef.to_csv('./MarketValueFactorAnalysis/Coefficients/FeaturesCoefficients.csv', header=True)

max_length = feature_coef['Feature'].str.len().max()

# 将所有Feature名称统一为相同的长度
feature_coef['Feature'] = feature_coef['Feature'].apply(lambda x: x.ljust(max_length))


feature_coef['Representative Name'] = feature_coef.apply(lambda x: ' ' if x['Coefficients (B)'] == 0 else x['Feature'], axis=1)

# 计算绝对值的系数并排序，选取Top 10特征
top_features_abs_sorted = feature_coef['Coefficients (B)'].abs().sort_values(ascending=False).head(10)
top_features = feature_coef.loc[top_features_abs_sorted.index]  # 选取Top 10特征

# 对选定的特征按原始系数值排序，以确保图表反映实际的正负值和大小
top_features_sorted = top_features.sort_values(by='Coefficients (B)')

# 配置绘图样式和字体
plt.rcParams["font.family"] = "SimHei"
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams["font.size"] = 14

# 创建图表
fig, ax = plt.subplots(figsize=(10, 8))

# 创建图表
fig, ax = plt.subplots(figsize=(10, 8))
norm = plt.Normalize(-0.4, .4)
cmap = plt.cm.coolwarm

# 计算颜色
colors = cmap(norm(top_features_sorted['Coefficients (B)'].values))

# 手动绘制每个条形
for i, (coef, name) in enumerate(zip(top_features_sorted['Coefficients (B)'], top_features_sorted['Representative Name'])):
    ax.barh(y=i, width=coef, color=colors[i])

# 设置y轴的刻度标签
ax.set_yticks(range(len(top_features_sorted)))
ax.set_yticklabels(top_features_sorted['Representative Name'])

# 设置其他绘图属性
plt.xlabel('Coefficients', fontsize=14)
plt.ylabel('Features', fontsize=14)
plt.title(f'Top Features Selected by Lasso for {y.name}', fontsize=16)
plt.tight_layout()

# 添加颜色条
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax)
cbar.set_label('Coefficient Value')

plt.show()

# 选择前N个最重要的特征（例如，N=10）
top_n = 10
top_features = np.abs(elastic_net_cv.coef_).argsort()[-top_n:]
selected_features = X.columns[top_features]

# 创建包含选定特征和目标变量的DataFrame
selected_data = pd.concat([X.iloc[:, top_features], y], axis=1)

# 计算选定特征的相关性矩阵
corr_matrix_selected = selected_data.corr()

# 绘制相关性矩阵的热图
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix_selected, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix of Top Features and Target')
plt.xticks(rotation=90)
plt.yticks(rotation=0)
plt.show()


#绘制预测真实值
y_pred_adjusted = np.maximum(y_pred, 0)  # 将预测值小于0的调整为0

plt.figure(figsize=(8, 6))
sns.scatterplot(x=y_test, y=y_pred_adjusted, alpha=0.6, edgecolor=None, color='blue')
plt.xlabel('Actual Values', fontsize=14)
plt.ylabel('Predicted Values', fontsize=14)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
plt.fill_between([y_test.min(), y_test.max()], [y_test.min(), y_test.max()],
                 [y_test.min() * 0.9, y_test.max() * 1.1], color='gray', alpha=0.2)
plt.title('Actual vs. Predicted Values', fontsize=16)
plt.show()