import pandas as pd
import matplotlib.pyplot as plt
from pyecharts.charts import Bar
from pyecharts import options as opts


# 创建DataFrame
df = pd.read_excel("./data/美国 专利数量.xlsx")
print(df)
 
# 计算增量
df['Increase'] = df['专利数量'] - df['专利数量'].shift(1)

df_plot = pd.DataFrame()
df_plot['Year'] = df['申请年份']
lis = list(df['Increase'])
lis[0] = list(df['专利数量'])[0]
df_plot['value'] = lis
print(df_plot)

# 绘制瀑布图
df_plot.plot(kind='bar', stacked=True, x='Year', y='value')
year = list(df_plot['Year'])
number = list(df['专利数量'])
y_in = []
y_out = []
for i in lis:
    if(i>0):
        y_in.append(i)
        y_out.append("-")
    else:
        y_in.append("-")
        y_out.append(i)

bar = (
    Bar()
    .add_xaxis(xaxis_data = year)
    .add_yaxis(
        series_name="",
        y_axis=number,
        stack="Patent Number",
        itemstyle_opts=opts.ItemStyleOpts(color="rgba(0,0,0,0)"),
    )
    .add_yaxis(series_name="increase", y_axis=y_in, stack="Patent Number")
    .add_yaxis(series_name="decrease", y_axis=y_out, stack="Patent Number")
    .set_global_opts(yaxis_opts=opts.AxisOpts(type_="value"))
    .render("bar_waterfall_plot.html")
)
