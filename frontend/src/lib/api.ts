// Single place for all network calls. Requests go through the Vite `/api` proxy
// to the FastAPI backend.

import type {
  ActionItem,
  MeetingDetail,
  MeetingSummaryRow,
} from "../types";

const BASE = "/api";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(`${res.status}: ${detail}`);
  }
  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}

export const api = {
  listMeetings: () => request<MeetingSummaryRow[]>("/meetings"),

  getMeeting: (id: number) => request<MeetingDetail>(`/meetings/${id}`),

  createMeeting: (transcript: string) =>
    request<MeetingDetail>("/meetings", {
      method: "POST",
      body: JSON.stringify({ transcript }),
    }),

  deleteMeeting: (id: number) =>
    request<void>(`/meetings/${id}`, { method: "DELETE" }),

  toggleActionItem: (id: number) =>
    request<ActionItem>(`/action-items/${id}/toggle`, { method: "PATCH" }),
};
