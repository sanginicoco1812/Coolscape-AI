import os
from math import sqrt

import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

from streamlit_option_menu import option_menu
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

st.set_page_config(page_title="CoolScape AI", page_icon="🛰️", layout="wide")

datasets = {
    "Delhi": "datasets/Delhi_Master_Dataset_V3.csv",
    "Mumbai": "datasets/Mumbai_Master_Dataset.csv",
    "Hyderabad": "datasets/Hyderabad_Master_Dataset.csv",
    "Bengaluru": "datasets/Bengaluru_Master_Dataset.csv"
}

models = {
    "Delhi": "models/real_temperature_model_v3.pkl",
    "Mumbai": "models/mumbai_temperature_model.pkl",
    "Hyderabad": "models/hyderabad_temperature_model.pkl",
    "Bengaluru": "models/bengaluru_temperature_model.pkl"
}

image_paths = {
    "Delhi": {
        "importance": "images/feature_importance_real.png",
        "correlation": "images/correlation_matrix.png",
        "shap": "images/real_shap_summary.png"
    },
    "Mumbai": {
        "importance": "images/mumbai_feature_importance.png",
        "correlation": "images/mumbai_correlation_matrix.png",
        "shap": "images/mumbai_shap_summary.png"
    },
    "Hyderabad": {
        "importance": "images/hyderabad_feature_importance.png",
        "correlation": "images/hyderabad_correlation_matrix.png",
        "shap": "images/hyderabad_shap_summary.png"
    },
    "Bengaluru": {
        "importance": "images/bengaluru_feature_importance.png",
        "correlation": "images/bengaluru_correlation_matrix.png",
        "shap": "images/bengaluru_shap_summary.png"
    }
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
        "Bahadurgarh": (28.6924, 76.9239)
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
        "Kurla": (19.0726, 72.8845)
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
        "Mehdipatnam": (17.3949, 78.4398)
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
        "Rajajinagar": (12.9915, 77.5545)
    }
}

def nearest_place(lat, lon, city):
    best_name = "Unknown"
    best_dist = 999

    for name, (p_lat, p_lon) in known_places[city].items():
        dist = sqrt((lat - p_lat) ** 2 + (lon - p_lon) ** 2)
        if dist < best_dist:
            best_dist = dist
            best_name = name

    return best_name

def calculate_metrics(df, model):
    X = df[["NDVI", "Humidity", "WindSpeed", "BuildingDensity"]]
    y = df["LST"]

    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, pred)
    r2 = r2_score(y_test, pred)

    return round(mae, 2), round(r2, 3)

