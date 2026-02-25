"use client";

import { useState } from "react";
import { Clock, BookOpen, Sparkles, CheckCircle2, ChevronDown, ChevronUp, ExternalLink, BookOpen as BookIcon, FileText, Youtube } from "lucide-react";
import { api } from "@/lib/api";
import type { RoadmapItem, RoadmapWeekExpand } from "@/types";

interface RoadmapTimelineProps {
  slug: string;
  items: RoadmapItem[];
  topicsToStudyFirst?: string[];
  topicsToSkipOrReview?: string[];
  isAuthenticated?: boolean;
}

export default function RoadmapTimeline({
  slug,
  items,
  topicsToStudyFirst = [],
  topicsToSkipOrReview = [],
  isAuthenticated = false,
}: RoadmapTimelineProps) {
  const [expandedWeek, setExpandedWeek] = useState<number | null>(null);
  const [expandContent, setExpandContent] = useState<RoadmapWeekExpand | null>(null);
  const [expandLoading, setExpandLoading] = useState(false);

  const studySet = new Set(topicsToStudyFirst);
  const skipSet = new Set(topicsToSkipOrReview);

  const fetchExpand = async (weekNumber: number) => {
    if (expandedWeek === weekNumber) {
      setExpandedWeek(null);
      setExpandContent(null);
      return;
    }
    setExpandLoading(true);
    setExpandedWeek(weekNumber);
    setExpandContent(null);
    try {
      const url = isAuthenticated
        ? `/users/me/domains/${slug}/roadmap/weeks/${weekNumber}/expand`
        : `/categories/${slug}/roadmap/weeks/${weekNumber}/expand`;
      const data = await api.get<RoadmapWeekExpand>(url);
      setExpandContent(data);
    } catch {
      setExpandedWeek(null);
    } finally {
      setExpandLoading(false);
    }
  };

  if (items.length === 0) {
    return (
      <div className="py-16 text-center text-gray-500">
        No roadmap available yet for this domain.
      </div>
    );
  }

  return (
    <div className="relative">
      {(studySet.size > 0 || skipSet.size > 0) && (
        <p className="mb-4 text-sm text-gray-400">
          Labels below are based on your assessment. Click a week to see a detailed breakdown and resources.
        </p>
      )}
      <div className="absolute left-6 top-0 bottom-0 w-px bg-gray-800" />

      <div className="space-y-1">
        {items.map((item, idx) => {
          const isReview = skipSet.has(item.title);
          const isRecommended = studySet.has(item.title);
          const isExpanded = expandedWeek === item.week_number;
          return (
            <div key={item.id} className="relative flex gap-6 pl-0">
              <div className="relative z-10 flex h-12 w-12 shrink-0 items-center justify-center rounded-full border-2 border-gray-700 bg-gray-900 text-sm font-bold text-green-400">
                W{item.week_number}
              </div>

              <div className="flex-1">
                <button
                  type="button"
                  onClick={() => fetchExpand(item.week_number)}
                  className={`w-full rounded-xl border p-5 text-left transition-all hover:border-gray-700 ${
                    isReview
                      ? "border-gray-700/80 bg-gray-900/30"
                      : "border-gray-800 bg-gray-900/50"
                  } ${isExpanded ? "rounded-b-none border-b-0" : ""}`}
                >
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <h3 className="font-semibold text-white">{item.title}</h3>
                      {item.description && (
                        <p className="mt-1 text-sm text-gray-400">{item.description}</p>
                      )}
                    </div>
                    <div className="flex shrink-0 items-center gap-2">
                      {isRecommended && (
                        <span className="inline-flex items-center gap-1 rounded-lg bg-green-500/15 px-2.5 py-1 text-xs text-green-400">
                          <Sparkles className="h-3.5 w-3.5" />
                          Recommended next
                        </span>
                      )}
                      {isReview && (
                        <span className="inline-flex items-center gap-1 rounded-lg bg-gray-600/20 px-2.5 py-1 text-xs text-gray-400">
                          <CheckCircle2 className="h-3.5 w-3.5" />
                          You&apos;re strong — review if needed
                        </span>
                      )}
                      <span className="rounded-lg bg-gray-800 px-2.5 py-1 text-xs text-gray-300">
                        Week {item.week_number}
                      </span>
                      {isExpanded ? (
                        <ChevronUp className="h-5 w-5 text-gray-500" />
                      ) : (
                        <ChevronDown className="h-5 w-5 text-gray-500" />
                      )}
                    </div>
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
                </button>

                {isExpanded && (
                  <div className="rounded-b-xl border border-t-0 border-gray-800 bg-gray-900/30 p-5">
                    {expandLoading ? (
                      <div className="flex items-center justify-center py-8">
                        <div className="h-8 w-8 animate-spin rounded-full border-2 border-green-500 border-t-transparent" />
                      </div>
                    ) : expandContent ? (
                      <div className="space-y-6">
                        {expandContent.granular_tasks?.length > 0 && (
                          <div>
                            <h4 className="mb-2 text-sm font-medium text-gray-300">What to do</h4>
                            <ul className="list-inside list-disc space-y-1 text-sm text-gray-400">
                              {expandContent.granular_tasks.map((task, i) => (
                                <li key={i}>{task}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                        {expandContent.resources?.length > 0 && (
                          <div>
                            <h4 className="mb-2 text-sm font-medium text-gray-300">Resources</h4>
                            <div className="flex flex-wrap gap-2">
                              {expandContent.resources.map((r, i) => (
                                <a
                                  key={i}
                                  href={r.url || "#"}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="inline-flex items-center gap-2 rounded-lg border border-gray-700 bg-gray-800/50 px-3 py-2 text-sm text-white transition hover:border-green-600 hover:bg-gray-800"
                                >
                                  {r.type === "youtube" && <Youtube className="h-4 w-4 text-red-500" />}
                                  {r.type === "article" && <FileText className="h-4 w-4 text-green-500" />}
                                  {r.type === "book" && <BookIcon className="h-4 w-4 text-amber-500" />}
                                  <span className="line-clamp-1">{r.title}</span>
                                  <ExternalLink className="h-3.5 w-3.5 shrink-0 text-gray-500" />
                                </a>
                              ))}
                            </div>
                            {expandContent.resources.filter((r) => r.reason || r.description).length > 0 && (
                              <ul className="mt-2 space-y-1 text-xs text-gray-500">
                                {expandContent.resources
                                  .filter((r) => r.reason || r.description)
                                  .map((r, i) => (
                                    <li key={i}>
                                      <span className="font-medium text-gray-400">{r.title}:</span> {r.reason || r.description}
                                    </li>
                                  ))}
                              </ul>
                            )}
                          </div>
                        )}
                      </div>
                    ) : null}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
