import { createSlice } from '@reduxjs/toolkit';
import Cookies from 'js-cookie';
const initialState = {
  isAuthenticated: false,
  user: null,
  isLoading: true,
  isSidebarOpen: false,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setAuth(state, action) {
      state.isAuthenticated = action.payload.isAuthenticated;
      state.user = action.payload.user;
    },
    setLoading(state, action) {
      state.isLoading = action.payload;
    },
    toggleSidebar(state) {
      state.isSidebarOpen = !state.isSidebarOpen;
    },
    logout(state) {
      state.isAuthenticated = false;
      state.user = null;
      Cookies.remove('user');
    },
  },
});

export const { setAuth, setLoading, toggleSidebar, logout } = authSlice.actions;

export default authSlice;