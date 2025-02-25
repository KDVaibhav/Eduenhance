// src/components/school-social-media/socSchoolPages/Feed.jsx
import React, { useState } from "react";
import Post from "../socSchoolComponents/Post";

const initialPosts = [
  {
    id: "1",
    author: "Teacher A",
    text: "Don't forget to complete your homework!",
    reactions: [{ type: "Like", count: 5 }],
    comments: [
      { text: "Thanks for the reminder!", timestamp: new Date().toISOString() },
    ],
  },
  // Add more posts here
];

const Feed = () => {
  const [posts, setPosts] = useState(initialPosts);
  const [newPostText, setNewPostText] = useState("");
  const [newPostImage, setNewPostImage] = useState(null);

  const handleEditPost = (id, newText) => {
    setPosts((prevPosts) =>
      prevPosts.map((post) =>
        post.id === id ? { ...post, text: newText } : post
      )
    );
  };

  const handleDeletePost = (id) => {
    setPosts((prevPosts) => prevPosts.filter((post) => post.id !== id));
  };

  const handleAddPost = (e) => {
    e.preventDefault();
    const newPost = {
      id: String(posts.length + 1),
      author: "Student", // Or fetch the current user’s name
      text: newPostText,
      image: newPostImage ? URL.createObjectURL(newPostImage) : null,
      reactions: [],
      comments: [],
    };
    setPosts((prevPosts) => [newPost, ...prevPosts]);
    setNewPostText("");
    setNewPostImage(null);
  };

  return (
    <div className="feed p-4">
      <div className="add-post bg-white p-4 rounded-lg shadow-md mb-4">
        <h2 className="text-xl font-semibold mb-2">Create a Post</h2>
        <form onSubmit={handleAddPost}>
          <textarea
            value={newPostText}
            onChange={(e) => setNewPostText(e.target.value)}
            placeholder="What's on your mind?"
            className="w-full p-2 border border-gray-300 rounded-md mb-2"
            rows="4"
            required
          />
          <input
            type="file"
            onChange={(e) => setNewPostImage(e.target.files[0])}
            className="mb-2"
          />
          {newPostImage && (
            <div className="mb-2">
              <img
                src={URL.createObjectURL(newPostImage)}
                alt="Preview"
                className="w-full h-auto rounded-lg"
              />
            </div>
          )}
          <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded-md"
          >
            Post
          </button>
        </form>
      </div>

      {posts.map((post) => (
        <Post
          key={post.id}
          post={post}
          onEdit={handleEditPost}
          onDelete={handleDeletePost}
        />
      ))}
    </div>
  );
};

export default Feed;
