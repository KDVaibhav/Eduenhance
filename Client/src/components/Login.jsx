import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
const backendLink = "https://localhost:3000/api/";

const Login = ({ handleAuth }) => {
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleFormSubmit = async () => {
    const isEmail = identifier.includes("@" && ".");
    let data;
    if (isEmail) {
      data = {
        email: identifier,
        password: password,
      };
    } else {
      data = {
        username: identifier,
        password: password,
      };
    }
    try {
      const response = await axios.post(`${backendLink}login`, data);
      console.log("Login Successful");
      localStorage.setItem("token", response.data.token);
      handleAuth();
      navigate("/dashboard");
    } catch (error) {
      console.error("Login error", error.response.data);
      setError(error.response.data.message);
    }
  };
  return (
    <div className="flex h-[calc(80vh)]  justify-center">
      <div className="flex w-2/3 bg-slate-200 border border-slate-300 rounded-xl">
        <div className="flex flex-col items-center p-20 pt-16 lg:w-1/2 w-full">
          <h1 className="text-4xl font-bold pb-10 text-blue-500">Login</h1>
          {error && <div>{error}</div>}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleFormSubmit();
            }}
            className="flex flex-col p-5 gap-5 justify-center border-2 bg-slate-400 h-5/6 w-5/6 border-blue-300 rounded-lg"
          >
            <div className="flex flex-col">
              <label>Username or Email</label>
              <input
                type="text"
                placeholder="Enter Username Or Email"
                value={identifier}
                onChange={(e) => setIdentifier(e.target.value)}
              />
            </div>
            <div className="flex flex-col">
              <label>Password</label>
              <input
                type="password"
                placeholder="Enter Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <button
              type="submit"
              className="rounded-lg bg-blue-600 text-slate-50 h-10"
            >
              Login
            </button>
            <div>
              <span>Didn't have an account </span>
              <Link
                to="/signUp"
                className="underline underline-offset-2 text-blue-500"
              >
                Sign Up
              </Link>
            </div>
          </form>
        </div>
        <div className="hidden lg:w-1/2">
          <div className="bg-blue-400">
            <img src=""></img>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
