import re

import numpy as np
import pandas as pd

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

pass_type_mapping = {
    # 1. single_trip
    "Pay-as-you-ride": "single_trip",
    "Single Trip (Pay-as-you-ride)": "single_trip",
    "Single Trip": "single_trip",
    "Single Trip Ride": "single_trip",
    "$1 Pay by Trip Winter Special": "single_trip",
    "$1 Pay by Trip Fall Special": "single_trip",
    "RideScout Single Tide": "single_trip",
    "RideScout Single Ride": "single_trip",
    "Single Trip ": "single_trip",
    # 2. one_day_pass
    "24 Hour Walk Up Pass": "one_day_pass",
    "Walk Up": "one_day_pass",
    "24-Hour Membership": "one_day_pass",
    # 3. monthly_pass
    "Local31": "monthly_pass",
    "Local30": "monthly_pass",
    "Local30 ($11 plus tax)": "monthly_pass",
    "Madtown Monthly": "monthly_pass",
    "Heartland Pass (Monthly Pay)": "monthly_pass",
    # 4. annual_membership
    "Local365": "annual_membership",
    "Local365+Guest Pass": "annual_membership",
    "Local365 ($80 plus tax)": "annual_membership",
    "Local365- 1/2 off Anniversary Special": "annual_membership",
    "Local365+Guest Pass- 1/2 off Anniversary Special": "annual_membership",
    "Local365 Youth (age 13-17 riders)": "annual_membership",
    "Local365 Youth with helmet (age 13-17 riders)": "annual_membership",
    "Local365 Youth (age 13-17 riders)- 1/2 off Special": "annual_membership",
    "Annual": "annual_membership",
    "Annual Membership": "annual_membership",
    "Annual Member": "annual_membership",
    "Annual Pass": "annual_membership",
    "Annual Pass (Original)": "annual_membership",
    "Annual Pass (30 minute)": "annual_membership",
    "Annual Plus": "annual_membership",
    "Annual Plus Membership": "annual_membership",
    "Republic Rider (Annual)": "annual_membership",
    "Republic Rider": "annual_membership",
    "Membership: pay once one-year commitment": "annual_membership",
    "Membership: pay once, one-year commitment": "annual_membership",
    "Heartland Pass (Annual Pay)": "annual_membership",
    "Founding Member": "annual_membership",
    "Aluminum Access": "annual_membership",
    "Denver B-cycle Founder": "annual_membership",
    "Annual ": "annual_membership",
    "Membership: pay once  one-year commitment": "annual_membership",
    "Annual Membership ": "annual_membership",
    # 5. student_or_special
    "Student Membership": "student_or_special",
    "Semester Membership": "student_or_special",
    "HT Ram Membership": "student_or_special",
    "UT Student Membership": "student_or_special",
    "Try Before You Buy Special": "student_or_special",
    "ACL Weekend Pass Special": "student_or_special",
    "ACL 2019 Pass": "student_or_special",
    "FunFunFun Fest 3 Day Pass": "student_or_special",
    "Explorer": "student_or_special",
    "Explorer ($8 plus tax)": "student_or_special",
    "3-Day Explorer": "student_or_special",
    "Weekender": "student_or_special",
    "3-Day Weekender": "student_or_special",
    "Weekender ($15 plus tax)": "student_or_special",
    "7-Day": "student_or_special",
    "RESTRICTED": "student_or_special",
    "U.T. Student Membership": "student_or_special",
}

trips_df["pass_type"] = trips_df["pass_type"].replace(pass_type_mapping)

trips_df["checkout_date"] = trips_df["checkout_time"].dt.date
trips_df["checkout_hour"] = trips_df["checkout_time"].dt.hour
trips_df["checkout_dayofweek"] = trips_df["checkout_time"].dt.day_name()
trips_df["checkout_month"] = trips_df["checkout_time"].dt.month_name()

