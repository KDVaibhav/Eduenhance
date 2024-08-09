import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import Cookies from "js-cookie";
import { useDispatch } from "react-redux";
import { setAuth } from "../features/authSlice";
// import axios from "axios";
// const API_URL = import.meta.env.REACT_APP_API_URL;
// const API_URL = "http://localhost:5000/";
// console.log(API_URL);

const Login = () => {
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [school, setSchool] = useState("");
  const [remember, setRemember] = useState(false);
  const [schools, setSchools] = useState([]);
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const dispatch = useDispatch();
  useEffect(() => {
    // Fetch schools from backend
    // axios
    //   .get(`${API_URL}school/getSchools`)
    //   .then((response) => setSchools(response.data.schools))
    //   .catch((error) => console.error("Error fetching schools:", error));
    const dummySchools = [
      { id: "1", name: "BNS" },
      { id: "2", name: "PMS" },
      { id: "3", name: "BRC" },
    ];
    setSchools(dummySchools);
  }, []);

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    const simulatedUser = {
      username: identifier,
      school: school,
      role: "Student",
      image: "/vaibhav.svg",
      class: "6",
    };
    try {
      if (identifier === "Vaibhav" && password === "Prabhupada@108") {
        dispatch(setAuth({ isAuthenticated: true, user: simulatedUser }));
        Cookies.set("user", JSON.stringify(simulatedUser), { expires: 7 });
        navigate(`/${simulatedUser.role.toLowerCase()}`);
        console.log("Successfully Logged in");
      } else {
        setError("Login failed. Please check your credentials.");
      }
    } catch (error) {
      console.error("Login error:", error);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="flex w-full max-w-4xl bg-white shadow-lg rounded-lg overflow-hidden">
        <div className="w-full lg:w-1/2 p-8 lg:p-12">
          <h1 className="text-3xl font-bold text-gray-800 mb-8">Login</h1>
          {error && (
            <div
              className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6"
              role="alert"
            >
              <p>{error}</p>
            </div>
          )}
          <form onSubmit={handleFormSubmit} className="space-y-6">
            <div>
              <label
                htmlFor="identifier"
                className="block text-sm font-medium text-gray-700"
              >
                Username or Email
              </label>
              <input
                id="identifier"
                type="text"
                placeholder="Enter Username or Email"
                value={identifier}
                onChange={(e) => setIdentifier(e.target.value)}
                className="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            <div>
              <label
                htmlFor="password"
                className="block text-sm font-medium text-gray-700"
              >
                Password
              </label>
              <input
                id="password"
                type="password"
                placeholder="Enter Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            <div>
              <label
                htmlFor="school"
                className="block text-sm font-medium text-gray-700"
              >
                School
              </label>
              <select
                id="school"
                value={school}
                onChange={(e) => setSchool(e.target.value)}
                className="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              >
                <option value="" disabled>
                  Select a school
                </option>
                {schools.map((school) => (
                  <option key={school.id} value={school.id}>
                    {school.name}
                  </option>
                ))}
              </select>
            </div>
            <div className="checkbox">
              <label className="block text-sm font-medium text-gray-700">
                <input
                  type="checkbox"
                  checked={remember}
                  onChange={(e) => setRemember(e.target.checked)}
                />{" "}
                Remember me
              </label>
            </div>
            <button
              type="submit"
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Login
            </button>
          </form>
          <p className="mt-8 text-center text-sm text-gray-600">
            Don't have an account?{" "}
            <Link
              to="/signup"
              className="font-medium text-indigo-600 hover:text-indigo-500"
            >
              Sign Up
            </Link>
          </p>
        </div>
        <div className="hidden lg:block lg:w-1/2 bg-cover bg-center"></div>
      </div>
    </div>
  );
};

export default Login;
