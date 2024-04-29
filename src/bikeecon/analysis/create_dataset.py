import pandas as pd
from bikeecon.utils import get_boroughs

BOROUGS = get_boroughs()


def road_causalties():
    df2016 = pd.read_csv("data/casualities_2016.csv")
    df2019 = pd.read_csv("data/casualities_2019.csv")
    df2016 = df2016[["Borough", "Tot", "Ped", "Cyc", "Car"]]
    df2019 = df2019[["Borough", "Tot", "Ped", "Cyc", "Car"]]
    # Use only boroughs in both datasets
    df2016 = df2016[df2016["Borough"].isin(BOROUGS)]
    df2019 = df2019[df2019["Borough"].isin(BOROUGS)]
    # Merge the two with column names
    df = pd.merge(df2016, df2019, on="Borough", suffixes=("_2016", "_2019"))
    # Calculate the change in casualties
    df["Tot_change"] = df["Tot_2019"] - df["Tot_2016"]
    df["Ped_change"] = df["Ped_2019"] - df["Ped_2016"]
    df["Cyc_change"] = df["Cyc_2019"] - df["Cyc_2016"]
    df["Car_change"] = df["Car_2019"] - df["Car_2016"]
    # Calculate percentage change
    df["Tot_change_percent"] = df["Tot_change"] / df["Tot_2016"] * 100
    df["Ped_change_percent"] = df["Ped_change"] / df["Ped_2016"] * 100
    df["Cyc_change_percent"] = df["Cyc_change"] / df["Cyc_2016"] * 100
    df["Car_change_percent"] = df["Car_change"] / df["Car_2016"] * 100
    return df


def emissions():
    df = pd.read_csv("data/Pollutants_updated.csv")
    df_return_2016 = pd.DataFrame(columns=["Borough", "NOx", "PM10", "PM2.5", "CO2"])
    df_return_2019 = pd.DataFrame(columns=["Borough", "NOx", "PM10", "PM2.5", "CO2"])
    for borough in BOROUGS:
        data = df[["Pollutant", "Year", borough]]
        # Extract the data for 2016 and 2019
        pollutant_dict_2016 = {}
        pollutant_dict_2019 = {}
        for pollutant in ["NOx", "PM10", "PM2.5", "CO2"]:
            df_borough = data[(data["Pollutant"] == pollutant) & (data["Year"] == 2016)]
            pollutant_dict_2016[pollutant] = df_borough[borough].values[0]
            df_borough = data[(data["Pollutant"] == pollutant) & (data["Year"] == 2019)]
            pollutant_dict_2019[pollutant] = df_borough[borough].values[0]
        pollutant_dict_2016["Borough"] = borough
        pollutant_dict_2019["Borough"] = borough
        df_return_2016.loc[len(df_return_2016)] = pollutant_dict_2016
        df_return_2019.loc[len(df_return_2019)] = pollutant_dict_2019
    # Merge the two with column names
    df = pd.merge(
        df_return_2016, df_return_2019, on="Borough", suffixes=("_2016", "_2019")
    )
    df["Total_2016"] = (
        df["NOx_2016"] + df["PM10_2016"] + df["PM2.5_2016"] + df["CO2_2016"]
    )
    df["Total_2019"] = (
        df["NOx_2019"] + df["PM10_2019"] + df["PM2.5_2019"] + df["CO2_2019"]
    )
    # Calculate the change in emissions
    for pollutant in ["NOx", "PM10", "PM2.5", "CO2", "Total"]:
        df[pollutant + "_change"] = df[pollutant + "_2019"] - df[pollutant + "_2016"]
        df[pollutant + "_change_percent"] = (
            df[pollutant + "_change"] / df[pollutant + "_2016"] * 100
        )
    return df


