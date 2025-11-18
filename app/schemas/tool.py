from pydantic import BaseModel, ConfigDict


class ToolBase(BaseModel):
    name: str
    slug: str
    description: str | None = None
    website_url: str | None = None
    logo_url:str | None = None
    pricing_type: str | None = None

class ToolCreate(ToolBase):
    pass

class ToolUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    website_url: str | None = None
    logo_url: str | None = None
    pricing_type: str | None = None

class Tool(ToolBase):
    id: int

    model_config = ConfigDict(from_attributes=True)