"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import DomainCard from "@/components/domain/DomainCard";
import { api } from "@/lib/api";
import type { Category } from "@/types";
import {
  ArrowRight,
  Code2,
  Users,
  Building2,
  Zap,
  GraduationCap,
} from "lucide-react";

const features = [
  {
    icon: GraduationCap,
    title: "Curated Roadmaps",
    description:
      "Week-by-week learning paths designed by practitioners for each data domain.",
  },
  {
    icon: Code2,
    title: "In-Browser SQL Sandbox",
    description:
      "Run SQL directly in your browser with DuckDB-WASM. No setup required.",
  },
  {
    icon: Building2,
    title: "Company-Tagged Questions",
    description:
      "Practice real interview questions tagged by company, role, and round.",
  },
  {
    icon: Users,
    title: "Community Driven",
    description:
      "Share interview experiences, find study partners, and learn together.",
  },
  {
    icon: Zap,
    title: "YouTube Study Guides",
    description:
      "Curated video lessons from top creators, organized by topic and difficulty.",
  },
];

export default function Home() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .get<Category[]>("/categories/")
      .then(setCategories)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-green-900/20 via-gray-950 to-gray-950" />
        <div className="relative mx-auto max-w-7xl px-4 py-20 sm:px-6 sm:py-28 lg:px-8">
          <div className="mx-auto max-w-3xl text-center">
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-green-500/20 bg-green-500/10 px-4 py-1.5 text-sm text-green-400">
              <span className="h-2 w-2 rounded-full bg-green-400 animate-pulse" />
              Open Source &amp; Free Forever
            </div>
            <h1 className="text-4xl font-extrabold tracking-tight text-white sm:text-6xl">
              Your One-Stop{" "}
              <span className="bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent">
                Data Career
              </span>{" "}
              Prep
            </h1>
            <p className="mt-6 text-lg leading-8 text-gray-400">
              Pick your domain. Get a curated roadmap, video study guides, and
              hands-on practice questions — all in one place. From Data
              Engineering to Generative AI.
            </p>
            <div className="mt-8 flex items-center justify-center">
              <a href="#domains">
                <Button size="lg">
                  Pick Your Domain
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Domain Picker */}
      <section id="domains" className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-white">
            Choose Your Data Domain
          </h2>
          <p className="mt-3 text-gray-400">
            10+ specialized tracks with roadmaps, videos, and practice questions
          </p>
        </div>

        {loading ? (
          <div className="mt-12 flex justify-center">
            <div className="h-8 w-8 animate-spin rounded-full border-2 border-green-500 border-t-transparent" />
          </div>
        ) : (
          <div className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {categories.map((cat) => (
              <DomainCard
                key={cat.id}
                name={cat.name}
                slug={cat.slug}
                description={cat.description}
              />
            ))}
          </div>
        )}
      </section>

      {/* Features */}
      <section className="border-t border-gray-800/50 bg-gray-900/20">
        <div className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-white">
              Everything You Need to Prepare
            </h2>
            <p className="mt-3 text-gray-400">
              Built for data professionals, by data professionals
            </p>
          </div>
          <div className="mt-12 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {features.map((feature) => (
              <div
                key={feature.title}
                className="rounded-xl border border-gray-800 bg-gray-900/40 p-6"
              >
                <div className="mb-4 flex h-11 w-11 items-center justify-center rounded-xl bg-green-500/10">
                  <feature.icon className="h-5 w-5 text-green-400" />
                </div>
                <h3 className="text-base font-semibold text-white">
                  {feature.title}
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-gray-400">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8">
        <Card className="relative overflow-hidden bg-gradient-to-br from-green-900/40 to-gray-900 text-center">
          <div className="relative z-10">
            <h2 className="text-3xl font-bold text-white">
              Ready to Start Learning?
            </h2>
            <p className="mx-auto mt-4 max-w-xl text-gray-400">
              Join thousands of data professionals preparing for their next
              interview. 100% free and open source.
            </p>
            <div className="mt-8 flex items-center justify-center gap-4">
              <Link href="/auth/register">
                <Button size="lg">
                  Create Free Account
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
              <a href="#domains">
                <Button variant="outline" size="lg">
                  Browse Domains
                </Button>
              </a>
            </div>
          </div>
        </Card>
      </section>
    </div>
  );
}
