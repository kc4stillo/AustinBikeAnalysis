import pandas as pd
import numpy as np

# Display settings
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
# -------------------------------
# 1. Load raw data
# -------------------------------
trips_df = pd.read_csv("Austin_MetroBike_Trips_20250925.csv")
kiosk_df = pd.read_csv("Austin_MetroBike_Kiosk_Locations_20250925.csv")

weather_df_1 = pd.read_csv("LCD_1.csv")
weather_df_2 = pd.read_csv("LCD_2.csv")

# -------------------------------
# 2. Clean weather data
# -------------------------------
weather_df = pd.concat([weather_df_1, weather_df_2], axis=0)

# Select only FM-15 reports
weather_df = weather_df[weather_df["REPORT_TYPE"] == "FM-15"]

weather_df = weather_df[
    [
        "DATE",
        "HourlyDryBulbTemperature",
        "HourlyPrecipitation",
        "HourlyRelativeHumidity",
        "HourlyVisibility",
        "HourlyWindSpeed",
    ]
]

weather_df = weather_df.rename(
    columns={
        "DATE": "date",
        "HourlyDryBulbTemperature": "temp",
        "HourlyPrecipitation": "precipitation",
        "HourlyRelativeHumidity": "humidity",
        "HourlyVisibility": "visibility",
        "HourlyWindSpeed": "wind_speed",
    }
)

# Clean temp column
weather_df["temp"] = weather_df["temp"].str.replace(r"s$", "", regex=True)
weather_df = weather_df.replace("*", np.nan)

# Clean precipitation
weather_df["precipitation"] = weather_df["precipitation"].replace(r"s$", "", regex=True)
weather_df["precipitation"] = weather_df["precipitation"].replace("T", 0.005)

# Clean visibility
weather_df["visibility"] = weather_df["visibility"].str.replace(r"V$", "", regex=True)
weather_df["visibility"] = weather_df["visibility"].str.replace(r"s$", "", regex=True)

# Convert datatypes
weather_df["date"] = pd.to_datetime(weather_df["date"])
weather_df["temp"] = weather_df["temp"].astype(float)
weather_df["precipitation"] = weather_df["precipitation"].astype(float)
weather_df["humidity"] = weather_df["humidity"].astype(float)
weather_df["visibility"] = weather_df["visibility"].astype(float)
weather_df["wind_speed"] = weather_df["wind_speed"].astype(float)

weather_df.ffill(inplace=True)
# -------------------------------
# 3. Clean trips data
# -------------------------------
trips_df = pd.read_csv("Austin_MetroBike_Trips_20250925.csv")

pd.DataFrame(trips_df["Membership or Pass Type"].value_counts())

trips_df["Membership or Pass Type"] = trips_df["Membership or Pass Type"].replace(
    "U.T. Student Membership", "Student Membership"
)


pd.DataFrame(trips_df["Membership or Pass Type"].value_counts())


# Convert columns to categories
trips_df["pass_type"] = trips_df["Membership or Pass Type"].astype("category")
trips_df["return_kiosk"] = trips_df["Return Kiosk"].astype("category")
trips_df["return_kiosk_id"] = trips_df["Return Kiosk ID"].astype("category")
trips_df["checkout_kiosk"] = trips_df["Checkout Kiosk"].astype("category")
trips_df["checkout_kiosk_id"] = trips_df["Checkout Kiosk ID"].astype("category")
trips_df["bike_type"] = trips_df["Bike Type"].astype("category")
trips_df["checkout_time"] = pd.to_datetime(trips_df["Checkout Datetime"])


# Drop unused columns
trips_df = trips_df.drop(
    labels=[
        "Membership or Pass Type",
        "Bike Type",
        "Checkout Datetime",
        "Checkout Date",
        "Checkout Time",
        "Checkout Kiosk ID",
        "Checkout Kiosk",
        "Return Kiosk ID",
        "Return Kiosk",
        "Month",
        "Year",
    ],
    axis=1,
)

# Rename columns
trips_df = trips_df.rename(
    columns={
        "Trip ID": "trip_id",
        "Bicycle ID": "bicycle_id",
        "Trip Duration Minutes": "duration",
    }
)

# Reorder columns
trips_df = trips_df[
    [
        "trip_id",
        "bicycle_id",
        "checkout_time",
        "checkout_kiosk_id",
        "checkout_kiosk",
        "return_kiosk_id",
        "return_kiosk",
        "duration",
        "bike_type",
        "pass_type",
    ]
]

# -------------------------------
# 4. Clean kiosk data
# -------------------------------
kiosk_df = kiosk_df.rename(
    columns={
        "Kiosk ID": "kiosk_id",
        "Kiosk Name": "kiosk_name",
        "Kiosk Status": "status",
        "Location": "location",
        "Address": "address",
        "Alternate Name": "alt_name",
        "City Asset Number": "city_asset_number",
        "Property Type": "property_type",
        "Number of Docks": "num_docks",
        "Power Type": "power_type",
        "Footprint Length": "footprint_length",
        "Footprint Width": "footprint_width",
        "Notes": "notes",
        "Council District": "council_district",
        "Image": "image",
        "Modified Date": "modified_date",
    }
)

# Convert datatypes
kiosk_df["status"] = kiosk_df["status"].astype("category")
kiosk_df["property_type"] = kiosk_df["property_type"].astype("category")
kiosk_df["power_type"] = kiosk_df["power_type"].astype("category")
kiosk_df["council_district"] = kiosk_df["council_district"].astype("category")
kiosk_df["num_docks"] = kiosk_df["num_docks"].astype("category")

# Extract latitude/longitude
kiosk_df[["latitude", "longitude"]] = (
    kiosk_df["location"].str.strip("()").str.split(",", expand=True)
)
kiosk_df["latitude"] = kiosk_df["latitude"].astype(float)
kiosk_df["longitude"] = kiosk_df["longitude"].astype(float)

# Drop unused columns
kiosk_df = kiosk_df.drop(
    labels=[
        "notes",
        "image",
        "modified_date",
        "location",
        "footprint_length",
        "footprint_width",
        "alt_name",
    ],
    axis=1,
)

# Reorder columns
kiosk_df = kiosk_df[
    [
        "kiosk_id",
        "kiosk_name",
        "status",
        "latitude",
        "longitude",
        "address",
        "council_district",
        "num_docks",
        "power_type",
        "property_type",
        "city_asset_number",
    ]
]

# -------------------------------
# 5. Save cleaned datasets
# -------------------------------
weather_df.to_csv("../cleaned_data/weather.csv", index=False)
trips_df.to_csv("../cleaned_data/metro_trips.csv", index=False)
kiosk_df.to_csv("../cleaned_data/kiosk.csv", index=False)
