import { Link, useNavigate } from "react-router-dom";

function Navbar() {

  const navigate = useNavigate();

  const token =
    localStorage.getItem("token");

  const email =
    localStorage.getItem("email");

  const logout = () => {

    localStorage.removeItem("token");

    localStorage.removeItem("email");

    navigate("/login");
  };

  return (

    <nav className="navbar">

      <div className="logo">
        DocuMind AI
      </div>

      <div className="nav-links">

        <Link to="/">
          Home
        </Link>

        {
          !token && (
            <>
              <Link to="/register">
                Register
              </Link>

              <Link to="/login">
                Login
              </Link>
            </>
          )
        }

        {
          token && (
            <>
              <span>
                {email}
              </span>

              <Link to="/chatbot">
                Chatbot
              </Link>

              <button
                onClick={logout}
              >
                Logout
              </button>
            </>
          )
        }

      </div>

    </nav>
  );
}

export default Navbar;