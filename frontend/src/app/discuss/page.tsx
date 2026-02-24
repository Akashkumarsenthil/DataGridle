"use client";

import { useState } from "react";
import Link from "next/link";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Badge from "@/components/ui/Badge";
import { MessageSquare, ThumbsUp, Plus, Clock } from "lucide-react";

const CATEGORIES = [
  { value: "all", label: "All" },
  { value: "interview_experience", label: "Interview Experiences" },
  { value: "study_partners", label: "Study Partners" },
  { value: "resume_review", label: "Resume Review" },
  { value: "mock_interviews", label: "Mock Interviews" },
  { value: "lounge", label: "Lounge" },
];

const MOCK_DISCUSSIONS = [
  {
    id: 1,
    title: "Google Data Engineer Interview Experience (L4) — Feb 2026",
    category: "interview_experience",
    author: "sql_ninja",
    upvotes: 47,
    comments: 12,
    createdAt: "2h ago",
  },
  {
    id: 2,
    title: "Looking for study partners for SQL practice — Bay Area",
    category: "study_partners",
    author: "data_learner",
    upvotes: 15,
    comments: 8,
    createdAt: "5h ago",
  },
  {
    id: 3,
    title: "Amazon DE interview — what to expect in the SQL round?",
    category: "interview_experience",
    author: "pipeline_pro",
    upvotes: 32,
    comments: 21,
    createdAt: "1d ago",
  },
  {
    id: 4,
    title: "Resume review — switching from SWE to DE",
    category: "resume_review",
    author: "career_pivot",
    upvotes: 23,
    comments: 14,
    createdAt: "1d ago",
  },
  {
    id: 5,
    title: "Best resources for learning window functions?",
    category: "lounge",
    author: "query_master",
    upvotes: 19,
    comments: 7,
    createdAt: "2d ago",
  },
];

export default function DiscussPage() {
  const [activeCategory, setActiveCategory] = useState("all");

  const filtered =
    activeCategory === "all"
      ? MOCK_DISCUSSIONS
      : MOCK_DISCUSSIONS.filter((d) => d.category === activeCategory);

  return (
    <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Discussions</h1>
          <p className="mt-1 text-gray-400">Share experiences, find study partners, ask questions</p>
        </div>
        <Button>
          <Plus className="h-4 w-4" />
          New Post
        </Button>
      </div>

      {/* Category tabs */}
      <div className="mb-6 flex flex-wrap gap-2">
        {CATEGORIES.map((cat) => (
          <Button
            key={cat.value}
            variant={activeCategory === cat.value ? "primary" : "ghost"}
            size="sm"
            onClick={() => setActiveCategory(cat.value)}
          >
            {cat.label}
          </Button>
        ))}
      </div>

      {/* Discussion list */}
      <div className="space-y-3">
        {filtered.map((discussion) => (
          <Link key={discussion.id} href={`/discuss/${discussion.id}`}>
            <Card hover className="group">
              <div className="flex items-start justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <h3 className="font-medium text-white group-hover:text-green-400 transition-colors">
                    {discussion.title}
                  </h3>
                  <div className="mt-2 flex flex-wrap items-center gap-3 text-xs text-gray-500">
                    <span>@{discussion.author}</span>
                    <Badge>{discussion.category.replace(/_/g, " ")}</Badge>
                    <span className="flex items-center gap-1">
                      <Clock className="h-3 w-3" />
                      {discussion.createdAt}
                    </span>
                  </div>
                </div>
                <div className="flex shrink-0 items-center gap-4 text-xs text-gray-500">
                  <span className="flex items-center gap-1">
                    <ThumbsUp className="h-3.5 w-3.5" />
                    {discussion.upvotes}
                  </span>
                  <span className="flex items-center gap-1">
                    <MessageSquare className="h-3.5 w-3.5" />
                    {discussion.comments}
                  </span>
                </div>
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
