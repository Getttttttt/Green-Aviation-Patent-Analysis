import plotly.express as px
import pandas as pd

# 假设country_distribution_data已加载
country_distribution_data = pd.read_excel('./IPCVisualization/Country_Distribution_Data.xlsx')

# 选择申请数量最多的前5个国家和IPC分类
top_countries = country_distribution_data.groupby('受理局')['申请数量'].sum().nlargest(5).index
top_ipc = country_distribution_data.groupby('处理后的IPC主分类号')['申请数量'].sum().nlargest(10).index

# 过滤数据
filtered_country_data = country_distribution_data[
    (country_distribution_data['受理局'].isin(top_countries)) &
    (country_distribution_data['处理后的IPC主分类号'].isin(top_ipc))
]

fig = px.scatter(
    filtered_country_data,
    x='申请年',
    y='处理后的IPC主分类号',
    size='申请数量',
    color='受理局',
    hover_name='受理局',
    title='Top 5 Countries and IPC Categories Over Time'
)

fig.update_layout(
    xaxis_title='Year',
    yaxis_title='IPC Category',
    legend_title='Country'
)

fig.show()
