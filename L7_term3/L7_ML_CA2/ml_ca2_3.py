

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













