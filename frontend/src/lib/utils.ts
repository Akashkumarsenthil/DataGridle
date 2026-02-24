import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

export function getDifficultyColor(difficulty: string) {
  switch (difficulty) {
    case "easy":
      return "text-green-500 bg-green-500/10";
    case "medium":
      return "text-yellow-500 bg-yellow-500/10";
    case "hard":
      return "text-red-500 bg-red-500/10";
    default:
      return "text-gray-500 bg-gray-500/10";
  }
}

export function getCategorySlug(name: string) {
  return name.toLowerCase().replace(/\s+/g, "-").replace(/_/g, "-");
}
