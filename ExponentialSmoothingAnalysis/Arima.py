from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np

# Load the dataset to understand its structure and contents
file_path = './Dataset/Top10Datas.csv'

models = {}
forecasts = {}
mape_losses = {}

# reading the CSV file
data = pd.read_csv(file_path, encoding='GB18030')

# Display the first few rows of the dataset and the data types of each column again
print(data.head(), data.dtypes)

# Sum the applications for each IPC code to find the top 10 IPCs with the highest total applications
ipc_totals = data.drop('申请年', axis=1).sum().sort_values(ascending=False).head(10)
print(ipc_totals)

# Check the range of years to determine how to split the dataset
years = data['申请年']
print(years)

# Calculate the number of years and determine the split for training and testing
total_years = len(years)
train_size = int(total_years * 0.8)
test_size = total_years - train_size

# Print the calculated sizes for training and testing datasets
print(train_size, test_size)

# Function to calculate RMSE
def rmse(actual, forecast):
    return np.sqrt(mean_squared_error(actual, forecast))

# Select a representative IPC code
ipc_example = 'B64D27'
train_data = data[ipc_example][:train_size]
test_data = data[ipc_example][train_size:total_years]

# Fit an ARIMA model
arima_model = ARIMA(train_data, order=(1, 1, 1))  # using a simple ARIMA(1,1,1) model
fitted_arima = arima_model.fit()

# ARIMA forecast
arima_forecast = fitted_arima.forecast(steps=test_size)

# Calculate RMSE for the ARIMA forecast
arima_rmse = rmse(test_data, arima_forecast)

# Retrieve RMSE for Exponential Smoothing model for comparison
exp_smooth_rmse = rmse(test_data, forecasts[ipc_example])

arima_rmse, exp_smooth_rmse
