"""Groq API client for LLM-powered personalized suggestions."""

import json
import logging
from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Map assessment topic names to roadmap item titles (for rule-based suggestions and frontend matching)
TOPIC_TO_ROADMAP_TITLE: dict[str, dict[str, str]] = {
    "data-engineering": {
        "SQL Basics": "SQL Fundamentals",
        "SQL Joins": "Joins & Set Operations",
        "Aggregations & GROUP BY": "Aggregations & Grouping",
        "Subqueries": "Subqueries & CTEs",
        "Window Functions": "Window Functions",
        "CTEs & Recursive Queries": "Subqueries & CTEs",
        "Data Modeling": "Data Modeling & Schema Design",
        "ETL Pipelines": "ETL/ELT Pipelines",
        "Apache Spark": "Apache Spark Essentials",
        "Airflow Orchestration": "Airflow & Orchestration",
        "Performance Optimization": "Performance Tuning & System Design",
        "System Design": "Performance Tuning & System Design",
    },
}


def get_client():
    try:
        from groq import Groq
        return Groq(api_key=settings.GROQ_API_KEY or "gsk_dummy")
    except Exception:
        return None


def build_suggestions_prompt(topic_strengths: list[dict], domain_slug: str, domain_name: str) -> str:
    """Build prompt for Groq to return curated next steps."""
    strengths_text = "\n".join(
        f"- {s.get('topic_name', 'Topic')}: {s.get('strength_label', 'beginner')} (score {s.get('score', 0):.0f})"
        for s in topic_strengths
    )
    return f"""You are a data career coach. Based on the user's self-assessed topic strengths below, suggest a short, actionable learning plan for the domain "{domain_name}" ({domain_slug}).

User's topic strengths (0-100 score, beginner/intermediate/advanced):
{strengths_text}

Respond with a JSON object only, no markdown or extra text:
{{
  "summary": "One sentence on their overall level and focus area",
  "next_steps": [
    {{ "title": "Step title", "reason": "Why this is recommended", "priority": 1 }},
    ...
  ],
  "topics_to_study_first": ["topic name 1", "topic name 2"],
  "topics_to_skip_or_review_lightly": ["topic name if any"]
}}

Keep next_steps to 3-5 items. Be specific and personalized. If they are strong in SQL, suggest advancing to window functions or system design; if weak in stats, suggest starting with fundamentals."""


async def get_personalized_suggestions(
    topic_strengths: list[dict],
    domain_slug: str,
    domain_name: str,
) -> dict | None:
    """Call Groq to get personalized suggestions. Returns None if API key missing or call fails."""
    if not settings.GROQ_API_KEY:
        logger.warning("Groq suggestions skipped: GROQ_API_KEY is not set")
        return None
    try:
        client = get_client()
        if not client:
            logger.warning("Groq suggestions skipped: could not create Groq client")
            return None
        prompt = build_suggestions_prompt(topic_strengths, domain_slug, domain_name)
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=800,
        )
        text = response.choices[0].message.content
        # Strip markdown code block if present
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)
    except Exception as e:
        logger.exception("Groq API call failed: %s", e)
        return None


def build_rule_based_suggestions(
    topic_strengths: list[dict],
    domain_slug: str,
    domain_name: str,
) -> dict:
    """Build personalized suggestions from topic strengths when Groq is unavailable.
    Returns same shape as LLM: summary, next_steps, topics_to_study_first, topics_to_skip_or_review_lightly.
    Uses roadmap titles so the frontend can match and annotate roadmap items.
    """
    mapping = TOPIC_TO_ROADMAP_TITLE.get(domain_slug, {})
    strengths_for_domain = [s for s in topic_strengths if s.get("category_slug") == domain_slug]
    topics_to_skip: list[str] = []
    topics_to_study: list[str] = []
    advanced_count = 0
    for s in strengths_for_domain:
        topic_name = s.get("topic_name", "")
        label = (s.get("strength_label") or "").lower()
        roadmap_title = mapping.get(topic_name)
        if not roadmap_title:
            continue
        if label == "advanced":
            advanced_count += 1
            if roadmap_title not in topics_to_skip:
                topics_to_skip.append(roadmap_title)
        else:
            if roadmap_title not in topics_to_study:
                topics_to_study.append(roadmap_title)

    # Build summary and next_steps from strengths
    if advanced_count >= len(strengths_for_domain) and len(strengths_for_domain) > 0:
        summary = (
            f"You're strong in {domain_name} fundamentals from your assessment. "
            "Focus on later weeks (ETL, Spark, System Design) and use earlier weeks for quick review."
        )
        next_steps = [
            {"title": "Week 5+: Window Functions", "reason": "Deepen analytical SQL", "priority": 1},
            {"title": "Week 6: Data Modeling & Schema Design", "reason": "Design for scale", "priority": 2},
            {"title": "Week 7+: ETL & Spark", "reason": "Build production pipelines", "priority": 3},
        ]
    elif topics_to_study:
        summary = (
            f"Based on your assessment, we suggest focusing on the topics below first, "
            f"then advancing to later weeks in the {domain_name} roadmap."
        )
        next_steps = [
            {"title": t, "reason": "Recommended from your assessment", "priority": i + 1}
            for i, t in enumerate(topics_to_study[:3])
        ]
    else:
        summary = (
            f"Your {domain_name} assessment is in. Follow the roadmap in order; "
            "we'll highlight what to focus on as you go."
        )
        next_steps = []

    return {
        "summary": summary,
        "next_steps": next_steps,
        "topics_to_study_first": topics_to_study,
        "topics_to_skip_or_review_lightly": topics_to_skip,
    }


