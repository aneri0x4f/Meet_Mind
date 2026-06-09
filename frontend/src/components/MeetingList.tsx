import { useMeetingsList, useDeleteMeeting } from "../hooks/useMeetings";
import { useUIStore } from "../store/uiStore";

export function MeetingList() {
  const { data: meetings, isLoading } = useMeetingsList();
  const selectedId = useUIStore((s) => s.selectedMeetingId);
  const selectMeeting = useUIStore((s) => s.selectMeeting);
  const deleteMeeting = useDeleteMeeting();

  if (isLoading) {
    return (
      <div className="space-y-2">
        {[0, 1, 2].map((i) => (
          <div
            key={i}
            className="h-14 animate-pulse rounded-lg bg-slate-200 dark:bg-slate-800"
          />
        ))}
      </div>
    );
  }

  if (!meetings || meetings.length === 0) {
    return (
      <p className="text-sm text-slate-500 dark:text-slate-400">
        No meetings yet — paste a transcript to get started.
      </p>
    );
  }

  return (
    <ul className="space-y-2">
      {meetings.map((m) => {
        const active = m.id === selectedId;
        return (
          <li key={m.id}>
            <div
              className={`flex items-center justify-between rounded-lg border p-3 ${
                active
                  ? "border-indigo-500 bg-indigo-50 dark:border-indigo-400 dark:bg-indigo-950/30"
                  : "border-slate-200 bg-white hover:border-slate-300 dark:border-slate-800 dark:bg-slate-900 dark:hover:border-slate-700"
              }`}
            >
              <button
                onClick={() => selectMeeting(m.id)}
                className="flex-1 text-left"
              >
                <div className="truncate text-sm font-medium text-slate-900 dark:text-slate-100">
                  {m.title}
                </div>
                <div className="text-xs text-slate-500 dark:text-slate-400">
                  {new Date(m.created_at).toLocaleString()}
                </div>
              </button>
              <button
                onClick={() => deleteMeeting.mutate(m.id)}
                className="ml-2 rounded p-1 text-slate-400 hover:text-red-600 dark:hover:text-red-400"
                aria-label="Delete meeting"
              >
                ✕
              </button>
            </div>
          </li>
        );
      })}
    </ul>
  );
}
