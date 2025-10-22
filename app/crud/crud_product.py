from sqlalchemy.orm import Session

from app import models
from app.models.category import Category
from app.models.tag import Tag
from app.schemas import product as schemas


def get_product(db: Session,
                product_id: int | None = None,
                slug: str | None = None) -> models.Product | None:
    """Retrieve a single product by ID or slug."""
    query = db.query(models.Product)
    if product_id is not None:
        return query.filter(models.Product.id == product_id).first()
    if slug is not None:
        return query.filter(models.Product.slug == slug).frist()
    return None

def get_products(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve multiple products."""
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product_in: schemas.ProductCreate) -> models.Product:
    """Create a new product."""
    product_data = product_in.model_dump(exclude_unset=True)
    category_ids = product_data.pop('category_ids', [])
    tag_ids = product_data.pop('tag_ids', [])

    db_product = models.Product(**product_data)

    for category_id in category_ids:
        category = db.query(Category).filter(Category.id == category_id).first()
        if category:
            db_product.categories.append(category)

    for tag_id in tag_ids:
        tag = db.query(Tag).filter(Tag.id == tag_id).first()
        if tag:
            db_product.tags.append(tag)

    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product



