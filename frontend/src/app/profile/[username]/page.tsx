"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import type { UserProfileWithStrengths, User } from "@/types";
import {
  Flame,
  CheckCircle2,
  Calendar,
  Target,
  Trophy,
  BarChart3,
  ChevronRight,
} from "lucide-react";

function strengthColor(label: string) {
  if (label === "advanced") return "text-green-400 bg-green-500/20";
  if (label === "intermediate") return "text-yellow-400 bg-yellow-500/20";
  return "text-gray-400 bg-gray-500/20";
}

export default function ProfilePage() {
  const params = useParams();
  const username = params.username as string;
  const { user: currentUser } = useAuth();
  const [profile, setProfile] = useState<UserProfileWithStrengths | User | null>(null);
  const [loading, setLoading] = useState(true);

  const isOwnProfile = currentUser?.username === username;

  useEffect(() => {
    if (!username) return;
    const url = isOwnProfile ? "/users/me/profile" : `/users/by-username/${username}`;
    api
      .get<UserProfileWithStrengths | User>(url)
      .then(setProfile)
      .catch(() => setProfile(null))
      .finally(() => setLoading(false));
  }, [username, isOwnProfile]);

  if (loading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-green-500 border-t-transparent" />
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-12 text-center">
        <p className="text-gray-400">Profile not found</p>
        <Link href="/" className="mt-4 inline-block text-green-400 hover:underline">
          Go home
        </Link>
      </div>
    );
  }

  const withStrengths = "topic_strengths" in profile ? (profile as UserProfileWithStrengths) : null;
  const strengthsByCategory = withStrengths
    ? (profile as UserProfileWithStrengths).topic_strengths.reduce(
        (acc, t) => {
          const key = t.category_slug;
          if (!acc[key]) acc[key] = { name: t.category_name, topics: [] };
          acc[key].topics.push(t);
          return acc;
        },
        {} as Record<string, { name: string; topics: typeof withStrengths.topic_strengths }>
      )
    : null;

  return (
    <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
      <Card className="mb-8">
        <div className="flex items-center gap-6">
          <div className="flex h-20 w-20 items-center justify-center rounded-full bg-green-600 text-3xl font-bold text-white">
            {profile.username[0]?.toUpperCase() || "U"}
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">@{profile.username}</h1>
            <div className="mt-2 flex flex-wrap items-center gap-3">
              <Badge variant="success">{profile.role}</Badge>
              {profile.created_at && (
                <span className="flex items-center gap-1 text-xs text-gray-500">
                  <Calendar className="h-3 w-3" />
                  Joined {new Date(profile.created_at).toLocaleDateString()}
                </span>
              )}
            </div>
          </div>
        </div>
      </Card>

      <div className="mb-8 grid gap-4 sm:grid-cols-4">
        {[
          { label: "Problems Solved", value: "0", icon: CheckCircle2, color: "text-green-400" },
          { label: "Day Streak", value: String(profile.streak_count ?? 0), icon: Flame, color: "text-orange-400" },
          { label: "Accuracy", value: "—", icon: Target, color: "text-blue-400" },
          { label: "Badges", value: "0", icon: Trophy, color: "text-yellow-400" },
        ].map((stat) => (
          <Card key={stat.label}>
            <div className="text-center">
              <stat.icon className={`mx-auto h-6 w-6 ${stat.color}`} />
              <p className="mt-2 text-2xl font-bold text-white">{stat.value}</p>
              <p className="text-xs text-gray-400">{stat.label}</p>
            </div>
          </Card>
        ))}
      </div>

      {withStrengths && strengthsByCategory && Object.keys(strengthsByCategory).length > 0 && (
        <Card className="mb-8">
          <h2 className="mb-4 flex items-center gap-2 text-lg font-semibold text-white">
            <BarChart3 className="h-5 w-5 text-green-400" />
            Topic strengths
          </h2>
          <p className="mb-4 text-sm text-gray-400">
            Based on your onboarding assessment. We use this to personalize your suggestions.
          </p>
          <div className="space-y-6">
            {Object.entries(strengthsByCategory).map(([slug, { name, topics }]) => (
              <div key={slug}>
                <Link
                  href={`/domain/${slug}`}
                  className="mb-2 flex items-center gap-1 text-sm font-medium text-green-400 hover:text-green-300"
                >
                  {name}
                  <ChevronRight className="h-4 w-4" />
                </Link>
                <div className="space-y-2">
                  {topics.map((t) => (
                    <div
                      key={t.topic_id}
                      className="flex items-center justify-between rounded-lg bg-gray-800/50 px-3 py-2"
                    >
                      <span className="text-sm text-white">{t.topic_name}</span>
                      <div className="flex items-center gap-3">
                        <div className="h-2 w-24 overflow-hidden rounded-full bg-gray-700">
                          <div
                            className="h-full rounded-full bg-green-500"
                            style={{ width: `${t.score}%` }}
                          />
                        </div>
                        <span
                          className={`rounded-full px-2 py-0.5 text-xs font-medium capitalize ${strengthColor(
                            t.strength_label
                          )}`}
                        >
                          {t.strength_label}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </Card>
      )}

      <Card>
        <h2 className="mb-4 text-lg font-semibold text-white">Recent Activity</h2>
        <div className="flex items-center justify-center py-8 text-gray-500">
          <p>No activity yet. Start solving questions!</p>
        </div>
      </Card>
    </div>
  );
}
