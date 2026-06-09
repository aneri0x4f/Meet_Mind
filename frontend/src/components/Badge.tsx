import type { ReactNode } from "react";
import type { NuggetCategory, Priority } from "../types";

const priorityStyles: Record<Priority, string> = {
  low: "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300",
  medium: "bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300",
  high: "bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300",
};

const categoryStyles: Record<NuggetCategory, string> = {
  quote: "bg-indigo-100 text-indigo-800 dark:bg-indigo-900/40 dark:text-indigo-300",
  insight: "bg-sky-100 text-sky-800 dark:bg-sky-900/40 dark:text-sky-300",
  decision: "bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300",
  risk: "bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300",
};

function Pill({ className, children }: { className: string; children: ReactNode }) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${className}`}
    >
      {children}
    </span>
  );
}

export function PriorityBadge({ priority }: { priority: Priority }) {
  return <Pill className={priorityStyles[priority]}>{priority}</Pill>;
}

export function CategoryBadge({ category }: { category: NuggetCategory }) {
  return <Pill className={categoryStyles[category]}>{category}</Pill>;
}
