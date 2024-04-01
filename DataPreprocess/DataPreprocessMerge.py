import pandas as pd

# Excel文件路径
file_paths = [
    './Dataset/20240401084753860.XLSX',
    './Dataset/20240401085613950.XLSX',
    './Dataset/20240401123514129.XLSX',
    './Dataset/20240401123832541.XLSX'
]

# 读取所有文件
dataframes = [pd.read_excel(file_path) for file_path in file_paths]

# 按列名匹配合并所有DataFrame
combined_df = pd.concat(dataframes, ignore_index=True)

# 保存到新的Excel文件
combined_df.to_excel('./Dataset/combined_excel.xlsx', index=False)

print("合并完成，文件已保存至 ./Dataset/combined_excel.xlsx")
