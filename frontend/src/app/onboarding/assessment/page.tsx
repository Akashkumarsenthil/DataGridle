"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Button from "@/components/ui/Button";
import Card from "@/components/ui/Card";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";
import type { AssessmentQuestion } from "@/types";

export default function OnboardingAssessmentPage() {
  const router = useRouter();
  const { user, loading: authLoading, refresh } = useAuth();
  const [questions, setQuestions] = useState<AssessmentQuestion[]>([]);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [step, setStep] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const [loadError, setLoadError] = useState("");

  useEffect(() => {
    if (authLoading) return;
    if (!user) {
      router.replace("/auth/login");
      return;
    }
    if (user.assessment_completed_at) {
      router.replace("/dashboard");
      return;
    }
    api
      .get<AssessmentQuestion[]>("/assessment/questions")
      .then(setQuestions)
      .catch(() => setLoadError("Failed to load questions"));
  }, [user, authLoading, router]);

  const current = questions[step];
  const progress = questions.length ? ((step + 1) / questions.length) * 100 : 0;

  const handleSubmitAssessment = async () => {
    const missing = questions.filter((q) => answers[q.id] === undefined || answers[q.id] === "");
    if (missing.length > 0) {
      return;
    }
    setSubmitting(true);
    try {
      await api.post("/assessment/submit", {
        answers: Object.entries(answers).map(([question_id, answer_value]) => ({
          question_id: Number(question_id),
          answer_value,
        })),
      });
      await refresh();
      router.replace("/dashboard");
    } catch {
      setSubmitting(false);
    }
  };

  if (authLoading || (user && !user.assessment_completed_at && !loadError && !questions.length)) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-green-500 border-t-transparent" />
      </div>
    );
  }

  if (loadError) {
    return (
      <div className="mx-auto max-w-lg px-4 py-12 text-center">
        <p className="text-red-400">{loadError}</p>
        <Button className="mt-4" onClick={() => router.push("/dashboard")}>
          Go to Dashboard
        </Button>
      </div>
    );
  }

  if (!current) {
    return null;
  }

  const optionKeys = current.options ? Object.keys(current.options) : [];
  const value = answers[current.id] ?? "";

  return (
    <div className="mx-auto max-w-2xl px-4 py-8 sm:px-6 lg:px-8">
      <div className="mb-8 text-center">
        <h1 className="text-2xl font-bold text-white">Quick skill check</h1>
        <p className="mt-2 text-gray-400">
          We’ll use this to personalize your learning path and suggestions.
        </p>
        <div className="mt-4 h-2 overflow-hidden rounded-full bg-gray-800">
          <div
            className="h-full rounded-full bg-green-500 transition-all"
            style={{ width: `${progress}%` }}
          />
        </div>
        <p className="mt-2 text-xs text-gray-500">
          Question {step + 1} of {questions.length}
        </p>
      </div>

      <Card className="p-6 sm:p-8">
        <h2 className="text-lg font-medium text-white">{current.question_text}</h2>

        {current.question_type === "scale" && current.scale_max && (
          <div className="mt-6 flex flex-wrap gap-2">
            {Array.from({ length: current.scale_max }, (_, i) => i + 1).map((n) => (
              <button
                key={n}
                type="button"
                onClick={() => setAnswers((a) => ({ ...a, [current.id]: String(n) }))}
                className={`h-12 w-12 rounded-lg border-2 text-lg font-medium transition-colors ${
                  value === String(n)
                    ? "border-green-500 bg-green-500/20 text-green-300"
                    : "border-gray-700 bg-gray-800 text-gray-300 hover:border-gray-600"
                }`}
              >
                {n}
              </button>
            ))}
          </div>
        )}

        {current.question_type === "mcq" && current.options && (
          <div className="mt-6 space-y-2">
            {optionKeys.map((key) => (
              <button
                key={key}
                type="button"
                onClick={() => setAnswers((a) => ({ ...a, [current.id]: key }))}
                className={`w-full rounded-lg border-2 px-4 py-3 text-left text-sm transition-colors ${
                  value === key
                    ? "border-green-500 bg-green-500/20 text-green-300"
                    : "border-gray-700 bg-gray-800 text-gray-300 hover:border-gray-600"
                }`}
              >
                <span className="font-medium uppercase text-gray-500">{key}.</span>{" "}
                {current.options[key]}
              </button>
            ))}
          </div>
        )}

        <div className="mt-8 flex justify-between">
          <Button
            variant="outline"
            onClick={() => setStep((s) => Math.max(0, s - 1))}
            disabled={step === 0}
          >
            Back
          </Button>
          {step < questions.length - 1 ? (
            <Button
              onClick={() => setStep((s) => s + 1)}
              disabled={value === ""}
            >
              Next
            </Button>
          ) : (
            <Button onClick={handleSubmitAssessment} disabled={value === "" || submitting}>
              {submitting ? "Saving…" : "Finish"}
            </Button>
          )}
        </div>
      </Card>
    </div>
  );
}
