import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================
# CHOOSE CITY HERE
# ==========================

CITY = "Bengaluru"

# Options:
# "Delhi"
# "Mumbai"
# "Hyderabad"
# "Bengaluru"

# ==========================
# DATASET PATHS
# ==========================

city_files = {
    "Delhi": "datasets/Delhi_Master_Dataset_V3.csv",
    "Mumbai": "datasets/Mumbai_Master_Dataset.csv",
    "Hyderabad": "datasets/Hyderabad_Master_Dataset.csv",
    "Bengaluru": "datasets/Bengaluru_Master_Dataset.csv"
}

known_places = {
    "Delhi": {
        "Dwarka": (28.5921, 77.0460),
        "Rohini": (28.7383, 77.0822),
        "Saket": (28.5245, 77.2066),
        "Noida": (28.5355, 77.3910),
        "Gurugram": (28.4595, 77.0266),
        "Faridabad": (28.4089, 77.3178),
        "Ghaziabad": (28.6692, 77.4538),
        "Central Delhi": (28.6139, 77.2090),
        "Okhla": (28.5358, 77.2832),
        "Bahadurgarh": (28.6924, 76.9239),
    },
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
    },
}

# ==========================
# CHECK CITY
# ==========================

if CITY not in city_files:
    raise ValueError("City name is wrong. Use Delhi, Mumbai, Hyderabad, or Bengaluru.")

# ==========================
# LOAD DATA
# ==========================

df = pd.read_csv(city_files[CITY])

# ==========================
# CLEAN BASIC DATA
# ==========================

df = df.dropna()

# ==========================
# CREATE MAP
# ==========================

df["Heat Risk"] = pd.cut(
    df["LST"],
    bins=[0, 30, 35, 40, 45, 100],
    labels=["Low", "Moderate", "High", "Very High", "Extreme"],
)

fig = px.scatter_mapbox(
    df,
    lat="Latitude",
    lon="Longitude",
    color="LST",
    color_continuous_scale="Hot",
    zoom=9,
    height=430,
    opacity=0.74,
    hover_data={
        "LST": ":.2f",
        "Heat Risk": True,
        "NDVI": ":.3f",
        "Humidity": ":.2f",
        "WindSpeed": ":.2f",
        "BuildingDensity": True,
    },
    title=f"{CITY} Urban Heat Hotspot Map",
)

fig.update_traces(marker={"size": 6}, selector={"type": "scattermapbox"})

places = known_places[CITY]
place_names = list(places.keys())
place_lats = [places[name][0] for name in place_names]
place_lons = [places[name][1] for name in place_names]

fig.add_trace(
    go.Scattermapbox(
        lat=place_lats,
        lon=place_lons,
        mode="markers",
        text=place_names,
        marker=dict(size=12, color="#2563eb", opacity=0.95),
        name="Place pins",
        hovertemplate="<b>%{text}</b><br>Place marker<extra></extra>",
    )
)

fig.update_layout(
    mapbox_style="open-street-map",
    mapbox_center={
        "lat": float(df["Latitude"].mean()),
        "lon": float(df["Longitude"].mean()),
    },
    paper_bgcolor="#020617",
    font=dict(color="#111827"),
    margin=dict(l=0, r=0, t=45, b=0),
    autosize=True,
    height=430,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=0.01,
        xanchor="left",
        x=0.01,
        bgcolor="rgba(255,255,255,0.82)",
        bordercolor="rgba(15,23,42,0.18)",
        borderwidth=1,
    ),
)

# ==========================
# SAVE AND SHOW
# ==========================

output_file = f"heatshield-frontend/public/heatmaps/{CITY.lower()}_heatmap.html"
fig.write_html(output_file)

print("Heatmap created successfully!")
print("Saved:", output_file)
