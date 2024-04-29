import os

import matplotlib.pyplot as plt
import pandas as pd

# Plot settings
plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (10, 6)
# Font size
plt.rcParams.update({"font.size": 14})

AIR_QUALITY_FILE = "data/Pollutants_updated.csv"
df = pd.read_csv(AIR_QUALITY_FILE)
pollutants = df["Pollutant"].unique()
years = [2019, 2016, 2013]
PLOT_DIR = "plots/air_quality/"
if not os.path.exists(PLOT_DIR):
    os.makedirs(PLOT_DIR)

boroughs = df.columns[2:]

for pollutant in pollutants:
    df_pollutant = df[df["Pollutant"] == pollutant]
    for borough in boroughs:
        plt.figure()
        plt.plot(years, df_pollutant[borough])
        plt.title(f"{pollutant} in {borough}")
        plt.xlabel("Year")
        plt.ylabel("Concentration")
        plt.savefig(PLOT_DIR + f"{pollutant}_{borough}.png")
        plt.close()
