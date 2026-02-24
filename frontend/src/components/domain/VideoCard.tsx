"use client";

import { Clock, ExternalLink } from "lucide-react";
import type { LearningResource } from "@/types";

function extractYoutubeId(url: string): string | null {
  const match = url.match(
    /(?:youtube\.com\/(?:watch\?v=|embed\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})/
  );
  return match ? match[1] : null;
}

function formatDuration(minutes: number | null): string {
  if (!minutes) return "";
  if (minutes < 60) return `${minutes} min`;
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return m > 0 ? `${h}h ${m}m` : `${h}h`;
}

interface VideoCardProps {
  resource: LearningResource;
}

export default function VideoCard({ resource }: VideoCardProps) {
  const videoId = extractYoutubeId(resource.url);
  const thumbnailUrl = videoId
    ? `https://img.youtube.com/vi/${videoId}/mqdefault.jpg`
    : null;

  return (
    <div className="group overflow-hidden rounded-xl border border-gray-800 bg-gray-900/50 transition-all hover:border-gray-700">
      {/* Thumbnail / Embed */}
      {videoId ? (
        <div className="relative aspect-video w-full overflow-hidden bg-black">
          <iframe
            src={`https://www.youtube.com/embed/${videoId}`}
            title={resource.title}
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
            className="absolute inset-0 h-full w-full"
          />
        </div>
      ) : (
        <div className="flex aspect-video items-center justify-center bg-gray-800 text-gray-500 text-sm">
          Video preview unavailable
        </div>
      )}

      {/* Info */}
      <div className="p-4">
        <h3 className="font-medium text-white text-sm leading-snug line-clamp-2">
          {resource.title}
        </h3>
        <div className="mt-2 flex items-center gap-3 text-xs text-gray-500">
          {resource.estimated_duration_minutes && (
            <span className="flex items-center gap-1">
              <Clock className="h-3 w-3" />
              {formatDuration(resource.estimated_duration_minutes)}
            </span>
          )}
          <a
            href={resource.url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1 text-green-500 hover:text-green-400 transition-colors"
          >
            <ExternalLink className="h-3 w-3" />
            YouTube
          </a>
        </div>
      </div>
    </div>
  );
}
