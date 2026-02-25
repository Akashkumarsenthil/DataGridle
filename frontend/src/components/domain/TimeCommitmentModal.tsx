"use client";

import { useState } from "react";
import { Calendar, X } from "lucide-react";

const PRESET_WEEKS = [
  { label: "4 weeks", value: 4 },
  { label: "8 weeks", value: 8 },
  { label: "12 weeks", value: 12 },
  { label: "6 months", value: 26 },
  { label: "1 year", value: 52 },
];

interface TimeCommitmentModalProps {
  domainName: string;
  onSave: (durationWeeks: number) => Promise<void>;
  onSkip?: () => void;
}

export default function TimeCommitmentModal({
  domainName,
  onSave,
  onSkip,
}: TimeCommitmentModalProps) {
  const [customWeeks, setCustomWeeks] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (weeks: number) => {
    if (weeks < 1 || weeks > 104) {
      setError("Choose between 1 and 104 weeks");
      return;
    }
    setError(null);
    setSaving(true);
    try {
      await onSave(weeks);
    } catch {
      setError("Failed to save. Try again.");
    } finally {
      setSaving(false);
    }
  };

  const handlePreset = (value: number) => handleSubmit(value);
  const handleCustom = () => {
    const n = parseInt(customWeeks, 10);
    if (Number.isNaN(n)) {
      setError("Enter a number");
      return;
    }
    handleSubmit(n);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4">
      <div className="w-full max-w-md rounded-2xl border border-gray-800 bg-gray-900 p-6 shadow-xl">
        <div className="mb-4 flex items-center justify-between">
          <div className="flex items-center gap-2 text-green-400">
            <Calendar className="h-5 w-5" />
            <span className="font-semibold">Set your pace</span>
          </div>
          {onSkip && (
            <button
              type="button"
              onClick={onSkip}
              className="rounded-lg p-1 text-gray-500 hover:bg-gray-800 hover:text-white"
              aria-label="Skip"
            >
              <X className="h-5 w-5" />
            </button>
          )}
        </div>
        <p className="mb-5 text-sm text-gray-400">
          How many weeks or months can you spend on <span className="text-white">{domainName}</span>? We&apos;ll tailor your roadmap and suggestions.
        </p>
        <div className="mb-4 grid grid-cols-2 gap-2 sm:grid-cols-3">
          {PRESET_WEEKS.map(({ label, value }) => (
            <button
              key={value}
              type="button"
              onClick={() => handlePreset(value)}
              disabled={saving}
              className="rounded-lg border border-gray-700 bg-gray-800/50 py-2.5 text-sm font-medium text-white transition hover:border-green-600 hover:bg-green-600/10 disabled:opacity-50"
            >
              {label}
            </button>
          ))}
        </div>
        <div className="flex gap-2">
          <input
            type="number"
            min={1}
            max={104}
            placeholder="Custom weeks"
            value={customWeeks}
            onChange={(e) => setCustomWeeks(e.target.value)}
            className="flex-1 rounded-lg border border-gray-700 bg-gray-800 px-3 py-2 text-sm text-white placeholder-gray-500 focus:border-green-500 focus:outline-none"
          />
          <button
            type="button"
            onClick={handleCustom}
            disabled={saving || !customWeeks.trim()}
            className="rounded-lg bg-green-600 px-4 py-2 text-sm font-medium text-white hover:bg-green-500 disabled:opacity-50"
          >
            OK
          </button>
        </div>
        {error && <p className="mt-2 text-sm text-red-400">{error}</p>}
      </div>
    </div>
  );
}
