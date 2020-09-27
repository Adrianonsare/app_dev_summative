#Import libraries
import pandas as pd
import  numpy as np
from sklearn import metrics
from sklearn.metrics import mean_squared_error, r2_score

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
import requests
import datetime as dt



solar=pd.read_csv('/home/adrian/Desktop/NOTEBOOKS/ALU_FLASK/MyProject/summ_data/solar_generation_data.csv')

wind=pd.read_csv('/home/adrian/Desktop/NOTEBOOKS/ALU_FLASK/MyProject/summ_data/wind_generation_data.csv')

#In the original dataset, wind data had 366 days, and did not have a month,Day column
#Last row dropped to make the length of the dataframe=365
#Month and day columns added to wind dataset
wind=wind[:-1]
Month = solar["Month"]
Day= solar["Day"]
wind = wind.join(Month)
wind = wind.join(Day)

#Rearrange ind dataset columns
wind=wind[['Month','Day','wind speed','direction','Power Output']]


#Mapping month string values to numeric
month_vals={'Jan':1,'Feb':2,'Mar':3,'Apr':4,
            'May':5,'Jun':6,'Jul':7,'Aug':8,
            'Sep':9,'Oct':10,'Nov':11,'Dec':12}


solar['Month']=solar.iloc[:,0].map(month_vals)
wind['Month']=wind.iloc[:,0].map(month_vals)

#Additional data preparation
solar.rename(columns={'Temp Hi': 'Temp_Hi','Temp Low': 'Temp_Low',
'Cloud Cover Percentage': 'Cloud_Cover_Percentage',
'Power Generated in MW':'Nom.Power_Generated_in_MW'},inplace=True)


#Convert data with degree symbol from string to float
#drop rainfall column
solar['Temp_Hi']=solar['Temp_Hi'].str.split("°", n = 1, expand = True)
solar['Temp_Low']=solar['Temp_Low'].str.split("°", n = 1, expand = True)
solar[['Temp_Hi','Temp_Low']] = solar[['Temp_Hi','Temp_Low']].astype(float)
solar=solar.drop(columns=['Rainfall in mm'])

#Fill out Missing Values
solar=solar.fillna(0)
wind=wind.fillna(0)

#Split data into features and target
X1 = solar.iloc[:, 0:6]
y1 = solar.iloc[:, -1]

X2 = wind.iloc[:, 0:4]
y2 = wind.iloc[:, -1]


#Split data into training and test sets
#solar
X_train, X_test, y_train, y_test = train_test_split(X1, y1, test_size=0.2, random_state=0)
#Wind
X1_train, X1_test, y1_train, y1_test = train_test_split(X2, y2, test_size=0.2, random_state=0)


#Initiate model
regressor = RandomForestRegressor(n_estimators=20, random_state=0)
regressor1 = RandomForestRegressor(n_estimators=20, random_state=0)
#Solar
regressor.fit(X_train, y_train)
# y_pred = regressor.predict(X_test)

#Wind
regressor1.fit(X1_train, y1_train)

#dump regressor in current working directory to permit call by dash app
pickle.dump(regressor, open('model_solar.pkl','wb'))
pickle.dump(regressor1, open('model_wind.pkl','wb'))



