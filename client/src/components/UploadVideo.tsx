import React, { useState } from "react";
import { uploadVideo } from "../utils/api";

const UploadVideo = () => {
  const [video, setVideo] = useState<File | null>(null);
  const [response, setResponse] = useState<any>(null);

  const handleUpload = async () => {
    if (!video) return;
    const formData = new FormData();
    formData.append("video", video);
    const res = await uploadVideo(formData);
    setResponse(res.data);
  };

  return (
    <div className="p-4">
      <input type="file" accept="video/*" onChange={(e) => setVideo(e.target.files?.[0] || null)} />
      <button onClick={handleUpload} className="bg-blue-500 px-4 py-2 text-white mt-2">Upload</button>
      {response && (
        <div className="mt-4">
          <p>People: {response.people}</p>
          <p>Vehicles: {response.vehicles}</p>
          <p>Cars: {response.car}</p>
          <p>Bikes: {response.bike}</p>
        </div>
      )}
    </div>
  );
};

export default UploadVideo;
