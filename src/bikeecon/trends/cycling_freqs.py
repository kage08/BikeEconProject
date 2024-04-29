import os

import matplotlib.pyplot as plt
import pandas as pd
from bikeecon.utils import get_boroughs

# Plot settings
plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (10, 6)
# Font size
plt.rcParams.update({"font.size": 14})


CYCLING_PERCENT_FILE = "data/Walking-Cycling.csv"

df = pd.read_csv(CYCLING_PERCENT_FILE)
df["Measure"] = df["Cycling_%"].apply(lambda x: float(x))

freq = "1x per week"
df = df[df["Frequency"] == freq]


df = df[["Local Authority", "Year", "Measure"]]


# Convert year of format "2010/11" to int 2010
df["Year"] = df["Year"].apply(lambda x: int(x.split("/")[0]) + 2)

# For each borough, plot the cycling frequency over time in seperate plots
PLOT_DIR = "plots/cycling_freqs_week/"
if not os.path.exists(PLOT_DIR):
    os.makedirs(PLOT_DIR)
boroughs = get_boroughs()
df = df[df["Local Authority"].isin(boroughs)]
for borough in boroughs:
    df_borough = df[df["Local Authority"] == borough]
    if df_borough.empty:
        continue
    plt.figure()
    plt.plot(df_borough["Year"], df_borough["Measure"])
    plt.title(f"Cycling frequency in {borough}")
    plt.xlabel("Year")
    plt.ylabel(f"% atleast {freq}")
    plt.savefig(PLOT_DIR + f"{borough}.png")
    plt.close()

# Get total cycling frequency over time
df_total = df[["Year", "Measure"]].groupby("Year").mean()
plt.figure()
plt.plot(df_total.index, df_total["Measure"])
plt.title("Total cycling frequency in London")
plt.xlabel("Year")
plt.ylabel(f"% atleast {freq}")
plt.savefig(PLOT_DIR + "Total.png")
plt.close()