def _build_expand_week_prompt(
    roadmap_title: str,
    roadmap_description: str | None,
    week_number: int,
    duration_weeks: int,
    topic_strengths: list[dict],
    domain_name: str,
) -> str:
    strengths_text = "\n".join(
        f"- {s.get('topic_name', 'Topic')}: {s.get('strength_label', 'beginner')}"
        for s in topic_strengths
    )
    return f"""You are a data career coach. The user is studying "{domain_name}" and has chosen to spend {duration_weeks} weeks on this domain. For Week {week_number}: "{roadmap_title}" ({roadmap_description or 'N/A'}), provide a granular breakdown and curated resources.

User's topic strengths for this domain:
{strengths_text or 'Not yet assessed.'}

Respond with a JSON object only, no markdown or extra text:
{{
  "granular_tasks": [
    "Day 1-2: Specific subtopic or task (e.g. SELECT and WHERE practice)",
    "Day 3-4: Next subtopic",
    "... 5-8 items total, split by days or sub-topics"
  ],
  "resources": [
    {{ "type": "youtube", "title": "Video title", "url": "https://www.youtube.com/watch?v=...", "description": "Why this helps" }},
    {{ "type": "article", "title": "Article title", "url": "https://medium.com/... or real article URL", "source": "Medium" }},
    {{ "type": "book", "title": "Book title", "author": "Author name", "url": "https://www.amazon.com/... or O'Reilly link", "reason": "Why recommended" }}
  ]
}}

Rules:
- granular_tasks: 5-8 items, each a short string. Adapt depth to user level (advanced = less basics, more projects).
- resources: Include 2-3 YouTube (real URLs), 1-2 articles (Medium, freeCodeCamp, or official docs), and 1-2 book recommendations with real Amazon or O'Reilly URLs. All URLs must be valid https links.
- If the user is advanced in this week's topic, suggest "Review" or "Deep dive" tasks and more advanced resources."""


async def expand_week_content(
    roadmap_title: str,
    roadmap_description: str | None,
    week_number: int,
    duration_weeks: int,
    topic_strengths: list[dict],
    domain_name: str,
) -> dict | None:
    """LLM-generated granular tasks and resources (YouTube, articles, books) for a roadmap week."""
    if not settings.GROQ_API_KEY:
        logger.warning("Expand week skipped: GROQ_API_KEY is not set")
        return None
    try:
        client = get_client()
        if not client:
            return None
        prompt = _build_expand_week_prompt(
            roadmap_title, roadmap_description, week_number,
            duration_weeks, topic_strengths, domain_name,
        )
        response = client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1200,
        )
        text = response.choices[0].message.content
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        data = json.loads(text)
        if "granular_tasks" not in data:
            data["granular_tasks"] = []
        if "resources" not in data:
            data["resources"] = []
        return data
    except Exception as e:
        logger.exception("Expand week LLM failed: %s", e)
        return None


def build_fallback_expand_week(roadmap_title: str, roadmap_description: str | None) -> dict:
    """Fallback when LLM is unavailable: minimal granular tasks and generic links."""
    return {
        "granular_tasks": [
            "Review key concepts and definitions",
            "Watch 1–2 introductory videos",
            "Try hands-on exercises or small projects",
            "Read one article or doc section",
        ],
        "resources": [
            {"type": "youtube", "title": "Search YouTube", "url": "https://www.youtube.com/results?search_query=" + roadmap_title.replace(" ", "+"), "description": "Find videos on this topic"},
            {"type": "article", "title": "Medium – " + roadmap_title, "url": "https://medium.com/search?q=" + roadmap_title.replace(" ", "%20"), "source": "Medium"},
            {"type": "book", "title": "O'Reilly Learning", "author": "Various", "url": "https://www.oreilly.com/", "reason": "Books and courses for technical topics"},
        ],
    }
