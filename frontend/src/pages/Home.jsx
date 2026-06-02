
import { Link } from "react-router-dom";

function Home() {

  return (

    <div className="home">

      <div className="hero-card">

        <h1>DocuMind AI 🤖</h1>

        <p>
          Upload PDFs and chat with your documents using AI.
        </p>

        <div className="home-buttons">

          <Link to="/register">
            <button className="btn-primary">
              Register
            </button>
          </Link>

          <Link to="/login">
            <button className="btn-secondary">
              Login
            </button>
          </Link>

        </div>

      </div>

    </div>

  );
}

export default Home;

