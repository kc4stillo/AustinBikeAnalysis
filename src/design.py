# %%
import matplotlib.pyplot as plt
import pandas as pd

# %%
trips_df = pd.read_csv("../data/cleaned_data/metro_trips.csv")

# Recast data types
trips_df = trips_df.astype(
    {
        "trip_id": "int64",
        "bicycle_id": "object",
        "bike_type": "category",
        "pass_type": "category",
        "duration": "int64",
        "checkout_kiosk_id": "category",
        "return_kiosk_id": "category",
    }
)
trips_df["checkout_time"] = pd.to_datetime(trips_df["checkout_time"])
trips_df["checkout_hour"] = trips_df["checkout_hour"].astype("int32")

# %%
weather_df = pd.read_csv("../data/cleaned_data/weather.csv")
weather_df["date"] = pd.to_datetime(weather_df["date"]).dt.round("H")
weather_df = weather_df.astype(
    {
        "temp": "float64",
        "precipitation": "float64",
        "humidity": "float64",
        "visibility": "float64",
        "wind_speed": "float64",
    }
)

# %%
kiosks_df = pd.read_csv("../data/cleaned_data/kiosk.csv")
kiosks_df = kiosks_df.astype(
    {
        "kiosk_id": "int64",
        "kiosk_name": "object",
        "status": "category",
        "address": "object",
        "latitude": "float64",
        "longitude": "float64",
    }
)

# %%


# %%
# seasonal ridership trends

plt.plot()
