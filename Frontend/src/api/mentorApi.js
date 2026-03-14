import api from "./client";

export const getMentors = async () => {
  const response = await api.get("/mentors");
  return response.data;
};

export const getMentorsAIRecommendations = async () => {
  const response = await api.get("/mentors/ai-recommendations");
  return response.data;
}