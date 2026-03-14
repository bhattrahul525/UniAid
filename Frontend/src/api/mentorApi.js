import api from "./client";

export const getMentors = async () => {
  const response = await api.get("/mentors");
  return response.data;
};

export const getMentorsAIRecommendations = async (params = {}) => {
  const payload = Object.fromEntries(
    Object.entries({
      request_text: params.requestText,
      top_k: params.topK,
      user_id: params.userId
    }).filter(([_, v]) => v !== undefined && v !== null)
  );

  const response = await api.post("/mentors/recommendations", payload);

  return response.data;
};
