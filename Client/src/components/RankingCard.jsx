import React from "react";

const RankingCard = ({ name, rank, color, dir }) => {
  const arrowRotation = dir === "up" ? "0" : "180";

  return (
    <div className="rounded-2xl w-36">
      <svg
        width="100%"
        height="100%"
        viewBox="0 0 200 100"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <rect width="200" height="100" rx="20" fill={color} />

        <mask
          id="mask0"
          style={{ maskType: "alpha" }}
          maskUnits="userSpaceOnUse"
          x="0"
          y="0"
          width="200"
          height="100"
        >
          <rect width="200" height="100" rx="20" fill={color} />
        </mask>
        <g mask="url(#mask0)">
          <rect
            x="159.711"
            width="200"
            height="100"
            rx="50"
            transform="rotate(45 159.711 0)"
            fill={color}
          />
          <rect
            x="121"
            y="-21"
            width="200"
            height="100"
            rx="50"
            fill="white"
            fillOpacity="0.3"
          />
          <rect
            x="69.6261"
            y="49.6259"
            width="199"
            height="99"
            rx="49.5"
            transform="rotate(-72.7023 69.6261 49.6259)"
            stroke="white"
            strokeOpacity="0.3"
          />
        </g>
        <text
          x="10"
          y="40%"
          dominantBaseline="middle"
          textAnchor="start"
          fill="white"
          fontSize="20"
          fontFamily="Arial"
        >
          {name}
        </text>
      </svg>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          marginTop: "-35px",
          marginLeft: "10px",
          color: "white",
        }}
      >
        <span style={{ marginLeft: "5px", color: "white" }}>{rank}</span>
        <svg
          width="20"
          height="15"
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          style={{ transform: `rotate(${arrowRotation}deg)` }}
        >
          <path
            d="M12 2L2 12H7V22H17V12H22L12 2Z"
            fill="none"
            stroke="white"
            strokeWidth={2}
          />
        </svg>
      </div>
    </div>
  );
};

export default RankingCard;
