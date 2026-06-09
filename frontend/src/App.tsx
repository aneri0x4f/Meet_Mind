import { MeetingDetail } from "./components/MeetingDetail";
import { MeetingList } from "./components/MeetingList";
import { ThemeToggle } from "./components/ThemeToggle";
import { TranscriptInput } from "./components/TranscriptInput";

export default function App() {
  return (
    <div className="mx-auto flex min-h-full max-w-6xl flex-col gap-6 p-6">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-slate-900 dark:text-slate-100">
            🧠 MeetMind
          </h1>
          <p className="text-sm text-slate-500 dark:text-slate-400">
            Turn meeting transcripts into summaries, action items, and nuggets.
          </p>
        </div>
        <ThemeToggle />
      </header>

      <div className="grid flex-1 gap-6 md:grid-cols-[320px_1fr]">
        <aside className="space-y-4">
          <TranscriptInput />
          <MeetingList />
        </aside>
        <main className="min-h-[60vh]">
          <MeetingDetail />
        </main>
      </div>
    </div>
  );
}
