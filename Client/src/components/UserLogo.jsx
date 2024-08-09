import React from 'react'
import { useSelector } from 'react-redux';
const UserLogo = () => {
  const { user } = useSelector((state)=>state.auth);
  if (!user) {
    return null;
  }
  // console.log("logo:", user);
  return (
    <div className='h-10 w-10'>
      {user.image ? (
        <img src={user.image} alt="User Avatar" className="h-full w-full rounded-full object-cover" />
      ) : (
        <span className="h-full w-full rounded-full bg-slate-300 flex items-center justify-center text-gray-600 font-bold">
          {user.username ? user.username[0].toUpperCase(): '?'}
        </span>
      )}
    </div>
  );
}

export default UserLogo