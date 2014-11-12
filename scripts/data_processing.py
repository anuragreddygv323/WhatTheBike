# Script to construct hourly data frame from initial CSV files.

# Data comes from the San Francisco Bike Share data visualization challenge.
# It can be downloaded here: http://www.bayareabikeshare.com/datachallenge

import pandas as pd
import sys

def make_merged_df(rebalancing_data, station_data, pickle = None):
    '''
    Given file paths to rebalancing and station CSV files,
    constructs merged pandas dataframe with parsed datetimes.
    Option to pickle.

    Arguments:
    rebalancing_data (string): File path to rebalancing data CSV.
    station_data (string): File path to station data CSV.
    pickle (string, optional): File path to pickle data.

    Returns: pandas dataframe.
    '''

    print "Now reading from CSV..."

    rebal = pd.read_csv(rebalancing_data)
    stations = pd.read_csv(station_data)
    
    print "Now merging..."
    merged = rebal.merge(stations[["station_id", "name", "dockcount"]], on="station_id")
    
    print "Now parsing datetimes..."
    merged.time = pd.to_datetime(merged.time, format = "%Y/%m/%d %H:%M:%S")
    
    if pickle is not None:
        print "Now sending to pickle..."
        merged.to_pickle(pickle)
    
        print "Successfully pickled."

    return merged



def make_hourly_df(merged, use_station_names = True, pickle = None):
        '''
        Construct multivariate time series –
        rows are hourly timestamps, columns are stations
        – from "merged" dataframe above.

        Arguments:
        merged (Pandas dataframe): Created with make_merged_df.
        use_station_names (bool, optional): Use station names instead of integers.
        pickle (string, optional): file path to pickle data frame.

        Returns: pandas dataframe.
        '''

        slim = merged[["time", "station_id", "bikes_available"]]
        
        hourly = slim.pivot(index = "time", columns = "station_id", values = "bikes_available")
        hourly.fillna(value = 0, inplace = True)
        hourly = hourly.resample("1H", "min")
        
        if use_station_names:
            names_dict = {sid : name for sid, name in zip(merged.station_id.unique(), 
                                 merged.name.unique())}

            hourly = hourly.rename(columns = names_dict)

        if pickle is not None:
            print "Now sending to pickle..."
            hourly.to_pickle(pickle)
            print "Successfully pickled."

        return hourly

if __name__ == "__main__":
    make_merged_df("201402_rebalancing_data.csv")
    make_hourly_df("201402_station_data.csv")

    