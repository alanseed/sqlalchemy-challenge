# sqlalchemy-challenge

## Introduction  
sqlalchemy-challenge consists of an api to serve data and an analysis of temperature and rainfall data for a set of weather stations on Honolulu, Hawaii. 

## Resources
The ```Resources``` directory contains
* hawaii_stations.csv  and hawaii_measurements.csv files of weather station metadata and observations, and  
* hawaii.sqlite database that contains these two data sets as tables  

## Files  
* ```app.py```  A python script to set up an api that has the following queries
    * /api/v1.0/precipitation  
    Returns JSON file with a dictionary of the station metadata and a list of dictionaries with date, prcp values  

    * /api/v1.0/station  
    Returns JSON file with a dictionary of station metadata for the network of weather stations  

    * /api/v1.0/tobs  
    Returns JSON file with a dictionary of the station metadata and a list of dictionaries with date, tobs values  

    * /api/v1.0/<start_date>  
    Takes parameter start_date as yyyy-mm-dd and returns the maximum, mean, and minimum temp of the observations that were recorded in the network on that day 

    * /api/v1.0/<start_date>/<end_date>
    Takes parameters start_date, end_date  as yyyy-mm-dd and returns the maximum, mean, and minimum temp of the observations that were recorded in the network between those days. 

* ```climate.ipynb```
A notebook to use sqlalchemy to access the sqlite data base and perform some basic data exploration  
* ```analysis_bonus_1.ipnb```  
A notebook with the bonus analysis to check if the mean temperature for June is statistically significantly different from the mean temperature for December  

* ```test/test_api.py```  
A python script to test that the responses from the API can be read properly 

