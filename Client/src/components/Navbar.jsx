import React, { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import UserLogo from "./UserLogo";
import { useSelector, useDispatch } from "react-redux";
import { toggleSidebar, logout } from "../features/authSlice";
const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const { isAuthenticated, user } = useSelector((state) => state.auth);
  const location = useLocation();
  const role = user?.role?.toLowerCase() || "student";
  const isOnDashboard = location.pathname === `/${role}`;
  const toggleMenu = () => setIsOpen(!isOpen);
  const dispatch = useDispatch();
  return (
    <nav className="bg-indigo-600 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            {/* Sidebar toggle button */}
            {isAuthenticated && (<>
              <button
                onClick={()=>dispatch(toggleSidebar())}
                className=" text-white hover:bg-indigo-500 px-3 py-2 rounded-md text-sm font-medium mr-4"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 6h16M4 12h10M4 18h16"
                  />
                </svg>
              </button>

            <Link to="/" className="flex-shrink-0">
              <img className="h-8 w-8" src="/favicon.svg" alt="Logo" />
            </Link>
            <div className="hidden md:block">
              {!isOnDashboard && <div className="ml-10 flex items-baseline space-x-4">
                <Link
                  to={`/${role}`}
                  className=" flex items-center text-white hover:bg-indigo-500 px-3 py-2 rounded-md text-sm font-medium"
                  >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="white"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className="feather feather-arrow-left h-5 w-5 mr-2"
                    >
                    <line x1="19" y1="12" x2="5" y2="12" />
                    <polyline points="12 19 5 12 12 5" />
                  </svg>
                  <span>
                    Dashboard
                  </span>
                </Link>
                {/* Add more navigation items here */}
              </div>}
            </div>
            </>
            )}
          </div>
          <div className="hidden md:block">
            <div className="ml-4 flex items-center md:ml-6">
              {isAuthenticated && user ? (
                <div className="flex items-center gap-2">
                  <UserLogo user={user} />
                  {/* <span className="text-white ml-2 mr-4">{user?.name}</span> */}
                  <button
                    onClick={()=>dispatch(logout())}
                    className="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded transition duration-300"
                  >
                    Logout
                  </button>
                </div>
              ) : (
                <div className="flex items-center space-x-4">
                  <Link
                    to="/login"
                    className="bg-indigo-500 hover:bg-indigo-400 text-white font-bold py-2 px-4 rounded transition duration-300"
                  >
                    Login
                  </Link>
                  <Link
                    to="/signup"
                    className="bg-white text-indigo-600 hover:bg-indigo-100 font-bold py-2 px-4 rounded transition duration-300"
                  >
                    Sign Up
                  </Link>
                </div>
              )}
            </div>
          </div>
          <div className="-mr-2 flex md:hidden">
            <button
              onClick={toggleMenu}
              className="inline-flex items-center justify-center p-2 rounded-md text-white hover:text-white hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-indigo-600 focus:ring-white"
            >
              <span className="sr-only">Open main menu</span>
              {isOpen ? (
                <svg
                  className="block h-6 w-6"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  aria-hidden="true"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              ) : (
                <svg
                  className="block h-6 w-6"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  aria-hidden="true"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                </svg>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu, show/hide based on menu state */}
      <div className={`md:hidden ${isOpen ? "block" : "hidden"}`}>
        <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
          <Link
            to="/"
            className="text-white hover:bg-indigo-500 block px-3 py-2 rounded-md text-base font-medium"
          >
            Home
          </Link>
          {/* Add more navigation items here */}
        </div>
        <div className="pt-4 pb-3 border-t border-indigo-500">
          {isAuthenticated && user ? (
            <div className="flex items-center px-5">
              <UserLogo user={user} />
              <div className="ml-3">
                <div className="text-base font-medium leading-none text-white">
                  {user?.name}
                </div>
                <div className="text-sm font-medium leading-none text-indigo-300">
                  {user?.email}
                </div>
              </div>
              <button
                onClick={()=>dispatch(logout())}
                className="ml-auto bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded transition duration-300"
              >
                Logout
              </button>
            </div>
          ) : (
            <div className="mt-3 px-2 space-y-1">
              <Link
                to="/login"
                className="block bg-indigo-500 hover:bg-indigo-400 text-white font-bold py-2 px-4 rounded transition duration-300"
              >
                Login
              </Link>
              <Link
                to="/signup"
                className="block bg-white text-indigo-600 hover:bg-indigo-100 font-bold py-2 px-4 rounded transition duration-300 mt-2"
              >
                Sign Up
              </Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
