import { useMeeting, useToggleActionItem } from "../hooks/useMeetings";
import { useUIStore } from "../store/uiStore";
import { CategoryBadge, PriorityBadge } from "./Badge";

function Card({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-slate-900">
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-500 dark:text-slate-400">
        {title}
      </h2>
      {children}
    </section>
  );
}

export function MeetingDetail() {
  const selectedId = useUIStore((s) => s.selectedMeetingId);
  const { data: meeting, isLoading } = useMeeting(selectedId);
  const toggle = useToggleActionItem(selectedId ?? 0);

  if (selectedId == null) {
    return (
      <div className="flex h-full items-center justify-center text-sm text-slate-500 dark:text-slate-400">
        Select a meeting, or analyze a new transcript.
      </div>
    );
  }

  if (isLoading || !meeting) {
    return (
      <div className="space-y-4">
        {[0, 1, 2].map((i) => (
          <div
            key={i}
            className="h-32 animate-pulse rounded-xl bg-slate-200 dark:bg-slate-800"
          />
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 dark:text-slate-100">
          {meeting.title}
        </h1>
        <div className="mt-2 flex flex-wrap gap-2">
          {meeting.topics.map((t) => (
            <span
              key={t}
              className="rounded-full bg-slate-100 px-2 py-0.5 text-xs text-slate-700 dark:bg-slate-800 dark:text-slate-300"
            >
              {t}
            </span>
          ))}
        </div>
      </div>

      <Card title="Summary">
        <p className="text-sm leading-relaxed text-slate-700 dark:text-slate-300">
          {meeting.summary || "No summary."}
        </p>
      </Card>

      <Card title="Action items">
        {meeting.action_items.length === 0 ? (
          <p className="text-sm text-slate-500 dark:text-slate-400">
            No action items.
          </p>
        ) : (
          <ul className="space-y-2">
            {meeting.action_items.map((a) => (
              <li
                key={a.id}
                className="flex items-start gap-3 rounded-lg border border-slate-100 p-2 dark:border-slate-800"
              >
                <input
                  type="checkbox"
                  checked={a.done}
                  onChange={() => toggle.mutate(a.id)}
                  className="mt-1 h-4 w-4 accent-indigo-600"
                />
                <div className="flex-1">
                  <p
                    className={`text-sm ${
                      a.done
                        ? "text-slate-400 line-through dark:text-slate-600"
                        : "text-slate-800 dark:text-slate-200"
                    }`}
                  >
                    {a.description}
                  </p>
                  <div className="mt-1 flex flex-wrap items-center gap-2 text-xs text-slate-500 dark:text-slate-400">
                    {a.owner && <span>👤 {a.owner}</span>}
                    {a.due_date && <span>📅 {a.due_date}</span>}
                    <PriorityBadge priority={a.priority} />
                  </div>
                </div>
              </li>
            ))}
          </ul>
        )}
      </Card>

      <Card title="Nuggets">
        {meeting.nuggets.length === 0 ? (
          <p className="text-sm text-slate-500 dark:text-slate-400">No nuggets.</p>
        ) : (
          <ul className="space-y-3">
            {meeting.nuggets.map((n) => (
              <li key={n.id} className="flex items-start gap-3">
                <CategoryBadge category={n.category} />
                <div className="flex-1">
                  <p className="text-sm text-slate-800 dark:text-slate-200">
                    {n.content}
                  </p>
                  {n.speaker && (
                    <p className="text-xs text-slate-500 dark:text-slate-400">
                      — {n.speaker}
                    </p>
                  )}
                </div>
              </li>
            ))}
          </ul>
        )}
      </Card>

      <Card title="People">
        {meeting.people.length === 0 ? (
          <p className="text-sm text-slate-500 dark:text-slate-400">
            No people identified.
          </p>
        ) : (
          <ul className="flex flex-wrap gap-3">
            {meeting.people.map((p) => (
              <li
                key={p.id}
                className="rounded-lg border border-slate-100 px-3 py-2 dark:border-slate-800"
              >
                <div className="text-sm font-medium text-slate-800 dark:text-slate-200">
                  {p.name}
                </div>
                <div className="text-xs text-slate-500 dark:text-slate-400">
                  {p.role ? `${p.role} · ` : ""}
                  {p.mentions} mention{p.mentions === 1 ? "" : "s"}
                </div>
              </li>
            ))}
          </ul>
        )}
      </Card>
    </div>
  );
}
