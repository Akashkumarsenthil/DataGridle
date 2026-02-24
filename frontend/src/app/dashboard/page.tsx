"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import { getDomainIcon, getDomainColors } from "@/components/domain/DomainCard";
import { api } from "@/lib/api";
import type { Category } from "@/types";
import {
  Flame,
  Target,
  CheckCircle2,
  Clock,
  ArrowRight,
} from "lucide-react";

export default function DashboardPage() {
  const [categories, setCategories] = useState<Category[]>([]);

  useEffect(() => {
    api
      .get<Category[]>("/categories/")
      .then(setCategories)
      .catch(() => {});
  }, []);

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">Dashboard</h1>
        <p className="mt-1 text-gray-400">
          Track your interview prep progress across all data domains
        </p>
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

      {/* Daily Challenge */}
      <Card className="mb-10 border-green-500/20 bg-gradient-to-r from-green-900/20 to-gray-900">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-xs font-medium text-green-400 uppercase tracking-wider">
              Daily Challenge
            </p>
            <h3 className="mt-2 text-lg font-semibold text-white">
              Today&apos;s challenge is ready!
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

      {/* Domain Progress Grid */}
      <div>
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-lg font-semibold text-white">Your Domains</h2>
          <Link
            href="/#domains"
            className="text-sm text-green-400 hover:text-green-300 transition-colors"
          >
            Browse all →
          </Link>
        </div>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {categories.map((cat) => {
            const Icon = getDomainIcon(cat.slug);
            const colors = getDomainColors(cat.slug);
            return (
              <Link key={cat.id} href={`/domain/${cat.slug}`}>
                <Card hover className="group h-full">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className={`rounded-lg p-2 ${colors.bg}`}>
                        <Icon className={`h-5 w-5 ${colors.text}`} />
                      </div>
                      <div>
                        <span className="font-medium text-white group-hover:text-green-400 transition-colors">
                          {cat.name}
                        </span>
                        <p className="text-xs text-gray-500 mt-0.5 line-clamp-1">
                          {cat.description}
                        </p>
                      </div>
                    </div>
                    <ArrowRight className="h-4 w-4 text-gray-600 group-hover:text-gray-400 transition-colors" />
                  </div>
                  <div className="mt-4">
                    <div className="flex justify-between text-xs text-gray-500">
                      <span>0% complete</span>
                      <span>0 solved</span>
                    </div>
                    <div className="mt-1.5 h-1.5 overflow-hidden rounded-full bg-gray-800">
                      <div
                        className="h-full rounded-full bg-green-500 transition-all"
                        style={{ width: "0%" }}
                      />
                    </div>
                  </div>
                </Card>
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
}