# Calculate return_time by adding duration (in minutes)
trips_df["return_time"] = trips_df["checkout_time"] + pd.to_timedelta(
    trips_df["duration"], unit="m"
)

# Extract return features
trips_df["return_date"] = trips_df["return_time"].dt.date
trips_df["return_hour"] = trips_df["return_time"].dt.hour
trips_df["return_dayofweek"] = trips_df["return_time"].dt.day_name()
trips_df["return_month"] = trips_df["return_time"].dt.month_name()


def to_snake_case(text):
    text = str(text).lower()  # lowercase and ensure it's a string
    text = re.sub(r"[@/&]", " ", text)  # replace special chars with space
    text = re.sub(r"[^a-z0-9\s]", "", text)  # remove punctuation
    text = re.sub(r"\s+", "_", text.strip())  # replace spaces with underscores
    return text


# Apply snake_case to both columns
trips_df["checkout_kiosk"] = trips_df["checkout_kiosk"].apply(to_snake_case)
trips_df["return_kiosk"] = trips_df["return_kiosk"].apply(to_snake_case)

# Merge duplicates by summing 'count' if it exists, otherwise drop duplicates
if "count" in trips_df.columns:
    checkout_clean = (
        trips_df.groupby("checkout_kiosk", as_index=False)["count"]
        .sum()
        .sort_values("count", ascending=False)
    )
    return_clean = (
        trips_df.groupby("return_kiosk", as_index=False)["count"]
        .sum()
        .sort_values("count", ascending=False)
    )
else:
    checkout_clean = trips_df.drop_duplicates(subset=["checkout_kiosk"])
    return_clean = trips_df.drop_duplicates(subset=["return_kiosk"])


trips_df = trips_df[
    [
        # Trip identifiers
        "trip_id",
        "bicycle_id",
        "bike_type",
        "pass_type",
        "duration",
        # Checkout info
        "checkout_time",
        "checkout_date",
        "checkout_hour",
        "checkout_dayofweek",
        "checkout_month",
        "checkout_kiosk_id",
        "checkout_kiosk",
        # Return info
        "return_time",
        "return_date",
        "return_hour",
        "return_dayofweek",
        "return_month",
        "return_kiosk_id",
        "return_kiosk",
    ]
]

# -------------------------------
# 4. Clean kiosk data
# -------------------------------

kiosk_df = kiosk_df[["Kiosk ID", "Kiosk Name", "Kiosk Status", "Location", "Address"]]

kiosk_df = kiosk_df.rename(
    columns={
        "Kiosk ID": "kiosk_id",
        "Kiosk Name": "kiosk_name",
        "Kiosk Status": "status",
        "Location": "location",
        "Address": "address",
    }
)

# Convert datatypes
kiosk_df["status"] = kiosk_df["status"].astype("category")

# Extract latitude/longitude
kiosk_df[["latitude", "longitude"]] = (
    kiosk_df["location"].str.strip("()").str.split(",", expand=True)
)
kiosk_df["latitude"] = kiosk_df["latitude"].astype(float)
kiosk_df["longitude"] = kiosk_df["longitude"].astype(float)

kiosk_df["kiosk_name"] = kiosk_df["kiosk_name"].apply(to_snake_case)

# Merge duplicates in kiosk_df by summing 'count' if it exists
if "count" in kiosk_df.columns:
    kiosk_df = (
        kiosk_df.groupby("kiosk_name", as_index=False)["count"]
        .sum()
        .sort_values("count", ascending=False)
    )
else:
    kiosk_df = kiosk_df.drop_duplicates(subset=["kiosk_name"])

kiosk_df.drop(labels=["location"], inplace=True, axis=1)

# -------------------------------
# 5. Save cleaned datasets
# -------------------------------
weather_df.to_csv("../cleaned_data/weather.csv", index=False)
trips_df.to_csv("../cleaned_data/metro_trips.csv", index=False)
kiosk_df.to_csv("../cleaned_data/kiosk.csv", index=False)
