import os
import pickle
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from bikeecon.utils import get_borough_from_address, get_boroughs

# Plot settings
plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (10, 6)
# Font size
plt.rcParams.update({"font.size": 14})

STATION_FILE = "data/bike-stations.csv"
RIDES_FILE = "data/bike-rides.csv"

BAD_ADDRESSES = [
    "Soul Buoy",
    "Baker Street",
]

df_stations = pd.read_csv(STATION_FILE)
df_rides = pd.read_csv(RIDES_FILE)

boroughs = get_boroughs()


def loc_to_borough(loc: str) -> str:
    if "(Baker Street)" in loc or "Soul Buoy" in loc:
        return "Unknown"
    if loc in BAD_ADDRESSES:
        return "Unknown"
    tries = 0
    while tries < 3:
        try:
            print("Getting location for", loc)
            borough = get_borough_from_address(loc)
            break
        except Exception as e:
            # If keyerror, return unknown
            if "city" in str(e):
                borough = "Unknown"
                return borough
            print("Failed to get location for", loc)
            print(e)
            print("Waiting and trying again")
            # Wait and try again
            time.sleep(15)
            tries += 1
    if tries == 3:
        return "Unknown"
    if (borough in boroughs) or ("London" in borough) or ("Westminster" in borough):
        return borough
    return "Unknown"


df_stations["Borough"] = df_stations["name"].apply(loc_to_borough)
df_stations.to_csv("data/bike-stations_updated.csv", index=False)
# Remove unknown boroughs
df_stations = df_stations[df_stations["Borough"] != "Unknown"]


years = list(range(2015, 2021))
borough_stations = {b: np.zeros(len(years)) for b in boroughs}

for i, year in enumerate(years):
    df_year = df_stations[df_stations["year"] == year]
    for borough in boroughs:
        borough_stations[borough][i] = df_year[df_year["Borough"] == borough].shape[0]


# Save data

with open("data/borough_stations.pkl", "wb") as f:
    pickle.dump(borough_stations, f)

# Lets plot the data
PLOT_DIR = "plots/stations_hires/"
if not os.path.exists(PLOT_DIR):
    os.makedirs(PLOT_DIR)
for borough in boroughs:
    plt.figure()
    plt.plot(years, borough_stations[borough])
    plt.title(f"Number of stations in {borough}")
    plt.xlabel("Year")
    plt.ylabel("Number of stations")
    plt.savefig(PLOT_DIR + f"{borough}.png")
    plt.close()

# Plot total stations across all boroughs
total_stations = np.zeros(len(years))

for i, year in enumerate(years):
    total_stations[i] = sum([borough_stations[b][i] for b in boroughs])

plt.figure()
plt.plot(years, total_stations)
plt.title("Total number of stations in London")
plt.xlabel("Year")
plt.ylabel("Number of stations")
plt.savefig(PLOT_DIR + "Total.png")
plt.close()

df_rides["Borough"] = df_rides["start_station_name"].apply(loc_to_borough)
df_rides = (
    df_rides[["year", "Borough", "num_rides"]]
    .groupby(["year", "Borough"])
    .sum()
    .reset_index()
)
# Remove unknown boroughs
df_rides.to_csv("data/bike-rides_updated.csv", index=False)
df_rides = df_rides[df_rides["Borough"] != "Unknown"]
df_rides.to_csv("data/bike-rides_updated.csv", index=False)


# Plot rides
df_rides = df_rides[df_rides["Borough"].isin(boroughs)]
for borough in boroughs:
    df_borough = df_rides[df_rides["Borough"] == borough]
    if df_borough.empty:
        continue
    plt.figure()
    plt.plot(df_borough["year"], df_borough["num_rides"])
    plt.title(f"Number of rides in {borough}")
    plt.xlabel("Year")
    plt.ylabel("Number of rides")
    plt.savefig(PLOT_DIR + f"{borough}_rides.png")
    plt.close()

# Plot total rides
df_total = df_rides[["year", "num_rides"]].groupby("year").sum()
plt.figure()
plt.plot(df_total.index, df_total["num_rides"])
plt.title("Total number of rides in London")
plt.xlabel("Year")
plt.ylabel("Number of rides")
plt.savefig(PLOT_DIR + "Total_rides.png")
plt.close()
