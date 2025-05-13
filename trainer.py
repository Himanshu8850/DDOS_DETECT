import pandas as pd
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
from sklearn.metrics import accuracy_score
import numpy as np

# Load the dataset, limiting the number of rows to 10,000
dataset = pd.read_csv('extracted_data.csv')
# dataset.columns = dataset.columns.str.strip()
# dataset = dataset.drop(dataset.columns[[5, 6]], axis=1)

dataset=dataset.iloc[:,1:]
print(dataset.head())


# dataset = pd.read_csv('extracted_data.csv')

# Data Preprocessing
# Remove any rows with missing values
dataset.dropna(inplace=True)

# Separate features and labels
X = dataset.iloc[1:,1:-1]# Features
# X=X.drop(X.columns[0],axis=1)
print(X.head())
y = dataset.iloc[1:,-1]              # Labels

# Scale features to a non-negative range
# ////////////////////////////////////////////////////////////////


# scaler = MinMaxScaler()
# X_scaled = scaler.fit_transform(X)

# ///////////////////////////////////////////////////////////////

# Feature Selection
# Implementing a filter-based feature selection (Chi-squared test)
# best_features = SelectKBest(score_func=chi2, k=10)
# X_selected = best_features.fit_transform(X_scaled, y)

# Split dataset into training and testing sets
X.columns = X.columns.str.strip()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(X_train.head())
print(y_train.head())
# X_train=X_train.iloc[:,1:]
# Initialize Random Forest classifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
rf_classifier.fit(X_train, y_train)

# Predictions on the testing set
y_pred = rf_classifier.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("\nAccuracy:", accuracy)
ch=[513,27702,54.0,0.0,0.0,883679823888.975,1722572756.119,0.001,0.072,0.0]
ch=np.array(ch)
ch=ch.reshape(1,-1)
print(rf_classifier.predict(ch))
with open('model4.pkl', 'wb') as file:
    pickle.dump(rf_classifier, file)