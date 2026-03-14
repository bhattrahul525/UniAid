import api from "./client";

export const loginUser = async (data) => {
  const response = await api.post("/user/login", {
    email: data.username,
    password: data.password
  });

  return response.data;
};

export const registerUser = async (data) => {
  const response = await api.post("/user/register", {
    email: data.email,
    password: data.password
  });

  return response.data;
};