import React, { useState, useEffect } from "react";

const initialAttendance = [
  { date: "2024-08-01", status: "Present" },
  { date: "2024-08-02", status: "Absent" },
  { date: "2024-08-03", status: "Present" },
  { date: "2024-08-04", status: "Late" },
  { date: "2024-08-05", status: "Present" },
  { date: "2024-08-06", status: "Absent" },
];

const Attendance = () => {
  const [attendance, setAttendance] = useState(initialAttendance);
  const [filter, setFilter] = useState("All");

  useEffect(() => {
    // Fetch attendance data from an API here if needed
  }, []);

  const filteredAttendance = attendance.filter((entry) => {
    if (filter === "All") return true;
    return entry.status === filter;
  });

  const attendanceSummary = {
    present: attendance.filter((entry) => entry.status === "Present").length,
    absent: attendance.filter((entry) => entry.status === "Absent").length,
    late: attendance.filter((entry) => entry.status === "Late").length,
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow-md max-w-3xl mx-auto">
      <h2 className="text-3xl font-bold mb-6 text-gray-800">Attendance</h2>

      <div className="flex justify-between items-center mb-4">
        <div className="flex space-x-2">
          <button
            className={`px-4 py-2 rounded-full ${
              filter === "All"
                ? "bg-blue-500 text-white"
                : "bg-gray-200 text-gray-800"
            }`}
            onClick={() => setFilter("All")}
          >
            All
          </button>
          <button
            className={`px-4 py-2 rounded-full ${
              filter === "Present"
                ? "bg-green-500 text-white"
                : "bg-gray-200 text-gray-800"
            }`}
            onClick={() => setFilter("Present")}
          >
            Present
          </button>
          <button
            className={`px-4 py-2 rounded-full ${
              filter === "Absent"
                ? "bg-red-500 text-white"
                : "bg-gray-200 text-gray-800"
            }`}
            onClick={() => setFilter("Absent")}
          >
            Absent
          </button>
          <button
            className={`px-4 py-2 rounded-full ${
              filter === "Late"
                ? "bg-yellow-500 text-white"
                : "bg-gray-200 text-gray-800"
            }`}
            onClick={() => setFilter("Late")}
          >
            Late
          </button>
        </div>

        <div className="text-right">
          <h3 className="text-lg font-semibold">Summary</h3>
          <p className="text-green-600">Present: {attendanceSummary.present}</p>
          <p className="text-red-600">Absent: {attendanceSummary.absent}</p>
          <p className="text-yellow-600">Late: {attendanceSummary.late}</p>
        </div>
      </div>

      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border border-gray-200">
          <thead>
            <tr className="bg-gray-200 text-gray-600 uppercase text-sm leading-normal">
              <th className="py-3 px-6 text-left">Date</th>
              <th className="py-3 px-6 text-left">Status</th>
            </tr>
          </thead>
          <tbody className="text-gray-600 text-sm font-light">
            {filteredAttendance.map((entry) => (
              <tr
                key={entry.date}
                className="border-b border-gray-200 hover:bg-gray-100"
              >
                <td className="py-3 px-6 text-left whitespace-nowrap">
                  {entry.date}
                </td>
                <td
                  className={`py-3 px-6 text-left whitespace-nowrap font-semibold ${
                    entry.status === "Present"
                      ? "text-green-600"
                      : entry.status === "Absent"
                      ? "text-red-600"
                      : "text-yellow-600"
                  }`}
                >
                  {entry.status}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Attendance;
