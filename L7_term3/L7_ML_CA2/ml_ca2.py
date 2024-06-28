import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
