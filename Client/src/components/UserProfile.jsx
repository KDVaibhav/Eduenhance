import React from "react";
import { useSelector } from "react-redux";

const UserProfile = () => {
  const { user } = useSelector((state) => state.auth);

  return (
    <div className="flex justify-end">
      <div className="max-w-72 w-1/3 h-96 overflow-hidden bg-white rounded-3xl">
        <div className="relative">
          <svg
            className="absolute inset-0 w-full"
            viewBox="0 0 400 200"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M0 0H400V180C400 180 316.5 154 200 180C83.5 206 0 180 0 180V0Z"
              fill="url(#paint0_linear_9_2484)"
              stroke="black"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <defs>
              <linearGradient
                id="paint0_linear_9_2484"
                x1={9.5}
                y1={8.99999}
                x2={400}
                y2={180}
                gradientUnits="userSpaceOnUse"
              >
                <stop stopColor="#5C24FC" />
                <stop offset={1} stopColor="#706982" />
              </linearGradient>
            </defs>
          </svg>

          <div className="absolute flex w-full z-10 h-full p-2 text-white">
            <div className="w-1/2 p-4">
              <div className="font-bold text-2xl">{user.username}</div>
              <div className="">{user.class}th</div>
            </div>
            <div className="w-1/2">
              <img src="/schoolBoy.svg" alt="schoolboy" />
            </div>
          </div>
        </div>
        <div className="mt-28 lg:mt-32 p-4">
          <div className="mid-heading">Biography</div>
          <div className="p-2">
            <img
              src="/boyAvatar.svg"
              alt="Boy Avatar"
              className="w-12 rounded-lg"
            />
          </div>
          <div className="">

          </div>
        </div>
      </div>
    </div>
  );
};

export default UserProfile;
