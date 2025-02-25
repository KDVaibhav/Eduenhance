// src/components/school-social-media/socSchoolComponents/Post.jsx
import React, { useState } from "react";
import "./Post.css"; // Import CSS for styling
import UserLogo from "@components/UserLogo";

const Post = ({ post, onEdit, onDelete }) => {
  const [reactions, setReactions] = useState(post.reactions || []);
  const [comment, setComment] = useState("");
  const [comments, setComments] = useState(post.comments || []);
  const [isEditing, setIsEditing] = useState(false);
  const [editText, setEditText] = useState(post.text);

  const handleReaction = (reaction) => {
    setReactions((prevReactions) => {
      const updatedReactions = [...prevReactions];
      const reactionIndex = updatedReactions.findIndex(
        (r) => r.type === reaction
      );
      if (reactionIndex === -1) {
        updatedReactions.push({ type: reaction, count: 1 });
      } else {
        updatedReactions[reactionIndex].count += 1;
      }
      return updatedReactions;
    });
  };

  const handleCommentSubmit = (e) => {
    e.preventDefault();
    setComments((prevComments) => [
      ...prevComments,
      { text: comment, timestamp: new Date().toISOString() },
    ]);
    setComment("");
  };

  const handleEditSubmit = (e) => {
    e.preventDefault();
    onEdit(post.id, editText);
    setIsEditing(false);
  };

  return (
    <div className="post bg-white p-4 rounded-lg shadow-md mb-4">
      <div className="post-header flex items-start mb-4">
        <img
          src={post.avatar || <UserLogo/>} // Replace with the actual avatar URL or a default image
          alt="User Avatar"
          className="w-12 h-12 rounded-full mr-4"
        />
        <div className="flex-1">
          <div className="flex items-center justify-between mb-2">
            <div className="post-author font-semibold text-lg">
              {post.author}
            </div>
            <div className="post-actions flex space-x-2">
              <button
                onClick={() => setIsEditing(!isEditing)}
                className="text-blue-500 hover:text-blue-700"
              >
                Edit
              </button>
              <button
                onClick={() => onDelete(post.id)}
                className="text-red-500 hover:text-red-700"
              >
                Delete
              </button>
            </div>
          </div>
          {isEditing ? (
            <form onSubmit={handleEditSubmit} className="mb-4">
              <textarea
                value={editText}
                onChange={(e) => setEditText(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-md"
                rows="3"
              />
              <button
                type="submit"
                className="bg-blue-500 text-white px-4 py-2 rounded-md mt-2"
              >
                Save
              </button>
            </form>
          ) : (
            <div className="post-content mb-4">
              <p>{post.text}</p>
              {post.image && (
                <img
                  src={post.image}
                  alt="Post"
                  className="w-full h-auto mt-2 rounded-md"
                />
              )}
            </div>
          )}
          <div className="post-reactions flex space-x-2 mb-4">
            {["Like", "Love", "Wow"].map((reaction) => (
              <button
                key={reaction}
                onClick={() => handleReaction(reaction)}
                className="reaction-button px-4 py-1 text-sm font-medium rounded-md hover:bg-gray-100"
              >
                {reaction} (
                {reactions
                  .filter((r) => r.type === reaction)
                  .reduce((acc, r) => acc + r.count, 0)}
                )
              </button>
            ))}
          </div>
          <div className="post-comments">
            <form onSubmit={handleCommentSubmit} className="flex mb-4">
              <input
                type="text"
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Add a comment..."
                className="flex-1 p-2 border border-gray-300 rounded-md"
              />
              <button
                type="submit"
                className="bg-blue-500 text-white px-4 py-2 rounded-md ml-2"
              >
                Post
              </button>
            </form>
            {comments.map((c, index) => (
              <div key={index} className="comment p-2 border-b border-gray-200">
                <p>{c.text}</p>
                <span className="text-gray-500 text-xs">
                  {new Date(c.timestamp).toLocaleTimeString()}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Post;
