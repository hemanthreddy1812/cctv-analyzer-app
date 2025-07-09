import React from "react";

const LiveStream = () => {
  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-2">Live CCTV Stream</h2>
      <img
        src="http://localhost:5000/video_feed"
        alt="Live CCTV"
        className="w-full border rounded"
      />
    </div>
  );
};

export default LiveStream;
