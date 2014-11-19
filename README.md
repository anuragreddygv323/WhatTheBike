# WhatTheBike

WhatTheBike allows you to predict bicycle availability at Bay Area Bike Share stations. There are two components: 

1. A univariate model, which treats each station as independent.

2. A multivariate model, which allows you select three bike stations and forecast their joint availability.

Currently the application is in alpha. Model fitting and forecasting is available for historical Bike Share data.

### Version

0.1 (in alpha)

### Installation

Installation consists of building the dataframe (called "hourly") and then using that dataframe to make forecasts.

Required Python packages are Pandas and statsmodels.

To install: download the raw data from the [Data Challenge].

[Data Challenge]:http://www.bayareabikeshare.com/datachallenge



