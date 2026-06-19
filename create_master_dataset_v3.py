import pandas as pd
from scipy.spatial import cKDTree

master = pd.read_csv("datasets/Delhi_Master_Dataset.csv")
building = pd.read_csv("datasets/Delhi_BuildingDensity_Clean.csv")

def add_nearest_feature(master_df, feature_df, feature_name):
    tree = cKDTree(feature_df[["Latitude", "Longitude"]].values)
    distances, indices = tree.query(master_df[["Latitude", "Longitude"]].values)
    master_df[feature_name] = feature_df.iloc[indices][feature_name].values
    return master_df

master_v3 = add_nearest_feature(master, building, "BuildingDensity")

master_v3.to_csv("datasets/Delhi_Master_Dataset_V3.csv", index=False)

print("Master V3 Shape:", master_v3.shape)
print(master_v3.head())
print("\nSaved: datasets/Delhi_Master_Dataset_V3.csv")