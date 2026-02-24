"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { api } from "@/lib/api";
import type { Category, RoadmapItem, LearningResource, Question } from "@/types";
import RoadmapTimeline from "@/components/domain/RoadmapTimeline";
import VideoCard from "@/components/domain/VideoCard";
import { getDomainIcon, getDomainColors } from "@/components/domain/DomainCard";
import Card from "@/components/ui/Card";
import { ArrowLeft, Map, PlayCircle, FileQuestion } from "lucide-react";

type TabKey = "roadmap" | "learn" | "practice";

const TABS: { key: TabKey; label: string; icon: typeof Map }[] = [
  { key: "roadmap", label: "Roadmap", icon: Map },
  { key: "learn", label: "Learn", icon: PlayCircle },
  { key: "practice", label: "Practice", icon: FileQuestion },
];

const DIFFICULTY_COLORS: Record<string, string> = {
  easy: "text-green-400 bg-green-500/10",
  medium: "text-yellow-400 bg-yellow-500/10",
  hard: "text-red-400 bg-red-500/10",
};

export default function DomainHubPage() {
  const params = useParams();
  const slug = params.slug as string;

  const [category, setCategory] = useState<Category | null>(null);
  const [roadmap, setRoadmap] = useState<RoadmapItem[]>([]);
  const [resources, setResources] = useState<LearningResource[]>([]);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [activeTab, setActiveTab] = useState<TabKey>("roadmap");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!slug) return;

    async function load() {
      setLoading(true);
      setError(null);
      try {
        const [cat, rm, res, qs] = await Promise.all([
          api.get<Category>(`/categories/${slug}/detail`),
          api.get<RoadmapItem[]>(`/categories/${slug}/roadmap`),
          api.get<LearningResource[]>(`/categories/${slug}/resources`),
          api.get<Question[]>(`/categories/${slug}/questions`),
        ]);
        setCategory(cat);
        setRoadmap(rm);
        setResources(res);
        setQuestions(qs);
      } catch (e: unknown) {
        setError(e instanceof Error ? e.message : "Failed to load domain data");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [slug]);

  if (loading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-green-500 border-t-transparent" />
      </div>
    );
  }

  if (error || !category) {
    return (
      <div className="flex min-h-[60vh] flex-col items-center justify-center gap-4">
        <p className="text-red-400">{error || "Domain not found"}</p>
        <Link href="/" className="text-sm text-green-400 hover:underline">
          ← Back to domains
        </Link>
      </div>
    );
  }

  const Icon = getDomainIcon(slug);
  const colors = getDomainColors(slug);
  const totalHours = roadmap.reduce((sum, r) => sum + r.estimated_hours, 0);

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      {/* Back link */}
      <Link
        href="/"
        className="mb-6 inline-flex items-center gap-2 text-sm text-gray-400 hover:text-white transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        All Domains
      </Link>

      {/* Header */}
      <div className="mb-8 flex items-start gap-5">
        <div className={`rounded-2xl p-4 ${colors.bg}`}>
          <Icon className={`h-10 w-10 ${colors.text}`} />
        </div>
        <div>
          <h1 className="text-3xl font-bold text-white">{category.name}</h1>
          <p className="mt-1 text-gray-400">{category.description}</p>
          <div className="mt-3 flex flex-wrap gap-4 text-sm text-gray-500">
            <span>{roadmap.length} week roadmap</span>
            <span>{totalHours} hours of content</span>
            <span>{resources.length} video lessons</span>
            <span>{questions.length} practice questions</span>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="mb-8 flex gap-1 rounded-xl bg-gray-900/80 p-1 border border-gray-800">
        {TABS.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            className={`flex flex-1 items-center justify-center gap-2 rounded-lg px-4 py-2.5 text-sm font-medium transition-all ${
              activeTab === tab.key
                ? "bg-green-600 text-white shadow-sm"
                : "text-gray-400 hover:text-white hover:bg-gray-800"
            }`}
          >
            <tab.icon className="h-4 w-4" />
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab content */}
      {activeTab === "roadmap" && <RoadmapTimeline items={roadmap} />}

      {activeTab === "learn" && (
        <div>
          {resources.length === 0 ? (
            <div className="py-16 text-center text-gray-500">
              No video resources available yet.
            </div>
          ) : (
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {resources.map((r) => (
                <VideoCard key={r.id} resource={r} />
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === "practice" && (
        <div>
          {questions.length === 0 ? (
            <div className="py-16 text-center text-gray-500">
              No practice questions available yet.
            </div>
          ) : (
            <div className="space-y-3">
              {questions.map((q) => (
                <Link key={q.id} href={`/question/${q.id}`}>
                  <Card hover className="group flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3">
                        <h3 className="font-medium text-white group-hover:text-green-400 transition-colors">
                          {q.title}
                        </h3>
                        <span
                          className={`rounded-full px-2 py-0.5 text-xs font-medium ${
                            DIFFICULTY_COLORS[q.difficulty] || "text-gray-400 bg-gray-800"
                          }`}
                        >
                          {q.difficulty}
                        </span>
                      </div>
                      <p className="mt-1 text-sm text-gray-500 line-clamp-1">
                        {q.description}
                      </p>
                    </div>
                    <span className="ml-4 shrink-0 rounded-lg bg-gray-800 px-2.5 py-1 text-xs text-gray-400 uppercase">
                      {q.question_type.replace("_", " ")}
                    </span>
                  </Card>
                </Link>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
