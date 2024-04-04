import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

import warnings
warnings.filterwarnings(action='ignore')

def onehot_encode(df, column):
    df = df.copy()
    dummies = pd.get_dummies(df[column], prefix=column)
    df = pd.concat([df, dummies], axis=1)
    df = df.drop(column, axis=1)
    return df

def preprocess_inputs(df):
    df = df.copy()
    
    # Clean Vegetable condition column
    df['Vegetable condition'] = df['Vegetable condition'].replace({'scarp': 'scrap'})
    
    # Strip whitespace from Vegetable column
    df['Vegetable'] = df['Vegetable'].str.strip()
    
    # Binary encoding
    df['Deasaster Happen in last 3month'] = df['Deasaster Happen in last 3month'].replace({'no': 0, 'yes': 1})
    
    # Ordinal encoding
    df['Month'] = df['Month'].replace({
        'jan': 1,
        'apr': 4,
        'july': 7,
        'sept': 9,
        'oct': 10,
        'dec': 12,
        'may': 5,
        'aug': 8,
        'june': 6,
        ' ': np.NaN,
        'march': 3
    })
    
    # Fill missing month values with column mode
    df['Month'] = df['Month'].fillna(df['Month'].mode()[0])
    
    # One-hot encoding
    for column in ['Season', 'Vegetable condition']:
        df = onehot_encode(df, column)
    
    return df
def predict_vegetable_price(data, vegetable_name):
    # Strip whitespace from vegetable_name
    vegetable_name = vegetable_name.strip()
    
    # Filter data for the specified vegetable
    vegetable_data = data[data['Vegetable'].str.strip() == vegetable_name]
    
    if vegetable_data.empty:
        print("No data found for the specified vegetable.")
        return None
    
    # Preprocess the filtered data
    preprocessed_data = preprocess_inputs(vegetable_data)
    
    # Reorder the columns to match the order during training
    X = preprocessed_data.reindex(columns=X_train.columns, fill_value=0)
    
    # Load the trained model
    model = RandomForestRegressor()  # Assuming RandomForestRegressor is the chosen model
    model.fit(X_train, y_train)
    
    # Predict price for the input data
    predicted_prices = model.predict(X)
    
    # Calculate the average predicted price
    average_predicted_price = predicted_prices.mean()
    
    return average_predicted_price

def method(vegetable_name):
    vegetable_name = 'tomato'
    predicted_prices = predict_vegetable_price(data, vegetable_name)
    return predicted_prices

data = pd.read_csv('Vegetable_market.csv')
preprocessed_data = preprocess_inputs(data)
y = preprocessed_data['Price per kg']
X = preprocessed_data.drop(['Vegetable', 'Price per kg'], axis=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, shuffle=True, random_state=1)
scaler = StandardScaler()
scaler.fit(X_train)
X_train = pd.DataFrame(scaler.transform(X_train), index=X_train.index, columns=X_train.columns)
X_test = pd.DataFrame(scaler.transform(X_test), index=X_test.index, columns=X_test.columns)
model = RandomForestRegressor()  # You can change the model if desired
model.fit(X_train, y_train)
model.fit(X_train, y_train)