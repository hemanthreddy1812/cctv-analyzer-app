import React, { useEffect, useState } from "react";
import axios from "axios";

const LiveCounts = () => {
  const [counts, setCounts] = useState({ person: 0, car: 0, bike: 0 });

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await axios.get("http://localhost:5000/counts");
        setCounts(res.data);
      } catch (err) {
        console.error("Failed to fetch counts");
      }
    }, 1000); // every 1 second

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex gap-6 mb-4 text-lg">
      <div>👤 People: {counts.person}</div>
      <div>🚗 Cars: {counts.car}</div>
      <div>🛵 Bikes: {counts.bike}</div>
    </div>
  );
};

export default LiveCounts;
