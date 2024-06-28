import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error
import statsmodels.api as sm


### load data
time_series_data = pd.read_csv('/Users/janet.xuishi/Documents/DA_L7/DA_L7/L7_term3/L7_ML_CA2/IT_Company_Time_Series.csv')
time_series_data.head()


time_series_data.info()

### This dataset provide us with a collection of time captureed the monthly demand for 15 different software products offered by this IT company. Each row in the dataset corresponds to a specific month and year, recording the number of units demanded for each product during that period. 

### We observed the Date coumn contains the date of each observation in the YYY-MM-DD format. There are Software_1 to Software_15 columns represent tthe demand for 15 unique software products. THe values are integer counts of the units demanded each month.

### we continue to explore the dataset, check for missing values
missing_values = time_series_data.isnull().sum()
data_types = time_series_data.dtypes

missing_values, data_types

### The dataset contains no missing alues, and Date is object type, we could convert next to a datetime format. Then We can plot the time series for each of the software product to idenify trends and seasonality.




# Convert the Date column to datetime format
time_series_data['Date'] = pd.to_datetime(time_series_data['Date'])

# Set the Date column as the index
time_series_data.set_index('Date', inplace=True)

# Plot time series data for each software product
plt.figure(figsize=(15, 10))

for column in time_series_data.columns:
    plt.plot(time_series_data.index, time_series_data[column], label=column)

plt.title('Software Demand Over Time')
plt.xlabel('Date')
plt.ylabel('Demand')
plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1))
plt.grid(True)
plt.show()

### This visualization indicated among the 15 unique software products over time the demand has been ups and downs trends over time. There appear to be a seaonal patters in the demand for serveral software products. Next, we'll take an in-depth view of each of software product's demand and oberser if there are any outliers.


# Plot time series data for each software product in separate subplots
fig, axes = plt.subplots(nrows=5, ncols=3, figsize=(20, 20), sharex=True)

