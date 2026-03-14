import { useQuery } from "@tanstack/react-query";
import { getMentors } from "../api/mentorApi";

export const useMentors = () => {
  return useQuery({
    queryKey: ["mentors"],
    queryFn: getMentors,
    staleTime: 1000 * 60 * 1 // cache for 1 minutes
  });
};