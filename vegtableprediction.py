import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error


usd_to_inr = 81.0

vegetable_prices_df = pd.read_csv("Vegetable_prices_pred.csv")


X = vegetable_prices_df[['Form', 'Yield', 'CupEquivalentSize', 'CupEquivalentUnit', 'CupEquivalentPrice']]
y = vegetable_prices_df['RetailPrice']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

categorical_features = ['Form', 'CupEquivalentUnit']
categorical_transformer = OneHotEncoder()

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', categorical_transformer, categorical_features)
    ])

pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('regressor', LinearRegression())])

pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)

mse = mean_squared_error(y_test, y_pred)

vegetable_data = vegetable_prices_df[vegetable_prices_df['Vegetable'] == 'Onions']
vegetable_features = vegetable_data[['Form', 'Yield', 'CupEquivalentSize', 'CupEquivalentUnit', 'CupEquivalentPrice']]
vegetable_price = pipeline.predict(vegetable_features)

vegetable_price_inr = vegetable_price * usd_to_inr

print(f"Predicted price of Vegetable: ₹{vegetable_price_inr[0]:.2f} per kilogram")
