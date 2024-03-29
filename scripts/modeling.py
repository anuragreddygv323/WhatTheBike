# Construct univariate and multivariate time series models for all stations.
# TODO: Add diagnostics.

import pandas as pd
import statsmodels.api as sm
from matplotlib import pyplot as plt
import cPickle
import sys

def load_data(path):
    '''
    Load Pandas dataframe of hourly station data from pickle.
    Drops stations with incomplete data.
    '''
    df = pd.read_pickle(path)
    df = df.drop(df.columns[-3:], axis = 1)

    return df


def fit_univar_models(df, pickle = None):
    '''
    Return dictionary of AR models. Keys are station_name (or station_id),
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
    TODO: Remove this function!

    Return dictionary of AR models. Keys are station_name (or station_id),
    values are statsmodels objects.

    Arguments:

    df (Pandas dataframe): multivariate time series dataframe.

    pickle (file, optional): opened file with write access.

    Returns:

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

def make_univar_forecast(models, station, start_time, end_time, in_sample=False):
    '''
    Create forecasts (predictions) for a particular station.

    Inputs:

    models (dictionary mapping stations to trained models)
    station (string): station name.
    start_time (string): date time to begin forecasting "201Y-mm-DD HH:mm:SS"
    end_time (string): time of last forecast
    in_sample (boolean): if false, use forecast. Else use filter.
    '''
    model = models[station]
    return model.predict(start_time, end_time, dynamic= not in_sample)

def make_univar_fc_plot(models, station, fc):
    '''
    Plots forecast with models.

    Inputs:

    models (dictionary mapping stations to trained models)
    station (string): station name.
    fc (numpy array): forecast, as generated by make_univar_forecast
    '''
    
    start_time = fc.index.min()
    end_time = fc.index.max()
    model = models[station]

    fig, ax = plt.subplots(figsize = (14, 10))
    pd.DataFrame(data=model.data.endog, index=model.data.dates).plot(ax=ax, label="Actual")
    fc.plot(ax = ax, label = "Forecast", style= "--", lw = 2, color="red")
    
    plt.legend(loc = 4, fontsize = 16)
    plt.ylim(0, df[station].max() + 1)
    plt.ylabel("Bikes Available", fontsize = 14)
    plt.title(station, fontsize = 15)
    ax.grid(False)

    return


def fit_multivar_model(df, first, second, third):
    return sm.tsa.VAR(df[[first, second, third]]).fit(maxlags = 24 * 7, trend = "ct")



def multivar_forecast(var, start_, end_, steps_ahead=1):
    y = pd.DataFrame(var.y, index=var.dates)
    ind = pd.tseries.index.DatetimeIndex(freq="H", start=start_, end=end_)
    preds = pd.DataFrame(columns=var.names, index=ind)
    for time in ind:
        preds.ix[time] = var.forecast(y.ix[:(time - steps_ahead)].values, steps=steps_ahead)[-1]
        
    return preds


def make_multivar_fc_plot(df, fc):
    fig, ax = plt.subplots(figsize=(16, 12))
    df.ix[fc.index, fc.columns].plot(ax = ax, color = ["r", "b", "g"]);
    fc.plot(ax = ax, style="--", lw=2, color = ["r", "b", "g"])
    ax.legend(list(fc.columns) + ["forecast"] * 3, loc=4, fontsize=16)
    ax.grid(False)
    return


