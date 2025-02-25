import React from "react";
import { Routes, Route } from "react-router-dom";
import Performance from "../../pages/Performance";
import Timetable from "../../pages/Timetable";
import Announcement from "../../pages/Announcement";
import Dashboard from "../../pages/Dashboard";
import HomAssign from "../../pages/HomAssign";
import Attendance from "../../pages/Attendance";
import SchoolSocialMedia from "../../pages/SchoolSocialMedia";
const Student = () => {
  return (
    <div className="bg-slate-200 p-4 h-screen">
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/performance" element={<Performance />} />
        <Route path="/timetable" element={<Timetable />} />
        <Route path="/announcements" element={<Announcement />} />
        <Route path="/homassign" element={<HomAssign />} />
        <Route path="/attendance" element={<Attendance />} />
        <Route path="/socSchool//*" element={<SchoolSocialMedia />} />

      </Routes>

    </div>
  );
};

export default Student;
