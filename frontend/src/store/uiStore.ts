// Client-only UI state (Zustand). Server data lives in TanStack Query — do not
// mirror it here.

import { create } from "zustand";

interface UIState {
  theme: "light" | "dark";
  selectedMeetingId: number | null;
  toggleTheme: () => void;
  setTheme: (theme: "light" | "dark") => void;
  selectMeeting: (id: number | null) => void;
}

function applyTheme(theme: "light" | "dark") {
  const root = document.documentElement;
  root.classList.toggle("dark", theme === "dark");
}

// Honor the initial class set on <html> (defaults to dark in index.html).
const initialTheme: "light" | "dark" =
  document.documentElement.classList.contains("dark") ? "dark" : "light";

export const useUIStore = create<UIState>((set, get) => ({
  theme: initialTheme,
  selectedMeetingId: null,
  toggleTheme: () => {
    const next = get().theme === "dark" ? "light" : "dark";
    applyTheme(next);
    set({ theme: next });
  },
  setTheme: (theme) => {
    applyTheme(theme);
    set({ theme });
  },
  selectMeeting: (id) => set({ selectedMeetingId: id }),
}));
