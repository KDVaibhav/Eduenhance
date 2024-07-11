import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
const backendLink = "https://localhost:3000/api/";

const Signup = () => {
  const [username, setUsername] = useState("");
  const [Email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleFormSubmit = async () => {
    let data = {
      username: username,
      email: email,
      password: password,
      };
    try {
      const response = await axios.post({ backendLink } + "Signup", data);
      console.log("Signup Successful");
      localStorage.setItem("token", response.data.token);
      navigate("/dashboard");
    } catch (error) {
      console.error("Signup error", error.response.data);
      setError(error.response.data.message);
    }
  };
  return (
    <div className="flex h-[calc(80vh)] justify-center">
      <div className="flex w-3/4 bg-slate-200 border border-slate-300 rounded-xl">
        <div className="flex flex-col items-center p-10 pt-16 lg:w-2/5  w-full">
          <h1 className="text-4xl font-bold pb-10 text-blue-500">Signup</h1>
          {error && <div>{error}</div>}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleFormSubmit();
            }}
            className="flex flex-col p-5 gap-5 border-2  bg-slate-400 h-5/6 w-5/6 border-blue-300 rounded-lg"
          >
            <div className="flex flex-col">
              <label>Username</label>
              <input
                type="text"
                placeholder="Enter Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </div>
            <div className="flex flex-col">
              <label>Email</label>
              <input
                type="text"
                placeholder="Enter Email"
                value={Email}
                onChange={(e) => setEmail(e.target.value)}
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
              Signup
            </button>
            <div className="flex justify-center">
              <span>Already have an account?</span>
              <Link
                to="/login"
                className="underline underline-offset-2 pl-2 text-blue-500"
              >
                login
              </Link>
            </div>
          </form>
        </div>
        <div className="hidden lg:w-1/2">
          <div className="bg-blue-400">
            <img src="favicon.ico"></img>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Signup;
