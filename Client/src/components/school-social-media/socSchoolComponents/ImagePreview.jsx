import React from "react";

const ImagePreview = ({ image }) => {
  return (
    <div className="mt-4">
      <img
        src={image}
        alt="Post content"
        className="w-full h-auto rounded-lg shadow-md"
      />
    </div>
  );
};

export default ImagePreview;
