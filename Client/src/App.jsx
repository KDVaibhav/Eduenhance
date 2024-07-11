import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "./App.css";
import Navbar from "./components/Navbar";
import Dashboard from "./components/Dashboard";
import Login from "./components/Login";
import Signup from "./components/Signup";
import Landing from "./components/Landing";
import { useState } from "react";
import { useAuth } from "./hooks/useAuth";

function App() {
  const [isAuthenticated, user, login, logout] = useAuth();

  return (
    <div>
      <BrowserRouter>
        <Navbar
          isAuthenticated={isAuthenticated}
          user={user}
          onLogout={logout}
        />
        <Routes>
          <Route exact path="/" element={<Landing />} />
          <Route exact path="/login" element={<Login handleAuth={login} />} />
          <Route exact path="/signup" element={<Signup handleAuth={login} />} />
          <Route
            exact
            path="/dashboard"
            element={
              <PrivateRoute isAuthenticated={isAuthenticated}>
                <Dashboard user={user} />
              </PrivateRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

function PrivateRoute({ children, isAuthenticated }) {
  return isAuthenticated ? children : <Navigate to="/login" />;
}

export default App;
