import pandas as pd
import requests
from config import API_KEY, LAT, LON, CITY_NAME

# Load breakpoint tables
df = pd.read_csv("aqi_checkpoints.csv")
df1 = pd.read_csv("aqi_categories.csv")


def find_cat(AQI):
    row = df1[(df1["AQI_Low"] <= AQI) & (AQI <= df1["AQI_High"])]
    if row.empty:
        return "Out of range", "Unknown"
    return row.iloc[0]["Category"], row.iloc[0]["Color"]


def getsub_index(value, pollutant):
    row = df[(df["Pollutant"] == pollutant) &
             (df["Conc_Low"] <= value) &
             (value <= df["Conc_High"])]

    if row.empty:
        print(f"{pollutant} value {value} out of range")
        return None

    y1 = row.iloc[0]["AQI_Low"]
    y2 = row.iloc[0]["AQI_High"]
    x1 = row.iloc[0]["Conc_Low"]
    x2 = row.iloc[0]["Conc_High"]

    return y1 + (value - x1) * (y2 - y1) / (x2 - x1)


def fetch_live_data():
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    components = data["list"][0]["components"]

    return {
        "PM2.5": components["pm2_5"],
        "PM10": components["pm10"],
        "NO2": components["no2"],
        "O3": components["o3"],
        "CO": components["co"] / 1000,  # convert µg/m3 → mg/m3
        "SO2": components["so2"],
        "NH3": components["nh3"],
        "Pb": 0  # not provided
    }


# ---------------- MAIN ----------------

print(f"\nFetching live AQI data for {CITY_NAME}...\n")

city_data = fetch_live_data()

aqi_values = []

for pollutant, value in city_data.items():
    sub_index = getsub_index(value, pollutant)

    if sub_index is not None:
        aqi_values.append(sub_index)

AQI = round(max(aqi_values))
category, color = find_cat(AQI)

print("Live Pollutant Data:")
for p, v in city_data.items():
    print(f"{p}: {v}")

print("\nFinal AQI:", AQI)
print("Category:", category)
print("Color:", color)