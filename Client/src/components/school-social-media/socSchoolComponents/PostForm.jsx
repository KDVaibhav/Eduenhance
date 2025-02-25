import React, { useState } from "react";
import ImagePreview from "./ImagePreview";

const PostForm = ({ addPost }) => {
  const [content, setContent] = useState("");
  const [image, setImage] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (content.trim()) {
      addPost({
        content,
        authorName: "Student",
        date: new Date().toLocaleDateString(),
        authorAvatar: "https://via.placeholder.com/40",
        image,
        likes: 0,
        comments: [],
      });
      setContent("");
      setImage(null);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white shadow-md rounded-lg p-6 mb-6"
    >
      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        className="w-full p-3 border border-gray-300 rounded-lg mb-4"
        placeholder="What's on your mind? Mention users with @ and tag with #"
        rows="4"
      />
      <div className="mb-4 flex flex-col items-start">
        <input
          type="file"
          accept="image/*"
          onChange={handleImageChange}
          className="mb-2"
        />
        {image && <ImagePreview image={image} />}
      </div>
      <button
        type="submit"
        className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
      >
        Post
      </button>
    </form>
  );
};

export default PostForm;
