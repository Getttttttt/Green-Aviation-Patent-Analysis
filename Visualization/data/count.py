import pandas as pd



# 加载数据集
df = pd.read_excel('./中国 同族.xlsx')

# 计算每年的专利数量总和
yearly_totals = df.groupby('Year')['INPADOC同族专利申请数量'].sum().reset_index()

# 保存结果到新的Excel文件中
output_file_path = './Yearly_INPADOC_Totals_china.xlsx'
yearly_totals.to_excel(output_file_path, index=False)

# 返回新文件的路径
output_file_path
