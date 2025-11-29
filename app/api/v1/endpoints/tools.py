from email.policy import default

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import crud_tool
from app.dependencies import get_current_superuser, get_db
from app.schemas.tool import Tool, ToolCreate, ToolUpdate

router = APIRouter()

@router.post("/", response_model=Tool, status_code=status.HTTP_201_CREATED)
def create_tool(
        tool: ToolCreate,
        db: Session = Depends(get_db),
        current_superuser: bool = Depends(get_current_superuser)
):
    db_tool = crud_tool.get_tool_by_slug(db, slug=tool.slug)
    if db_tool:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tool with this slug already exists")
    return crud_tool.create_tool(db, tool)

@router.get("/", response_model=list[Tool])
def read_tools(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tools = crud_tool.get_tools(db, skip=skip, limit=limit)
    return tools

@router.get("/{tool_id}", response_model=Tool)
def read_tool(tool_id: int, db: Session = Depends(get_db)):
    tool = crud_tool.get_tool(db, tool_id)
    if not tool:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tool not found")
    return tool

@router.get("/slug/{slug}", response_model=Tool)
def read_tool_by_slug(slug: str, db: Session = Depends(get_db)):
    tool = crud_tool.get_tool_by_slug(db, slug=slug)
    if not tool:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tool not found")
    return tool

@router.put("/{tool_id}", response_model= Tool)
def update_tool(
        tool_id: int,
        tool_update: ToolUpdate,
        db: Session = Depends(get_db),
        current_superuser: bool = Depends(get_current_superuser),
):
    db_tool = crud_tool.get_tool(db, tool_id=tool_id)
    if not db_tool:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tool not found")
    return crud_tool.update_tool(db, db_tool, tool_update)

@router.delete("/{tool_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tool(tool_id: int, db: Session = Depends(get_db), current_superuser: bool = Depends(get_current_superuser)):
    db_tool = crud_tool.get_tool(db, tool_id=tool_id)
    if not db_tool:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tool not found")
    crud_tool.delete_tool(db, db_tool)
    return
