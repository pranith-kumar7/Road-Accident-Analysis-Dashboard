import pandas as pd
import matplotlib.pyplot as plt

# Load raw accident data
df = pd.read_csv("road_accident_raw.csv")

# Basic inspection
print(df.info())
print(df.isna().sum())

# Remove duplicate records
df = df.drop_duplicates()

# Handle missing categorical values
df["Weather"] = df["Weather"].fillna("Unknown")
df["Road_Surface"] = df["Road_Surface"].fillna("Unknown")

# Convert date and derive analysis fields
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month_name()
df["Month_Number"] = df["Date"].dt.month
df["Day"] = df["Date"].dt.day

df["Hour"] = pd.to_datetime(df["Time"], format="%H:%M").dt.hour
df["Time_Period"] = pd.cut(
    df["Hour"],
    bins=[-1, 5, 11, 17, 21, 24],
    labels=["Night", "Morning", "Afternoon", "Evening", "Late Night"],
    right=False
)

# Export Power BI-ready data
df.to_csv("road_accident_cleaned.csv", index=False)
df.to_excel("road_accident_cleaned.xlsx", index=False)

# Basic EDA outputs
severity = df["Severity"].value_counts()
monthly = df.groupby(["Month_Number", "Month"]).size().reset_index(name="Accidents")
weather = df.groupby("Weather").size().reset_index(name="Accidents")
location = df.groupby("Location_Type").size().reset_index(name="Accidents")

severity.to_csv("severity_summary.csv")
monthly.sort_values("Month_Number").to_csv("monthly_summary.csv", index=False)
weather.to_csv("weather_summary.csv", index=False)
location.to_csv("location_summary.csv", index=False)

print("Cleaning and analysis completed.")
