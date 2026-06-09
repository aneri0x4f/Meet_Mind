// TanStack Query hooks for meetings + action items.

import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";
import { api } from "../lib/api";

export const meetingKeys = {
  all: ["meetings"] as const,
  detail: (id: number) => ["meetings", id] as const,
};

export function useMeetingsList() {
  return useQuery({ queryKey: meetingKeys.all, queryFn: api.listMeetings });
}

export function useMeeting(id: number | null) {
  return useQuery({
    queryKey: id ? meetingKeys.detail(id) : ["meetings", "none"],
    queryFn: () => api.getMeeting(id as number),
    enabled: id != null,
  });
}

export function useCreateMeeting() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (transcript: string) => api.createMeeting(transcript),
    onSuccess: (meeting) => {
      qc.invalidateQueries({ queryKey: meetingKeys.all });
      qc.setQueryData(meetingKeys.detail(meeting.id), meeting);
    },
  });
}

export function useDeleteMeeting() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => api.deleteMeeting(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: meetingKeys.all }),
  });
}

export function useToggleActionItem(meetingId: number) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (itemId: number) => api.toggleActionItem(itemId),
    onSuccess: () =>
      qc.invalidateQueries({ queryKey: meetingKeys.detail(meetingId) }),
  });
}
