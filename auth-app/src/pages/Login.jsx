import { useState } from "react";

import { useNavigate } from "react-router-dom";

import axios from "axios";

function Login() {

    const navigate = useNavigate();

    const [email, setEmail] = useState("");

    const [password, setPassword] = useState("");

    const loginUser = async () => {

        try {

            await axios.post(
                "http://127.0.0.1:8000/auth/login",
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

        <div style={{ padding: "40px" }}>

            <h1>Login</h1>

            <input
                type="email"
                placeholder="Enter Email"
                value={email}
                onChange={(e) =>
                    setEmail(e.target.value)
                }
            />

            <br /><br />

            <input
                type="password"
                placeholder="Enter Password"
                value={password}
                onChange={(e) =>
                    setPassword(e.target.value)
                }
            />

            <br /><br />

            <button onClick={loginUser}>
                Login
            </button>

        </div>
    );
}

export default Login;