// Sidebar.jsx
import React from "react";
import { Link } from "react-router-dom";
import UserLogo from "./UserLogo";
import { useSelector, useDispatch } from "react-redux";
import { toggleSidebar, logout } from "../features/authSlice";
const Sidebar = () => {
  const dispatch = useDispatch();
  const options = useSelector((state) => state.sidebar.options);
  const { isSidebarOpen, isAuthenticated, user } = useSelector(
    (state) => state.auth
  );
  // console.log(options)
  return (
    <>
      {isAuthenticated && (
        <>
          {/* Overlay for mobile */}
          <div
            className={`fixed inset-0 bg-gray-600 bg-opacity-75 z-20 lg:hidden transition-opacity duration-300 ${
              isSidebarOpen ? "opacity-100" : "opacity-0 pointer-events-none"
            }`}
            onClick={() => dispatch(toggleSidebar())}
          ></div>

          {/* Sidebar */}
          <div
            className={`fixed lg:static inset-y-0 left-0 z-30 w-64 bg-white transform transition-transform duration-300 ease-in-out lg:translate-x-0 ${
              isSidebarOpen ? "translate-x-0" : "-translate-x-full"
            } flex flex-col h-full`}
          >
            <div className="flex-grow p-6">
              <div className="flex items-center justify-between mb-6">
                <img className="h-8 w-auto" src="/favicon.svg" alt="Logo" />
                <button onClick={() => dispatch(toggleSidebar())}>
                  <svg
                    className="w-6 h-6 cursor-pointer"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>

              {options.length > 0 ? (
                <nav className="space-y-1">
                  {options.map((option, index) => (
                    <Link
                      to={`/student/${option.path}`}
                      key={index}
                      className="text-gray-900 hover:bg-gray-100 hover:text-gray-900 group flex items-center px-2 py-2 text-base leading-6 font-medium rounded-md"
                    >
                      {option.name}
                    </Link>
                  ))}
                </nav>
              ) : (
                <div>No options available</div>
              )}
            </div>

            <div className="border-t border-gray-200 p-4">
              {isAuthenticated ? (
                <div className="flex items-center">
                  <UserLogo />
                  <div className="ml-3">
                    <div className="text-base font-medium leading-none text-gray-900">
                      {user?.name}
                    </div>
                    <div className="text-sm font-medium leading-none text-gray-500">
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
                <div className="space-y-2">
                  <Link
                    to="/login"
                    className="block w-full bg-indigo-500 hover:bg-indigo-400 text-white font-bold py-2 px-4 rounded transition duration-300 text-center"
                  >
                    Login
                  </Link>
                  <Link
                    to="/signup"
                    className="block w-full bg-white text-indigo-600 hover:bg-indigo-100 font-bold py-2 px-4 rounded transition duration-300 text-center border border-indigo-600"
                  >
                    Sign Up
                  </Link>
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </>
  );
};

export default Sidebar;
