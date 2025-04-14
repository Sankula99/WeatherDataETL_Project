import json
import requests
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sb
#Get API from OpenWeather for Sydney
api_k = "8bd57a2fbfb96c06ec7b64c69ce07071"
lat =-33.8688
lon = 151.2093
url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&cnt=5&appid={api_k}"


response = requests.get(url)

data = response.json()
json_str = json.dumps(data, indent=4)
print(json_str)

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
weather_data.append({date_time,temp_s,feel,min, max,pressure,groundLvl,humidity})
print(weather_data)
df= pd.DataFrame(weather_data)
df.head()