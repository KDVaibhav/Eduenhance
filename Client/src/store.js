import { configureStore } from '@reduxjs/toolkit';
import sidebarSlice from './features/sidebarSlice';
import authSlice from './features/authSlice';

export const store = configureStore({
  reducer: {
    sidebar: sidebarSlice.reducer,
    auth: authSlice.reducer,
  },
});