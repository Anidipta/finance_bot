import { Route, Routes } from "react-router-dom";
import { Toaster } from "react-hot-toast";

import Landing from "./pages/landing/Landing";
import Signup from "./pages/auth/Signup";
import Login from "./pages/auth/Login";
import ParticleBackground from "./components/ParticleBackground";
import Chat from "./pages/chat/Chat";

function App() {
  return (
    <>
      <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black">
        <ParticleBackground />

        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/login" element={<Login />} />
          <Route path="/chat" element={<Chat />} />
        </Routes>

        <Toaster />
      </div>
    </>
  )
}

export default App;
