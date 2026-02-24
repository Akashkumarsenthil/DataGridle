import Link from "next/link";
import Card from "@/components/ui/Card";
import Button from "@/components/ui/Button";
import {
  Database,
  BrainCircuit,
  BarChart3,
  Cpu,
  ArrowRight,
  Code2,
  Users,
  Building2,
  Zap,
} from "lucide-react";

const categories = [
  {
    name: "Data Engineering",
    slug: "data-engineering",
    icon: Database,
    description: "SQL, ETL pipelines, data modeling, Spark, Airflow",
    color: "text-blue-400",
    bgColor: "bg-blue-500/10",
    questions: 150,
  },
  {
    name: "Data Science",
    slug: "data-science",
    icon: BarChart3,
    description: "Statistics, pandas, hypothesis testing, A/B tests",
    color: "text-purple-400",
    bgColor: "bg-purple-500/10",
    questions: 120,
  },
  {
    name: "Machine Learning",
    slug: "machine-learning",
    icon: BrainCircuit,
    description: "Model training, evaluation, feature engineering, NLP",
    color: "text-orange-400",
    bgColor: "bg-orange-500/10",
    questions: 100,
  },
  {
    name: "Data Analytics",
    slug: "data-analytics",
    icon: Cpu,
    description: "Business metrics, dashboards, product analytics, SQL",
    color: "text-green-400",
    bgColor: "bg-green-500/10",
    questions: 80,
  },
];

const features = [
  {
    icon: Code2,
    title: "In-Browser SQL Sandbox",
    description: "Run SQL directly in your browser with DuckDB-WASM. No setup. Zero cost.",
  },
  {
    icon: Building2,
    title: "Company-Tagged Questions",
    description: "Practice real interview questions tagged by company, role, and round.",
  },
  {
    icon: Users,
    title: "Community Driven",
    description: "Share interview experiences, find study partners, and learn together.",
  },
  {
    icon: Zap,
    title: "Structured Learning Paths",
    description: "Follow curated roadmaps from beginner to interview-ready.",
  },
];

export default function Home() {
  return (
    <div>
      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-green-900/20 via-gray-950 to-gray-950" />
        <div className="relative mx-auto max-w-7xl px-4 py-24 sm:px-6 sm:py-32 lg:px-8">
          <div className="mx-auto max-w-3xl text-center">
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-green-500/20 bg-green-500/10 px-4 py-1.5 text-sm text-green-400">
              <span className="h-2 w-2 rounded-full bg-green-400 animate-pulse" />
              Open Source &amp; Free Forever
            </div>
            <h1 className="text-4xl font-extrabold tracking-tight text-white sm:text-6xl">
              Master Data Interviews.{" "}
              <span className="bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent">
                Structured.
              </span>
            </h1>
            <p className="mt-6 text-lg leading-8 text-gray-400">
              The LeetCode for Data roles. Practice SQL, Python, ML, and analytics interview
              questions — with company tags, community discussions, and an in-browser code sandbox.
            </p>
            <div className="mt-10 flex items-center justify-center gap-4">
              <Link href="/auth/register">
                <Button size="lg">
                  Get Started Free
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
              <Link href="/questions">
                <Button variant="outline" size="lg">
                  Browse Questions
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Categories */}
      <section className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-white">Choose Your Path</h2>
          <p className="mt-3 text-gray-400">Four specialized tracks for data-focused interviews</p>
        </div>
        <div className="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {categories.map((cat) => (
            <Link key={cat.slug} href={`/${cat.slug}`}>
              <Card hover className="group h-full">
                <div className={`mb-4 inline-flex rounded-lg p-3 ${cat.bgColor}`}>
                  <cat.icon className={`h-6 w-6 ${cat.color}`} />
                </div>
                <h3 className="text-lg font-semibold text-white group-hover:text-green-400 transition-colors">
                  {cat.name}
                </h3>
                <p className="mt-2 text-sm text-gray-400">{cat.description}</p>
                <p className="mt-4 text-xs text-gray-500">{cat.questions}+ questions</p>
              </Card>
            </Link>
          ))}
        </div>
      </section>

      {/* Features */}
      <section className="border-t border-gray-800/50 bg-gray-900/20">
        <div className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-white">Everything You Need</h2>
            <p className="mt-3 text-gray-400">Built for data professionals, by data professionals</p>
          </div>
          <div className="mt-12 grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
            {features.map((feature) => (
              <div key={feature.title} className="text-center">
                <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-green-500/10">
                  <feature.icon className="h-6 w-6 text-green-400" />
                </div>
                <h3 className="text-base font-semibold text-white">{feature.title}</h3>
                <p className="mt-2 text-sm text-gray-400">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8">
        <Card className="relative overflow-hidden bg-gradient-to-br from-green-900/40 to-gray-900 text-center">
          <div className="relative z-10">
            <h2 className="text-3xl font-bold text-white">Ready to Start Practicing?</h2>
            <p className="mx-auto mt-4 max-w-xl text-gray-400">
              Join thousands of data professionals preparing for their next interview.
              100% free and open source.
            </p>
            <div className="mt-8">
              <Link href="/auth/register">
                <Button size="lg">
                  Create Free Account
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
            </div>
          </div>
        </Card>
      </section>
    </div>
  );
}