def bike_station_space():
    df_stations = pd.read_csv("data/bike-stations_updated.csv")
    df_rides = pd.read_csv("data/bike-rides_updated.csv")
    # Remove unknown boroughs
    df_rides = df_rides[df_rides["Borough"] != "Unknown"]
    df_stations = df_stations[df_stations["Borough"] != "Unknown"]
    # Revove rpws with year empty
    df_rides = df_rides.dropna(subset=["year"])
    df_rides["year"] = df_rides["year"].astype(int)
    df_stations = df_stations.dropna(subset=["year"])
    df_stations["year"] = df_stations["year"].astype(int)
    # Remove years after 2019
    df_rides = df_rides[df_rides["year"] <= 2019]
    df_stations = df_stations[df_stations["year"] <= 2019]
    df_stations = df_stations[df_stations["Borough"].isin(BOROUGS)]
    df_rides = df_rides[df_rides["Borough"].isin(BOROUGS)]

    df_stations = df_stations[["Borough", "year", "docks_count"]]
    # Sum the number of docks for each borough for each year
    df_stations = df_stations.groupby(["Borough", "year"]).sum().reset_index()

    # Get sum of dock counts for all years per borough
    df_stations_borough = df_stations.groupby("Borough").sum().reset_index()
    df_stations_borough = df_stations_borough.rename(
        columns={"docks_count": "total_docks"}
    )
    df_stations_borough = df_stations_borough[["Borough", "total_docks"]]

    # Same for rides
    df_rides_borough = df_rides.groupby("Borough").sum().reset_index()
    df_rides_borough = df_rides_borough.rename(columns={"num_rides": "total_rides"})
    df_rides_borough = df_rides_borough[["Borough", "total_rides"]]

    # Merge the two
    df_stations_borough = pd.merge(
        df_stations_borough, df_rides_borough, on="Borough", how="outer"
    )

    return df_stations_borough


def cycling_proportion():
    df = pd.read_csv("data/Walking-Cycling.csv")
    df["Borough"] = df["Local Authority"]
    df = df[df["Borough"].isin(BOROUGS)]
    df_2016 = df[df["Year"] == "2014/15"]
    df_2019 = df[df["Year"] == "2017/18"]
    df_2016_month = df_2016[df_2016["Frequency"] == "1x per month"]
    df_2016_month = df_2016_month[["Borough", "Cycling_%"]]
    df_2016_week = df_2016[df_2016["Frequency"] == "1x per week"]
    df_2016_week = df_2016_week[["Borough", "Cycling_%"]]
    df_2019_month = df_2019[df_2019["Frequency"] == "1x per month"]
    df_2019_month = df_2019_month[["Borough", "Cycling_%"]]
    df_2019_week = df_2019[df_2019["Frequency"] == "1x per week"]
    df_2019_week = df_2019_week[["Borough", "Cycling_%"]]
    df_2016 = pd.merge(
        df_2016_month, df_2016_week, on="Borough", suffixes=("_month", "_week")
    )
    df_2019 = pd.merge(
        df_2019_month, df_2019_week, on="Borough", suffixes=("_month", "_week")
    )
    df = pd.merge(df_2016, df_2019, on="Borough", suffixes=("_2016", "_2019"))
    df["Cycling_%_change_month"] = (
        df["Cycling_%_month_2019"] - df["Cycling_%_month_2016"]
    )
    df["Cycling_%_change_week"] = df["Cycling_%_week_2019"] - df["Cycling_%_week_2016"]
    return df


def get_demographics():
    df = pd.read_csv(("data/london-borough-profiles-2016 Data set.csv"))
    column_dict = {
        "Area name": "Borough",
        "GLA Population Estimate 2016": "Population",
        "Population density (per hectare) 2016": "Population density",
        "Average Age, 2016": "Average Age",
        "Proportion of population of working-age, 2016": "15-65 Age%",
        "Proportion of population aged 65 & over, 2016": "65+ Age%",
        "% of population from BAME groups (2016)": "BAME%",
        "Unemployment rate (2015)": "Unemployment rate%",
        "Modelled Household median income estimates 2012/13": "Median income",
        "Jobs Density, 2014": "Jobs density",
        "Number of cars per household, (2011 Census)": "Cars per household",
    }
    # Extract and rename columns
    df = df[list(column_dict.keys())]
    df = df.rename(columns=column_dict)
    # Remove unknown boroughs
    df = df[df["Borough"].isin(BOROUGS)]

    df["Population"] = pd.to_numeric(
        df["Population"].apply(lambda x: x.replace(",", "").strip())
    )
    df["Population density"] = pd.to_numeric(df["Population density"])
    df["Average Age"] = pd.to_numeric(df["Average Age"])
    df["15-65 Age%"] = pd.to_numeric(df["15-65 Age%"])
    df["65+ Age%"] = pd.to_numeric(df["65+ Age%"])
    df["BAME%"] = pd.to_numeric(df["BAME%"], errors="coerce")
    df["Unemployment rate%"] = pd.to_numeric(df["Unemployment rate%"], errors="coerce")
    df["Median income"] = pd.to_numeric(
        df["Median income"].apply(lambda x: x[1:].replace(",", ""))
    )
    df["Cars per household"] = pd.to_numeric(df["Cars per household"])

    return df