for i, column in enumerate(time_series_data.columns):
    ax = axes[i//3, i%3]
    ax.plot(time_series_data.index, time_series_data[column], label=column)
    ax.set_title(column)
    ax.grid(True)

fig.suptitle('Software Demand Over Time for Each Product')
plt.tight_layout()
plt.show()


# Create a 3x5 box plot layout for all the software products to detect outliers
fig, axes = plt.subplots(nrows=3, ncols=5, figsize=(30, 20))

# Iterate over all the software products to create individual box plots
for i, column in enumerate(time_series_data.columns):
    ax = axes[i//5, i%5]
    ax.boxplot(time_series_data[column], patch_artist=True)
    ax.set_title(column)
    ax.grid(True)

fig.suptitle('Box Plots for Software Products to Detect Outliers')
plt.tight_layout()
plt.show()



### By separating individual software products, we can observe the outliers indicated outside of the whiskers: 
### Software_2, Software_3, Software_4, Software_5, Software_9, Software_10, Software_12, Software_13. 
### This info may need further investigation as we go.



### Detect and handle outliers using the IQR method
def detect_outliers(data):
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return data[(data < lower_bound) | (data > upper_bound)]

# Identify outliers for the selected software products
outliers = {}
for column in ['Software_2', 'Software_3', 'Software_4', 'Software_5', 'Software_9', 'Software_10', 'Software_12', 'Software_13']:
    outliers[column] = detect_outliers(time_series_data[column])

# Display the outliers
for column, data in outliers.items():
    print(f"Outliers in {column}:")
    print(data)
    print("\n")

# Replace outliers with the median values of the respective columns
for column in outliers.keys():
    median_value = time_series_data[column].median()
    time_series_data[column] = time_series_data[column].apply(
        lambda x: median_value if x in outliers[column].values else x
    )

# Verify if the outliers have been replaced
summary_stats = time_series_data[['Software_2', 'Software_3', 'Software_4', 'Software_5', 'Software_9', 'Software_10', 'Software_12', 'Software_13']].describe()
print(summary_stats)

# Plot box plots for the selected software products after outlier replacement
fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(20, 10))

for i, column in enumerate(['Software_2', 'Software_3', 'Software_4', 'Software_5', 'Software_9', 'Software_10', 'Software_12', 'Software_13']):
    ax = axes[i//4, i%4]
    ax.boxplot(time_series_data[column], patch_artist=True)
    ax.set_title(column)
    ax.grid(True)

fig.suptitle('Box Plots After Outlier Replacement')
plt.tight_layout()
plt.show()


### Time Series Forecasting - SARIMAX


# Identify the top 3 software products based on total demand
total_demand = time_series_data.sum(axis=0)
top_3_products = total_demand.nlargest(3).index
print(f"Top 3 Software Products: {top_3_products}")

#### Top 3 Software Products: Index(['Software_9', 'Software_12', 'Software_13'], dtype='object')




### Based on our top 3 performing software products: 'Software_9', 'Software_12', 'Software_13'
### We apply function to fit and forecast using SARIMA models

### Function to fit, forecast, and evaluate using SARIMA models
def fit_forecast(data, product_name):
    # Check for missing values in the data
    print(f"Checking for missing values in {product_name}:")
    print(data.isnull().sum())

    # Split the data into 75% training and 25% test sets
    split_index = int(len(data) * 0.75)
    train_data = data[:split_index]
    test_data = data[split_index:]

    # Define SARIMA model parameters
    order = (1, 1, 1)
    seasonal_order = (1, 1, 1, 12)

    # Fit SARIMA model to the training data
    model = SARIMAX(train_data, order=order, seasonal_order=seasonal_order)
    results = model.fit()

    # Forecasting for the test set
    forecast_steps_test = len(test_data)
    forecast_test = results.get_forecast(steps=forecast_steps_test)
    forecast_values_test = forecast_test.predicted_mean
    forecast_values_test.index = test_data.index

    # Forecasting for the next 52 weeks (one year)
    forecast_steps_52 = 52
    forecast_52 = results.get_forecast(steps=forecast_steps_52)
    forecast_df_52 = pd.DataFrame({
        'Forecast': forecast_52.predicted_mean.round()
    })
    forecast_df_52.index = pd.date_range(start=forecast_values_test.index[-1] + pd.Timedelta(days=1), periods=forecast_steps_52, freq='W')

    # Plotting the results
    plt.figure(figsize=(14, 7))

    # Observed values and forecast for the test set
    plt.plot(data.index, data, label='Observed', color='blue')
    plt.plot(forecast_values_test.index, forecast_values_test, label='Forecast Test Set', color='orange')

    # Forecast for the next 52 weeks
    plt.plot(forecast_df_52.index, forecast_df_52['Forecast'], label='Forecast 52 weeks', color='green')

    plt.title(f'SARIMAX {product_name} Forecasting')
    plt.xlabel('Date')
    plt.ylabel(f'{product_name} Demand')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Display the table results for the next 52 weeks forecast
    print(forecast_df_52)

# Apply the function to the top 3 products
for product in top_3_products:
    print(f"\nForecasting and evaluating for {product}")
    fit_forecast(time_series_data[product], product)








### 3. Classification and Anomaly Detection

import pandas as pd

### load data
csv = '/Users/janet.xuishi/Documents/DA_L7/DA_L7/L7_term3/L7_ML_CA2/IT_Company_System_Issues_Classification.csv'
data = pd.read_csv(csv)

data_head = data.head()
data_describe = data.describe()
data_info = data.info()
missing_values = data.isnull().sum()

data_head, data_describe, data_info, missing_values



### In our dataset there are no missing values. Next we can carry out encoding categorical features.

from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.model_selection import train_test_split


### Select features and target
features = data[['Issue_Type', 'System_Component', 'Customer_Impact', 'Time_to_Resolve_hrs', 'Reported_By', 'Previous_Occurrences', 'Issue_Reported_Month']]
target = data['Priority']

### One-hot encode categorical features
categorical_features = ['Issue_Type', 'System_Component', 'Customer_Impact', 'Reported_By', 'Issue_Reported_Month']
one_hot_encoder = OneHotEncoder(sparse=False, drop='first')
encoded_features = one_hot_encoder.fit_transform(features[categorical_features])

### Combine encoded features with numerical features
numerical_features = features[['Time_to_Resolve_hrs', 'Previous_Occurrences']].values
all_features = pd.concat([pd.DataFrame(encoded_features), pd.DataFrame(numerical_features)], axis=1)

### Label encode the target variable
label_encoder = LabelEncoder()
encoded_target = label_encoder.fit_transform(target)

### Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(all_features, encoded_target, test_size=0.2, random_state=42)













