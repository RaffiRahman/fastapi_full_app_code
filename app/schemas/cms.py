from pydantic import BaseModel, ConfigDict


class MenuItem(BaseModel):
    title: str
    url: str
    children: list["MenuItem"] = []

    model_config = ConfigDict(from_attributes=True)


class Menu(BaseModel):
    name: str
    items: list[MenuItem]

    model_config = ConfigDict(from_attributes=True)


class Page(BaseModel):
    slug: str
    title: str
    subtitle: str | None = None
    body: str | None = None
    language: str

    model_config = ConfigDict(from_attributes=True)


class SiteSetting(BaseModel):
    key: str
    value: str | None = None

    model_config = ConfigDict(from_attributes=True)