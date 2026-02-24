"use client";

import { Clock, BookOpen } from "lucide-react";
import type { RoadmapItem } from "@/types";

interface RoadmapTimelineProps {
  items: RoadmapItem[];
}

export default function RoadmapTimeline({ items }: RoadmapTimelineProps) {
  if (items.length === 0) {
    return (
      <div className="py-16 text-center text-gray-500">
        No roadmap available yet for this domain.
      </div>
    );
  }

  return (
    <div className="relative">
      <div className="absolute left-6 top-0 bottom-0 w-px bg-gray-800" />

      <div className="space-y-1">
        {items.map((item, idx) => (
          <div key={item.id} className="relative flex gap-6 pl-0">
            {/* Timeline dot */}
            <div className="relative z-10 flex h-12 w-12 shrink-0 items-center justify-center rounded-full border-2 border-gray-700 bg-gray-900 text-sm font-bold text-green-400">
              W{item.week_number}
            </div>

            {/* Content */}
            <div className="flex-1 rounded-xl border border-gray-800 bg-gray-900/50 p-5 transition-all hover:border-gray-700">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <h3 className="font-semibold text-white">{item.title}</h3>
                  {item.description && (
                    <p className="mt-1 text-sm text-gray-400">{item.description}</p>
                  )}
                </div>
                <span className="shrink-0 rounded-lg bg-gray-800 px-2.5 py-1 text-xs text-gray-300">
                  Week {item.week_number}
                </span>
              </div>

              <div className="mt-3 flex items-center gap-4 text-xs text-gray-500">
                <span className="flex items-center gap-1">
                  <Clock className="h-3.5 w-3.5" />
                  {item.estimated_hours}h estimated
                </span>
                <span className="flex items-center gap-1">
                  <BookOpen className="h-3.5 w-3.5" />
                  Step {idx + 1} of {items.length}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
