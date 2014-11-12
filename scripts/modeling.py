# Construct univariate time series models for all stations.

# TODO: Add multivariate models.

import pandas as pd
import statsmodels.api as sm
from matplotlib import pyplot as plt
import cPickle
import sys

def load_data(file):
    '''
    Load Pandas dataframe from pickle.
    '''
    df = pd.read_pickle(path)
    df = df.drop(df.columns[-3:], axis = 1)

    return df

def fit_models(df, pickle = None):
    '''
    Return dictionary of AR models. Key are station_name (or station_id),
    values are statsmodels objects.

    Arguments:

    df (Pandas dataframe): multivariate time series dataframe.

    pickle (file, optional): opened file with write access.

    Returns: 
    '''
    models = {}

    col_names = df.columns
    
    for col in col_names:
        models[col] = sm.tsa.AR(df[[col]]).fit(maxlag = 24 * 14, trend = "c")

    if pickle is not None:
        cPickle.dump(models, pickle, protocol= 2)

    return models


def make_univar_forecast(station, start_time, end_time, in_sample = False):
    '''
    Plot number of available bikes along with one-hour-ahead forecast.

    Arguments:
    station (string or int): station name (string) or station id (int).

    start_time (string): String of time to begin forecasting. 
    Must be of form "201Y-MM-DD HH:MM:SS"

    end_time (string): String of time to end forecasting.

    in_sample (bool, optional): If True, forecasts are lagged 

    '''


    model = models[station]
    fc = model.predict(start_time, end_time, dynamic = not in_sample)
    fig, ax = plt.subplots(figsize = (14, 10))

    df.ix[start_time : end_time, station].plot(ax = ax, label = "Actual")
    fc.plot(ax = ax, label = "Forecast", style= "--", lw = 2)
    
    plt.legend(loc = 2)
    plt.ylim(0, model.Y.max() + 1)
    plt.ylabel("Bikes Available", fontsize = 14)
    plt.title(station, fontsize = 15)

    return 


