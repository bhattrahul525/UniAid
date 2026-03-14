import { createSlice } from "@reduxjs/toolkit";

const storedAuth = localStorage.getItem("auth");

const initialState = storedAuth
  ? JSON.parse(storedAuth)
  : {
      token: null,
      user: null,
      isAuthenticated: false
    };

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    setAuth(state, action) {
      state.token = action.payload.token;
      state.user = action.payload.user;
      state.isAuthenticated = true;
    },
    logout: (state) => {
      state.token = null;
      state.user = null;
      state.isAuthenticated = false;
      localStorage.removeItem("auth");
    }
  }
});

export const { setAuth, logout } = authSlice.actions;
export default authSlice.reducer;
