export interface User {
  id: string;
  username: string;
  email: string;
  role: "user" | "creator" | "admin" | "moderator";
  is_verified: boolean;
  experience_level: string | null;
  target_role: string | null;
  avatar_url: string | null;
  streak_count: number;
  created_at: string;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string | null;
  icon_url: string | null;
}

export interface Topic {
  id: number;
  category_id: number;
  name: string;
  difficulty_level: string;
  order_index: number;
}

export interface Question {
  id: number;
  topic_id: number;
  category_id: number;
  creator_id: string;
  title: string;
  description: string;
  question_type: "sql" | "python" | "mcq" | "case_study";
  difficulty: "easy" | "medium" | "hard";
  starter_code: string | null;
  status: string;
  interview_year: number | null;
  frequency_count: number;
  created_at: string;
  test_cases?: Record<string, unknown> | null;
  expected_output?: Record<string, unknown> | null;
  explanation?: string | null;
}

export interface Submission {
  id: number;
  question_id: number;
  submitted_code: string;
  language: string;
  result: "pass" | "fail" | "partial" | "error";
  execution_time_ms: number | null;
  score: number | null;
  submitted_at: string;
}

export interface Company {
  id: number;
  company_name: string;
  logo_url: string | null;
  industry: string | null;
  description: string | null;
}

export interface Discussion {
  id: number;
  author_id: string;
  category: string;
  title: string;
  body: string;
  upvotes: number;
  downvotes: number;
  is_locked: boolean;
  created_at: string;
}

export interface DiscussionComment {
  id: number;
  discussion_id: number;
  author_id: string;
  parent_comment_id: number | null;
  body: string;
  upvotes: number;
  downvotes: number;
  created_at: string;
}

export interface RoadmapItem {
  id: number;
  category_id: number;
  title: string;
  description: string | null;
  order_index: number;
  week_number: number;
  estimated_hours: number;
}

export interface LearningResource {
  id: number;
  category_id: number;
  topic_id: number | null;
  roadmap_item_id: number | null;
  title: string;
  url: string;
  resource_type: "video" | "article" | "playlist";
  difficulty_level: string | null;
  estimated_duration_minutes: number | null;
  order_in_playlist: number;
}
