import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import Hamburger from './Hamburger';
import UserLogo from './UserLogo';
const Navbar = ({isAuthenticated}) => {
  const [open, setOpen] = useState(false);
  const handleToggle = () => {
    setOpen(!open);
    if (open) {
      toggleSidebar;
    }
  }
  return (
    <div className="flex bg-gray-700 mb-10 p-4 text-white ">
      <div className="flex items-center w-1/3">
        <div className="lg:hidden p-2 hover:bg-slate-600 hover: rounded-lg" onClick={handleToggle}>
          <Hamburger open={open} />
        </div>
        <Link to="/" className="flex items-center p-2">
          <img src="/favicon.svg" className="w-8" />
          <p className="pl-2 text-2xl">EDUEnhance</p>
        </Link>
      </div>
      <div className="flex items-center w-2/3 justify-end">
        {isAuthenticated ? (<div className="flex items-center justify-center gap-5">
          <Link to="/login" className="bg-blue-400 p-2 rounded-lg ">
            Login
          </Link>
          <Link
            to="/signup"
            className="bg-blue-400 p-2 rounded-lg text-slate-200"
          >
            Signup
          </Link>
        </div>) : (<UserLogo/>)}
      </div>
    </div>
  );
}

export default Navbar