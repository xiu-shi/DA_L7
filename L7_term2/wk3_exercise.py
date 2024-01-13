import pandas as pd
import numpy as np

# Load data into a Pandas DataFrame
data = pd.read_csv('your_data_file.csv')

# Calculate the mean
mean = np.mean(data)

# Calculate the median
median = np.median(data)

# Calculate the mode
mode = data.mode().iloc[0]

# Display the results
print("Mean:", mean)
print("Median:", median)
print("Mode:", mode)

# Save the results
# ...
