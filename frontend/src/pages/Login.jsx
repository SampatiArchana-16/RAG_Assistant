
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import axios from "axios";

function Login() {

  const navigate = useNavigate();

  const [email, setEmail] = useState("");

  const [password, setPassword] = useState("");

  const loginUser = async () => {

    try {

      await axios.post(
        "https://rag-backend-0bjx.onrender.com/auth/login",
        {
          email,
          password
        }
      );

      alert("Login Successful");

      navigate("/chatbot");

    } catch (error) {

      alert(
        error.response?.data?.detail ||
        "Invalid Email or Password"
      );
    }
  };

  return (

    <div className="auth-page">

      <div className="auth-card">

        <h2>Welcome Back</h2>

        <input
          type="email"
          placeholder="Enter Email"
          value={email}
          onChange={(e) =>
            setEmail(e.target.value)
          }
        />

        <input
          type="password"
          placeholder="Enter Password"
          value={password}
          onChange={(e) =>
            setPassword(e.target.value)
          }
        />

        <button
          className="auth-btn"
          onClick={loginUser}
        >
          Login
        </button>

        <p>
          New User?
          <Link to="/register">
            Register
          </Link>
        </p>

      </div>

    </div>
  );
}

export default Login;