def show_image(path):
    if os.path.exists(path):
        st.image(path, use_container_width=True)
    else:
        st.warning(f"Missing image: {path}")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#020617,#052e2b,#020617);
    color:white;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#020617,#064e3b);
    border-right: 1px solid #2dd4bf;
}
.card {
    padding: 24px;
    border-radius: 22px;
    background: rgba(15,23,42,0.78);
    border: 1px solid rgba(148,163,184,0.25);
}
.kpi {
    padding: 24px;
    border-radius: 22px;
    text-align:center;
    background: linear-gradient(135deg,rgba(127,29,29,.85),rgba(234,88,12,.65));
}
.cool {
    padding: 24px;
    border-radius: 22px;
    text-align:center;
    background: linear-gradient(135deg,rgba(7,89,133,.85),rgba(15,118,110,.65));
}
.reco {
    padding: 28px;
    border-radius: 24px;
    background: linear-gradient(135deg,#064e3b,#0f766e);
    border: 1px solid #5eead4;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🛰️ CoolScape AI")
    st.caption("Urban Heat Command Center")
    st.markdown("---")

    city = st.selectbox(
        "Select City",
        ["Delhi", "Mumbai", "Hyderabad", "Bengaluru"]
    )

    page = option_menu(
        menu_title=None,
        options=["Dashboard", "Heat Map", "Top Places", "Cooling Simulator", "AI Analytics"],
        icons=["speedometer", "map", "geo-alt", "tree", "bar-chart"],
        default_index=0,
        styles={
            "container": {"background-color": "transparent"},
            "icon": {"color": "#5eead4", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "margin": "8px 0",
                "border-radius": "14px",
                "padding": "12px",
                "color": "#d1fae5",
                "--hover-color": "rgba(20,184,166,.25)",
            },
            "nav-link-selected": {
                "background": "linear-gradient(90deg,#0f766e,#14b8a6)",
                "color": "white",
                "font-weight": "700",
            },
        }
    )

df = pd.read_csv(datasets[city])
model = joblib.load(models[city])

df = df.dropna().reset_index(drop=True)

# Remove unrealistic LST artifacts
df = df[(df["LST"] >= 20) & (df["LST"] <= 65)].reset_index(drop=True)

df["Place"] = df.apply(
    lambda row: nearest_place(row["Latitude"], row["Longitude"], city),
    axis=1
)

df["Risk"] = pd.cut(
    df["LST"],
    bins=[0, 30, 35, 40, 45, 100],
    labels=["Low", "Moderate", "High", "Very High", "Extreme"]
)

df["Suggested Action"] = df.apply(
    lambda r: "Increase green cover" if r["NDVI"] < 0.2 else "Monitor and maintain vegetation",
    axis=1
)

mae, r2 = calculate_metrics(df, model)

place_summary = df.groupby("Place").agg(
    Max_LST=("LST", "max"),
    Min_LST=("LST", "min"),
    Avg_LST=("LST", "mean"),
    Avg_NDVI=("NDVI", "mean"),
    Avg_BuildingDensity=("BuildingDensity", "mean")
).reset_index()

place_summary = place_summary.sort_values("Avg_LST", ascending=False).reset_index(drop=True)

hot_count = min(5, max(1, len(place_summary) // 2))
cool_count = min(5, max(1, len(place_summary) - hot_count))

top_hottest = place_summary.head(hot_count).copy().reset_index(drop=True)
top_hottest.insert(0, "Rank", range(1, len(top_hottest) + 1))

remaining_places = place_summary[
    ~place_summary["Place"].isin(top_hottest["Place"])
].copy()

top_coolest = remaining_places.sort_values(
    "Avg_LST", ascending=True
).head(cool_count).reset_index(drop=True)

top_coolest.insert(0, "Rank", range(1, len(top_coolest) + 1))

hottest_region = place_summary.sort_values("Avg_LST", ascending=False).iloc[0]
coolest_region = place_summary.sort_values("Avg_LST", ascending=True).iloc[0]

if page == "Dashboard":
    st.title(f"🛰️ CoolScape AI: {city} Heat Intelligence")

    c1, c2, c3, c4 = st.columns(4)

    c1.markdown(f"""
    <div class="kpi">
    <h2>{hottest_region['Avg_LST']:.2f}°C</h2>
    <p>🔥 Hottest Region: {hottest_region['Place']}</p>
    </div>
    """, unsafe_allow_html=True)

    c2.markdown(f"""
    <div class="cool">
    <h2>{coolest_region['Avg_LST']:.2f}°C</h2>
    <p>❄️ Coolest Region: {coolest_region['Place']}</p>
    </div>
    """, unsafe_allow_html=True)

    c3.metric("Model MAE", f"{mae}°C")
    c4.metric("R² Score", r2)

    st.markdown(f"""
    <div class="card">
    <h3>{city} Urban Heat Intelligence</h3>
    <p>
    This dashboard detects heat hotspots, ranks non-overlapping hot/cool regions,
    and simulates cooling interventions using satellite and weather data.
    </p>
    </div>
    """, unsafe_allow_html=True)

elif page == "Heat Map":
    st.title(f"🗺️ {city} Interactive Heat Map")

    threshold = st.slider(
        "Show locations hotter than",
        float(round(df["LST"].min(), 1)),
        float(round(df["LST"].max(), 1)),
        float(round(df["LST"].mean(), 1))
    )

    filtered = df[df["LST"] >= threshold]

    fig = px.scatter_mapbox(
        filtered,
        lat="Latitude",
        lon="Longitude",
        color="LST",
        color_continuous_scale="Hot",
        zoom=9,
        height=730,
        hover_name="Place",
        hover_data={
            "LST": ":.2f",
            "Risk": True,
            "Suggested Action": True,
            "NDVI": ":.3f",
            "Humidity": ":.2f",
            "WindSpeed": ":.2f",
            "BuildingDensity": True,
        }
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    st.plotly_chart(fig, use_container_width=True)

elif page == "Top Places":
    st.title(f"🔥❄️ Hottest and Coolest Regions in {city}")

    c1, c2 = st.columns(2)

    with c1:
        st.subheader(f"🔥 Top {len(top_hottest)} Hottest Regions")
        st.dataframe(
            top_hottest[["Rank", "Place", "Max_LST", "Avg_LST", "Avg_NDVI", "Avg_BuildingDensity"]],
            use_container_width=True,
            hide_index=True
        )

    with c2:
        st.subheader(f"❄️ Top {len(top_coolest)} Coolest Regions")
        st.dataframe(
            top_coolest[["Rank", "Place", "Min_LST", "Avg_LST", "Avg_NDVI", "Avg_BuildingDensity"]],
            use_container_width=True,
            hide_index=True
        )

    fig = px.bar(
        top_hottest,
        x="Place",
        y="Avg_LST",
        color="Avg_LST",
        color_continuous_scale="Hot",
        title=f"{city}: Hottest Regions by Average LST"
    )

    st.plotly_chart(fig, use_container_width=True)

elif page == "Cooling Simulator":
    st.title(f"🌳 {city} Cooling Intervention Simulator")

    selected_place = st.selectbox(
        "Select Place",
        sorted(df["Place"].unique())
    )

    place_df = df[df["Place"] == selected_place]
    hotspot = place_df.sort_values("LST", ascending=False).iloc[0]

    ndvi_increase = st.slider("Increase vegetation / NDVI (%)", 0, 60, 20)
    building_reduction = st.slider("Reduce building density (%)", 0, 60, 20)

    current = pd.DataFrame([{
        "NDVI": hotspot["NDVI"],
        "Humidity": hotspot["Humidity"],
        "WindSpeed": hotspot["WindSpeed"],
        "BuildingDensity": hotspot["BuildingDensity"]
    }])

    current_temp = model.predict(current)[0]

    green = current.copy()
    green["NDVI"] *= (1 + ndvi_increase / 100)

    building = current.copy()
    building["BuildingDensity"] *= (1 - building_reduction / 100)

    green_temp = model.predict(green)[0]
    building_temp = model.predict(building)[0]

    veg_cooling = current_temp - green_temp
    building_cooling = current_temp - building_temp

    a, b, c = st.columns(3)

    a.metric("Current Temp", f"{current_temp:.2f} °C")
    b.metric("Vegetation Scenario", f"{green_temp:.2f} °C", f"-{veg_cooling:.2f} °C")
    c.metric("Urban Density Scenario", f"{building_temp:.2f} °C", f"-{building_cooling:.2f} °C")

    best = "Increase vegetation cover" if veg_cooling >= building_cooling else "Urban density / cool-roof intervention"
    best_cooling = max(veg_cooling, building_cooling)

    st.markdown(f"""
    <div class="reco">
    <h2>✅ Recommendation for {selected_place}</h2>
    <p><b>{best}</b></p>
    <p>Estimated cooling potential: <b>{best_cooling:.2f} °C</b></p>
    </div>
    """, unsafe_allow_html=True)

    st.write("### Hotspot Details")
    st.dataframe(hotspot.to_frame().T, use_container_width=True)

elif page == "AI Analytics":
    st.title(f"📊 {city} AI Analytics")

    paths = image_paths[city]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Feature Importance")
        show_image(paths["importance"])

    with col2:
        st.subheader("Correlation Matrix")
        show_image(paths["correlation"])

    st.subheader("SHAP Summary")
    show_image(paths["shap"])