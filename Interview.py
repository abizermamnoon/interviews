# Read this from https://medium.com/swlh/pandas-datareader-federal-reserve-economic-data-fred-a360c5795013
#import all packages
import pandas_datareader as pdr
import fredapi as fa  
import pandas as pd 
import plotly.express as px
import requests
import datetime
import numpy as np
import kaleido


import os
import requests
from dotenv import load_dotenv, find_dotenv

def req(value1: str, value2: str):

  payload = {'arg1': value1, 'arg2': value2}
  
  # Load in the environment variables
  
  path_to_dotenv = find_dotenv() # NOTE: You will likely not need to do this
  load_dotenv(path_to_dotenv) # NOTE: This often works without any arguments -- try that first
  
  apikey = os.environ.get("Name_of_api_key_env_variable", None) # Returns None if there is no variable with that name
  
  # Can add a try/except here with an assert to check if apikey is not None
  
  payload["key"] = apikey
  
  r = requests.get('https://httpbin.org/get', params=payload)
  
  # This will send a GET request to
  # https://httpbin.org/get?arg1=value1&arg2=value2&key=149EXAMPLEKEY1023
  
  return r.json()

# encode start and end date in start and end https://towardsdev.com/fred-api-get-us-economic-data-using-python-e51ac8e7b1cc
start = datetime.datetime(2000,1,1)
end   =  datetime.datetime(2020,1,1)

# creates a data frame of the different datasets in fred between 2000 and 2020 https://towardsdev.com/fred-api-get-us-economic-data-using-python-e51ac8e7b1cc
df = pdr.DataReader(['PAYEMS','CPIAUCSL','GDPC1'],'fred',start,end)
# Rename the columns in dataframe https://www.geeksforgeeks.org/how-to-rename-columns-in-pandas-dataframe/
df = df.rename(columns = {'PAYEMS': 'Quarterly Total Nonfarm Employment',
                           'CPIAUCSL': 'Quarterly Consumer Price Index',
                            'GDPC1' : 'Real GDP'
                            })
display(df)
#Convert dataframe to csv file https://towardsdatascience.com/how-to-export-pandas-dataframe-to-csv-2038e43d9c03
df.to_csv('economic_indicators.csv')

# Import plotly graph objects
import plotly.graph_objects as go 
from plotly.subplots import make_subplots

#Create histogram of quarterly CPI https://plotly.com/python/histograms/
Histogram = px.histogram(df, x = 'Quarterly Consumer Price Index')
Histogram.show()

# Create scatterplot of Total Nonfarm Employment Vs Quarterly CPI https://www.sharpsightlabs.com/blog/plotly-scatter-plot/
Scatterplot2 = px.scatter(data_frame = df,
            x = 'Quarterly Total Nonfarm Employment',
            y = 'Quarterly Consumer Price Index')
Scatterplot2.show()

#Create a two y-axes time series plot https://plotly.com/python/multiple-axes/
fig = make_subplots(specs = [[{"secondary_y": True}]])
# Add y axis with scale of Nonfarm Employment
fig.add_trace(
    go.Scatter(data_frame = df, x = 'date', y = 'Quarterly Total Nonfarm Employment', 
            name = "Quarterly Total Nonfarm Employment"), secondary_y = False)
# Add y axis with scale of Real GDP
fig.add_trace(
    go.Scatter(data_frame = df, x = 'date ', y = 'Real GDP', 
           name = "Real GDP"), secondary_y = True)
fig.update_layout( title_text = "Real GDP VS Total Nonfarm Employment")
# Create scatterplot of Real GDP vs Quarterly CPI
Scatterplot = px.scatter(data_frame = df,
            x = 'Real GDP',
            y = 'Quarterly Consumer Price Index')
Scatterplot.show()
