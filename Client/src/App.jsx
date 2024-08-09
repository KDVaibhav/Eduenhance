import React, { useEffect } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  useParams,
  Navigate,
} from "react-router-dom";
import Cookies from "js-cookie";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Admin from "./Routes/Admin/Admin";
import Teacher from "./Routes/Teachers/Teacher";
import Student from "./Routes/Students/Student";
import Loader from "@components/Loader";
import Landing from "./pages/Landing";
import Navbar from "@components/Navbar";
import Sidebar from "@components/Sidebar";
import { setOptionsByRole } from "./features/sidebarSlice";
import { useDispatch, useSelector } from "react-redux";
import { setAuth, setLoading } from './features/authSlice';
const roleComponents = {
  admin: Admin,
  teacher: Teacher,
  student: Student,
};

const App = () => {
  const dispatch = useDispatch();
  const { isAuthenticated, user } = useSelector((state) => state.auth);
  useEffect(() => {
    if (user && user.role) {
      dispatch(setOptionsByRole(user.role.toLowerCase()));
    }
  }, [user, dispatch]);

  useEffect(() => {
    const simulatedUser = Cookies.get("user");
    if (simulatedUser) {
      const parsedUser = JSON.parse(simulatedUser);
      dispatch(setAuth({ isAuthenticated: true, user: parsedUser }))
      
    }
    dispatch(setLoading(false));
  }, [dispatch]);
  return (
    <div className="flex h-screen overflow-hidden">
      <BrowserRouter>
        <Sidebar />
        <div className="flex flex-1 flex-col overflow-hidden">
          <Navbar />
          <main className="flex-1 overflow-x-hidden overflow-y-auto">
            <Routes>
              <Route exact path="/" element={<Landing />} />
              <Route
                exact
                path="/login"
                element={isAuthenticated ? <Landing /> : <Login />}
              />
              <Route exact path="/signup" element={<Signup />} />
              <Route
                exact
                path="/:role/*"
                element={<PrivateRoute isAuthenticated={isAuthenticated} />}
              />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </div>
  );
};

function PrivateRoute({ isAuthenticated }) {
  const { role } = useParams();
  const { user, isLoading } = useSelector(
    (state) => state.auth
  );
  if (isLoading) return <Loader />;
  if (!isAuthenticated) return <Navigate to="/login" />;
  const RoleComponent = roleComponents[role];
  if (!user || !user.role) {
    console.error("User or user role is undefined");
    return <Navigate to="/login" />;
  }
  if (!RoleComponent || user.role.toLowerCase() !== role) {
    return <Navigate to={`/${user.role.toLowerCase()}`} />;
  }
  return <RoleComponent />;
}

export default App;
