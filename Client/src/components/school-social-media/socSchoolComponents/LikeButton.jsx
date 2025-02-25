import React, { useState } from "react";

const LikeButton = ({ likes }) => {
  const [liked, setLiked] = useState(false);
  const [likeCount, setLikeCount] = useState(likes);

  const handleLike = () => {
    setLiked(!liked);
    setLikeCount(likeCount + (liked ? -1 : 1));
  };

  return (
    <button
      onClick={handleLike}
      className={`text-lg ${liked ? "text-red-500" : "text-gray-500"}`}
    >
      ❤️ {likeCount}
    </button>
  );
};

export default LikeButton;
