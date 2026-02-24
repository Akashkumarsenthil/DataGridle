"use client";

import { useState } from "react";
import Link from "next/link";
import Card from "@/components/ui/Card";
import Input from "@/components/ui/Input";
import { Search, Building2 } from "lucide-react";

const MOCK_COMPANIES = [
  { id: 1, name: "Google", industry: "Technology", questions: 45 },
  { id: 2, name: "Amazon", industry: "E-commerce / Cloud", questions: 62 },
  { id: 3, name: "Meta", industry: "Social Media", questions: 38 },
  { id: 4, name: "Apple", industry: "Technology", questions: 25 },
  { id: 5, name: "Netflix", industry: "Streaming", questions: 18 },
  { id: 6, name: "Microsoft", industry: "Technology", questions: 40 },
  { id: 7, name: "Uber", industry: "Transportation", questions: 30 },
  { id: 8, name: "Stripe", industry: "Fintech", questions: 22 },
  { id: 9, name: "Spotify", industry: "Music / Streaming", questions: 15 },
  { id: 10, name: "Airbnb", industry: "Travel / Hospitality", questions: 20 },
  { id: 11, name: "LinkedIn", industry: "Social / Professional", questions: 28 },
  { id: 12, name: "Twitter / X", industry: "Social Media", questions: 12 },
];

export default function CompaniesPage() {
  const [search, setSearch] = useState("");

  const filtered = MOCK_COMPANIES.filter((c) =>
    c.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="mx-auto max-w-5xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">Companies</h1>
        <p className="mt-1 text-gray-400">Practice interview questions by company</p>
      </div>

      <div className="relative mb-8 max-w-md">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-500" />
        <Input
          placeholder="Search companies..."
          className="pl-10"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {filtered.map((company) => (
          <Link key={company.id} href={`/companies/${company.id}`}>
            <Card hover className="group">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gray-800 text-sm font-bold text-white">
                  {company.name[0]}
                </div>
                <div>
                  <h3 className="font-medium text-white group-hover:text-green-400 transition-colors">
                    {company.name}
                  </h3>
                  <p className="text-xs text-gray-500">{company.industry}</p>
                </div>
              </div>
              <div className="mt-4 flex items-center justify-between text-xs text-gray-500">
                <span>{company.questions} questions</span>
                <Building2 className="h-3.5 w-3.5" />
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
