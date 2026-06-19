import pandas as pd
import plotly.express as px

df = pd.read_csv("datasets/Mumbai_Master_Dataset.csv")

df["Heat Risk"] = pd.cut(
    df["LST"],
    bins=[0, 30, 35, 40, 100],
    labels=["Low", "Moderate", "High", "Extreme"]
)

fig = px.scatter_mapbox(
    df,
    lat="Latitude",
    lon="Longitude",
    color="LST",
    color_continuous_scale="Hot",
    zoom=9,
    height=750,
    hover_data={
        "LST": ":.2f",
        "Heat Risk": True,
        "NDVI": ":.3f",
        "Humidity": ":.2f",
        "WindSpeed": ":.2f",
        "BuildingDensity": True
    },
    title="Mumbai Urban Heat Hotspot Map"
)

fig.update_layout(
    mapbox_style="open-street-map",
    margin={"r": 0, "t": 40, "l": 0, "b": 0}
)

fig.write_html("images/mumbai_heatmap.html")
fig.show()

print("Saved: images/mumbai_heatmap.html")