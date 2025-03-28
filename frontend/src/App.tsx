import { Navigate, Route, Routes } from "react-router-dom";
import { Toaster } from "react-hot-toast";

import { useAuthContext } from "./context/AuthContext";
import Landing from "./pages/landing/Landing";
import Signup from "./pages/auth/Signup";
import Login from "./pages/auth/Login";
import ParticleBackground from "./components/ParticleBackground";
import Chat from "./pages/chat/Chat";
import Stocks from "./pages/stocks/Stocks";

function App() {
  const { authUser } = useAuthContext();

  return (
    <>
      <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black">
        <ParticleBackground />

        <Routes>
          <Route path="/" element={authUser ? <Navigate to="/chat" /> : <Landing />} />
          <Route path="/login" element={authUser ? <Navigate to="/chat" /> : <Login />} />
          <Route path="/signup" element={authUser ? <Navigate to="/chat" /> : <Signup />} />
          <Route path="/chat" element={authUser ? <Chat /> : <Navigate to="/" />} />
          <Route path="/stocks" element={authUser ? <Stocks /> : <Navigate to="/" />} />
        </Routes>

        <Toaster />
      </div>
    </>
  )
}

export default App;
