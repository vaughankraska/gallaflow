import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
from sklearn.metrics import mean_squared_error


def create_date_features(df):
    df = df.copy()
    df['year'] = df.index.year
    df['quarter'] = df.index.quarter
    df['month'] = df.index.month
    df['dayofyear'] = df.index.dayofyear
    return df


def clean_nas(df):
    df = df.copy()
    df.ffill(inplace=True)
    df.dropna(inplace=True)
    return df


df = pd.read_csv('data/daily.csv', parse_dates=['date'])
df = df.set_index('date')

df = create_date_features(df)
df = clean_nas(df)
TARGET = 'CFS'
FEATURES = ['TAVG_origValue', 'WTEQ_average', 'WTEQ_origValue',
            'year', 'quarter', 'month', 'dayofyear']

cutoff = pd.to_datetime('2018-01-01')
train = df.loc[df.index < cutoff]
X_train = train[FEATURES]
y_train = train[TARGET]

test = df.loc[df.index >= cutoff]
X_test = test[FEATURES]
y_test = test[TARGET]

reg = xgb.XGBRegressor(
        n_estimators=1000,
        early_stopping_rounds=50,
        learning_rate=0.01
        )
reg.fit(X_train, y_train,
        eval_set=[(X_train, y_train), (X_test, y_test)],
        verbose=10
        )

importances = pd.DataFrame(data=reg.feature_importances_,
                           index=reg.feature_names_in_,
                           columns=['importances'])
print(importances.sort_values('importances'))
