"use client";

import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import Badge from "@/components/ui/Badge";
import { Users, FileQuestion, Shield, BarChart3 } from "lucide-react";

export default function AdminDashboardPage() {
  return (
    <div className="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">Admin Dashboard</h1>
        <p className="mt-1 text-gray-400">Manage users, questions, and platform settings</p>
      </div>

      {/* Stats */}
      <div className="mb-10 grid gap-4 sm:grid-cols-4">
        {[
          { label: "Total Users", value: "0", icon: Users, color: "text-blue-400" },
          { label: "Total Questions", value: "0", icon: FileQuestion, color: "text-green-400" },
          { label: "Pending Approvals", value: "0", icon: Shield, color: "text-yellow-400" },
          { label: "Active Today", value: "0", icon: BarChart3, color: "text-purple-400" },
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

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Pending Creators */}
        <Card>
          <h2 className="mb-4 text-lg font-semibold text-white">Pending Creator Applications</h2>
          <div className="flex items-center justify-center py-8 text-gray-500">
            No pending applications.
          </div>
        </Card>

        {/* Pending Questions */}
        <Card>
          <h2 className="mb-4 text-lg font-semibold text-white">Pending Questions</h2>
          <div className="flex items-center justify-center py-8 text-gray-500">
            No questions awaiting review.
          </div>
        </Card>
      </div>
    </div>
  );
}
