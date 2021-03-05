# Summary Statistics
import pandas as pd
import numpy as np
import calendar
import re

# statistical models
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split, KFold, cross_val_score, GridSearchCV
from sklearn import linear_model
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import RFE
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

class PreProcessing():
    def __init__(self):
        pass

    #     data cleaning
    def transform(self, data):
        data.dropna(axis='index', how='all', inplace=True)
        data.columns = data.columns.str.replace(" ", "").str.title()
        data.Day = pd.to_datetime(data.Date).dt.strftime("%A")
        data['Format'] = np.where(data['Format'] == "Video Graphic", "Video",
                                  np.where(data['Format'].isnull(), "Missing",
                                           np.where(data['Format'] == 'Photo', "Image", data['Format'].str.strip())))
        data = data.fillna(0)
        #         new total_engagement column
        data['Totalengagement2'] = data['Retweets_Shares'] + data.Likes + data.Mediaviews + data.Linkclicks + data.Detailexpands + \
                                   data.Userprofileclicks + data.Mediaengagements
        #         measure post length
        data['PostLength'] = data.Post.str.strip().apply(lambda x: len(str(x)))
        #     count hashtags and mentions
        data['Hashtags'] = data.Post.str.strip().apply(lambda x: len(
            set([re.sub(r"(\W+)$", "", j) for j in set([i for i in str(x).split() if i.startswith("#")])])))
        data['With_hash'] = data.Hashtags.apply(lambda x: 1 if x > 0 else 0)
        data['Mentions'] = data.Post.str.strip().apply(lambda x: len(
            set([re.sub(r"(\W+)$", "", j) for j in set([i for i in str(x).split() if i.startswith("@")])])))
        data['With_mentions'] = data.Mentions.apply(lambda x: 1 if x > 0 else 0)
        #         categorical data encoding
        pred_var = ['Account', 'Month', 'Day', 'Format', 'Totalengagement2', 'With_hash', 'PostLength', \
                    'Hashtags', 'Mentions', 'With_mentions']
        accounts = {'Twitter': 0, 'Facebook': 1, 'LinkedIn': 2}
        months = {'January': 0, 'February': 1, 'March': 2, 'April': 3, 'May': 4, 'June': 5, 'July': 6, 'August': 7,
                  'September': 8, 'October': 9,
                  'November': 10, 'December': 11}
        days = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
        formats = {'Article': 0, 'Graphic': 1, 'Image': 2, 'Missing': 3, 'Status Update': 4, 'Video': 5}
        data = data[data.Format != "Share"]
        data.replace({'Account': accounts, 'Month': months, 'Day': days, 'Format': formats}, inplace=True)
        # #         tell python that these vars are categorical
        #         data.Account = data.Account.astype("category")
        #         data.Month = data.Month.astype("category")
        #         data.Format = data.Format.astype("category")

        data = data[pred_var]

        return data

    #     train test split
    def split_files(self, data):
        #         train test split
        X = data.drop('Totalengagement2', axis=1)
        y = data.Totalengagement2
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
        return X_train, X_test, y_train, y_test

    #     standerdise
    def normalization(self, trainset):
        scaler = StandardScaler()
        scaler.fit(X=trainset[['PostLength', 'Hashtags', 'Mentions']])
        return scaler

    def combine_normalised(self, normalized, originalfile):
        numerical_vars = ['PostLength', 'Hashtags', 'Mentions']
        dt = pd.concat([originalfile.drop(numerical_vars, axis=1).reset_index(drop=True),
                        normalized], axis=1)

        return dt
