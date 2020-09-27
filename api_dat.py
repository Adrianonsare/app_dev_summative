def read_api():
    ''' takes api urls, reads into json format,
     generates dataframes and formats colimns to fit into format of original dataset'''
    
    #Solar
    import requests
    import pandas as pd
    #Takes the url

    
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=-19.461907&lon=142.110216&exclude=[current,minutely,hourly]&appid=686a8268d2d60adfa1efd1b0f3d7ffe5"
    url1="https://api.openweathermap.org/data/2.5/onecall?lat=53.556563&lon=8.598084&exclude=[current,minutely,hourly]&appid=686a8268d2d60adfa1efd1b0f3d7ffe5"

    #Website Actions
    jsonData = requests.get(url).json()
    jsonData1 = requests.get(url1).json()


    #import daily forecast data

    d_date = pd.DataFrame(jsonData['daily']) 
    d_date1 = pd.DataFrame(jsonData1['daily']) 

  
    #Rebuild initial dataframe
    df_solar=pd.concat([d_date.drop(['temp'], axis=1), d_date['temp'].apply(pd.Series)], axis=1)
    df_wind=pd.concat([d_date1.drop(['temp'], axis=1), d_date1['temp'].apply(pd.Series)], axis=1)


    #Converting date column in data imported from API to Day and month columns resembling training dataset
    df_solar['Day']=pd.to_datetime(df_solar.iloc[:,0],unit = 's').dt.day
    df_solar['Month']=pd.to_datetime(df_solar.iloc[:,0],unit = 's').dt.month
    df_solar=df_solar.iloc[0:7,]

    df_wind['Day']=pd.to_datetime(df_wind.iloc[:,0],unit = 's').dt.day
    df_wind['Month']=pd.to_datetime(df_wind.iloc[:,0],unit = 's').dt.month


    df_solar=df_solar.rename(columns={"wind_speed":"wind speed","wind_deg":"direction","max": "Temp_Hi","min": "Temp_Low",
                                    "clouds": "Cloud_Cover_Percentage","uvi":"Solar"})

    df_solar.drop(columns=['sunrise','sunset','feels_like','pressure',
                            'humidity','dew_point','weather','dt','pop',
                            'night','eve','morn','wind speed','direction'],inplace=True)

    df_wind=df_wind.rename(columns={"wind_speed":"wind speed","wind_deg":"direction","max": "Temp_Hi","min": "Temp_Low",
                                    "clouds": "Cloud_Cover_Percentage","uvi":"Solar","rain": "Rainfall_in_mm"})

    df_wind.drop(columns=['sunrise','sunset','feels_like','pressure',
                            'humidity','dew_point','weather','dt','pop',
                            'night','eve','morn','Cloud_Cover_Percentage','Solar','Temp_Low',
                        'Temp_Hi','day'],inplace=True)

    #Slice dataframes from weather API to have separate wind and solar dataframes
    df_solar = df_solar[['Month','Day','Temp_Hi','Temp_Low','Solar','Cloud_Cover_Percentage']]
    df_wind = df_wind[['Month','Day','wind speed','direction']]
    return df_solar,df_wind 
