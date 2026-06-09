import { useState } from "react";
import { useCreateMeeting } from "../hooks/useMeetings";
import { useUIStore } from "../store/uiStore";

export function TranscriptInput() {
  const [text, setText] = useState("");
  const createMeeting = useCreateMeeting();
  const selectMeeting = useUIStore((s) => s.selectMeeting);

  const submit = () => {
    if (!text.trim()) return;
    createMeeting.mutate(text, {
      onSuccess: (meeting) => {
        selectMeeting(meeting.id);
        setText("");
      },
    });
  };

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900">
      <label className="mb-2 block text-sm font-medium text-slate-700 dark:text-slate-300">
        Paste a meeting transcript
      </label>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={8}
        placeholder="Speaker: ..."
        className="w-full resize-y rounded-lg border border-slate-200 bg-slate-50 p-3 text-sm outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/30 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-100"
      />
      <div className="mt-3 flex items-center gap-3">
        <button
          onClick={submit}
          disabled={createMeeting.isPending || !text.trim()}
          className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {createMeeting.isPending ? "Analyzing…" : "Analyze meeting"}
        </button>
        {createMeeting.isError && (
          <span className="text-sm text-red-600 dark:text-red-400">
            {(createMeeting.error as Error).message}
          </span>
        )}
      </div>
    </div>
  );
}
