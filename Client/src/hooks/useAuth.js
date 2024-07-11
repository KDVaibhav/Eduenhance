import { useState, useEffect } from "react";
import Cookies from "js-cookie";

const API_URL = process.env.REACT_APP_API_URL;
export function useAuth() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = Cookies.get("auth_token");
    if (token) {
      validateToken(token);
    }
  }, []);

  const validateToken = async (token) => {
    try {
      const response = await fetch(`${API_URL}validate-token`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ token }),
      });
      if (response.ok) {
        const userData = await response.json();
        setIsAuthenticated(true);
        setUser(userData);
      } else {
        Cookies.remove("auth_token");
      }
    } catch (error) {
      console.error("Error validating token:", error);
    }
  };

  const login = async (credentials) => {
    try {
      const response = await fetch(`${API_URL}login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(credentials),
      });
      if (response.ok) {
        const { user, token } = await response.json();
        setIsAuthenticated(true);
        setUser(user);
        Cookies.set("auth_token", token, { expires: 7 });
        return true;
      } else {
        return false;
      }
    } catch (error) {
      console.error("Login error:", error);
      return false;
    }
  };

  const logout = () => {
    setIsAuthenticated(false);
    setUser(null);
    Cookies.remover("auth_token");
  };
  return { isAuthenticated, user, login, logout };
}
