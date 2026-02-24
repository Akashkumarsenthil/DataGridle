from pydantic import BaseModel


class CompanyResponse(BaseModel):
    id: int
    company_name: str
    logo_url: str | None
    industry: str | None
    description: str | None

    model_config = {"from_attributes": True}
