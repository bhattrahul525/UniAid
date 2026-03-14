export const getProfile = async (userId, api) => {
  const response = await api.get(`/user/${userId}`);
  return response.data;
};

export const upsertProfile = async (data, api) => {
  const response = await api.post("/user/profile", data);
  return response.data;
};