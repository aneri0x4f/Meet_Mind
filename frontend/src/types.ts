// Shared types mirroring the backend response schemas.

export type Priority = "low" | "medium" | "high";
export type NuggetCategory = "quote" | "insight" | "decision" | "risk";

export interface ActionItem {
  id: number;
  meeting_id: number;
  description: string;
  owner: string | null;
  due_date: string | null;
  priority: Priority;
  done: boolean;
}

export interface Nugget {
  id: number;
  meeting_id: number;
  content: string;
  category: NuggetCategory;
  speaker: string | null;
}

export interface Person {
  id: number;
  meeting_id: number;
  name: string;
  role: string | null;
  mentions: number;
}

export interface MeetingSummaryRow {
  id: number;
  title: string;
  summary: string | null;
  created_at: string;
}

export interface MeetingDetail {
  id: number;
  title: string;
  summary: string | null;
  topics: string[];
  created_at: string;
  action_items: ActionItem[];
  nuggets: Nugget[];
  people: Person[];
}
