"use client";

import { useParams } from "next/navigation";
import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import {
  Flame,
  CheckCircle2,
  Calendar,
  Target,
  Trophy,
} from "lucide-react";

export default function ProfilePage() {
  const params = useParams();
  const username = params.username as string;

  return (
    <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
      {/* Profile header */}
      <Card className="mb-8">
        <div className="flex items-center gap-6">
          <div className="flex h-20 w-20 items-center justify-center rounded-full bg-green-600 text-3xl font-bold text-white">
            {username[0]?.toUpperCase() || "U"}
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">@{username}</h1>
            <div className="mt-2 flex flex-wrap items-center gap-3">
              <Badge variant="success">User</Badge>
              <span className="flex items-center gap-1 text-xs text-gray-500">
                <Calendar className="h-3 w-3" />
                Joined recently
              </span>
            </div>
          </div>
        </div>
      </Card>

      {/* Stats */}
      <div className="mb-8 grid gap-4 sm:grid-cols-4">
        {[
          { label: "Problems Solved", value: "0", icon: CheckCircle2, color: "text-green-400" },
          { label: "Day Streak", value: "0", icon: Flame, color: "text-orange-400" },
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

      {/* Recent activity */}
      <Card>
        <h2 className="mb-4 text-lg font-semibold text-white">Recent Activity</h2>
        <div className="flex items-center justify-center py-8 text-gray-500">
          <p>No activity yet. Start solving questions!</p>
        </div>
      </Card>
    </div>
  );
}
