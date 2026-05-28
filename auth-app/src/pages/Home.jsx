import { Link } from "react-router-dom";

function Home() {

    return (

        <div
            style={{
                textAlign: "center",
                marginTop: "100px"
            }}
        >

            <h1>
                DocuMind AI 🤖
            </h1>

            <p>
                Intelligent PDF RAG Assistant
            </p>

            <div
                style={{
                    marginTop: "30px"
                }}
            >

                <Link to="/register">

                    <button
                        style={{
                            padding: "10px 20px",
                            marginRight: "20px"
                        }}
                    >
                        Register
                    </button>

                </Link>

                <Link to="/login">

                    <button
                        style={{
                            padding: "10px 20px"
                        }}
                    >
                        Login
                    </button>

                </Link>

            </div>

        </div>
    );
}

export default Home;