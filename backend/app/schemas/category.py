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
