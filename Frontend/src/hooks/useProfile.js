import { useQuery, useMutation } from "@tanstack/react-query";
import { getProfile, upsertProfile } from "../api/profileApi";
import api from "../api/client";
import { useSelector } from "react-redux";

export const useProfile = () => {
  const userId = useSelector((state) => state.auth.user?.user_id);

  return useQuery({
    queryKey: ["profile", userId],
    queryFn: () => getProfile(userId, api),
    enabled: !!userId,
    retry: false
  });
};

export const useUpdateProfile = () => {
  return useMutation({
    mutationFn: (data) => upsertProfile(data, api)
  });
};