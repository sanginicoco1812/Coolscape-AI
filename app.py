import os
from math import sqrt

import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
import gdown

from streamlit_option_menu import option_menu
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score


st.set_page_config(
    page_title="CoolScape AI",
    page_icon="🌍",
    layout="wide"
)


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

# Replace these with your actual Google Drive FILE IDs
model_drive_ids = {
    "Delhi": "https://drive.google.com/file/d/12azeSQ_JnfhY8CGvFYF6G-qViGHq-KVM/view?usp=sharing",
    "Mumbai": "https://drive.google.com/file/d/15kDG-y2af6wAtRaaDmjrFBzFp-q1oDft/view?usp=sharing",
    "Hyderabad": "https://drive.google.com/file/d/1FaymPjoahhIBG9wArpcrSWSy7pZA62po/view?usp=sharing",
    "Bengaluru": "https://drive.google.com/file/d/1P93X9wyBjlTEu2Gc-fM3y5kDBb54NHnf/view?usp=sharing"
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


def download_model_if_missing(city):
    os.makedirs("models", exist_ok=True)

    model_path = models[city]

    if not os.path.exists(model_path):
        file_id = model_drive_ids[city]

        if file_id.startswith("PASTE_"):
            st.error(
                f"Google Drive file ID missing for {city} model. "
                "Please update model_drive_ids in app.py."
            )
            st.stop()

        url = f"https://drive.google.com/uc?id={file_id}"

        with st.spinner(f"Downloading {city} model..."):
            gdown.download(url, model_path, quiet=False)

    return model_path


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
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, pred)
    r2 = r2_score(y_test, pred)

    return round(mae, 2), round(r2, 3)


def show_image(path):
    if os.path.exists(path):
        st.image(path, use_container_width=True)
    else:
        st.warning(f"Missing file: {path}")


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(20, 184, 166, 0.18), transparent 34%),
        radial-gradient(circle at bottom right, rgba(249, 115, 22, 0.16), transparent 32%),
        linear-gradient(135deg, #020617 0%, #071a1a 48%, #020617 100%);
    color: #f8fafc;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617 0%, #062f2f 58%, #031313 100%);
    border-right: 1px solid rgba(45, 212, 191, 0.35);
    box-shadow: 8px 0 28px rgba(0,0,0,0.35);
}

.sidebar-title {
    padding: 22px 18px;
    border-radius: 22px;
    background: linear-gradient(135deg, rgba(15,23,42,0.92), rgba(13,148,136,0.22));
    border: 1px solid rgba(94,234,212,0.32);
    margin-bottom: 18px;
}

.sidebar-title h2 {
    margin: 0;
    color: #ccfbf1;
    font-size: 24px;
    font-weight: 800;
}

.sidebar-title p {
    margin-top: 6px;
    color: #94a3b8;
    font-size: 13px;
}

.hero {
    padding: 42px;
    border-radius: 30px;
    background:
        linear-gradient(135deg, rgba(15,23,42,0.92), rgba(6,95,70,0.64)),
        linear-gradient(45deg, rgba(14,165,233,0.12), transparent);
    border: 1px solid rgba(94,234,212,0.32);
    box-shadow: 0 0 52px rgba(45,212,191,0.16);
}

.hero h1 {
    font-size: 58px;
    line-height: 1.02;
    margin: 0;
    font-weight: 850;
    color: #ecfeff;
}

.hero p {
    color: #cbd5e1;
    font-size: 18px;
    max-width: 850px;
    margin-top: 14px;
}

.section-card {
    padding: 26px;
    border-radius: 24px;
    background: rgba(15,23,42,0.76);
    border: 1px solid rgba(148,163,184,0.24);
    box-shadow: 0 18px 48px rgba(0,0,0,0.24);
}

.metric-card-hot {
    padding: 24px;
    border-radius: 22px;
    background: linear-gradient(135deg, rgba(127,29,29,0.90), rgba(234,88,12,0.68));
    border: 1px solid rgba(251,146,60,0.45);
    box-shadow: 0 15px 38px rgba(234,88,12,0.18);
}

.metric-card-cool {
    padding: 24px;
    border-radius: 22px;
    background: linear-gradient(135deg, rgba(7,89,133,0.88), rgba(15,118,110,0.68));
    border: 1px solid rgba(125,211,252,0.36);
    box-shadow: 0 15px 38px rgba(14,165,233,0.14);
}

.metric-card-neutral {
    padding: 24px;
    border-radius: 22px;
    background: linear-gradient(135deg, rgba(15,23,42,0.88), rgba(8,47,73,0.72));
    border: 1px solid rgba(94,234,212,0.26);
}

.metric-card-hot h2,
.metric-card-cool h2,
.metric-card-neutral h2 {
    margin: 0;
    font-size: 34px;
    font-weight: 800;
    color: white;
}

.metric-card-hot p,
.metric-card-cool p,
.metric-card-neutral p {
    color: #d1d5db;
    margin: 8px 0 0 0;
    font-size: 14px;
}

