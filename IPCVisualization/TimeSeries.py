import plotly.graph_objects as go
import pandas as pd

# 假设time_series_data_yearly已加载
time_series_data_yearly = pd.read_excel('./IPCVisualization/Time_Series_Data_Yearly.xlsx')

# 确保'申请年'是DataFrame的索引
time_series_data_yearly.set_index('申请年', inplace=True)

# 筛选出申请数量最多的前10个IPC分类号
top_ipc_categories = time_series_data_yearly.iloc[-1].sort_values(ascending=False).head(10).index

filtered_time_series_data = time_series_data_yearly[top_ipc_categories]

fig = go.Figure()
for category in filtered_time_series_data.columns:
    fig.add_trace(go.Scatter(
        x=filtered_time_series_data.index, 
        y=filtered_time_series_data[category],
        mode='lines',
        stackgroup='one',  # define stack group
        name=category
    ))

fig.update_layout(
    title='Top 10 IPC Categories Over Time',
    xaxis_title='Year',
    yaxis_title='Cumulative Patent Applications',
    hovermode="x"
)

fig.show()