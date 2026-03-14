import { useQuery } from "@tanstack/react-query";
import { getSessions } from "../api/sessionApi";

export const useSessions = () => {
  return useQuery({
    queryKey: ["sessions"],
    queryFn: getSessions,
    staleTime: 1000 * 60 * 1 // 5 minutes
  });
};