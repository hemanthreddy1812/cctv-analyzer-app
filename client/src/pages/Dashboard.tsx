import React from "react";
import LiveStream from "../components/LiveStream";
import LiveCounts from "../components/LiveCounts";

const Dashboard = () => {
  return (
    <div className="max-w-3xl mx-auto mt-10">
      <h1 className="text-3xl font-bold mb-6">CCTV Video Analyzer</h1>
      <LiveCounts />
      <LiveStream />
    </div>
  );
};

export default Dashboard;
