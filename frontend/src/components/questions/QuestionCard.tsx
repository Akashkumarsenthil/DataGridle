"use client";

import Link from "next/link";
import Badge from "@/components/ui/Badge";
import { getDifficultyColor } from "@/lib/utils";
import type { Question } from "@/types";

interface QuestionCardProps {
  question: Question;
}

const difficultyVariant = {
  easy: "success" as const,
  medium: "warning" as const,
  hard: "danger" as const,
};

export default function QuestionCard({ question }: QuestionCardProps) {
  return (
    <Link
      href={`/question/${question.id}`}
      className="group flex items-center justify-between rounded-lg border border-gray-800 bg-gray-900/30 px-5 py-4 transition-all hover:border-gray-700 hover:bg-gray-900/60"
    >
      <div className="flex-1">
        <h3 className="text-sm font-medium text-white group-hover:text-green-400 transition-colors">
          {question.title}
        </h3>
        <div className="mt-1.5 flex items-center gap-3">
          <Badge variant={difficultyVariant[question.difficulty]}>
            {question.difficulty}
          </Badge>
          <span className="text-xs text-gray-500 uppercase">{question.question_type}</span>
        </div>
      </div>
      <div className="text-right">
        {question.frequency_count > 0 && (
          <span className="text-xs text-gray-500">{question.frequency_count}x asked</span>
        )}
      </div>
    </Link>
  );
}