.recommendation-card {
    padding: 18px 20px;
    margin-bottom: 14px;
    border-radius: 16px;
    background: rgba(15,23,42,0.78);
    border-left: 5px solid #14b8a6;
    border-top: 1px solid rgba(148,163,184,0.18);
    border-right: 1px solid rgba(148,163,184,0.18);
    border-bottom: 1px solid rgba(148,163,184,0.18);
}

.recommendation-card b {
    color: #ccfbf1;
    font-size: 16px;
}

.recommendation-card span {
    color: #cbd5e1;
    font-size: 14px;
}

div[data-testid="stMetric"] {
    background: rgba(15,23,42,0.76);
    border: 1px solid rgba(148,163,184,0.22);
    padding: 18px;
    border-radius: 18px;
}

hr {
    border-color: rgba(148,163,184,0.18);
}

.stDataFrame {
    border-radius: 18px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown("""
    <div class="sidebar-title">
        <h2>CoolScape AI</h2>
        <p>Urban heat intelligence platform</p>
    </div>
    """, unsafe_allow_html=True)

    city = st.selectbox(
        "City workspace",
        ["Delhi", "Mumbai", "Hyderabad", "Bengaluru"]
    )

    page = option_menu(
        menu_title=None,
        options=[
            "Command Center",
            "Heat Map",
            "Hot & Cool Regions",
            "Cooling Simulator",
            "AI Analytics"
        ],
        icons=[
            "speedometer2",
            "map",
            "geo-alt",
            "sliders",
            "bar-chart-line"
        ],
        default_index=0,
        styles={
            "container": {
                "background-color": "transparent",
                "padding": "0px"
            },
            "icon": {
                "color": "#5eead4",
                "font-size": "18px"
            },
            "nav-link": {
                "font-size": "15px",
                "margin": "8px 0",
                "border-radius": "14px",
                "padding": "12px",
                "color": "#d1fae5",
                "--hover-color": "rgba(20,184,166,.22)"
            },
            "nav-link-selected": {
                "background": "linear-gradient(90deg,#0f766e,#14b8a6)",
                "color": "white",
                "font-weight": "700"
            },
        }
    )

    st.markdown("---")
    st.caption("Satellite, weather and urban morphology data")


df = pd.read_csv(datasets[city])

model_path = download_model_if_missing(city)
model = joblib.load(model_path)

df = df.dropna().reset_index(drop=True)

df = df[
    (df["LST"] >= 20) &
    (df["LST"] <= 65)
].reset_index(drop=True)

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
    lambda r: "Increase green cover" if r["NDVI"] < 0.2 else "Maintain vegetation and monitor heat",
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

place_summary = place_summary.sort_values(
    "Avg_LST",
    ascending=False
).reset_index(drop=True)

hot_count = min(5, max(1, len(place_summary) // 2))
cool_count = min(5, max(1, len(place_summary) - hot_count))

top_hottest = place_summary.head(hot_count).copy().reset_index(drop=True)
top_hottest.insert(0, "Rank", range(1, len(top_hottest) + 1))

remaining_places = place_summary[
    ~place_summary["Place"].isin(top_hottest["Place"])
].copy()

top_coolest = remaining_places.sort_values(
    "Avg_LST",
    ascending=True
).head(cool_count).reset_index(drop=True)

top_coolest.insert(0, "Rank", range(1, len(top_coolest) + 1))

hottest_region = place_summary.sort_values(
    "Avg_LST",
    ascending=False
).iloc[0]

coolest_region = place_summary.sort_values(
    "Avg_LST",
    ascending=True
).iloc[0]

city_avg_temp = df["LST"].mean()
extreme_points = len(df[df["Risk"] == "Extreme"])
high_risk_percent = (len(df[df["Risk"].isin(["Very High", "Extreme"])]) / len(df)) * 100


if page == "Command Center":
    st.markdown(f"""
    <div class="hero">
        <h1>{city} Urban Heat Command Center</h1>
        <p>
        A decision-support dashboard for identifying heat-risk regions, explaining
        urban heat drivers, and simulating practical cooling interventions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    c1, c2, c3, c4 = st.columns(4)

    c1.markdown(f"""
    <div class="metric-card-hot">
        <h2>{hottest_region['Avg_LST']:.2f}°C</h2>
        <p>Hottest region: {hottest_region['Place']}</p>
    </div>
    """, unsafe_allow_html=True)

    c2.markdown(f"""
    <div class="metric-card-cool">
        <h2>{coolest_region['Avg_LST']:.2f}°C</h2>
        <p>Coolest region: {coolest_region['Place']}</p>
    </div>
    """, unsafe_allow_html=True)

    c3.markdown(f"""
    <div class="metric-card-neutral">
        <h2>{city_avg_temp:.2f}°C</h2>
        <p>Average surface temperature</p>
    </div>
    """, unsafe_allow_html=True)

    c4.markdown(f"""
    <div class="metric-card-neutral">
        <h2>{high_risk_percent:.1f}%</h2>
        <p>High-risk heat zones</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    c5, c6 = st.columns(2)

    with c5:
        st.markdown("""
        <div class="section-card">
            <h3>Model performance</h3>
            <p>The model estimates land surface temperature using vegetation,
            humidity, wind speed and building-density indicators.</p>
        </div>
        """, unsafe_allow_html=True)

        st.metric("Mean Absolute Error", f"{mae} °C")
        st.metric("R² Score", r2)

    with c6:
        st.markdown("""
        <div class="section-card">
            <h3>Planning use case</h3>
            <p>Use the heat map to identify vulnerable zones, then open the cooling
            simulator to compare practical interventions for each region.</p>
        </div>
        """, unsafe_allow_html=True)

        st.metric("Sample points analyzed", f"{len(df):,}")
        st.metric("Extreme heat points", f"{extreme_points:,}")


elif page == "Heat Map":
    st.title(f"{city} Interactive Heat Map")
    st.caption("Filter by temperature threshold and hover over points to inspect local heat conditions.")

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
            "BuildingDensity": True
        }
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.info(f"Showing {len(filtered):,} locations hotter than {threshold:.1f}°C.")


elif page == "Hot & Cool Regions":
    st.title(f"{city} Hot and Cool Region Ranking")
    st.caption("Regions are ranked using average LST to avoid misleading single-pixel extremes.")

    c1, c2 = st.columns(2)

    with c1:
        st.subheader(f"Top {len(top_hottest)} hottest regions")
        st.dataframe(
            top_hottest[
                [
                    "Rank",
                    "Place",
                    "Max_LST",
                    "Avg_LST",
                    "Avg_NDVI",
                    "Avg_BuildingDensity"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    with c2:
        st.subheader(f"Top {len(top_coolest)} coolest regions")
        st.dataframe(
            top_coolest[
                [
                    "Rank",
                    "Place",
                    "Min_LST",
                    "Avg_LST",
                    "Avg_NDVI",
                    "Avg_BuildingDensity"
                ]
            ],
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

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white"
    )

    st.plotly_chart(fig, use_container_width=True)


elif page == "Cooling Simulator":
    st.title(f"{city} Cooling Intervention Simulator")
    st.caption("Compare multiple mitigation strategies for a selected hotspot region.")

    selected_place = st.selectbox(
        "Select region",
        sorted(df["Place"].unique())
    )

    place_df = df[df["Place"] == selected_place]
    hotspot = place_df.sort_values("LST", ascending=False).iloc[0]

    left, right = st.columns([1, 1])

    with left:
        st.markdown("""
        <div class="section-card">
            <h3>Scenario controls</h3>
            <p>Adjust the intervention intensity and compare predicted cooling impacts.</p>
        </div>
        """, unsafe_allow_html=True)

        ndvi_increase = st.slider("Vegetation increase (%)", 0, 60, 20)
        building_reduction = st.slider("Built-up density reduction (%)", 0, 60, 20)

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

    with right:
        st.markdown("""
        <div class="section-card">
            <h3>Selected hotspot profile</h3>
            <p>The simulator uses the hottest sampled point within the selected region.</p>
        </div>
        """, unsafe_allow_html=True)

        st.dataframe(
            hotspot[
                [
                    "Place",
                    "Latitude",
                    "Longitude",
                    "LST",
                    "NDVI",
                    "Humidity",
                    "WindSpeed",
                    "BuildingDensity"
                ]
            ].to_frame().T,
            use_container_width=True
        )

    st.write("")

    a, b, c = st.columns(3)

    a.metric("Current predicted temperature", f"{current_temp:.2f} °C")
    b.metric("Vegetation scenario", f"{green_temp:.2f} °C", f"-{veg_cooling:.2f} °C")
    c.metric("Built-up density scenario", f"{building_temp:.2f} °C", f"-{building_cooling:.2f} °C")

    recommendations = []

    if hotspot["NDVI"] < 0.25:
        recommendations.append(
            ("Urban Forestry and Tree Plantation", veg_cooling)
        )

    if hotspot["BuildingDensity"] > 800:
        recommendations.append(
            ("Cool Roof Implementation", max(building_cooling, 0.35))
        )

    if hotspot["BuildingDensity"] > 1200:
        recommendations.append(
            ("Green Roof Development", max(building_cooling * 0.9, 0.30))
        )

    if hotspot["WindSpeed"] < 2:
        recommendations.append(
            ("Urban Ventilation Corridor Planning", 0.80)
        )

    if hotspot["NDVI"] < 0.15:
        recommendations.append(
            ("Pocket Parks and Roadside Green Buffers", max(veg_cooling * 0.7, 0.50))
        )

    recommendations = sorted(
        recommendations,
        key=lambda item: item[1],
        reverse=True
    )

    st.subheader("Recommended Cooling Strategies")

    if len(recommendations) == 0:
        st.info("No major intervention required for this sampled condition.")
    else:
        for rank, (strategy, impact) in enumerate(recommendations[:5], start=1):
            st.markdown(
                f"""
                <div class="recommendation-card">
                    <b>{rank}. {strategy}</b><br>
                    <span>Estimated cooling potential: {impact:.2f} °C</span>
                </div>
                """,
                unsafe_allow_html=True
            )


elif page == "AI Analytics":
    st.title(f"{city} AI Analytics")
    st.caption("Model interpretation outputs used to understand heat-driving factors.")

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