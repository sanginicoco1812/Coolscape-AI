import "../Styles/Navbar.css";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="logo">
        ISRO Hackathon
      </div>

      <ul className="nav-links">
        <li>Home</li>
        <li>Features</li>
        <li>About</li>
        <li>Contact</li>
      </ul>
    </nav>
  );
}

export default Navbar;