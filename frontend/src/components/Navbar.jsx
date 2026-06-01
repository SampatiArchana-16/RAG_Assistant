import { Link } from "react-router-dom";

function Navbar() {

  return (

    <nav className="navbar">

      <div className="logo">
        DocuMind AI
      </div>

      <div className="nav-links">

        <Link to="/">
          Home
        </Link>

        <Link to="/register">
          Register
        </Link>

        <Link to="/login">
          Login
        </Link>

      </div>

    </nav>

  );
}

export default Navbar;