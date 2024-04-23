import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import seaborn as sns
import pandas as pd
import numpy as np

def predata():
    # 加载数据集
    file_path = '../Dataset/Dataset.xlsx'
    df = pd.read_excel(file_path)
    #print(df.head())
    # 提取年份信息
    df['申请年份'] = df['申请日'].astype(str).str[:4]
    # 根据受理局和申请年份对数据进行分组，计算每个组的专利数量
    patent_counts = df.groupby(['受理局', '申请年份']).size().reset_index(name='专利数量')
    # 保存结果
    output_file_path = './Patent_Counts_by_Year_and_Authority.xlsx'
    patent_counts.to_excel(output_file_path, index=False)


def visual():
    csv_file_path = './Patent_Counts_by_Year_and_Authority.xlsx'
    patent_counts_csv = pd.read_excel(csv_file_path)
    # 将数据转换为每个年份一个记录，每个受理局一个列的形式
    patent_counts_pivot = patent_counts_csv.pivot(index='申请年份', columns='受理局', values='专利数量').fillna(0)
    # top25
    top_authorities = patent_counts_csv.groupby('受理局')['专利数量'].sum().nlargest(25).index
    # 字体
    font_path = './simsun.ttc'
    font_prop_label = FontProperties(fname=font_path, size=13)
    font_prop = FontProperties(fname=font_path, size=18)
    font_prop_title = FontProperties(fname=font_path, size=20)
    # 设置图表大小和风格
    plt.figure()
    sns.set(style="whitegrid")
    # 生成一个唯一颜色的列表
    all_colors = plt.cm.tab20c(np.linspace(0, 1, len(patent_counts_pivot.columns)))
    # 绘制堆叠图，使用自定义的颜色列表
    ax = patent_counts_pivot.plot(kind='bar', stacked=True, figsize=(14, 8), color=all_colors)

    # 设置标题和标签
    #plt.title('全球专利申请数量变化趋势', fontproperties=font_prop_title)
    plt.xlabel('申请年份', fontproperties=font_prop)
    plt.ylabel('专利申请数量', fontproperties=font_prop)
    plt.xticks(rotation=45)
    # 前30图例
    handles, labels = ax.get_legend_handles_labels()
    top_handles = [handles[labels.index(auth)] for auth in top_authorities if auth in labels]
    top_labels = [auth for auth in top_authorities if auth in labels]
    legend = ax.legend(top_handles, top_labels, title='前25国家', bbox_to_anchor=(1.05, 1), loc='upper left', prop=font_prop_label)
    plt.setp(legend.get_title(), fontproperties=font_prop_label,  ha='left')
    # 显示图例
    #plt.legend(title='Authority', bbox_to_anchor=(1.05, 1), loc='upper left', prop=font_prop)
    # 显示图表
    plt.tight_layout()
    plt.savefig('./Annual Patent Counts by Authority.png')
    plt.show()



if __name__=='__main__':
    #predata()
    visual()