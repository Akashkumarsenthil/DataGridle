"use client";

import { useState } from "react";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Badge from "@/components/ui/Badge";
import Input from "@/components/ui/Input";
import Link from "next/link";
import { Search, Filter, CheckCircle2 } from "lucide-react";

const MOCK_QUESTIONS = [
  { id: 1, title: "Find Duplicate Emails", difficulty: "easy" as const, type: "sql", company: "Google", frequency: 42 },
  { id: 2, title: "Running Total of Sales", difficulty: "medium" as const, type: "sql", company: "Amazon", frequency: 38 },
  { id: 3, title: "Rank Employees by Department Salary", difficulty: "medium" as const, type: "sql", company: "Meta", frequency: 35 },
  { id: 4, title: "Find the Median Salary", difficulty: "hard" as const, type: "sql", company: "Apple", frequency: 28 },
  { id: 5, title: "Cumulative Sum with Window Functions", difficulty: "medium" as const, type: "sql", company: "Netflix", frequency: 33 },
  { id: 6, title: "Identify Churned Users", difficulty: "medium" as const, type: "sql", company: "Spotify", frequency: 25 },
  { id: 7, title: "Top N Products per Category", difficulty: "hard" as const, type: "sql", company: "Amazon", frequency: 30 },
  { id: 8, title: "Sessionize User Events", difficulty: "hard" as const, type: "sql", company: "Uber", frequency: 22 },
  { id: 9, title: "Calculate Retention Rate", difficulty: "medium" as const, type: "sql", company: "Stripe", frequency: 27 },
  { id: 10, title: "Pivot Table with CASE Statements", difficulty: "easy" as const, type: "sql", company: "Microsoft", frequency: 40 },
];

const difficultyVariant = {
  easy: "success" as const,
  medium: "warning" as const,
  hard: "danger" as const,
};

export default function QuestionsPage() {
  const [search, setSearch] = useState("");
  const [difficultyFilter, setDifficultyFilter] = useState<string | null>(null);

  const filtered = MOCK_QUESTIONS.filter((q) => {
    const matchesSearch = q.title.toLowerCase().includes(search.toLowerCase());
    const matchesDifficulty = !difficultyFilter || q.difficulty === difficultyFilter;
    return matchesSearch && matchesDifficulty;
  });

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">Practice Questions</h1>
        <p className="mt-1 text-gray-400">SQL, Python, and case study interview problems</p>
      </div>

      {/* Filters */}
      <div className="mb-6 flex flex-wrap items-center gap-3">
        <div className="relative flex-1 min-w-[200px]">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-500" />
          <Input
            placeholder="Search questions..."
            className="pl-10"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <div className="flex items-center gap-2">
          <Filter className="h-4 w-4 text-gray-500" />
          {["easy", "medium", "hard"].map((d) => (
            <Button
              key={d}
              variant={difficultyFilter === d ? "primary" : "outline"}
              size="sm"
              onClick={() => setDifficultyFilter(difficultyFilter === d ? null : d)}
            >
              {d}
            </Button>
          ))}
        </div>
      </div>

      {/* Question list */}
      <div className="space-y-2">
        {filtered.map((q) => (
          <Link key={q.id} href={`/question/${q.id}`}>
            <div className="group flex items-center gap-4 rounded-lg border border-gray-800 bg-gray-900/30 px-5 py-4 transition-all hover:border-gray-700 hover:bg-gray-900/60">
              <CheckCircle2 className="h-5 w-5 shrink-0 text-gray-700" />
              <div className="flex-1 min-w-0">
                <h3 className="text-sm font-medium text-white group-hover:text-green-400 transition-colors truncate">
                  {q.id}. {q.title}
                </h3>
              </div>
              <div className="flex items-center gap-3 shrink-0">
                <span className="hidden sm:inline text-xs text-gray-500">{q.company}</span>
                <Badge variant={difficultyVariant[q.difficulty]}>
                  {q.difficulty}
                </Badge>
                <span className="text-xs text-gray-600">{q.frequency}x</span>
              </div>
            </div>
          </Link>
        ))}
      </div>

      {filtered.length === 0 && (
        <Card className="text-center py-12">
          <p className="text-gray-400">No questions match your filters.</p>
        </Card>
      )}
    </div>
  );
}
