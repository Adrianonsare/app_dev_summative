# app_dev_summative
Submission of Flask Summative

The application used Plotly Dash

There are three python Files:
  1.model.py: Contains the model training workflow. It taked the solar egenration data 
  
  2.api_dat.py: Contains a function that does an API request from the weather APIl extracts the daily forecast data, converts the data into two dataframes, whose                   columns match the wind and solar generation data used in the model. This is later imported as a module into the dash app.
  
  3.dash_app.py:The full dash app. Contains the workflow that allows upload of a maintenance file (solar_farm.csv) that is used to derate the predictions on the API                weather data, based on the maintenance schedule and the days of the month and the month.This module also makes calls to the pickled RandomForest                    Regression Models for both the solar and wind predictions. The module also makes calls to the api_dat.py module for the data from the API call
  
  
 There are 3 .csv files:
  1.solar_generation_data,wind_generation_data: The csv files with the features and target used to train the regression model
  
  2.solar_farm.csv: The maintenane schedule file.
  
  
  
 To run the app:
  1.Run model.py(to train and save the model)
  2.Run apu_dat.py to make the api call
  3.Run dash_app.py to to access the local host webpage,upload the maintenance file(solar_farm.csv), make predictions and display
  
  
 NB:Note that the available weather data for the solar farm location was for 6 days rather than 7 days
  
  
  
