import { useQuery } from "@tanstack/react-query";
import { getMentors, getMentorsAIRecommendations } from "../api/mentorApi";

export const useMentors = () => {
  return useQuery({
    queryKey: ["mentors"],
    queryFn: getMentors,
    staleTime: 1000 * 60 * 1 // cache for 1 minutes
  });
};

export const useMentorRecommendations = (params) => {
  console.log("Fetching mentor recommendations with params:", params)
  return useQuery({
    queryKey: ["mentor-recommendations", params],
    queryFn: () => getMentorsAIRecommendations(params),
    enabled: !!params
  });
};