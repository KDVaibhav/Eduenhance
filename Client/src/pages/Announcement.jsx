import React, { useState } from "react";

const initialAnnouncements = [
  {
    id: "1",
    title: "School Reopening",
    date: "2024-08-01",
    category: "General",
    content:
      "The school will reopen on 15th August 2024 after the summer break.",
  },
  {
    id: "2",
    title: "Exam Schedule Released",
    date: "2024-08-02",
    category: "Exams",
    content:
      "The schedule for the mid-term exams has been released. Check the exam section for details.",
  },
  {
    id: "3",
    title: "Annual Sports Day",
    date: "2024-08-05",
    category: "Events",
    content:
      "The annual sports day will be held on 20th September 2024. Students are encouraged to participate.",
  },
];

const AnnouncementPage = () => {
  const [announcements, setAnnouncements] = useState(initialAnnouncements);
  const [filter, setFilter] = useState("All");
  const [searchTerm, setSearchTerm] = useState("");

  const filteredAnnouncements = announcements.filter((announcement) => {
    if (filter === "All" && searchTerm === "") return true;
    return (
      (filter === "All" || announcement.category === filter) &&
      (searchTerm === "" ||
        announcement.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        announcement.content.toLowerCase().includes(searchTerm.toLowerCase()))
    );
  });

  return (
    <div className="p-6 bg-white rounded-lg shadow-md max-w-5xl mx-auto">
      <h2 className="text-3xl font-bold mb-6 text-gray-800">Announcements</h2>

      <div className="flex justify-between items-center mb-6">
        <input
          type="text"
          placeholder="Search announcements..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="p-2 border border-gray-300 rounded-lg w-1/3"
        />

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
              filter === "General"
                ? "bg-green-500 text-white"
                : "bg-gray-200 text-gray-800"
            }`}
            onClick={() => setFilter("General")}
          >
            General
          </button>
          <button
            className={`px-4 py-2 rounded-full ${
              filter === "Exams"
                ? "bg-yellow-500 text-white"
                : "bg-gray-200 text-gray-800"
            }`}
            onClick={() => setFilter("Exams")}
          >
            Exams
          </button>
          <button
            className={`px-4 py-2 rounded-full ${
              filter === "Events"
                ? "bg-purple-500 text-white"
                : "bg-gray-200 text-gray-800"
            }`}
            onClick={() => setFilter("Events")}
          >
            Events
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredAnnouncements.length > 0 ? (
          filteredAnnouncements.map((announcement) => (
            <div
              key={announcement.id}
              className="p-4 bg-gray-100 rounded-lg shadow-md"
            >
              <h3 className="text-xl font-semibold text-gray-800 mb-2">
                {announcement.title}
              </h3>
              <p className="text-sm text-gray-600 mb-4">
                <strong>Date:</strong> {announcement.date}
              </p>
              <p className="text-gray-700">{announcement.content}</p>
              <p className="text-sm text-gray-500 mt-4">
                <strong>Category:</strong> {announcement.category}
              </p>
            </div>
          ))
        ) : (
          <p className="text-gray-500 text-center col-span-full">
            No announcements found.
          </p>
        )}
      </div>
    </div>
  );
};

export default AnnouncementPage;
