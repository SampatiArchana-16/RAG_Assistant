
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import axios from "axios";

function Register() {

    const navigate = useNavigate();

    const [email, setEmail] = useState("");

    const [password, setPassword] = useState("");

    const registerUser = async () => {

        try {

            const response = await axios.post(
                "https://rag-backend-0bjx.onrender.com/auth/register",
                {
                    email,
                    password
                }
            );

            alert(response.data.message);

            navigate("/login");

        } catch (error) {

            console.log("FULL ERROR:", error);

            console.log("RESPONSE:", error.response);

            console.log("DATA:", error.response?.data);

            alert(
                JSON.stringify(error.response?.data)
            );
        }
    };

    return (

        <div className="auth-page">

            <div className="auth-card">

                <h2>Create Account</h2>

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
                    onClick={registerUser}
                >
                    Register
                </button>

                <p>
                    Already have an account?
                    <Link to="/login">
                        Login
                    </Link>
                </p>

            </div>

        </div>
    );
}

export default Register;

