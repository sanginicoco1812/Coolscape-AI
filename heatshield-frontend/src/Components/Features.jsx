import "../Styles/Features.css";

function Features() {
  return (
    <section className="features">
      <h2>Our Features</h2>

      <div className="feature-cards">
        <div className="card">
          <h3>AI Analysis</h3>
          <p>Smart insights powered by machine learning.</p>
        </div>

        <div className="card">
          <h3>Satellite Data</h3>
          <p>Process and visualize geospatial information.</p>
        </div>

        <div className="card">
          <h3>Real-Time Dashboard</h3>
          <p>Monitor predictions and analytics instantly.</p>
        </div>
      </div>
    </section>
  );
}

export default Features;