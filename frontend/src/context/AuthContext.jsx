import { createContext, useContext, useState } from "react";
import axiosClient from "../api/axiosClient";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(
    localStorage.getItem("access_token") || null,
  );

  const login = async (email, password) => {
    try {
      // FastAPI OAuth2PasswordRequestForm expects form-data or adjust if using JSON UserLogin schema
      const response = await axiosClient.post("/auth/login", {
        email,
        password,
      });
      const { access_token, user: userData } = response.data;

      localStorage.setItem("access_token", access_token);
      setToken(access_token);
      setUser(userData);
      return { success: true };
    } catch (error) {
      return {
        success: false,
        message: error.response?.data?.detail || "Invalid credentials",
      };
    }
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
