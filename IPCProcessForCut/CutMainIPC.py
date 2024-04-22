import pandas as pd

# Load the dataset
file_path = './Dataset/Dataset.xlsx'
data = pd.read_excel(file_path)

# Display the first few rows of the dataframe to understand its structure
data.head(), data.columns

# Define a function to extract the part before "/" or retain "0" as is
def process_ipc_code(code):
    if code == 0:
        return 0
    else:
        return code.split('/')[0]

# Apply the function to the "IPC主分类号" column and create a new column
data['处理后的IPC主分类号'] = data['IPC主分类号'].apply(process_ipc_code)

# Display the first few rows of the dataframe to verify the changes
data[['IPC主分类号', '处理后的IPC主分类号']].head()

new_file_path = './Dataset/Modified_Dataset0422.xlsx'
data.to_excel(new_file_path, index=False)