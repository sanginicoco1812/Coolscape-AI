import { useEffect, useState } from "react";
function App() {
  const [ndvi, setNdvi] = useState("");
  const [humidity, setHumidity] = useState("");
  const [windSpeed, setWindSpeed] = useState("");
  const [buildingDensity, setBuildingDensity] = useState("");
  const [city, setCity] = useState("Delhi");
  const [temperature, setTemperature] = useState(null);
  const [riskLevel, setRiskLevel] = useState("");
  const [aiFactors, setAiFactors] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [coolingIndex, setCoolingIndex] = useState(null);
  const [confidence, setConfidence] = useState(null);
  const [predictionMode, setPredictionMode] = useState("");
  const [placeSearch, setPlaceSearch] = useState("");
  const [heatThreshold, setHeatThreshold] = useState(40);
  const [isScanning, setIsScanning] = useState(false); // Add this line
  const [showBreakingNews, setShowBreakingNews] = useState(true);

  useEffect(() => {
    if (!window.matchMedia("(pointer: fine)").matches) return undefined;

    const root = document.documentElement;
    let cursorX = window.innerWidth / 2;
    let cursorY = window.innerHeight / 2;
    let outlineX = cursorX;
    let outlineY = cursorY;
    let animationFrame;

    const updatePosition = (event) => {
      cursorX = event.clientX;
      cursorY = event.clientY;
      root.style.setProperty("--cursor-x", `${cursorX}px`);
      root.style.setProperty("--cursor-y", `${cursorY}px`);
    };

    const animateOutline = () => {
      outlineX += (cursorX - outlineX) * 0.18;
      outlineY += (cursorY - outlineY) * 0.18;
      root.style.setProperty("--cursor-outline-x", `${outlineX}px`);
      root.style.setProperty("--cursor-outline-y", `${outlineY}px`);
      animationFrame = requestAnimationFrame(animateOutline);
    };

    const setHoverState = (event) => {
      if (
        event.target.closest(
          "button, a, input, select, textarea, iframe, .card-hover, .dock-hover"
        )
      ) {
        root.classList.add("cursor-hovering");
      } else {
        root.classList.remove("cursor-hovering");
      }
    };

    root.classList.add("mission-cursor-enabled");
    root.style.setProperty("--cursor-x", `${cursorX}px`);
    root.style.setProperty("--cursor-y", `${cursorY}px`);
    root.style.setProperty("--cursor-outline-x", `${outlineX}px`);
    root.style.setProperty("--cursor-outline-y", `${outlineY}px`);

    window.addEventListener("mousemove", updatePosition);
    window.addEventListener("mouseover", setHoverState);
    animationFrame = requestAnimationFrame(animateOutline);

    return () => {
      root.classList.remove("mission-cursor-enabled", "cursor-hovering");
      window.removeEventListener("mousemove", updatePosition);
      window.removeEventListener("mouseover", setHoverState);
      cancelAnimationFrame(animationFrame);
    };
  }, []);

  const heatmapFiles = {
    Delhi: {
      type: "html",
      src: "/heatmaps/delhi_heatmap.html",
    },
    Mumbai: {
      type: "html",
      src: "/heatmaps/mumbai_heatmap.html",
    },
    Hyderabad: {
      type: "html",
      src: "/heatmaps/hyderabad_heatmap.html",
    },
    Bengaluru: {
      type: "html",
      src: "/heatmaps/bengaluru_heatmap.html",
    },
  };
	  const placeHeatIndex = {
    Delhi: [
      { name: "Dwarka", risk: "High", temperature: 40.8, focus: "Cool roofs and shaded transit edges" },
      { name: "Rohini", risk: "Very High", temperature: 42.4, focus: "Tree-cover expansion and reflective pavements" },
      { name: "Saket", risk: "Moderate", temperature: 37.6, focus: "Pocket parks and pedestrian shade" },
      { name: "Noida", risk: "High", temperature: 41.2, focus: "Green buffers around dense commercial corridors" },
      { name: "Gurugram", risk: "Very High", temperature: 42.8, focus: "Cool roofs and urban ventilation corridors" },
      { name: "Faridabad", risk: "High", temperature: 40.9, focus: "Industrial shade and surface cooling" },
      { name: "Ghaziabad", risk: "Very High", temperature: 42.1, focus: "Reflective pavements and roadside canopy" },
      { name: "Central Delhi", risk: "High", temperature: 40.4, focus: "Tree canopy protection near civic zones" },
      { name: "Okhla", risk: "Very High", temperature: 42.6, focus: "Industrial cool roofing and heat-safe work zones" },
      { name: "Bahadurgarh", risk: "High", temperature: 40.2, focus: "Green buffers along built-up edges" },
    ],
    Mumbai: [
      { name: "South Mumbai", risk: "Moderate", temperature: 36.5, focus: "Coastal ventilation and shaded walkways" },
      { name: "Bandra", risk: "High", temperature: 38.8, focus: "Humidity-sensitive shade and street trees" },
      { name: "Andheri", risk: "Very High", temperature: 40.7, focus: "Cool roofs around dense transit corridors" },
      { name: "Borivali", risk: "Moderate", temperature: 36.9, focus: "Canopy continuity near residential edges" },
      { name: "Thane", risk: "High", temperature: 39.4, focus: "Lake-edge cooling and open-space protection" },
      { name: "Navi Mumbai", risk: "High", temperature: 38.9, focus: "Ventilation corridors and shaded public routes" },
      { name: "Chembur", risk: "Very High", temperature: 40.5, focus: "Industrial heat mitigation and reflective surfaces" },
      { name: "Powai", risk: "Moderate", temperature: 37.2, focus: "Lake cooling protection and green buffers" },
      { name: "Malad", risk: "High", temperature: 38.6, focus: "Pedestrian shade and humidity-aware planning" },
      { name: "Worli", risk: "Moderate", temperature: 36.7, focus: "Coastal airflow preservation" },
      { name: "Dadar", risk: "High", temperature: 38.4, focus: "Shaded station-area movement corridors" },
      { name: "Kurla", risk: "Very High", temperature: 40.9, focus: "Cool roofs and low-albedo surface replacement" },
    ],
    Hyderabad: [
      { name: "Charminar", risk: "High", temperature: 39.7, focus: "Shaded heritage walkways and cool pavements" },
      { name: "Secunderabad", risk: "High", temperature: 39.4, focus: "Station-area shade and ventilation corridors" },
      { name: "HITEC City", risk: "Very High", temperature: 41.1, focus: "Green IT corridors and cool roofs" },
      { name: "Gachibowli", risk: "High", temperature: 39.9, focus: "Corporate campus tree buffers" },
      { name: "Madhapur", risk: "Very High", temperature: 41.3, focus: "Cool roofs and reflective parking surfaces" },
      { name: "Kukatpally", risk: "High", temperature: 40.1, focus: "Residential canopy and surface cooling" },
      { name: "Banjara Hills", risk: "Moderate", temperature: 37.8, focus: "Canopy preservation and slope ventilation" },
      { name: "Begumpet", risk: "High", temperature: 39.2, focus: "Roadside trees and shaded public access" },
      { name: "LB Nagar", risk: "Very High", temperature: 41.6, focus: "Green corridors and road heat mitigation" },
      { name: "Shamshabad", risk: "High", temperature: 40.0, focus: "Heat-safe airport approach corridors" },
      { name: "Uppal", risk: "High", temperature: 39.8, focus: "Lake restoration and canopy stitching" },
      { name: "Mehdipatnam", risk: "Moderate", temperature: 37.9, focus: "Shaded pedestrian routes" },
    ],
    Bengaluru: [
      { name: "MG Road", risk: "High", temperature: 38.7, focus: "Street trees and shaded commercial walking routes" },
      { name: "Whitefield", risk: "Very High", temperature: 40.8, focus: "Green IT corridors and cool roofs" },
      { name: "Electronic City", risk: "Very High", temperature: 40.5, focus: "Campus canopy and ventilation corridors" },
      { name: "Koramangala", risk: "High", temperature: 38.9, focus: "Tree canopy protection and cool pavements" },
      { name: "Indiranagar", risk: "High", temperature: 38.4, focus: "Street shade and surface cooling" },
      { name: "Hebbal", risk: "Moderate", temperature: 36.8, focus: "Lake ventilation and green buffers" },
      { name: "Yelahanka", risk: "Moderate", temperature: 36.5, focus: "Canopy protection near growth edges" },
      { name: "Jayanagar", risk: "Moderate", temperature: 36.9, focus: "Preserve mature tree cover" },
      { name: "Marathahalli", risk: "Very High", temperature: 40.2, focus: "IT corridor cooling and traffic-edge shade" },
      { name: "Kengeri", risk: "Moderate", temperature: 36.7, focus: "Green buffers along expansion zones" },
      { name: "HSR Layout", risk: "High", temperature: 38.5, focus: "Neighborhood canopy and cool rooftops" },
      { name: "Rajajinagar", risk: "High", temperature: 38.8, focus: "Built-density cooling and shaded markets" },
	    ],
	  };
	  const searchedPlaces = placeHeatIndex[city].filter((place) =>
	    place.name.toLowerCase().includes(placeSearch.trim().toLowerCase())
	  );
	  const thresholdPlaces = searchedPlaces.filter(
	    (place) => place.temperature >= heatThreshold
	  );
	  const visiblePlaces = placeSearch.trim()
	    ? thresholdPlaces
	    : thresholdPlaces.slice(0, 6);
	  const thresholdCount = thresholdPlaces.length;
	  const hottestVisiblePlace = [...visiblePlaces].sort((a, b) => b.temperature - a.temperature)[0];
	  const coolingEngineMode =
	    coolingIndex === null
	      ? "Awaiting Prediction"
	      : coolingIndex >= 70
	      ? "Preserve Cooling Assets"
	      : coolingIndex >= 45
	      ? "Targeted Cooling Required"
	      : "Critical Cooling Intervention";
	  const coolingEngineColor =
	    coolingIndex === null
	      ? "#94a3b8"
	      : coolingIndex >= 70
	      ? "#22c55e"
	      : coolingIndex >= 45
	      ? "#f97316"
	      : "#ef4444";
	  const landsatCityStats = {
	    Delhi: { samples: 1200, avgNdvi: 0.276, avgLst: 41.21, maxLst: 51.37 },
	    Mumbai: { samples: 1200, avgNdvi: 0.181, avgLst: 37.48, maxLst: 52.24 },
	    Hyderabad: { samples: 1200, avgNdvi: 0.363, avgLst: 41.13, maxLst: 49.87 },
	    Bengaluru: { samples: 1200, avgNdvi: 0.408, avgLst: 37.67, maxLst: 45.1 },
	  };
	  const activeLandsatStats = landsatCityStats[city];
	  const satelliteDataCards = [
	    {
	      label: "Satellite Source",
	      value: "Landsat 8/9",
	      detail: "Collection 2 Level 2",
	      color: "#38bdf8",
	    },
	    {
	      label: "Data Window",
	      value: "Apr-Jun 2025",
	      detail: "NDVI + LST composite",
	      color: "#86efac",
	    },
	    {
	      label: "Pipeline Status",
	      value: "CSV Exported",
	      detail: "Local dataset available",
	      color: "#fdba74",
	    },
	  ];
	  const clamp = (value, min, max) => Math.min(Math.max(value, min), max);
  const hasInputData =
  ndvi !== "" || humidity !== "" || windSpeed !== "" || buildingDensity !== "";
  const liveNdvi = Number(ndvi) || 0;
  const liveHumidity = Number(humidity) || 0;
  const liveWind = Number(windSpeed) || 0;
  const liveDensity = Number(buildingDensity) || 0;
  const livePredictedTemp = 35 - liveNdvi * 5 - liveHumidity * 0.03 - liveWind * 0.08 + liveDensity * 0.12;
  const activeTemperature = temperature !== null ? Number(temperature) : hasInputData ? livePredictedTemp : null;
  const rawFeatureScores = {
    ndvi: Math.max(8, 100 - clamp(liveNdvi * 100, 0, 100)),
    humidity: Math.max(8, clamp(liveHumidity, 0, 100)),
    wind: Math.max(8, 100 - clamp(liveWind * 4, 0, 100)),
    density: Math.max(8, clamp(liveDensity, 0, 100)),
  };
  const totalFeatureScore =
  rawFeatureScores.ndvi +
  rawFeatureScores.humidity +
  rawFeatureScores.wind +
  rawFeatureScores.density;
  const featureWeights = hasInputData? {
    ndvi: Math.round((rawFeatureScores.ndvi / totalFeatureScore) * 100),
    humidity: Math.round((rawFeatureScores.humidity / totalFeatureScore) * 100),
    wind: Math.round((rawFeatureScores.wind / totalFeatureScore) * 100),
    density: Math.round((rawFeatureScores.density / totalFeatureScore) * 100),
  }
  : {
      ndvi: 45,
      humidity: 30,
      wind: 15,
      density: 10,
    };
    const thermalPosition = activeTemperature === null? 52
    : clamp(((activeTemperature - 28) / 18) * 100, 6, 94);
    const thermalStatus =
    activeTemperature === null
    ? "Awaiting Input"
    : activeTemperature >= 40
    ? "Critical Thermal Anomaly"
    : activeTemperature >= 35
    ? "Moderate Radiation"
    : "Cool Green Zone";
    const thermalStatusColor =  activeTemperature === null
    ? "#94a3b8"
    : activeTemperature >= 40
    ? "#ef4444"
    : activeTemperature >= 35
    ? "#f97316"
    : "#22c55e";

    const cityRecommendations = {
      Delhi: ["Expand tree cover in heat-stressed corridors", "Deploy cool roofs on dense built-up blocks", "Use reflective pavements near high-footfall zones"],
      Mumbai: ["Protect coastal ventilation corridors", "Build shaded walkways around transit zones", "Use humidity-sensitive planning for dense neighborhoods"],
      Hyderabad: ["Restore lake-edge cooling buffers", "Connect green corridors across hot zones", "Scale cool roofs in IT and residential clusters"],
      Bengaluru: ["Protect mature tree canopy", "Create green IT corridors", "Preserve ventilation corridors across dense growth areas"],
    };

    const getRiskLevel = (value) => {
      if (value >= 45) return "Extreme";
      if (value >= 40) return "High";
      if (value >= 35) return "Moderate";
      return "Low";
    };

    const buildFallbackPrediction = () => {
      const ndviValue = clamp(Number(ndvi) || activeLandsatStats.avgNdvi, 0, 1);
      const humidityValue = clamp(Number(humidity) || 62, 0, 100);
      const windValue = clamp(Number(windSpeed) || 8, 0, 40);
      const densityValue = clamp(Number(buildingDensity) || 70, 0, 100);
      const baseTemp = activeLandsatStats.avgLst;
      const predicted = clamp(
        baseTemp + densityValue * 0.045 + humidityValue * 0.018 - windValue * 0.08 - ndviValue * 4.2,
        28,
        52
      );
      const fallbackCoolingIndex = Math.round(
        clamp(
          ndviValue * 42 + windValue * 1.3 + (100 - densityValue) * 0.28 + (100 - humidityValue) * 0.12 + (52 - predicted) * 1.15,
          0,
          100
        )
      );
      const fallbackFactors = [];

      if (ndviValue < 0.25) fallbackFactors.push("Low NDVI indicates limited vegetation cooling capacity.");
      if (densityValue > 70) fallbackFactors.push("High building density can trap heat and reduce surface cooling.");
      if (windValue < 8) fallbackFactors.push("Low wind speed weakens natural ventilation.");
      if (humidityValue > 70) fallbackFactors.push("High humidity can increase perceived heat stress.");
      if (predicted >= 40) fallbackFactors.push("High predicted surface temperature indicates a priority heat-risk zone.");
      if (fallbackFactors.length === 0) fallbackFactors.push("Inputs show a comparatively balanced thermal profile for this city.");

      return {
        temperature: predicted.toFixed(1),
        risk: getRiskLevel(predicted),
        coolingIndex: fallbackCoolingIndex,
        confidence: 82,
        factors: fallbackFactors,
        recommendations: cityRecommendations[city] || cityRecommendations.Delhi,
      };
    };

    async function handlePrediction() {
      setIsScanning(true);
    
    try {
      const configuredApiUrl = import.meta.env.VITE_API_URL;
      const isLocalFrontend = ["localhost", "127.0.0.1"].includes(window.location.hostname);

      if (!configuredApiUrl && !isLocalFrontend) {
        throw new Error("Public frontend is running without a hosted backend API.");
      }

      const apiBaseUrl = configuredApiUrl || "http://127.0.0.1:8000";
      const response = await fetch(`${apiBaseUrl}/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          city: city,
          ndvi: Number(ndvi),
          humidity: Number(humidity),
          windSpeed: Number(windSpeed),
          buildingDensity: Number(buildingDensity),
        }),
      });

    const data = await response.json();

    if (!response.ok || data.status !== "success") {
      throw new Error(data.message || "Prediction request failed");
    }

    const roundedTemp = Number(data.temperature).toFixed(1);

    setTemperature(roundedTemp);
    setRiskLevel(data.risk);
    setAiFactors(data.factors || []);
    setRecommendations(data.recommendations || []);
    setCoolingIndex(data.coolingIndex ?? null);
    setConfidence(data.confidence ?? null);
    setPredictionMode("api");
   } catch (error) {
    console.error("Prediction failed:", error);
    const fallback = buildFallbackPrediction();
    setTemperature(fallback.temperature);
    setRiskLevel(fallback.risk);
    setAiFactors(fallback.factors);
    setRecommendations(fallback.recommendations);
    setCoolingIndex(fallback.coolingIndex);
    setConfidence(fallback.confidence);
    setPredictionMode("demo");
   } finally {
    setIsScanning(false);
   }
}
  // ================= MAIN APP LAYOUT =================

  return (
  <div
    className="app-shell"
    style={{
      minHeight: "100vh",
      padding: "24px",
      fontFamily: "'Plus Jakarta Sans', sans-serif",
      color: "#f8fafc",
      position: "relative"
    }}
  >
    {isScanning && <div className="scanning-overlay"></div>}
    {showBreakingNews && (
      <div className="breaking-news-overlay" role="dialog" aria-modal="true" aria-label="Breaking news">
        <div className="breaking-news-card">
          <div className="breaking-news-kicker">
            <span className="breaking-news-pulse"></span>
            Breaking News
          </div>
          <h2>ISRO Hackathon Mission Console Activated</h2>
          <p>
            HEATSHIELD INDIA is now visualizing Landsat 8/9 April-June 2025 satellite samples for urban heat intelligence across Indian cities.
          </p>
          <div className="breaking-news-meta">
            <span>Earth Observation Layer Online</span>
            <span>NDVI + LST Exported</span>
            <span>Team 404 Brain Not Found</span>
          </div>
          <button
            className="dock-hover"
            type="button"
            onClick={() => setShowBreakingNews(false)}
          >
            Enter Dashboard
          </button>
        </div>
      </div>
    )}
    <div className="cursor-dot"></div>
    <div className="cursor-outline"></div>
    <div className="thermal-backdrop" aria-hidden="true"></div>
    <aside className="side-quick-nav" aria-label="Section quick navigation">
      {[
        { label: "Home", target: "home" },
        { label: "Prediction", target: "prediction" },
        { label: "Heatmap", target: "heatmap" },
        { label: "Insights", target: "insights" },
        { label: "About", target: "about" },
      ].map((item) => (
        <button
          key={item.label}
          className="quick-nav-dot"
          type="button"
          aria-label={item.label}
          onClick={() => {
            if (item.target === "home") {
              window.scrollTo({ top: 0, behavior: "smooth" });
              return;
            }
            document.getElementById(item.target)?.scrollIntoView({ behavior: "smooth" });
          }}
        >
          <span className="quick-nav-label">{item.label}</span>
        </button>
      ))}
    </aside>

    {/* ================= PAGE BACKGROUND WRAPPER ================= ^ */}

    <div className="top-marquee-band" aria-label="HeatShield India mission updates">
      <div className="top-marquee-track">
        {[...Array(2)].map((_, loopIndex) => (
          <div className="top-marquee-content" key={loopIndex} aria-hidden={loopIndex === 1}>
            <span>ISRO Hackathon 2026</span>
            <strong>HEATSHIELD INDIA mission console is live</strong>
            <span>Landsat 8/9 Apr-Jun 2025 NDVI + LST exported</span>
            <strong>Urban cooling intelligence for Delhi, Mumbai, Hyderabad, Bengaluru</strong>
            <span>Team 404 Brain Not Found</span>
          </div>
        ))}
      </div>
    </div>

    {/* ================= NAVBAR SECTION ================= */}
  <nav
  className="main-nav"
  style={{
    maxWidth: "1200px",
    margin: "0 auto 40px",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "16px 24px",
    border: "1px solid rgba(255, 255, 255, 0.05)",
    borderRadius: "12px",
    backgroundColor: "rgba(15, 23, 42, 0.4)",
    backdropFilter: "blur(16px)",
    boxShadow: "0 4px 30px rgba(0, 0, 0, 0.4)",
  }}
>
  {/* The "Lightning" Scan Line */}
  
  <div
    style={{
      position: "fixed",
      top: 0,
      left: 0,
      width: "100%",
      height: "2px",
      background: "linear-gradient(90deg, transparent, rgba(249, 115, 22, 0.5), transparent)",
      zIndex: 0,
      animation: "scanline 8s linear infinite"
    }}
  ></div>

  <style>
    {`
      @keyframes scanline {
        0% { transform: translateY(-100vh); }
        100% { transform: translateY(100vh); }
      }
    `}
  </style>
  <div
  className="brand-mark"
  style={{
    fontSize: "15px",
    fontWeight: "800",
    letterSpacing: "1.5px",
    fontFamily: "'Orbitron', sans-serif",
    color: "#ffffff",
  }}
>
  HEATSHIELD <span style={{ color: "#f97316" }}>INDIA</span>
</div>

  <div
    className="nav-menu"
    style={{
      display: "flex",
      gap: "24px",
      color: "#cbd5e1",
      fontSize: "14px",
    }}
  >
    <span
    className="dock-hover"
  style={navLinkStyle}
  onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
>
  Home
</span>
<span
className="dock-hover"
  style={navLinkStyle}
  onClick={() =>
    document.getElementById("prediction").scrollIntoView({ behavior: "smooth" })
  }
>
  Prediction
</span>
<span
  className="dock-hover"
  style={navLinkStyle}
  onClick={() =>
    document.getElementById("heatmap").scrollIntoView({ behavior: "smooth" })
  }
>
  Heatmap
</span>
<span
  className="dock-hover"
  style={navLinkStyle}
  onClick={() =>
    document.getElementById("insights").scrollIntoView({ behavior: "smooth" })
  }
>
  Insights
</span>
<span
  className="dock-hover"
  style={navLinkStyle}
  onClick={() =>
    document.getElementById("about").scrollIntoView({ behavior: "smooth" })
  }
>
  About
</span>
  </div>
  </nav>
{/* ================= HERO SECTION ================= */}
      <section
  className="hero-section"
  style={{
    maxWidth: "1180px",
    margin: "0 auto 56px",
    display: "grid",
    gridTemplateColumns: "1.05fr 0.95fr",
    gap: "40px",
    alignItems: "center",
  }}
>
  
  <div className="hero-copy">
    <div className="home-news-headline">
      <span>ISRO Hackathon 2026</span>
      <strong>Satellite-powered urban heat risk dashboard for climate-resilient Indian cities</strong>
    </div>
    <p
  style={{
    color: "#f97316",
    fontSize: "11px",
    fontWeight: "700",
    marginBottom: "12px",
    textTransform: "uppercase",
    letterSpacing: "1.5px",
    fontFamily: "'Orbitron', sans-serif",
  }}
>
  AI Climate Analytics Engine
</p>

<h1
  style={{
    color: "#f8fafc",
    fontSize: "42px",
    fontWeight: "800",
    letterSpacing: "-0.5px",
    lineHeight: "1.2",
    marginBottom: "16px",
    maxWidth: "800px",
    marginLeft: "auto",
    marginRight: "auto",
    textAlign: "center"
  }}
>
  Physics-Informed Urban Thermal Analysis
</h1>

<p
  style={{
    fontSize: "14px",
    color: "#94a3b8",
    maxWidth: "680px",
    lineHeight: "1.6",
    marginBottom: "32px",
    marginLeft: "auto",
    marginRight: "auto",
    textAlign: "center"
  }}
>
  Synthesizing satellite Earth-observation telemetry, relative humidity configurations, and surface friction indices to map real-time microclimate anomalies.
</p>

    <div style={{ display: "flex", gap: "12px", flexWrap: "wrap", justifyContent: "center" }}>
  <button
  className="dock-hover"
    onClick={() => document.getElementById("prediction").scrollIntoView({ behavior: "smooth" })}
    style={{
      padding: "12px 20px",
      fontSize: "13px",
      fontWeight: "700",
      letterSpacing: "0.5px",
      backgroundColor: "#f97316",
      color: "white",
      border: "none",
      borderRadius: "6px",
      cursor: "pointer",
      boxShadow: "0 4px 20px rgba(249,115,22,0.25)",
      transition: "transform 0.2s ease, opacity 0.2s ease",
    }}
  >
    LAUNCH CONSOLE SIMULATOR
  </button>

  <button
  className="dock-hover"
    onClick={() => document.getElementById("heatmap").scrollIntoView({ behavior: "smooth" })}
    style={{
      padding: "12px 20px",
      fontSize: "13px",
      fontWeight: "700",
      letterSpacing: "0.5px",
      backgroundColor: "rgba(255,255,255,0.03)",
      color: "#e2e8f0",
      border: "1px solid rgba(255,255,255,0.08)",
      borderRadius: "6px",
      cursor: "pointer",
      transition: "background 0.2s ease",
    }}
  >
    VIEW RADIATIVE MAPS
  </button>
</div>
  </div>
{/* Hero visual: India heat index graphic */}
  <div
  className="float-hero"
  style={{
    position: "relative",
    minHeight: "380px",
      borderRadius: "28px",
      background:
        "radial-gradient(circle at center, rgba(34,197,94,0.28), transparent 35%), linear-gradient(145deg, rgba(15,23,42,0.8), rgba(15,23,42,0.35))",
      border: "1px solid rgba(255,255,255,0.12)",
      boxShadow: "0 30px 80px rgba(0,0,0,0.35)",
      overflow: "hidden",
    }}
  >
    <div
      style={{
        position: "absolute",
        width: "260px",
        height: "260px",
        borderRadius: "50%",
        left: "50%",
        top: "50%",
        transform: "translate(-50%, -50%)",
        background:
          "radial-gradient(circle at 35% 30%, #bbf7d0, #22c55e 28%, #166534 48%, #052e16 72%)",
        boxShadow:
          "0 0 50px rgba(34,197,94,0.55), inset -35px -25px 45px rgba(0,0,0,0.45)",
      }}
    ></div>
        <div
      style={{
        position: "absolute",
        top: "42px",
        left: "32px",
        color: "#86efac",
        fontSize: "13px",
        letterSpacing: "1.6px",
        textTransform: "uppercase",
        fontWeight: "bold",
      }}
    >
      India Heat Index
    </div>

    <div style={{ ...hotspotStyle, top: "35%", left: "62%" }}></div>
<div style={{ ...cityLabelStyle, top: "32%", left: "65%" }}>Delhi</div>

<div style={{ ...hotspotStyle, top: "48%", left: "43%" }}></div>
<div style={{ ...cityLabelStyle, top: "45%", left: "32%" }}>Ahmedabad</div>

<div style={{ ...hotspotStyle, top: "61%", left: "58%" }}></div>
<div style={{ ...cityLabelStyle, top: "58%", left: "61%" }}>Hyderabad</div>

<div style={{ ...hotspotStyle, top: "72%", left: "45%" }}></div>
<div style={{ ...cityLabelStyle, top: "69%", left: "35%" }}>Mumbai</div>

    <div
      style={{
        position: "absolute",
        left: "28px",
        bottom: "10px",
        backgroundColor: "rgba(2,6,23,0.72)",
        border: "1px solid rgba(255,255,255,0.12)",
        borderRadius: "18px",
        padding: "16px",
        color: "#e2e8f0",
      }}
    >
      <p style={{ margin: "0 0 6px", color: "#f97316", fontWeight: "bold" }}>
        Heat Risk Scan
      </p>
      <p style={{ margin: 0, fontSize: "14px", color: "#cbd5e1" }}>
        Delhi • Ahmedabad • Hyderabad • Mumbai
      </p>
    </div>
  </div>
</section>
{/* ================= DASHBOARD METRIC CARDS SECTION ================= */}
      <div
  className="metric-grid"
  style={{
    display: "grid",
    gap: "16px",
    maxWidth: "1200px",
    margin: "40px auto 40px",
  }}
>
  {/* CARD 1: NDVI */}
  <div className="card-hover animate-card" style={{
     backgroundColor: "rgba(15, 23, 42, 0.4)", border: "1px solid rgba(255, 255, 255, 0.04)", padding: "24px", borderRadius: "12px", position: "relative" }}>
    <h3 style={{ margin: "0 0 4px 0", fontSize: "12px", color: "#94a3b8", letterSpacing: "1px", textTransform: "uppercase" }}>NDVI Telemetry</h3>
    <p style={{ fontSize: "36px", fontWeight: "700", margin: "6px 0", color: "#22c55e" }}>0.42</p>
    <span style={{ fontSize: "11px", color: "#64748b" }}>Vegetation Density Index</span>
  </div>

  {/* CARD 2: HUMIDITY */}
  <div className="card-hover animate-card" style={{
     backgroundColor: "rgba(15, 23, 42, 0.4)", border: "1px solid rgba(255, 255, 255, 0.04)", padding: "24px", borderRadius: "12px", position: "relative" }}>
    <h3 style={{ margin: "0 0 4px 0", fontSize: "12px", color: "#94a3b8", letterSpacing: "1px", textTransform: "uppercase" }}>Relative Humidity</h3>
    <p style={{ fontSize: "36px", fontWeight: "700", margin: "6px 0", color: "#3b82f6" }}>68%</p>
    <span style={{ fontSize: "11px", color: "#64748b" }}>Atmospheric Moisture</span>
  </div>

  {/* CARD 3: WIND SPEED */}
  <div className="card-hover animate-card" style={{
     backgroundColor: "rgba(15, 23, 42, 0.4)", border: "1px solid rgba(255, 255, 255, 0.04)", padding: "24px", borderRadius: "12px", position: "relative" }}>
    <h3 style={{ margin: "0 0 4px 0", fontSize: "12px", color: "#94a3b8", letterSpacing: "1px", textTransform: "uppercase" }}>Wind Velocity</h3>
    <p style={{ fontSize: "36px", fontWeight: "700", margin: "6px 0", color: "#a855f7" }}>12 <span style={{ fontSize: "16px", color: "#64748b" }}>km/h</span></p>
    <span style={{ fontSize: "11px", color: "#64748b" }}>Surface Ventilation Vector</span>
  </div>

  {/* CARD 4: PREDICTED TEMPERATURE */}
  <div className="card-hover animate-card" style={{
     backgroundColor: "rgba(15, 23, 42, 0.4)", border: "1px solid rgba(255, 255, 255, 0.04)", padding: "24px", borderRadius: "12px", position: "relative" }}>
    <h3 style={{ margin: "0 0 4px 0", fontSize: "12px", color: "#94a3b8", letterSpacing: "1px", textTransform: "uppercase" }}>Computed Thermal</h3>
    <p style={{ fontSize: "36px", fontWeight: "700", margin: "6px 0", color: temperature ? "#fb7185" : "#475569" }}>
      {temperature !== null ? `${temperature}°C` : "--"}
    </p>
    <span style={{ fontSize: "11px", color: "#64748b" }}>Target Output Level</span>
  </div>

  {/* CARD 5: URBAN COOLING INDEX */}
  <div className="card-hover animate-card" style={{
     backgroundColor: "rgba(15, 23, 42, 0.4)", border: "1px solid rgba(34, 197, 94, 0.16)", padding: "24px", borderRadius: "12px", position: "relative" }}>
    <h3 style={{ margin: "0 0 4px 0", fontSize: "12px", color: "#94a3b8", letterSpacing: "1px", textTransform: "uppercase" }}>Urban Cooling Index</h3>
    <p style={{ fontSize: "36px", fontWeight: "700", margin: "6px 0", color: coolingIndex !== null ? "#86efac" : "#475569" }}>
      {coolingIndex !== null ? coolingIndex : "--"}
    </p>
    <span style={{ fontSize: "11px", color: "#64748b" }}>0-100 cooling resilience score</span>
  </div>

  {/* CARD 6: AI CONFIDENCE */}
  <div className="card-hover animate-card" style={{
     backgroundColor: "rgba(15, 23, 42, 0.4)", border: "1px solid rgba(249, 115, 22, 0.18)", padding: "24px", borderRadius: "12px", position: "relative" }}>
    <h3 style={{ margin: "0 0 4px 0", fontSize: "12px", color: "#94a3b8", letterSpacing: "1px", textTransform: "uppercase" }}>AI Confidence</h3>
    <p style={{ fontSize: "36px", fontWeight: "700", margin: "6px 0", color: confidence !== null ? "#fdba74" : "#475569" }}>
      {confidence !== null ? `${confidence}%` : "--"}
    </p>
    <span style={{ fontSize: "11px", color: "#64748b" }}>Input reliability and model fit</span>
  </div>
</div>


{/* ================= PREDICTION CONTROL PANEL SECTION ================= */}

      <div
  id="prediction"
  style={{
    maxWidth: "700px",
    margin: "0 auto 40px",
    padding: "28px",
    borderRadius: "16px",
    backgroundColor: "rgba(11, 17, 32, 0.7)",
    border: "1px solid rgba(255, 255, 255, 0.05)",
    boxShadow: "0 8px 32px rgba(0, 0, 0, 0.3)",
  }}
>
  <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "20px" }}>
    <span style={{ width: "8px", height: "8px", backgroundColor: "#f97316", borderRadius: "50%" }}></span>
    <h2 style={{ color: "#f8fafc", margin: 0, fontSize: "18px", fontFamily: "'Orbitron', sans-serif", letterSpacing: "0.5px" }}>
      Predictive Engine Control Panel
    </h2>
  </div>

        <div
          className="prediction-grid"
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(3, 1fr)",
            gap: "16px",
            marginBottom: "20px",
          }}
        >
          {/* CITY FIELD */}
          <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
            <label
              style={{
                fontSize: "12px",
                color: "#94a3b8",
                fontWeight: "600",
                textAlign: "left",
              }}
           >
             Select City
           </label>
           
           <select
              value={city}
              onChange={(e) => setCity(e.target.value)}
              style={{
                backgroundColor: "rgba(3, 7, 18, 0.5)",
                border: "1px solid rgba(255, 255, 255, 0.08)",
                borderRadius: "6px",
                padding: "10px 14px",
                color: "#f8fafc",
                outline: "none",
                fontSize: "14px",
              }}
            >
              <option value="Delhi">Delhi</option>
              <option value="Mumbai">Mumbai</option>
              <option value="Hyderabad">Hyderabad</option>
              <option value="Bengaluru">Bengaluru</option>
            </select>
          </div>
          {/* NDVI FIELD */}
          <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
            <label style={{ fontSize: "12px", color: "#94a3b8", fontWeight: "600", textAlign: "left" }}>
              NDVI Value
            </label>
            <input
              style={{
                backgroundColor: "rgba(3, 7, 18, 0.5)",
                border: "1px solid rgba(255, 255, 255, 0.08)",
                borderRadius: "6px",
                padding: "10px 14px",
                color: "#f8fafc",
                outline: "none",
                fontSize: "14px"
              }}
              placeholder="e.g. 0.35"
              value={ndvi}
              onChange={(event) => setNdvi(event.target.value)}
            />
          </div>
          {/* HUMIDITY FIELD */}
          <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
            <label style={{ fontSize: "12px", color: "#94a3b8", fontWeight: "600", textAlign: "left" }}>Humidity (%)</label>
            <input 
              style={{ backgroundColor: "rgba(3, 7, 18, 0.5)", border: "1px solid rgba(255, 255, 255, 0.08)", borderRadius: "6px", padding: "10px 14px", color: "#f8fafc", outline: "none", fontSize: "14px" }} 
              placeholder="e.g. 65" 
              value={humidity} 
              onChange={(event) => setHumidity(event.target.value)} 
            />
          </div>

          {/* WIND SPEED FIELD */}
          <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
            <label style={{ fontSize: "12px", color: "#94a3b8", fontWeight: "600", textAlign: "left" }}>Wind Speed (km/h)</label>
            <input 
              style={{ backgroundColor: "rgba(3, 7, 18, 0.5)", border: "1px solid rgba(255, 255, 255, 0.08)", borderRadius: "6px", padding: "10px 14px", color: "#f8fafc", outline: "none", fontSize: "14px" }} 
              placeholder="e.g. 14" 
              value={windSpeed} 
              onChange={(event) => setWindSpeed(event.target.value)} 
            />
          </div>

          {/* BUILDING DENSITY FIELD */}
          <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
            <label style={{ fontSize: "12px", color: "#94a3b8", fontWeight: "600", textAlign: "left" }}>Building Density (%)</label>
            <input 
              style={{ backgroundColor: "rgba(3, 7, 18, 0.5)", border: "1px solid rgba(255, 255, 255, 0.08)", borderRadius: "6px", padding: "10px 14px", color: "#f8fafc", outline: "none", fontSize: "14px" }} 
              placeholder="e.g. 75" 
              value={buildingDensity} 
              onChange={(event) => setBuildingDensity(event.target.value)} 
            />
          </div>
        </div>

        <button
        className="dock-hover"
          onClick={handlePrediction}
          style={{
            width: "100%",
            padding: "12px",
            fontSize: "13px",
            fontWeight: "700",
            letterSpacing: "1px",
            fontFamily: "'Orbitron', sans-serif",
            background: "linear-gradient(135deg, #f97316, #ea580c)",
            color: "white",
            border: "none",
            borderRadius: "6px",
            cursor: "pointer",
            marginTop: "10px",
            boxShadow: "0 4px 20px rgba(249, 115, 22, 0.2)",
          }}
        >
          {isScanning ? "SCANNING THERMAL DATA..." : "EXECUTE PREDICTIVE SIMULATION"}
        </button>

        {temperature !== null && (
          <div
            style={{
              marginTop: "20px",
              padding: "20px",
              backgroundColor: "rgba(244, 63, 94, 0.03)",
              border: "1px solid rgba(244, 63, 94, 0.15)",
              borderRadius: "8px",
              textAlign: "center",
            }}
          >
            <h4 style={{ margin: "0 0 6px 0", fontSize: "11px", color: "#f43f5e", letterSpacing: "1px", fontFamily: "'Orbitron', sans-serif" }}>
              SIMULATION MATRIX COMPLETE
            </h4>
            <div style={{ fontSize: "42px", fontWeight: "800", color: "#fda4af", margin: "4px 0" }}>
              {temperature}°C
            </div>
            <div
              style={{
                display: "inline-block",
                fontSize: "11px",
                fontWeight: "700",
                letterSpacing: "0.5px",
                color: riskLevel === "Extreme" || riskLevel === "High" ? "#ef4444" : riskLevel === "Moderate" ? "#f97316" : "#22c55e",
                backgroundColor: "rgba(0, 0, 0, 0.2)",
                padding: "4px 10px",
                borderRadius: "4px",
                border: "1px solid rgba(255, 255, 255, 0.05)",
                marginBottom: "20px",
              }}
            >
              SYSTEM STATE STATS: {riskLevel} RISK CORRIDOR
            </div>

            {predictionMode && (
              <div
                style={{
                  margin: "0 auto 20px",
                  width: "fit-content",
                  color: predictionMode === "api" ? "#86efac" : "#bae6fd",
                  backgroundColor: predictionMode === "api" ? "rgba(34,197,94,0.1)" : "rgba(14,165,233,0.1)",
                  border: predictionMode === "api" ? "1px solid rgba(34,197,94,0.24)" : "1px solid rgba(14,165,233,0.24)",
                  borderRadius: "999px",
                  padding: "7px 11px",
                  fontSize: "11px",
                  fontWeight: "800",
                  letterSpacing: "0.45px",
                }}
              >
                {predictionMode === "api"
                  ? "Live backend API response"
                  : "Public demo mode: backend API not connected on Netlify"}
              </div>
            )}

            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
                gap: "12px",
                margin: "0 0 22px",
              }}
            >
              <div style={{ backgroundColor: "rgba(34,197,94,0.08)", border: "1px solid rgba(34,197,94,0.18)", borderRadius: "8px", padding: "14px" }}>
                <h3 style={{ margin: "0 0 8px", color: "#86efac", fontSize: "12px", letterSpacing: "1px", fontFamily: "'Orbitron', sans-serif" }}>
                  Urban Cooling Index
                </h3>
                <strong style={{ color: "#f8fafc", fontSize: "28px" }}>{coolingIndex !== null ? coolingIndex : "--"}</strong>
              </div>

              <div style={{ backgroundColor: "rgba(249,115,22,0.08)", border: "1px solid rgba(249,115,22,0.2)", borderRadius: "8px", padding: "14px" }}>
                <h3 style={{ margin: "0 0 8px", color: "#fdba74", fontSize: "12px", letterSpacing: "1px", fontFamily: "'Orbitron', sans-serif" }}>
                  AI Confidence Score
                </h3>
                <strong style={{ color: "#f8fafc", fontSize: "28px" }}>{confidence !== null ? `${confidence}%` : "--"}</strong>
              </div>
            </div>

              <hr
              style={{
                margin: "24px 0",
                border: "1px solid rgba(255,255,255,0.08)",
              }} 
              />
              <h3
              style={{
                color: "#f8fafc",
                textAlign: "left",
                marginBottom: "12px",
              }}
              >
                AI Heat Analysis
              </h3>
              {aiFactors.map((factor, index) => (
              <div
              key={index}
              style={{
                color: "#cbd5e1",
                textAlign: "left",
                marginBottom: "8px",
              }}
            >
              - {factor}
              </div>
            ))}
            <h3
            style={{
              color: "#86efac",
              textAlign: "left",
              marginTop: "24px",
              marginBottom: "12px",
            }}
            >
              Cooling Recommendations
            </h3>
            {recommendations.map((item, index) => (
            <div
            key={index}
            style={{
              color: "#86efac",
              textAlign: "left",
              marginBottom: "8px",
            }}
            >
            - {item}
            </div>
          ))}

            <div
              style={{
                marginTop: "28px",
                padding: "20px",
                borderRadius: "16px",
                background:
                  "linear-gradient(135deg, rgba(14,165,233,0.12), rgba(34,197,94,0.08), rgba(249,115,22,0.08))",
                border: "1px solid rgba(125,211,252,0.18)",
                boxShadow: "0 16px 38px rgba(0,0,0,0.22)",
                textAlign: "left",
              }}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  gap: "16px",
                  alignItems: "center",
                  flexWrap: "wrap",
                  marginBottom: "16px",
                }}
              >
                <div>
                  <h3
                    style={{
                      margin: "0 0 8px",
                      color: "#f8fafc",
                      fontSize: "17px",
                      fontFamily: "'Orbitron', sans-serif",
                      letterSpacing: "0.8px",
                    }}
                  >
                    Urban Cooling Decision Engine
                  </h3>
                  <p style={{ margin: 0, color: "#94a3b8", fontSize: "13px", lineHeight: "1.6" }}>
                    Converts model output into city-specific cooling actions for planners.
                  </p>
                </div>

                <span
                  style={{
                    color: coolingEngineColor,
                    backgroundColor: "rgba(2,6,23,0.48)",
                    border: `1px solid ${coolingEngineColor}55`,
                    borderRadius: "999px",
                    padding: "8px 12px",
                    fontSize: "11px",
                    fontWeight: "800",
                    textTransform: "uppercase",
                    letterSpacing: "0.65px",
                  }}
                >
                  {coolingEngineMode}
                </span>
              </div>

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(auto-fit, minmax(170px, 1fr))",
                  gap: "12px",
                }}
              >
                <div style={{ padding: "14px", borderRadius: "12px", backgroundColor: "rgba(2,6,23,0.42)", border: "1px solid rgba(255,255,255,0.08)" }}>
                  <div style={{ color: "#94a3b8", fontSize: "11px", fontWeight: "800", letterSpacing: "0.8px", textTransform: "uppercase" }}>
                    Cooling Score
                  </div>
                  <strong style={{ display: "block", marginTop: "8px", color: "#86efac", fontSize: "26px" }}>
                    {coolingIndex !== null ? coolingIndex : "--"}
                  </strong>
                </div>

                <div style={{ padding: "14px", borderRadius: "12px", backgroundColor: "rgba(2,6,23,0.42)", border: "1px solid rgba(255,255,255,0.08)" }}>
                  <div style={{ color: "#94a3b8", fontSize: "11px", fontWeight: "800", letterSpacing: "0.8px", textTransform: "uppercase" }}>
                    Priority Zones
                  </div>
                  <strong style={{ display: "block", marginTop: "8px", color: "#fdba74", fontSize: "26px" }}>
                    {thresholdCount}
                  </strong>
                </div>

                <div style={{ padding: "14px", borderRadius: "12px", backgroundColor: "rgba(2,6,23,0.42)", border: "1px solid rgba(255,255,255,0.08)" }}>
                  <div style={{ color: "#94a3b8", fontSize: "11px", fontWeight: "800", letterSpacing: "0.8px", textTransform: "uppercase" }}>
                    Strategy Focus
                  </div>
                  <strong style={{ display: "block", marginTop: "8px", color: "#bae6fd", fontSize: "14px", lineHeight: "1.45" }}>
                    {recommendations[0] || "Run a prediction to generate action guidance"}
                  </strong>
                </div>
              </div>
            </div>
        </div>
      )}
    </div>

      {/* ================= INSIGHTS / FEATURE IMPORTANCE SECTION ================= */}


            <div
  id="insights"
  style={{
    backgroundColor: "rgba(11, 17, 32, 0.7)",
    border: "1px solid rgba(255, 255, 255, 0.05)",
    padding: "40px",
    borderRadius: "16px",
    maxWidth: "1200px",
    margin: "40px auto 0",
    boxShadow: "0 8px 32px rgba(0, 0, 0, 0.3)",
    boxSizing: "border-box"
  }}
>
  <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "32px" }}>
    <span style={{ width: "10px", height: "10px", backgroundColor: "#22c55e", borderRadius: "50%", boxShadow: "0 0 12px #22c55e" }}></span>
    <h2 style={{ color: "#f8fafc", margin: 0, fontSize: "20px", fontFamily: "'Orbitron', sans-serif", letterSpacing: "0.75px" }}>
      Neural Weights & Feature Attribution Matrix
    </h2>
  </div>

  <div style={{ display: "flex", flexDirection: "column", gap: "24px" }}>
    {/* NDVI */}
    <div className="insight-row" style={{ display: "grid", gridTemplateColumns: "180px 1fr 60px", alignItems: "center", gap: "20px" }}>
      <span style={{ color: "#94a3b8", fontWeight: "700", fontSize: "14px", textAlign: "left" }}>NDVI Telemetry</span>
      <div style={{ height: "16px", backgroundColor: "rgba(255, 255, 255, 0.03)", borderRadius: "6px", overflow: "hidden", border: "1px solid rgba(255,255,255,0.05)", padding: "2px" }}>
        <div className="bar-fill-animate" style={{ height: "100%", width: `${featureWeights.ndvi}%`, backgroundColor: "#22c55e", borderRadius: "4px", boxShadow: "0 0 10px rgba(34, 197, 94, 0.5)" }}></div>
      </div>
      <strong style={{ color: "#f8fafc", textAlign: "right", fontSize: "16px", fontFamily: "'Orbitron', sans-serif" }}>45%</strong>
    </div>

    {/* HUMIDITY */}
    <div className="insight-row" style={{ display: "grid", gridTemplateColumns: "180px 1fr 60px", alignItems: "center", gap: "20px" }}>
      <span style={{ color: "#94a3b8", fontWeight: "700", fontSize: "14px", textAlign: "left" }}>Air Moisture</span>
      <div style={{ height: "16px", backgroundColor: "rgba(255, 255, 255, 0.03)", borderRadius: "6px", overflow: "hidden", border: "1px solid rgba(255,255,255,0.05)", padding: "2px" }}>
        <div className="bar-fill-animate" style={{ height: "100%", width: `${featureWeights.humidity}%`, backgroundColor: "#3b82f6", borderRadius: "4px", boxShadow: "0 0 10px rgba(59, 130, 246, 0.5)" }}></div>
      </div>
      <strong style={{ color: "#f8fafc", textAlign: "right", fontSize: "16px", fontFamily: "'Orbitron', sans-serif" }}>30%</strong>
    </div>

    {/* WIND SPEED */}
    <div className="insight-row" style={{ display: "grid", gridTemplateColumns: "180px 1fr 60px", alignItems: "center", gap: "20px" }}>
      <span style={{ color: "#94a3b8", fontWeight: "700", fontSize: "14px", textAlign: "left" }}>Wind Velocity</span>
      <div style={{ height: "16px", backgroundColor: "rgba(255, 255, 255, 0.03)", borderRadius: "6px", overflow: "hidden", border: "1px solid rgba(255,255,255,0.05)", padding: "2px" }}>
        <div className="bar-fill-animate" style={{ height: "100%", width: `${featureWeights.wind}%`, backgroundColor: "#a855f7", borderRadius: "4px", boxShadow: "0 0 10px rgba(168, 85, 247, 0.5)" }}></div>
      </div>
      <strong style={{ color: "#f8fafc", textAlign: "right", fontSize: "16px", fontFamily: "'Orbitron', sans-serif" }}>15%</strong>
    </div>

    {/* BUILDING DENSITY */}
    <div className="insight-row" style={{ display: "grid", gridTemplateColumns: "180px 1fr 60px", alignItems: "center", gap: "20px" }}>
      <span style={{ color: "#94a3b8", fontWeight: "700", fontSize: "14px", textAlign: "left" }}>Urban Canopy</span>
      <div style={{ height: "16px", backgroundColor: "rgba(255, 255, 255, 0.03)", borderRadius: "6px", overflow: "hidden", border: "1px solid rgba(255,255,255,0.05)", padding: "2px" }}>
        <div  className="bar-fill-animate" style={{ height: "100%", width: `${featureWeights.density}%`, backgroundColor: "#fb7185", borderRadius: "4px", boxShadow: "0 0 10px rgba(251, 113, 113, 0.5)" }}></div>
      </div>
      <strong style={{ color: "#f8fafc", textAlign: "right", fontSize: "16px", fontFamily: "'Orbitron', sans-serif" }}>10%</strong>
    </div>
  </div>
</div>

{/* ================= SATELLITE DATA SOURCE SECTION ================= */}

<section
  className="card-hover animate-card"
  style={{
    maxWidth: "1200px",
    margin: "40px auto 0",
    padding: "34px",
    borderRadius: "22px",
    background:
      "linear-gradient(135deg, rgba(14,165,233,0.13), rgba(15,23,42,0.74) 44%, rgba(249,115,22,0.1))",
    border: "1px solid rgba(125, 211, 252, 0.16)",
    boxShadow: "0 22px 58px rgba(0, 0, 0, 0.32)",
  }}
>
  <div
    style={{
      display: "flex",
      justifyContent: "space-between",
      alignItems: "flex-start",
      gap: "20px",
      flexWrap: "wrap",
      marginBottom: "24px",
    }}
  >
    <div>
      <p
        style={{
          margin: "0 0 10px",
          color: "#38bdf8",
          fontSize: "11px",
          fontWeight: "800",
          letterSpacing: "1.4px",
          textTransform: "uppercase",
          fontFamily: "'Orbitron', sans-serif",
        }}
      >
        Earth Observation Data Layer
      </p>
      <h2
        style={{
          margin: 0,
          color: "#f8fafc",
          fontSize: "22px",
          fontFamily: "'Orbitron', sans-serif",
          letterSpacing: "0.8px",
        }}
      >
        Landsat April-June 2025 Integration
      </h2>
    </div>

    <span
      style={{
        color: "#bbf7d0",
        backgroundColor: "rgba(34,197,94,0.12)",
        border: "1px solid rgba(34,197,94,0.28)",
        borderRadius: "999px",
        padding: "9px 13px",
        fontSize: "11px",
        fontWeight: "900",
        textTransform: "uppercase",
        letterSpacing: "0.7px",
      }}
    >
      Exported Dataset
    </span>
  </div>

  <p
    style={{
      margin: "0 0 22px",
      maxWidth: "780px",
      color: "#cbd5e1",
      fontSize: "14px",
      lineHeight: "1.7",
    }}
  >
    HEATSHIELD INDIA now includes exported Google Earth Engine samples for Landsat-derived NDVI and land surface temperature. The current {city} summary below is calculated from the April-June 2025 CSV dataset downloaded into the project.
  </p>

  <div
    style={{
      display: "grid",
      gridTemplateColumns: "repeat(auto-fit, minmax(210px, 1fr))",
      gap: "14px",
    }}
  >
    {satelliteDataCards.map((card) => (
      <article
        key={card.label}
        style={{
          padding: "18px",
          borderRadius: "16px",
          backgroundColor: "rgba(2,6,23,0.48)",
          border: `1px solid ${card.color}33`,
          boxShadow: `0 0 26px ${card.color}14`,
        }}
      >
        <div
          style={{
            color: "#94a3b8",
            fontSize: "11px",
            fontWeight: "900",
            letterSpacing: "0.8px",
            textTransform: "uppercase",
            marginBottom: "10px",
          }}
        >
          {card.label}
        </div>
        <strong
          style={{
            display: "block",
            color: card.color,
            fontSize: "22px",
            fontWeight: "900",
            marginBottom: "8px",
          }}
        >
          {card.value}
        </strong>
        <span style={{ color: "#94a3b8", fontSize: "13px", lineHeight: "1.5" }}>
          {card.detail}
        </span>
      </article>
    ))}
  </div>

  <div
    style={{
      display: "grid",
      gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
      gap: "14px",
      marginTop: "18px",
      paddingTop: "18px",
      borderTop: "1px solid rgba(255,255,255,0.1)",
    }}
  >
    <article style={{ padding: "16px", borderRadius: "14px", backgroundColor: "rgba(15,23,42,0.58)", border: "1px solid rgba(255,255,255,0.08)" }}>
      <div style={{ color: "#94a3b8", fontSize: "11px", fontWeight: "900", letterSpacing: "0.8px", textTransform: "uppercase", marginBottom: "8px" }}>
        {city} Samples
      </div>
      <strong style={{ color: "#f8fafc", fontSize: "26px" }}>{activeLandsatStats.samples}</strong>
    </article>

    <article style={{ padding: "16px", borderRadius: "14px", backgroundColor: "rgba(15,23,42,0.58)", border: "1px solid rgba(34,197,94,0.16)" }}>
      <div style={{ color: "#94a3b8", fontSize: "11px", fontWeight: "900", letterSpacing: "0.8px", textTransform: "uppercase", marginBottom: "8px" }}>
        Average NDVI
      </div>
      <strong style={{ color: "#86efac", fontSize: "26px" }}>{activeLandsatStats.avgNdvi.toFixed(3)}</strong>
    </article>

    <article style={{ padding: "16px", borderRadius: "14px", backgroundColor: "rgba(15,23,42,0.58)", border: "1px solid rgba(249,115,22,0.18)" }}>
      <div style={{ color: "#94a3b8", fontSize: "11px", fontWeight: "900", letterSpacing: "0.8px", textTransform: "uppercase", marginBottom: "8px" }}>
        Average LST
      </div>
      <strong style={{ color: "#fdba74", fontSize: "26px" }}>{activeLandsatStats.avgLst.toFixed(2)}°C</strong>
    </article>

    <article style={{ padding: "16px", borderRadius: "14px", backgroundColor: "rgba(15,23,42,0.58)", border: "1px solid rgba(239,68,68,0.18)" }}>
      <div style={{ color: "#94a3b8", fontSize: "11px", fontWeight: "900", letterSpacing: "0.8px", textTransform: "uppercase", marginBottom: "8px" }}>
        Max LST
      </div>
      <strong style={{ color: "#fca5a5", fontSize: "26px" }}>{activeLandsatStats.maxLst.toFixed(2)}°C</strong>
    </article>
  </div>
</section>

{/* ================= HEATMAP / RADIATIVE SPECTRUM SECTION ================= */}


 <div
  id="heatmap"
  className="card-hover animate-card"
  style={{
    backgroundColor: "rgba(11, 17, 32, 0.7)",
    border: "1px solid rgba(255, 255, 255, 0.05)",
    padding: "40px",
    borderRadius: "24px",
    maxWidth: "1200px",
    margin: "60px auto 0",
    boxShadow: "0 20px 50px rgba(0, 0, 0, 0.4)",
    boxSizing: "border-box"
  }}
>
  
  {/* TITLE AREA */}
  <div style={{ marginBottom: "50px" }}>
    <h2 style={{ color: "#f8fafc", margin: "0 0 12px 0", fontSize: "28px", fontFamily: "'Orbitron', sans-serif", letterSpacing: "1px" }}>
      SURFACE RADIATIVE SPECTRUM CORRIDOR
    </h2>
    <p style={{ color: "#94a3b8", fontSize: "16px", maxWidth: "600px" }}>
      Continuous thermodynamic tracking of surface friction and albedo feedback loops across the urban canopy.
    </p>
  </div>
  <h3
   style={{
     color: "#f8fafc",
     marginBottom: "16px",
     textAlign: "center",
     fontFamily: "'Orbitron', sans-serif",
     fontSize: "20px",
     fontWeight: "700",
   }}
  >
  {city} Urban Heatmap
  </h3>

		  <div className="heatmap-frame-wrap" style={{ marginTop: "30px", marginBottom: "48px" }}>
	    {heatmapFiles[city].type === "image" ? (
	      <img
       src={heatmapFiles[city].src}
       alt={`${city} Heatmap`}
       style={{
         width: "100%",
         height: "600px",
         objectFit: "contain",
         borderRadius: "18px",
         border: "1px solid rgba(255,255,255,0.12)",
         backgroundColor: "#020617",
       }}
     />
   ) : (
     <iframe
       src={heatmapFiles[city].src}
       title={`${city} Heatmap`}
       style={{
         width: "100%",
         height: "430px",
         border: "none",
         borderRadius: "18px",
         overflow: "hidden",
         backgroundColor: "#020617",
         boxShadow: "0 20px 45px rgba(0,0,0,0.35)",
       }}
	     />
		   )}
			 </div>
  <div
    style={{
      margin: "0 0 48px",
      padding: "22px",
      borderRadius: "14px",
      backgroundColor: "rgba(2, 6, 23, 0.48)",
      border: "1px solid rgba(255,255,255,0.08)",
    }}
  >
    <div
      className="place-grid"
      style={{
        display: "flex",
        justifyContent: "space-between",
        gap: "18px",
        alignItems: "flex-end",
        flexWrap: "wrap",
        marginBottom: "18px",
      }}
    >
      <div>
        <h3
          style={{
            margin: "0 0 8px",
            color: "#f8fafc",
            fontSize: "18px",
            fontFamily: "'Orbitron', sans-serif",
            letterSpacing: "0.75px",
          }}
        >
          Place Heat Search
        </h3>
	        <p style={{ margin: 0, color: "#94a3b8", fontSize: "14px", lineHeight: "1.6" }}>
	          Search {city} zones, filter hotter regions, and hover the blue map pins for temperature and zone category.
	        </p>
      </div>

      {hottestVisiblePlace && (
        <div
          style={{
            padding: "10px 14px",
            borderRadius: "8px",
            color: "#fed7aa",
            backgroundColor: "rgba(249,115,22,0.1)",
            border: "1px solid rgba(249,115,22,0.22)",
            fontSize: "12px",
            fontWeight: "700",
          }}
        >
          Hottest match: {hottestVisiblePlace.name} - {hottestVisiblePlace.temperature.toFixed(1)}°C
        </div>
      )}
    </div>

    <div
      style={{
        marginBottom: "18px",
        padding: "16px",
        borderRadius: "14px",
        background:
          "linear-gradient(135deg, rgba(249,115,22,0.12), rgba(34,197,94,0.08))",
        border: "1px solid rgba(255,255,255,0.1)",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          gap: "14px",
          alignItems: "center",
          flexWrap: "wrap",
          marginBottom: "12px",
        }}
      >
        <div>
          <strong
            style={{
              color: "#f8fafc",
              fontSize: "14px",
              fontFamily: "'Orbitron', sans-serif",
              letterSpacing: "0.55px",
            }}
          >
            Heat Threshold Control
          </strong>
          <p style={{ margin: "6px 0 0", color: "#94a3b8", fontSize: "13px" }}>
            Showing regions at or above the selected temperature.
          </p>
        </div>
        <div
          style={{
            color: "#fed7aa",
            fontWeight: "800",
            fontSize: "13px",
            padding: "8px 12px",
            borderRadius: "999px",
            backgroundColor: "rgba(249,115,22,0.14)",
            border: "1px solid rgba(249,115,22,0.24)",
          }}
        >
          {thresholdCount} zones {">="} {heatThreshold}°C
        </div>
      </div>
      <input
        className="heat-threshold-slider"
        type="range"
        min="35"
        max="45"
        step="0.5"
        value={heatThreshold}
        onChange={(event) => setHeatThreshold(Number(event.target.value))}
        style={{ width: "100%" }}
      />
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          color: "#64748b",
          fontSize: "11px",
          fontWeight: "700",
          marginTop: "8px",
        }}
      >
        <span>35°C</span>
        <span>40°C</span>
        <span>45°C</span>
      </div>
    </div>

    <input
      value={placeSearch}
      onChange={(event) => setPlaceSearch(event.target.value)}
      placeholder={`Search places in ${city}`}
      style={{
        width: "100%",
        padding: "12px 14px",
        borderRadius: "8px",
        border: "1px solid rgba(255, 255, 255, 0.1)",
        backgroundColor: "rgba(3, 7, 18, 0.62)",
        color: "#f8fafc",
        outline: "none",
        fontSize: "14px",
        marginBottom: "16px",
      }}
    />

    <div
      style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(190px, 1fr))",
        gap: "12px",
      }}
    >
      {visiblePlaces.length > 0 ? (
        visiblePlaces.map((place) => {
          const riskColor =
            place.risk === "Very High"
              ? "#ef4444"
              : place.risk === "High"
              ? "#f97316"
              : "#22c55e";

          return (
            <article
              key={place.name}
              className="card-hover"
              style={{
                padding: "16px",
                borderRadius: "10px",
                backgroundColor: "rgba(15, 23, 42, 0.62)",
                border: "1px solid rgba(255,255,255,0.08)",
                textAlign: "left",
              }}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  gap: "10px",
                  alignItems: "center",
                  marginBottom: "12px",
                }}
              >
                <strong style={{ color: "#f8fafc", fontSize: "15px" }}>{place.name}</strong>
                <span
                  style={{
                    color: riskColor,
                    fontSize: "11px",
                    fontWeight: "800",
                    textTransform: "uppercase",
                    letterSpacing: "0.5px",
                  }}
                >
                  {place.risk}
                </span>
              </div>
              <div style={{ color: riskColor, fontSize: "26px", fontWeight: "800", marginBottom: "8px" }}>
                {place.temperature.toFixed(1)}°C
              </div>
              <p style={{ margin: 0, color: "#94a3b8", fontSize: "13px", lineHeight: "1.5" }}>
                {place.focus}
              </p>
            </article>
          );
        })
      ) : (
        <div
          style={{
            gridColumn: "1 / -1",
            padding: "16px",
            color: "#94a3b8",
            border: "1px dashed rgba(255,255,255,0.14)",
            borderRadius: "8px",
            textAlign: "center",
          }}
        >
          No matching heatmap place found for {city}.
        </div>
      )}
    </div>
  </div>
	  {/* THE EXPANDED THERMAL GRADIENT ENGINE */}
	  <div className="thermal-spectrum" style={{ position: "relative", padding: "40px 0 60px 0" }}>
    
    <div 
      style={{ 
        height: "48px", 
        background: "linear-gradient(to right, #16a34a, #22c55e, #a3e635, #eab308, #f97316, #dc2626, #7f1d1d)", 
        borderRadius: "12px",
        boxShadow: "0 8px 30px rgba(0,0,0,0.3)",
        border: "1px solid rgba(255,255,255,0.1)"
      }}
    >
      {/* INDICATORS - NOW SPACED FOR MAXIMUM IMPACT */}
      <div className="spectrum-marker spectrum-marker-cool" style={{ position: "absolute", left: "15%", top: "-20px", display: "flex", flexDirection: "column", alignItems: "center" }}>
        <span style={{ fontSize: "12px", fontFamily: "'Orbitron', sans-serif", fontWeight: "700", color: "#86efac", marginBottom: "8px" }}>ECOLOGICAL BUFFER</span>
        <div style={{ width: "3px", height: "80px", backgroundColor: "#86efac", opacity: 0.8 }}></div>
      </div>

      <div className="spectrum-marker spectrum-marker-mid" style={{ position: "absolute", left: "52%", top: "-20px", display: "flex", flexDirection: "column", alignItems: "center" }}>
        <span style={{ fontSize: "12px", fontFamily: "'Orbitron', sans-serif", fontWeight: "700", color: "#fde68a", marginBottom: "8px" }}>URBAN CHILL SECTOR</span>
        <div style={{ width: "3px", height: "80px", backgroundColor: "#fde68a", opacity: 0.8 }}></div>
      </div>

      <div className="spectrum-marker spectrum-marker-hot" style={{ position: "absolute", left: "85%", top: "-20px", display: "flex", flexDirection: "column", alignItems: "center" }}>
        <span style={{ fontSize: "12px", fontFamily: "'Orbitron', sans-serif", fontWeight: "700", color: "#fca5a5", marginBottom: "8px" }}>CRITICAL THERMAL ANOMALY</span>
        <div style={{ width: "3px", height: "80px", backgroundColor: "#fca5a5", opacity: 1, boxShadow: "0 0 12px #ef4444" }}></div>
      </div>
    </div>
    <div
  className="active-spectrum-marker"
  style={{
    position: "absolute",
    left: `${thermalPosition}%`,
    top: "18px",
    transform: "translateX(-50%)",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    zIndex: 4,
  }}
>
  <span
    style={{
      fontSize: "11px",
      fontFamily: "'Orbitron', sans-serif",
      fontWeight: "800",
      color: thermalStatusColor,
      marginBottom: "8px",
      whiteSpace: "nowrap",
    }}
  >
    {thermalStatus}
  </span>

  <div
    style={{
      width: "4px",
      height: "88px",
      backgroundColor: thermalStatusColor,
      boxShadow: `0 0 18px ${thermalStatusColor}`,
      borderRadius: "999px",
    }}
  ></div>

  <span
    style={{
      marginTop: "8px",
      fontSize: "12px",
      color: "#f8fafc",
      fontWeight: "800",
    }}
  >
    {activeTemperature === null ? "--" : `${activeTemperature.toFixed(1)}°C`}
  </span>
</div>
  </div>

  {/* LOWER METRIC FOOTER - ENLARGED */}
  <div className="spectrum-legend-grid" style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "40px", borderTop: "1px solid rgba(255,255,255,0.1)", paddingTop: "30px" }}>
    <div>
      <div style={{ color: "#22c55e", fontWeight: "800", fontSize: "18px", marginBottom: "8px" }}>Cool Green Zones</div>
      <div style={{ color: "#94a3b8", fontSize: "14px", lineHeight: "1.6" }}>High canopy density and active vegetation-based cooling corridors.</div>
    </div>
    <div>
      <div style={{ color: "#eab308", fontWeight: "800", fontSize: "18px", marginBottom: "8px" }}>Moderate Radiation</div>
      <div style={{ color: "#94a3b8", fontSize: "14px", lineHeight: "1.6" }}>Suburban transitional zones requiring minor thermal mitigation.</div>
    </div>
    <div>
      <div style={{ color: "#ef4444", fontWeight: "800", fontSize: "18px", marginBottom: "8px" }}>Albedo Core Hotspots</div>
      <div style={{ color: "#94a3b8", fontSize: "14px", lineHeight: "1.6" }}>High built-density areas exhibiting significant heat retention.</div>
    </div>
  </div>
</div>


{/* ================= HEATMAP / RADIATIVE SPECTRUM SECTION ================= */}



                  <div
        style={{
          maxWidth: "980px",
          margin: "40px auto 0",
        }}
      >
        <h2
          style={{
            color: "#f8fafc",
            textAlign: "center",
            marginBottom: "24px",
          }}
        >
          High-Risk City Zones
        </h2>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
            gap: "18px",
          }}
        >
          <div style={cityCardStyle}>
  <div style={{ ...riskStripStyle, background: "#dc2626" }}></div>
  <h3 style={{ color: "#f8fafc", marginBottom: "8px" }}>Delhi</h3>
  <p style={{ color: "#cbd5e1", marginBottom: "14px" }}>Very High Heat Risk</p>
  <strong style={{ color: "#fb7185", fontSize: "28px" }}>42.1°C</strong>
</div>

<div style={cityCardStyle}>
  <div style={{ ...riskStripStyle, background: "#f97316" }}></div>
  <h3 style={{ color: "#f8fafc", marginBottom: "8px" }}>Ahmedabad</h3>
  <p style={{ color: "#cbd5e1", marginBottom: "14px" }}>High Heat Risk</p>
  <strong style={{ color: "#fdba74", fontSize: "28px" }}>41.4°C</strong>
</div>

<div style={cityCardStyle}>
  <div style={{ ...riskStripStyle, background: "#facc15" }}></div>
  <h3 style={{ color: "#f8fafc", marginBottom: "8px" }}>Hyderabad</h3>
  <p style={{ color: "#cbd5e1", marginBottom: "14px" }}>Moderate Heat Risk</p>
  <strong style={{ color: "#fde68a", fontSize: "28px" }}>38.7°C</strong>
</div>

<div style={cityCardStyle}>
  <div style={{ ...riskStripStyle, background: "#22c55e" }}></div>
  <h3 style={{ color: "#f8fafc", marginBottom: "8px" }}>Mumbai</h3>
  <p style={{ color: "#cbd5e1", marginBottom: "14px" }}>Humidity-Linked Risk</p>
  <strong style={{ color: "#86efac", fontSize: "28px" }}>36.9°C</strong>
</div>
        </div>
      </div>
      <div

    //ABOUT / MISSION OBJECTIVE STATEMNENT 


  id="about"
  style={{
    maxWidth: "800px",
    margin: "60px auto 0",
    padding: "40px",
    backgroundColor: "rgba(3, 7, 18, 0.4)",
    borderLeft: "4px solid #f97316",
    borderTop: "1px solid rgba(255, 255, 255, 0.05)",
    borderRight: "1px solid rgba(255, 255, 255, 0.05)",
    borderBottom: "1px solid rgba(255, 255, 255, 0.05)",
    borderRadius: "0 12px 12px 0",
    textAlign: "left",
  }}
>
  <h2
    style={{
      color: "#ffffff",
      marginBottom: "20px",
      fontSize: "20px",
      fontFamily: "'Orbitron', sans-serif",
      letterSpacing: "1px",
      textTransform: "uppercase",
    }}
  >
    System Intelligence & Mission Objective
  </h2>

  <p
    style={{
      color: "#cbd5e1",
      fontSize: "15px",
      lineHeight: "1.8",
      fontFamily: "'Plus Jakarta Sans', sans-serif",
      margin: 0,
    }}
  >
    HeatShield India is an advanced geospatial analytics framework developed for the 2026 Bharatiya Antariksh Hackathon. By synthesizing multi-source satellite telemetry with urban surface friction metrics, the system identifies microclimate anomalies to guide urban heat mitigation strategies. Our objective is to assist policymakers in optimizing green cover expansion, reducing high-albedo material impact, and restoring natural ventilation corridors to ensure long-term thermal resilience in urban centers.
  </p>
</div>

{/* ================= FOOTER SECTION ================= */}

      <footer
        style={{
          maxWidth: "1180px",
          margin: "48px auto 0",
          padding: "22px 0",
          borderTop: "1px solid rgba(255,255,255,0.12)",
          display: "flex",
          justifyContent: "space-between",
          gap: "16px",
          flexWrap: "wrap",
          color: "#cbd5e1",
          fontSize: "14px",
        }}
      >
        <span>Powered by Team 404 Brain Not Found</span>
        <span>Built for ISRO Hackathon 2026 • Urban Heat Mitigation</span>
      </footer>
    </div>
  );
}

// ================= STYLE CONSTANTS =================

const hotspotStyle = {
  position: "absolute",
  width: "16px",
  height: "16px",
  borderRadius: "50%",
  backgroundColor: "#ef4444",
  boxShadow: "0 0 0 8px rgba(239,68,68,0.22), 0 0 28px rgba(239,68,68,0.9)",
  animation: "pulseHotspot 1.8s ease-in-out infinite",
};
const cityCardStyle = {
  position: "relative",
  overflow: "hidden",
  backgroundColor: "rgba(15, 23, 42, 0.72)",
  padding: "24px",
  borderRadius: "18px",
  border: "1px solid rgba(255, 255, 255, 0.12)",
  boxShadow: "0 18px 45px rgba(0, 0, 0, 0.25)",
  color: "#f8fafc",
};
const riskStripStyle = {
  position: "absolute",
  top: 0,
  left: 0,
  width: "100%",
  height: "5px",
};
const cityLabelStyle = {
  position: "absolute",
  color: "#f8fafc",
  fontSize: "12px",
  backgroundColor: "rgba(2, 6, 23, 0.65)",
  border: "1px solid rgba(255, 255, 255, 0.12)",
  borderRadius: "999px",
  padding: "5px 9px",
};
const navLinkStyle = {
  cursor: "pointer",
  transition: "0.2s",
};
const styleSheet = document.createElement("style");
styleSheet.innerText = `
  @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
  @keyframes pulseHotspot { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
  .animate-card { animation: fadeIn 0.6s ease-out forwards; }
  .card-hover { transition: transform 0.3s ease; }
  .card-hover:hover { transform: translateY(-5px); border-color: rgba(249, 115, 22, 0.4); }
  .scanning-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(transparent, rgba(249, 115, 22, 0.1), transparent); animation: scan-move 2s linear infinite; pointer-events: none; z-index: 100; }
  @keyframes scan-move { 0% { transform: translateY(-100%); } 100% { transform: translateY(100%); } }
    .bar-fill-animate {
    transform-origin: left;
    animation: growBar 1.1s ease-out forwards;
  }

  @keyframes growBar {
    from {
      transform: scaleX(0);
    }
    to {
      transform: scaleX(1);
    }
  }
      .dock-hover {
    display: inline-block;
    transition: transform 0.18s ease, filter 0.18s ease;
  }

  .dock-hover:hover {
    transform: scale(1.06);
    filter: brightness(1.15);
  }

  .dock-hover:active {
    transform: scale(0.98);
  }
`;
document.head.appendChild(styleSheet);

export default App;
