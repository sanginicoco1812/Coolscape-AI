import pandas as pd
from math import sqrt

# Change city here
CITY = "Mumbai"   # Mumbai, Hyderabad, Bengaluru

datasets = {
    "Mumbai": "datasets/Mumbai_Master_Dataset.csv",
    "Hyderabad": "datasets/Hyderabad_Master_Dataset.csv",
    "Bengaluru": "datasets/Bengaluru_Master_Dataset.csv"
}

known_places = {
    "Mumbai": {
        "South Mumbai": (18.9388, 72.8354),
        "Bandra": (19.0596, 72.8295),
        "Andheri": (19.1136, 72.8697),
        "Borivali": (19.2307, 72.8567),
        "Thane": (19.2183, 72.9781),
        "Navi Mumbai": (19.0330, 73.0297),
        "Chembur": (19.0522, 72.9005),
        "Powai": (19.1176, 72.9060),
        "Malad": (19.1860, 72.8484),
        "Worli": (19.0176, 72.8174),
        "Dadar": (19.0178, 72.8478),
        "Kurla": (19.0726, 72.8845),
    },

    "Hyderabad": {
        "Charminar": (17.3616, 78.4747),
        "Secunderabad": (17.4399, 78.4983),
        "HITEC City": (17.4483, 78.3915),
        "Gachibowli": (17.4401, 78.3489),
        "Madhapur": (17.4486, 78.3908),
        "Kukatpally": (17.4948, 78.3996),
        "Banjara Hills": (17.4126, 78.4483),
        "Begumpet": (17.4445, 78.4664),
        "LB Nagar": (17.3457, 78.5522),
        "Shamshabad": (17.2512, 78.4377),
        "Uppal": (17.4056, 78.5591),
        "Mehdipatnam": (17.3949, 78.4398),
    },

    "Bengaluru": {
        "MG Road": (12.9756, 77.6068),
        "Whitefield": (12.9698, 77.7500),
        "Electronic City": (12.8452, 77.6602),
        "Koramangala": (12.9352, 77.6245),
        "Indiranagar": (12.9784, 77.6408),
        "Hebbal": (13.0358, 77.5970),
        "Yelahanka": (13.1007, 77.5963),
        "Jayanagar": (12.9250, 77.5938),
        "Marathahalli": (12.9569, 77.7011),
        "Kengeri": (12.9081, 77.4873),
        "HSR Layout": (12.9116, 77.6474),
        "Rajajinagar": (12.9915, 77.5545),
    }
}

def nearest_place(lat, lon, places):
    best_name = None
    best_dist = 999

    for name, (p_lat, p_lon) in places.items():
        dist = sqrt((lat - p_lat) ** 2 + (lon - p_lon) ** 2)

        if dist < best_dist:
            best_dist = dist
            best_name = name

    return best_name

df = pd.read_csv(datasets[CITY])

df["Place"] = df.apply(
    lambda row: nearest_place(
        row["Latitude"],
        row["Longitude"],
        known_places[CITY]
    ),
    axis=1
)

place_summary = df.groupby("Place").agg(
    Max_LST=("LST", "max"),
    Min_LST=("LST", "min"),
    Avg_LST=("LST", "mean"),
    Avg_NDVI=("NDVI", "mean"),
    Avg_BuildingDensity=("BuildingDensity", "mean")
).reset_index()

top_10_hottest = place_summary.sort_values(
    "Max_LST",
    ascending=False
).head(10)

top_10_coolest = place_summary.sort_values(
    "Min_LST",
    ascending=True
).head(10)

print(f"\n🔥 TOP 10 HOTTEST PLACES IN {CITY}")
print(top_10_hottest)

print(f"\n❄️ TOP 10 COOLEST PLACES IN {CITY}")
print(top_10_coolest)

top_10_hottest.to_csv(
    f"datasets/{CITY}_Top10_Hottest_Places.csv",
    index=False
)

top_10_coolest.to_csv(
    f"datasets/{CITY}_Top10_Coolest_Places.csv",
    index=False
)

print("\nSaved:")
print(f"datasets/{CITY}_Top10_Hottest_Places.csv")
print(f"datasets/{CITY}_Top10_Coolest_Places.csv")