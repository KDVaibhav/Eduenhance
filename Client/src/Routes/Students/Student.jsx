import React from "react";
import { Routes, Route } from "react-router-dom";
import Performance from "../../pages/Performance";
import Timetable from "../../pages/Timetable";
import Announcement from "../../pages/Announcement";
import Dashboard from "../../pages/Dashboard";
import HomAssign from "../../pages/HomAssign";
const Student = () => {
  return (
    <div className="bg-slate-200 p-4 h-screen">
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/performance" element={<Performance />} />
        <Route path="/timetable" element={<Timetable />} />
        <Route path="/announcements" element={<Announcement />} />
        <Route path="/homassign" element={<HomAssign />} />
      </Routes>

    </div>
  );
};

export default Student;
