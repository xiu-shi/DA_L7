

### 3. Classification Model 


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


###((800, 22), (200, 22), (800,), (200,))

### Plot the distribution of:
### Issue_Type, System_Component, and Customer_Impact 
### with respect to Priority

plt.figure(figsize=(12, 6))
sns.countplot(x='Issue_Type', hue='Priority', data=data)
plt.title('Distribution of Issue_Type by Priority')
plt.xlabel('Issue Type')
plt.ylabel('Count')
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
sns.countplot(x='System_Component', hue='Priority', data=data)
plt.title('Distribution of System_Component by Priority')
plt.xlabel('System Component')
plt.ylabel('Count')
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
sns.countplot(x='Customer_Impact', hue='Priority', data=data)
plt.title('Distribution of Customer_Impact by Priority')
plt.xlabel('Customer Impact')
plt.ylabel('Count')
plt.tight_layout()
plt.show()



### Our dataset has been successfully preprocessed and split into training and test sets in 80/20 ratio
### Training set: 800 samples, 22 features
### Testing set: 200 samples, 22 features

### Build model: our existing features can be encoded, we’ll train a random forest classifier with the preprocessed data.

from sklearn.ensemble import RandomForestClassifier

### Initialize the Random Forest Classifier
classifier = RandomForestClassifier(n_estimators=100, random_state=42)

### Train the model
classifier.fit(X_train, y_train)

### Evaluate our model

from sklearn.metrics import classification_report

### Predict on the test set
y_pred = classifier.predict(X_test)

### Evaluate the model
report = classification_report(y_test, y_pred, target_names=label_encoder.classes_)
print(report)





### 4. Anomaly(outlier) Detection Algorithm









