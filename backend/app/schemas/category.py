from pydantic import BaseModel


class CategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None
    icon_url: str | None

    model_config = {"from_attributes": True}


class TopicResponse(BaseModel):
    id: int
    category_id: int
    name: str
    difficulty_level: str
    order_index: int

    model_config = {"from_attributes": True}


class RoadmapItemResponse(BaseModel):
    id: int
    category_id: int
    title: str
    description: str | None
    order_index: int
    week_number: int
    estimated_hours: int

    model_config = {"from_attributes": True}


class LearningResourceResponse(BaseModel):
    id: int
    category_id: int
    topic_id: int | None
    roadmap_item_id: int | None
    title: str
    url: str
    resource_type: str
    difficulty_level: str | None
    estimated_duration_minutes: int | None
    order_in_playlist: int

    model_config = {"from_attributes": True}
