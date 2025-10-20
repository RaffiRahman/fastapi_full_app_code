from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.menu import Menu
from app.models.menu_item import MenuItem
from app.models.page import Page
from app.models.site_setting import SiteSetting
from app.schemas import cms as schemas


router = APIRouter()


@router.get("/menus/{location_slug}", response_model=schemas.Menu)
def read_menu(location_slug: str, db: Session = Depends(get_db)):
    """Retrieve a menu by its location slug."""
    menu = db.query(Menu).filter(Menu.location_slug == location_slug).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    items = (
        db.query(MenuItem)
        .filter(MenuItem.menu_id == menu.id)
        .order_by(MenuItem.order)
        .all()
    )

    def build_tree(parent: MenuItem) -> schemas.MenuItem:
        children = (
            db.query(MenuItem)
            .filter(MenuItem.parent_id == parent.id)
            .order_by(MenuItem.order)
            .all()
        )
        return schemas.MenuItem(
            title=str(parent.title),
            url=str(parent.url),
            children=[build_tree(child) for child in children],
        )
    return schemas.Menu(name=str(menu.name), items=[build_tree(i) for i in items])
