import pandas as pd

file_path = './Dataset/IPCDatasetWithRegionAndTime.csv'

# Try loading the dataset again with a different encoding, guessing it might be "gbk" since the data includes Chinese characters
data = pd.read_csv(file_path, encoding='gbk')

# Display the first few rows of the dataframe and check data types again to understand its structure and content
data.head(), data.dtypes


# Convert ApplicationDate to datetime format
data['Year'] = (data['ApplicationDate'] // 1000000).astype(int)  # Extract the year from the ApplicationDate

# Define the year ranges
year_ranges = {
    "2013-2015": (2013, 2015),
    "2013-2020": (2013, 2020),
    "2013-2024": (2013, 2024)
}

print(data.head())

# Create a dictionary to store the filtered dataframes based on year ranges
filtered_by_years = {}

for label, (start_year, end_year) in year_ranges.items():
    filtered_by_years[label] = data[(data['Year'] >= start_year) & (data['Year'] <= end_year)][['IPC']]

# Save the filtered dataframes to CSV files
for label, df in filtered_by_years.items():
    file_name = f"./IPCNetworkDividedByTimeAndRegion/IPCDividedDataset/{label}_Total.csv"
    df.to_csv(file_name, index=False)

# Show the file paths for the created files
file_paths_years = {label: f"./IPCNetworkDividedByTimeAndRegion/IPCDividedDataset/{label}_Total.csv" for label in filtered_by_years}
file_paths_years

# Define the regions of interest
regions_of_interest = {
    "中国": "中国",
    "美国": "美国",
    "欧洲专利局": "欧洲专利局",
    "俄罗斯": "俄罗斯"
}

# Create a dictionary to store the filtered dataframes based on regions
filtered_by_regions = {}

for label, region in regions_of_interest.items():
    filtered_by_regions[label] = data[data['Region'] == region][['IPC']]

# Save the filtered dataframes to CSV files
for label, df in filtered_by_regions.items():
    file_name = f"./IPCNetworkDividedByTimeAndRegion/IPCDividedDataset/Total_{label}.csv"
    df.to_csv(file_name, index=False)

# Show the file paths for the created files
file_paths_regions = {label: f"./IPCNetworkDividedByTimeAndRegion/IPCDividedDataset/Total_{label}.csv" for label in filtered_by_regions}
file_paths_regions

# Create a dictionary to store the filtered dataframes based on combined year and region criteria
combined_filters = {}

for year_label, year_df in filtered_by_years.items():
    for region_label, region in regions_of_interest.items():
        combined_key = f"{year_label}_{region_label}"
        combined_df = year_df[data['Region'] == region][['IPC']]
        combined_filters[combined_key] = combined_df

# Save the filtered dataframes to CSV files
for label, df in combined_filters.items():
    file_name = f"./IPCNetworkDividedByTimeAndRegion/IPCDividedDataset/{label}.csv"
    df.to_csv(file_name, index=False)

# Show the file paths for the created files
file_paths_combined = {label: f"./IPCNetworkDividedByTimeAndRegion/IPCDividedDataset/{label}.csv" for label in combined_filters}
file_paths_combined
