"use client";

import Link from "next/link";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import {
  Flame,
  Target,
  CheckCircle2,
  Clock,
  ArrowRight,
  Database,
  BarChart3,
  BrainCircuit,
  Cpu,
} from "lucide-react";

const categoryCards = [
  { name: "Data Engineering", slug: "data-engineering", icon: Database, color: "text-blue-400", progress: 0 },
  { name: "Data Science", slug: "data-science", icon: BarChart3, color: "text-purple-400", progress: 0 },
  { name: "Machine Learning", slug: "machine-learning", icon: BrainCircuit, color: "text-orange-400", progress: 0 },
  { name: "Data Analytics", slug: "data-analytics", icon: Cpu, color: "text-green-400", progress: 0 },
];

export default function DashboardPage() {
  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">Dashboard</h1>
        <p className="mt-1 text-gray-400">Track your interview prep progress</p>
      </div>

      {/* Stats row */}
      <div className="mb-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {[
          { label: "Day Streak", value: "0", icon: Flame, color: "text-orange-400" },
          { label: "Questions Solved", value: "0", icon: CheckCircle2, color: "text-green-400" },
          { label: "Accuracy", value: "—", icon: Target, color: "text-blue-400" },
          { label: "Time Practiced", value: "0h", icon: Clock, color: "text-purple-400" },
        ].map((stat) => (
          <Card key={stat.label} className="flex items-center gap-4">
            <div className="rounded-lg bg-gray-800 p-2.5">
              <stat.icon className={`h-5 w-5 ${stat.color}`} />
            </div>
            <div>
              <p className="text-2xl font-bold text-white">{stat.value}</p>
              <p className="text-xs text-gray-400">{stat.label}</p>
            </div>
          </Card>
        ))}
      </div>

      {/* Daily Question */}
      <Card className="mb-10 border-green-500/20 bg-gradient-to-r from-green-900/20 to-gray-900">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-xs font-medium text-green-400 uppercase tracking-wider">Daily Challenge</p>
            <h3 className="mt-2 text-lg font-semibold text-white">
              Today&apos;s SQL challenge is ready!
            </h3>
            <p className="mt-1 text-sm text-gray-400">
              Solve the daily question to maintain your streak.
            </p>
          </div>
          <Link href="/questions">
            <Button>
              Solve Now
              <ArrowRight className="h-4 w-4" />
            </Button>
          </Link>
        </div>
      </Card>

      {/* Category Progress */}
      <div>
        <h2 className="mb-4 text-lg font-semibold text-white">Your Categories</h2>
        <div className="grid gap-4 sm:grid-cols-2">
          {categoryCards.map((cat) => (
            <Link key={cat.slug} href={`/${cat.slug}`}>
              <Card hover className="group">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <cat.icon className={`h-5 w-5 ${cat.color}`} />
                    <span className="font-medium text-white group-hover:text-green-400 transition-colors">
                      {cat.name}
                    </span>
                  </div>
                  <ArrowRight className="h-4 w-4 text-gray-600 group-hover:text-gray-400 transition-colors" />
                </div>
                <div className="mt-4">
                  <div className="flex justify-between text-xs text-gray-500">
                    <span>{cat.progress}% complete</span>
                    <span>0 / 0 solved</span>
                  </div>
                  <div className="mt-1.5 h-1.5 overflow-hidden rounded-full bg-gray-800">
                    <div
                      className="h-full rounded-full bg-green-500 transition-all"
                      style={{ width: `${cat.progress}%` }}
                    />
                  </div>
                </div>
              </Card>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
