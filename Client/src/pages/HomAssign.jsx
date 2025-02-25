import React, { useState } from "react";
import "./HomAssign.css"; // Import CSS for styling

const initialAssignments = [
  {
    id: "1",
    title: "Math Homework",
    dueDate: "2024-08-15",
    description: "Complete exercises 1-20 from chapter 5.",
    status: "Not Submitted",
    file: null,
    submissionText: null,
  },
  {
    id: "2",
    title: "History Essay",
    dueDate: "2024-08-20",
    description: "Write an essay on the Renaissance period.",
    status: "Submitted",
    file: "history_essay.pdf",
    submissionText: null,
  },
];

const HomAssign = () => {
  const [assignments, setAssignments] = useState(initialAssignments);
  const [newAssignment, setNewAssignment] = useState({
    title: "",
    dueDate: "",
    description: "",
  });
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [sortOrder, setSortOrder] = useState("none");
  const [file, setFile] = useState(null);
  const [submissionText, setSubmissionText] = useState("");

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  const handleSaveAssignment = () => {
    const newAssignmentId = String(assignments.length + 1);
    const assignmentToAdd = {
      id: newAssignmentId,
      ...newAssignment,
      status: "Not Submitted",
      file: file ? URL.createObjectURL(file) : null,
      submissionText: submissionText,
    };
    setAssignments([...assignments, assignmentToAdd]);
    setFile(null);
    setSubmissionText("");
    closeModal();
  };

  const handleSubmit = (id) => {
    setAssignments((prevAssignments) =>
      prevAssignments.map((assignment) =>
        assignment.id === id
          ? {
              ...assignment,
              status: "Submitted",
              file: file ? URL.createObjectURL(file) : assignment.file,
              submissionText: submissionText || assignment.submissionText,
            }
          : assignment
      )
    );
    setFile(null);
    setSubmissionText("");
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSortChange = (e) => {
    setSortOrder(e.target.value);
  };

  const sortedAssignments = [...assignments].sort((a, b) => {
    if (sortOrder === "dueDateAsc") {
      return new Date(a.dueDate) - new Date(b.dueDate);
    } else if (sortOrder === "dueDateDesc") {
      return new Date(b.dueDate) - new Date(a.dueDate);
    } else if (sortOrder === "status") {
      return a.status.localeCompare(b.status);
    } else {
      return 0;
    }
  });

  return (
    <div className="assignments-container">
      <h2 className="header">Assignments</h2>
      <div className="controls">
        <button className="add-button" onClick={openModal}>
          + Add Assignment
        </button>
        <select
          className="sort-select"
          onChange={handleSortChange}
          value={sortOrder}
        >
          <option value="none">Sort By</option>
          <option value="dueDateAsc">Due Date (Asc)</option>
          <option value="dueDateDesc">Due Date (Desc)</option>
          <option value="status">Status</option>
        </select>
      </div>
      <ul className="assignments-list">
        {sortedAssignments.map((assignment) => (
          <li key={assignment.id} className="assignment-item">
            <div className="assignment-header">
              <h3>{assignment.title}</h3>
              <span
                className={`status ${assignment.status
                  .toLowerCase()
                  .replace(" ", "-")}`}
              >
                {assignment.status}
              </span>
            </div>
            <p>
              <strong>Due Date:</strong> {assignment.dueDate}
            </p>
            <p>
              <strong>Description:</strong> {assignment.description}
            </p>
            {assignment.submissionText && (
              <p>
                <strong>Submission:</strong> {assignment.submissionText}
              </p>
            )}
            {assignment.file && (
              <p>
                <strong>Submitted File:</strong>{" "}
                <a
                  href={assignment.file}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {assignment.file.split("/").pop()}
                </a>
              </p>
            )}
            {assignment.status === "Not Submitted" && (
              <div className="submission-options">
                <textarea
                  placeholder="Type your submission here..."
                  value={submissionText}
                  onChange={(e) => setSubmissionText(e.target.value)}
                />
                <input type="file" accept=".pdf" onChange={handleFileChange} />
                <button
                  className="submit-button"
                  onClick={() => handleSubmit(assignment.id)}
                >
                  Submit
                </button>
              </div>
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
                <input
                  type="date"
                  value={newAssignment.dueDate}
                  onChange={(e) =>
                    setNewAssignment({
                      ...newAssignment,
                      dueDate: e.target.value,
                    })
                  }
                  required
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
