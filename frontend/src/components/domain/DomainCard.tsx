"use client";

import Link from "next/link";
import {
  Database,
  BarChart3,
  BrainCircuit,
  Cpu,
  Settings2,
  Wrench,
  Sparkles,
  PieChart,
  Layers,
  Eye,
  type LucideIcon,
} from "lucide-react";

const ICON_MAP: Record<string, LucideIcon> = {
  "data-engineering": Database,
  "data-science": BarChart3,
  "machine-learning": BrainCircuit,
  "data-analytics": Cpu,
  mlops: Settings2,
  "devops-dataops": Wrench,
  "generative-ai": Sparkles,
  "business-intelligence": PieChart,
  "data-architecture": Layers,
  "nlp-computer-vision": Eye,
};

const COLOR_MAP: Record<string, { text: string; bg: string; border: string }> = {
  "data-engineering": { text: "text-blue-400", bg: "bg-blue-500/10", border: "border-blue-500/30" },
  "data-science": { text: "text-purple-400", bg: "bg-purple-500/10", border: "border-purple-500/30" },
  "machine-learning": { text: "text-orange-400", bg: "bg-orange-500/10", border: "border-orange-500/30" },
  "data-analytics": { text: "text-green-400", bg: "bg-green-500/10", border: "border-green-500/30" },
  mlops: { text: "text-cyan-400", bg: "bg-cyan-500/10", border: "border-cyan-500/30" },
  "devops-dataops": { text: "text-yellow-400", bg: "bg-yellow-500/10", border: "border-yellow-500/30" },
  "generative-ai": { text: "text-pink-400", bg: "bg-pink-500/10", border: "border-pink-500/30" },
  "business-intelligence": { text: "text-indigo-400", bg: "bg-indigo-500/10", border: "border-indigo-500/30" },
  "data-architecture": { text: "text-teal-400", bg: "bg-teal-500/10", border: "border-teal-500/30" },
  "nlp-computer-vision": { text: "text-rose-400", bg: "bg-rose-500/10", border: "border-rose-500/30" },
};

interface DomainCardProps {
  name: string;
  slug: string;
  description: string | null;
}

export function getDomainIcon(slug: string): LucideIcon {
  return ICON_MAP[slug] || Database;
}

export function getDomainColors(slug: string) {
  return COLOR_MAP[slug] || COLOR_MAP["data-engineering"];
}

export default function DomainCard({ name, slug, description }: DomainCardProps) {
  const Icon = getDomainIcon(slug);
  const colors = getDomainColors(slug);

  return (
    <Link href={`/domain/${slug}`}>
      <div
        className={`group relative overflow-hidden rounded-2xl border ${colors.border} bg-gray-900/60 p-6 transition-all hover:scale-[1.02] hover:border-opacity-60 hover:shadow-lg hover:shadow-black/20`}
      >
        <div className={`mb-4 inline-flex rounded-xl p-3 ${colors.bg}`}>
          <Icon className={`h-7 w-7 ${colors.text}`} />
        </div>
        <h3 className="text-lg font-semibold text-white group-hover:text-green-400 transition-colors">
          {name}
        </h3>
        <p className="mt-2 text-sm leading-relaxed text-gray-400">{description}</p>
        <div className="mt-4 flex items-center gap-1 text-xs font-medium text-gray-500 group-hover:text-gray-300 transition-colors">
          Start learning →
        </div>
      </div>
    </Link>
  );
}
