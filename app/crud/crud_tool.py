from sqlalchemy.orm import Session

from app.models.tool import Tool
from app.schemas.tool import ToolCreate, ToolUpdate


def get_tool(db: Session, tool_id: int) -> Tool | None:
    return db.query(Tool).filter(Tool.id == tool_id).first()

def get_tool_by_slug(db:Session, slug: str) -> Tool | None:
    return db.query(Tool).filter(Tool.slug == slug).first()

def get_tools(db: Session, skip: int = 0, limit: int = 100) -> list[Tool]:
    return db.query(Tool).offset(skip).limit(limit).all()

def create_tool(db: Session, tool: ToolCreate) -> Tool:
    db_tool = Tool(**tool.model_dump())
    db.add(db_tool)
    db.commit()
    db.refresh(db_tool)
    return db_tool

def update_tool(db: Session, tool: Tool, tool_in: ToolUpdate) -> Tool:
    for field, value in tool_in.model_dump(exclude_unset=True).items():
        setattr(tool, field, value)
    db.add(tool)
    db.commit()
    db.refresh(tool)
    return tool

def delete_tool(db: Session, tool: Tool):
    db.delete(tool)
    db.commit()


