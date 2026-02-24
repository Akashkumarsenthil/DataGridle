"use client";

import { useParams } from "next/navigation";
import Badge from "@/components/ui/Badge";
import Card from "@/components/ui/Card";
import SqlEditor from "@/components/questions/SqlEditor";
import { Building2, Clock, Tag } from "lucide-react";

const MOCK_QUESTION = {
  id: 1,
  title: "Find Duplicate Emails",
  difficulty: "easy" as const,
  question_type: "sql",
  description: `Write a SQL query to find all duplicate emails in the \`users\` table.

**Table: users**

| Column | Type |
|--------|------|
| id | int |
| email | varchar |

**Example Input:**

| id | email |
|----|-------|
| 1 | a@b.com |
| 2 | c@d.com |
| 3 | a@b.com |

**Expected Output:**

| email |
|-------|
| a@b.com |
`,
  starter_code: "-- Write your SQL query below\nSELECT email\nFROM users\nGROUP BY email\nHAVING COUNT(*) > 1;",
  company: "Google",
  frequency_count: 42,
  interview_year: 2025,
};

const difficultyVariant = {
  easy: "success" as const,
  medium: "warning" as const,
  hard: "danger" as const,
};

export default function QuestionDetailPage() {
  const params = useParams();

  const question = MOCK_QUESTION;

  return (
    <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Left: Problem description */}
        <div className="space-y-4">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <Badge variant={difficultyVariant[question.difficulty]}>
                {question.difficulty}
              </Badge>
              <span className="text-xs text-gray-500 uppercase">{question.question_type}</span>
            </div>
            <h1 className="text-xl font-bold text-white">
              {question.id}. {question.title}
            </h1>
          </div>

          <div className="flex flex-wrap items-center gap-4 text-xs text-gray-500">
            <span className="flex items-center gap-1">
              <Building2 className="h-3.5 w-3.5" />
              {question.company}
            </span>
            <span className="flex items-center gap-1">
              <Tag className="h-3.5 w-3.5" />
              Asked {question.frequency_count}x
            </span>
            <span className="flex items-center gap-1">
              <Clock className="h-3.5 w-3.5" />
              {question.interview_year}
            </span>
          </div>

          <Card className="prose prose-invert prose-sm max-w-none">
            <div
              className="text-sm text-gray-300 leading-relaxed"
              dangerouslySetInnerHTML={{ __html: formatMarkdown(question.description) }}
            />
          </Card>
        </div>

        {/* Right: Code editor */}
        <div className="lg:sticky lg:top-20 lg:self-start">
          <SqlEditor
            starterCode={question.starter_code || undefined}
            onSubmit={(code) => {
              console.log("Submitted:", code);
            }}
          />
        </div>
      </div>
    </div>
  );
}

function formatMarkdown(text: string): string {
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/`(.*?)`/g, '<code class="rounded bg-gray-800 px-1.5 py-0.5 text-green-400">$1</code>')
    .replace(/\n\n/g, "<br/><br/>")
    .replace(/\n/g, "<br/>")
    .replace(/\|(.*)\|/g, (match) => {
      const cells = match.split("|").filter(Boolean).map((c) => c.trim());
      return `<tr>${cells.map((c) => `<td class="border border-gray-700 px-3 py-1.5">${c}</td>`).join("")}</tr>`;
    });
}
