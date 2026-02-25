"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import type { Category, RoadmapItem, LearningResource, Question, DomainPreference, ResourcesByWeek } from "@/types";
import RoadmapTimeline from "@/components/domain/RoadmapTimeline";
import VideoCard from "@/components/domain/VideoCard";
import TimeCommitmentModal from "@/components/domain/TimeCommitmentModal";
import { getDomainIcon, getDomainColors } from "@/components/domain/DomainCard";
import Card from "@/components/ui/Card";
import { ArrowLeft, Map, PlayCircle, FileQuestion, Sparkles } from "lucide-react";

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
  const [suggestions, setSuggestions] = useState<{
    personalized: boolean;
    data?: {
      summary?: string;
      next_steps?: { title: string; reason: string; priority: number }[];
      topics_to_study_first?: string[];
      topics_to_skip_or_review_lightly?: string[];
    };
  } | null>(null);
  const [domainPreference, setDomainPreference] = useState<DomainPreference | null | undefined>(undefined);
  const [resourcesByWeek, setResourcesByWeek] = useState<ResourcesByWeek[]>([]);
  const { user } = useAuth();

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

  useEffect(() => {
    if (!slug || !user?.assessment_completed_at) return;
    api
      .get<{ personalized: boolean; data: Record<string, unknown> }>(`/users/me/suggestions?domain=${slug}`)
      .then(setSuggestions)
      .catch(() => setSuggestions(null));
  }, [slug, user?.assessment_completed_at]);

  useEffect(() => {
    if (!slug) return;
    api.get<ResourcesByWeek[]>(`/categories/${slug}/resources/grouped`).then(setResourcesByWeek).catch(() => setResourcesByWeek([]));
  }, [slug]);

  useEffect(() => {
    if (!slug || !user) return;
    api
      .get<DomainPreference | null>(`/users/me/domains/${slug}/preference`)
      .then((v) => setDomainPreference(v ?? null))
      .catch(() => setDomainPreference(undefined));
  }, [slug, user]);

  const savePreference = async (durationWeeks: number) => {
    await api.put<DomainPreference>(`/users/me/domains/${slug}/preference`, { duration_weeks: durationWeeks });
    setDomainPreference({ duration_weeks: durationWeeks });
  };

  const showTimeModal = user && domainPreference === null && !loading;

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
      {showTimeModal && (
        <TimeCommitmentModal
          domainName={category.name}
          onSave={savePreference}
          onSkip={() => savePreference(10)}
        />
      )}
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

      {/* Personalized suggestions (when logged in and assessment done) */}
      {suggestions?.data && (
        <Card className="mb-8 border-green-500/20 bg-gradient-to-r from-green-900/10 to-gray-900">
          <div className="flex items-center gap-2 text-green-400 mb-2">
            <Sparkles className="h-5 w-5" />
            <span className="font-medium">
              {suggestions.personalized ? "Recommended for you" : "Complete your assessment for personalized tips"}
            </span>
          </div>
          {suggestions.personalized && (
            <p className="text-xs text-gray-500 mb-1">Based on your assessment.</p>
          )}
          {suggestions.data.summary && (
            <p className="text-sm text-gray-300 mb-3">{suggestions.data.summary}</p>
          )}
          {suggestions.data.next_steps && suggestions.data.next_steps.length > 0 && (
            <ul className="list-disc list-inside space-y-1 text-sm text-gray-400">
              {suggestions.data.next_steps.slice(0, 4).map((s, i) => (
                <li key={i}>
                  <span className="text-white">{s.title}</span>
                  {s.reason && <span className="text-gray-500"> — {s.reason}</span>}
                </li>
              ))}
            </ul>
          )}
        </Card>
      )}

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
      {activeTab === "roadmap" && (
        <RoadmapTimeline
          slug={slug}
          items={roadmap}
          topicsToStudyFirst={suggestions?.data?.topics_to_study_first}
          topicsToSkipOrReview={suggestions?.data?.topics_to_skip_or_review_lightly}
          isAuthenticated={!!user}
        />
      )}

      {activeTab === "learn" && (
        <div>
          {resourcesByWeek.length === 0 ? (
            <div className="py-16 text-center text-gray-500">
              No video resources available yet.
            </div>
          ) : (
            <div className="space-y-10">
              {resourcesByWeek
                .filter((g) => g.week_number > 0)
                .map((group) => {
                  const byTopic = group.resources.reduce(
                    (acc, r) => {
                      const topic = r.topic_name || "General";
                      if (!acc[topic]) acc[topic] = [];
                      acc[topic].push(r);
                      return acc;
                    },
                    {} as Record<string, typeof group.resources>
                  );
                  const topics = Object.keys(byTopic);
                  return (
                    <div key={group.roadmap_item_id ?? `week-${group.week_number}`}>
                      <h3 className="mb-4 text-lg font-semibold text-white">
                        Week {group.week_number}: {group.roadmap_title}
                      </h3>
                      {topics.length > 1 ? (
                        <div className="space-y-6">
                          {topics.map((topic) => (
                            <div key={topic}>
                              <h4 className="mb-2 text-sm font-medium text-gray-400">{topic}</h4>
                              <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                                {byTopic[topic].map((r) => (
                                  <VideoCard key={r.id} resource={r} />
                                ))}
                              </div>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                          {group.resources.map((r) => (
                            <VideoCard key={r.id} resource={r} />
                          ))}
                        </div>
                      )}
                    </div>
                  );
                })}
              {resourcesByWeek.some((g) => g.week_number === 0) && (
                <div>
                  <h3 className="mb-4 text-lg font-semibold text-white">Other</h3>
                  <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                    {resourcesByWeek
                      .find((g) => g.week_number === 0)
                      ?.resources.map((r) => (
                        <VideoCard key={r.id} resource={r} />
                      ))}
                  </div>
                </div>
              )}
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
