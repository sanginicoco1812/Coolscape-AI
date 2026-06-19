import pandas as pd
import plotly.express as px

# Load Hyderabad dataset
df = pd.read_csv("datasets/Hyderabad_Master_Dataset.csv")

# Create Heat Risk Category
df["Heat Risk"] = pd.cut(
    df["LST"],
    bins=[0, 30, 35, 40, 45, 100],
    labels=["Low", "Moderate", "High", "Very High", "Extreme"]
)

# Interactive Map
fig = px.scatter_mapbox(
    df,
    lat="Latitude",
    lon="Longitude",
    color="LST",
    color_continuous_scale="Hot",
    zoom=9,
    height=800,
    hover_data={
        "LST": ":.2f",
        "Heat Risk": True,
        "NDVI": ":.3f",
        "Humidity": ":.2f",
        "WindSpeed": ":.2f",
        "BuildingDensity": True
    },
    title="🔥 Hyderabad Urban Heat Hotspot Map"
)

fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r": 0, "t": 50, "l": 0, "b": 0}
)

# Save interactive map
fig.write_html("images/hyderabad_heatmap.html")

# Show map
fig.show()

print("✅ Saved: images/hyderabad_heatmap.html")