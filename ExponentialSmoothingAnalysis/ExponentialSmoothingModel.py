import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import numpy as np

# Load the dataset to understand its structure and contents
file_path = './Dataset/Top10Datas.csv'

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


# Function to calculate MAPE (Mean Absolute Percentage Error)
def mape(actual, forecast):
    return np.mean(np.abs((actual - forecast) / actual)) * 100

# Initialize a dictionary to store the models and forecasts
models = {}
forecasts = {}
mape_losses = {}

# Train models and evaluate them using the test data
for ipc in ipc_totals.index:
    # Prepare the training and test datasets for the selected IPC
    train_data = data[ipc][:train_size]
    test_data = data[ipc][train_size:total_years]
    
    # Build and fit the model using the training dataset
    model = ExponentialSmoothing(train_data, trend='add', seasonal=None)
    fitted_model = model.fit(optimized=True)
    
    # Forecast using the model
    forecast = fitted_model.forecast(steps=test_size)
    
    # Calculate MAPE loss
    loss = mape(test_data, forecast)
    
    # Store the results
    models[ipc] = fitted_model
    forecasts[ipc] = forecast
    mape_losses[ipc] = loss

print(mape_losses)


# Initialize a dictionary to store the final models and future forecasts
final_models = {}
future_forecasts = {}

# Forecast the next 3 years for each IPC
for ipc in ipc_totals.index:
    # Use the entire dataset for training
    full_data = data[ipc]
    
    # Build and fit the model using the entire dataset
    model = ExponentialSmoothing(full_data, trend='add', seasonal=None)
    fitted_model = model.fit(optimized=True)
    
    # Forecast for the next 3 years
    forecast = fitted_model.forecast(steps=3)
    
    # Store the results
    final_models[ipc] = fitted_model
    future_forecasts[ipc] = forecast

print(future_forecasts)

# Retrieve and print model parameters for each IPC code
model_params = {ipc: model.params for ipc, model in final_models.items()}

# Let's display the model parameters for each IPC
print(model_params)

