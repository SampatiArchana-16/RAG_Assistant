import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import Home from "./pages/Home";

import Register from "./pages/Register";

import Login from "./pages/Login";

import Chatbot from "./pages/Chatbot";

function App() {

  return (

    <BrowserRouter>

      <Routes>

        {/* HOME */}

        <Route
          path="/"
          element={<Home />}
        />

        {/* REGISTER */}

        <Route
          path="/register"
          element={<Register />}
        />

        {/* LOGIN */}

        <Route
          path="/login"
          element={<Login />}
        />

        {/* CHATBOT */}

        <Route
          path="/chatbot"
          element={<Chatbot />}
        />

      </Routes>

    </BrowserRouter>
  );
}

export default App;