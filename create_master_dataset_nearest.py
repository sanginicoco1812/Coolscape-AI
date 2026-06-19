import pandas as pd
from scipy.spatial import cKDTree

ndvi = pd.read_csv("datasets/Delhi_NDVI_Clean.csv")
lst = pd.read_csv("datasets/Delhi_LST_Clean.csv")
humidity = pd.read_csv("datasets/Delhi_Humidity_Clean.csv")
wind = pd.read_csv("datasets/Delhi_WindSpeed_Clean.csv")

# First merge NDVI + LST directly because their coordinates match
master = ndvi.merge(lst, on=["Latitude", "Longitude"], how="inner")

def add_nearest_feature(master_df, feature_df, feature_name):
    tree = cKDTree(feature_df[["Latitude", "Longitude"]].values)
    distances, indices = tree.query(master_df[["Latitude", "Longitude"]].values)

    master_df[feature_name] = feature_df.iloc[indices][feature_name].values
    return master_df

master = add_nearest_feature(master, humidity, "Humidity")
master = add_nearest_feature(master, wind, "WindSpeed")

master.to_csv("datasets/Delhi_Master_Dataset.csv", index=False)

print("Master Dataset Shape:", master.shape)
print(master.head())
print("\nSaved: datasets/Delhi_Master_Dataset.csv")