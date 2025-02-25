import React from "react";

const Comment = ({ comment }) => {
  return (
    <div className="bg-gray-100 p-4 rounded-lg mb-2">
      <p className="text-gray-800">
        {comment.text.split(" ").map((word, index) =>
          word.startsWith("@") ? (
            <span key={index} className="text-blue-500 font-semibold">
              {word}{" "}
            </span>
          ) : (
            <span key={index}>{word} </span>
          )
        )}
      </p>
    </div>
  );
};

export default Comment;
