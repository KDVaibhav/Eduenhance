import { studentOptions } from "../data";
import { createSlice } from "@reduxjs/toolkit";
const initialState = {
  options:[],
}

export const sidebarSlice = createSlice({
  name: 'sidebar',
  initialState,
  reducers: {
    setOptions: (state, action) => {
      state.options = action.payload;
    },
    setOptionsByRole: (state, action) => {
      switch (action.payload) {
        case 'student':
          state.options = studentOptions;
          break;
        case 'teacher':
          state.options = teacherOptions;
          break;
        case 'admin':
          state.options = adminOptions;
          break;
        default:
          state.options = [];
      }
    },
  },
});

export const { setOptions, setOptionsByRole } = sidebarSlice.actions;
export default sidebarSlice;