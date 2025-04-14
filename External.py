import json
import requests
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import os
from dotenv import load_dotenv
#Get API from OpenWeather for Sydney
#hide token using .env file and loading using python-dotenv package
load_dotenv()
API_KEY =os.getenv("API_KEY")
lat =-33.8688
lon = 151.2093
url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&cnt=5&appid={API_KEY}"

response = requests.get(url)
data = response.json()
json_str = json.dumps(data, indent=4)
#print(json_str)

def keltoCel(temp_k):
    return temp_k -273.15

if response.status_code == 200:
    data = response.json()
    weather_data = []
    for report in data['list']:
        date_time = datetime.utcfromtimestamp(report['dt'])
        temp_s = keltoCel(report['main']['temp'])
        feel = keltoCel(report['main']['feels_like'])
        min =keltoCel(report['main']['temp_min'])
        max = keltoCel(report['main']['temp_max'])
        pressure = (report['main']['pressure'])
        groundLvl = (report['main']['pressure'])
        humidity = (report['main']['humidity'])
        #Append Renames the column from numbers to words
        weather_data.append({"DateTIME":date_time,"TEMP":temp_s,"Feels":feel,"Min":min,"Max": max,"Pressure":
                             pressure,"GroundLVL": groundLvl,"Humid":humidity})
    df= pd.DataFrame(weather_data)
    df.head()
    df.info()
    #Convert the DateTime column to datetime format
    df['DateTIME'] = pd.to_datetime(df['DateTIME'])

    #Extract day and hour from the DateTime column
    df['Day'] = df['DateTIME'].dt.date
    df['Hour'] = df['DateTIME'].dt.hour

    #Pivot the DataFrame 
    df_pivot =df.pivot(index='Day', columns='Hour', values='TEMP')
    
    #Average value of temperature
    average_value = df['TEMP'].mean()

    #Plotting the data on a graph
    plt.figure(figsize=(12, 6))
    plt.plot(df['DateTIME'], df['TEMP'], marker='o', linestyle='-', color='b')
    plt.axhline(y=average_value, color='r', linestyle='--', label='Average Temperature')
    plt.title('Temperature Forecast for Sydney')
    plt.xlabel('Date and Time')
    plt.ylabel('value')
    plt.legend(loc ='upper left')
    plt.grid(True)
    plt.show()

    #Heatmap 
    plt.figure(figsize=(12, 3))
    sns.heatmap(df_pivot, cmap='YlGnBu', annot=True, fmt=".1f",linewidths=0.5)
    plt.title('Day/Hour Temperature Heatmap')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Day')
    plt.show()
