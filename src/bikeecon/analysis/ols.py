# Import OLSEstimator from statsmodels
import pandas as pd
import statsmodels.api as sm
from bikeecon.analysis.create_dataset import (
    bike_station_space,
    cycling_proportion,
    emissions,
    get_demographics,
    road_causalties,
)

df_road = road_causalties()
df_emissions = emissions()
df_demographics = get_demographics()
df_bike = bike_station_space()
df_cycling = cycling_proportion()


TARGET_VAR = "Tot_change_percent"  # Road casualties

# Num of biking stations


OTHER_VARS = [
    "Population density",
    "15-65 Age%",
    "65+ Age%",
    "BAME%",
    "Unemployment rate%",
    "Median income",
    "Jobs density",
    # "Cars per household",
]


# Merge the datasets
df = pd.merge(df_road, df_emissions, on="Borough")
df = pd.merge(df, df_demographics, on="Borough")
df = pd.merge(df, df_bike, on="Borough")
df = pd.merge(df, df_cycling, on="Borough")

# Drop rows with missing values
df = df.dropna()

DEP_VAR = "total_rides"
df[DEP_VAR] = df[DEP_VAR] / df["Population"]
OTHER_VARS = OTHER_VARS + [DEP_VAR]

# Use only the columns we need
df = df[[TARGET_VAR] + OTHER_VARS]


# df["Median income"] = df["Median income"] / 1000_000

# Create the model
X = df[OTHER_VARS]
y = df[TARGET_VAR]
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()
print(model.summary())
