import React, { useState } from "react";

const reactions = [
  { type: "Like", icon: "👍" },
  { type: "Love", icon: "❤️" },
  { type: "Haha", icon: "😂" },
  { type: "Wow", icon: "😮" },
  { type: "Sad", icon: "😢" },
  { type: "Angry", icon: "😡" },
];

const Reactions = ({ reactionsCount, onReaction }) => {
  const [showReactions, setShowReactions] = useState(false);

  return (
    <div className="relative flex items-center space-x-2">
      <button
        onClick={() => setShowReactions(!showReactions)}
        className="flex items-center space-x-1 text-gray-600 hover:text-gray-900 focus:outline-none"
      >
        <span>{reactionsCount} Reactions</span>
        <span className="text-xl">❤️</span>
      </button>
      {showReactions && (
        <div className="absolute top-8 left-0 bg-white border border-gray-300 rounded-lg shadow-lg p-2 w-32">
          {reactions.map((reaction) => (
            <button
              key={reaction.type}
              onClick={() => onReaction(reaction.type)}
              className="flex items-center space-x-2 px-2 py-1 hover:bg-gray-100 rounded-md transition-colors"
            >
              <span className="text-xl">{reaction.icon}</span>
              <span>{reaction.type}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default Reactions;
