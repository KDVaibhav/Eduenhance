import React, { useState, useRef, useEffect } from "react";
import Calendar from "@toast-ui/react-calendar";
import "@toast-ui/calendar/dist/toastui-calendar.min.css";
import "./studentCalender.css";
const initialEvents = [
  {
    id: "1",
    calendarId: "1",
    title: "Math Exam",
    category: "time",
    start: "2024-07-20T10:00:00",
    end: "2024-07-20T12:00:00",
    bgColor: "#FF6347",
  },
  {
    id: "2",
    calendarId: "1",
    title: "Art Class",
    category: "allday",
    start: "2024-07-25",
    end: "2024-07-25",
    bgColor: "#FFB6C1",
  },
];

const colors = [
  { name: "Tomato", value: "#FF6347" },
  { name: "Pink", value: "#FFB6C1" },
  { name: "Gold", value: "#FFD700" },
  { name: "Green", value: "#90EE90" },
  { name: "SkyBlue", value: "#87CEEB" },
  { name: "Purple", value: "#DDA0DD" },
  { name: "Orange", value: "#FFA500" },
  { name: "Red", value: "#FF0000" },
  { name: "Blue", value: "#0000FF" },
  { name: "Lime", value: "#00FF00" },
];

const StudentCalendar = () => {
  const [events, setEvents] = useState(initialEvents);
  const [newEvent, setNewEvent] = useState({
    title: "",
    start: "",
    end: "",
    bgColor: colors[0].value,
    recurrence: "none",
    reminder: "none",
  });
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [view, setView] = useState("month");
  const [currentDate, setCurrentDate] = useState(new Date());
  const calendarRef = useRef(null);

  useEffect(() => {
    const calendarInstance = calendarRef.current.getInstance();
    setCurrentDate(calendarInstance.getDate());
  }, []);

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  const handleSaveEvent = () => {
    const newEventId = String(events.length + 1);
    const eventToAdd = {
      id: newEventId,
      calendarId: "1",
      title: newEvent.title,
      category: "time",
      start: newEvent.start,
      end: newEvent.end,
      bgColor: newEvent.bgColor,
      recurrence: newEvent.recurrence,
      reminder: newEvent.reminder,
    };
    setEvents([...events, eventToAdd]);
    closeModal();
  };

  const handleChangeView = (view) => {
    if (calendarRef.current) {
      calendarRef.current.getInstance().changeView(view);
      setView(view);
    }
  };

  const handleNavigation = (direction) => {
    const calendarInstance = calendarRef.current.getInstance();
    if (direction === "prev") {
      calendarInstance.prev();
    } else if (direction === "next") {
      calendarInstance.next();
    }
    setCurrentDate(calendarInstance.getDate());
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    if (isNaN(date)) {
      console.error("Invalid Date passed to formatDate:", dateString);
      return "Invalid Date";
    }
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
    });
  };

  const onBeforeUpdateSchedule = (event) => {
    const { schedule, changes } = event;

    setEvents((prevEvents) =>
      prevEvents.map((ev) =>
        ev.id === schedule.id
          ? {
              ...ev,
              ...changes,
            }
          : ev
      )
    );
  };

  return (
    <div className="funky-calendar">
      <div className="calendar-toolbar">
        <div className="navigation">
          <button onClick={() => handleNavigation("prev")}>Previous</button>
          <span className="current-month">{formatDate(currentDate)}</span>
          <button onClick={() => handleNavigation("next")}>Next</button>
        </div>
        <button onClick={openModal}>Add Event</button>
        <div className="view-selector">
          <div className="hidden lg:block">
            <button
              className={`view-button ${view === "month" ? "active" : ""}`}
              onClick={() => handleChangeView("month")}
            >
              Month View
            </button>
            <button
              className={`view-button ${view === "week" ? "active" : ""}`}
              onClick={() => handleChangeView("week")}
            >
              Week View
            </button>
            <button
              className={`view-button ${view === "day" ? "active" : ""}`}
              onClick={() => handleChangeView("day")}
            >
              Day View
            </button>
          </div>
          <select
            className="view-dropdown lg:hidden"
            value={view}
            onChange={(e) => handleChangeView(e.target.value)}
          >
            <option value="month">Month View</option>
            <option value="week">Week View</option>
            <option value="day">Day View</option>
          </select>
        </div>
      </div>
      <Calendar
        ref={calendarRef}
        height="500px"
        events={events}
        isReadOnly={false}
        useCreationPopup={true}
        useDetailPopup={true}
        view={view}
        onBeforeUpdateSchedule={onBeforeUpdateSchedule}
        draggable={true}
      />

      {isModalOpen && (
        <div className="modal">
          <div className="modal-content">
            <span className="close" onClick={closeModal}>
              &times;
            </span>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSaveEvent();
              }}
            >
              <div className="mb-4">
                <label className="block mb-2">Event Title</label>
                <input
                  type="text"
                  value={newEvent.title}
                  onChange={(e) =>
                    setNewEvent({ ...newEvent, title: e.target.value })
                  }
                  className="input"
                />
              </div>
              <div className="mb-4">
                <label className="block mb-2">Start Date</label>
                <input
                  type="datetime-local"
                  value={newEvent.start}
                  onChange={(e) =>
                    setNewEvent({ ...newEvent, start: e.target.value })
                  }
                  className="input"
                />
              </div>
              <div className="mb-4">
                <label className="block mb-2">End Date</label>
                <input
                  type="datetime-local"
                  value={newEvent.end}
                  onChange={(e) =>
                    setNewEvent({ ...newEvent, end: e.target.value })
                  }
                  className="input"
                />
              </div>
              <div className="mb-4">
                <label className="block mb-2">Color</label>
                <select
                  value={newEvent.bgColor}
                  onChange={(e) =>
                    setNewEvent({ ...newEvent, bgColor: e.target.value })
                  }
                  className="input"
                >
                  {colors.map((color) => (
                    <option key={color.value} value={color.value}>
                      {color.name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="mb-4">
                <label className="block mb-2">Recurrence</label>
                <select
                  value={newEvent.recurrence}
                  onChange={(e) =>
                    setNewEvent({ ...newEvent, recurrence: e.target.value })
                  }
                  className="input"
                >
                  <option value="none">None</option>
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                </select>
              </div>
              <div className="mb-4">
                <label className="block mb-2">Reminder</label>
                <select
                  value={newEvent.reminder}
                  onChange={(e) =>
                    setNewEvent({ ...newEvent, reminder: e.target.value })
                  }
                  className="input"
                >
                  <option value="none">None</option>
                  <option value="10">10 minutes before</option>
                  <option value="30">30 minutes before</option>
                  <option value="60">1 hour before</option>
                </select>
              </div>
              <button type="submit" className="btn">
                Save Event
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default StudentCalendar;
