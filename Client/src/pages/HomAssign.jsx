import React, { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css"; // Import CSS for react-datepicker
import "./HomAssign.css"; // Import CSS for styling

const initialAssignments = [
  {
    id: "1",
    title: "Math Homework",
    dueDate: new Date("2024-08-15"),
    description: "Complete exercises 1-20 from chapter 5.",
    status: "Not Submitted",
  },
  {
    id: "2",
    title: "History Essay",
    dueDate: new Date("2024-08-20"),
    description: "Write an essay on the Renaissance period.",
    status: "Submitted",
  },
];

const HomAssign = () => {
  const [assignments, setAssignments] = useState(initialAssignments);
  const [newAssignment, setNewAssignment] = useState({
    title: "",
    dueDate: new Date(),
    description: "",
  });
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [filterStatus, setFilterStatus] = useState("All");
  const [sortOrder, setSortOrder] = useState("asc");

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  const handleSaveAssignment = () => {
    const newAssignmentId = String(assignments.length + 1);
    const assignmentToAdd = {
      id: newAssignmentId,
      ...newAssignment,
      status: "Not Submitted",
    };
    setAssignments([...assignments, assignmentToAdd]);
    closeModal();
  };

  const handleSubmit = (id) => {
    setAssignments((prevAssignments) =>
      prevAssignments.map((assignment) =>
        assignment.id === id
          ? { ...assignment, status: "Submitted" }
          : assignment
      )
    );
  };

  const filteredAssignments = assignments.filter((assignment) =>
    filterStatus === "All" ? true : assignment.status === filterStatus
  );

  const sortedAssignments = filteredAssignments.sort((a, b) =>
    sortOrder === "asc"
      ? new Date(a.dueDate) - new Date(b.dueDate)
      : new Date(b.dueDate) - new Date(a.dueDate)
  );

  return (
    <div className="assignments-container">
      <h2>Assignments</h2>
      <div className="toolbar">
        <button className="add-button" onClick={openModal}>
          Add Assignment
        </button>
        <select
          className="filter-select"
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value)}
        >
          <option value="All">All</option>
          <option value="Not Submitted">Not Submitted</option>
          <option value="Submitted">Submitted</option>
        </select>
        <select
          className="sort-select"
          value={sortOrder}
          onChange={(e) => setSortOrder(e.target.value)}
        >
          <option value="asc">Due Date Ascending</option>
          <option value="desc">Due Date Descending</option>
        </select>
      </div>
      <ul className="assignments-list">
        {sortedAssignments.map((assignment) => (
          <li key={assignment.id} className="assignment-item">
            <h3>{assignment.title}</h3>
            <p>
              <strong>Due Date:</strong> {assignment.dueDate.toDateString()}
            </p>
            <p>
              <strong>Description:</strong> {assignment.description}
            </p>
            <p>
              <strong>Status:</strong> {assignment.status}
            </p>
            {assignment.status === "Not Submitted" && (
              <button
                className="submit-button"
                onClick={() => handleSubmit(assignment.id)}
              >
                Submit
              </button>
            )}
          </li>
        ))}
      </ul>

      {isModalOpen && (
        <div className="modal">
          <div className="modal-content">
            <span className="close" onClick={closeModal}>
              &times;
            </span>
            <h3>Add New Assignment</h3>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSaveAssignment();
              }}
            >
              <div className="form-group">
                <label>Title</label>
                <input
                  type="text"
                  value={newAssignment.title}
                  onChange={(e) =>
                    setNewAssignment({
                      ...newAssignment,
                      title: e.target.value,
                    })
                  }
                  required
                />
              </div>
              <div className="form-group">
                <label>Due Date</label>
                <DatePicker
                  selected={newAssignment.dueDate}
                  onChange={(date) =>
                    setNewAssignment({
                      ...newAssignment,
                      dueDate: date,
                    })
                  }
                  dateFormat="yyyy-MM-dd"
                  className="date-picker"
                  placeholderText="Select a due date"
                />
              </div>
              <div className="form-group">
                <label>Description</label>
                <textarea
                  value={newAssignment.description}
                  onChange={(e) =>
                    setNewAssignment({
                      ...newAssignment,
                      description: e.target.value,
                    })
                  }
                  required
                />
              </div>
              <button type="submit" className="submit-button">
                Save
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default HomAssign;
