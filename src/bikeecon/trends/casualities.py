import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Plot settings
plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (10, 6)
# Font size
plt.rcParams.update({"font.size": 14})

CASUALTIES_FILES = [
    "data/casualities_2016.csv",
    "data/casualities_2017.csv",
    "data/casualities_2018.csv",
    "data/casualities_2019.csv",
]

years = [2016, 2017, 2018, 2019]
dfs = [pd.read_csv(file) for file in CASUALTIES_FILES]
columns = ["Tot", "Ped", "Cyc", "Car"]

dfs = [df[["Borough", "Tot", "Ped", "Cyc", "Car"]] for df in dfs]

# For each borough, plot the casualties over time in seperate plots
PLOT_DIR = "plots/casualties/"
if not os.path.exists(PLOT_DIR):
    os.makedirs(PLOT_DIR)

boroughs = dfs[0]["Borough"].unique()
for borough in boroughs:
    df_boroughs = [df[df["Borough"] == borough] for df in dfs]
    if any(df_borough.empty for df_borough in df_boroughs):
        continue
    plt.figure()
    dataset = np.array(
        [df_borough[columns].values[0] for df_borough in df_boroughs]
    )  # year x caluality type
    for i, column in enumerate(columns):
        plt.plot(years, dataset[:, i], label=column)
    plt.title(f"Casualties in {borough}")
    plt.xlabel("Year")
    plt.ylabel("Casualties")
    plt.legend()
    plt.savefig(PLOT_DIR + f"{borough}.png")
    plt.close()

for borough in boroughs:
    df_boroughs = [df[df["Borough"] == borough] for df in dfs]
    if any(df_borough.empty for df_borough in df_boroughs):
        continue
    plt.figure()
    dataset = np.array(
        [df_borough[columns].values[0] for df_borough in df_boroughs]
    )  # year x caluality type
    plt.plot(years, dataset[:, 2], label="Cyclist")
    plt.title(f"Casualties in {borough}")
    plt.xlabel("Year")
    plt.ylabel("Casualties")
    plt.legend()
    plt.savefig(PLOT_DIR + f"{borough}_cyclist.png")
    plt.close()
