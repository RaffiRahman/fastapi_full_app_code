from sqlalchemy.orm import Session

from app.models import product
from app.models.category import Category
from app.models.tag import Tag
from app.schemas import product as schemas


def get_product(db: Session,
                product_id: int | None = None,
                slug: str | None = None) -> product.Product | None:
    """Retrieve a single product by ID or slug."""
    query = db.query(product.Product)
    if product_id is not None:
        return query.filter(product.Product.id == product_id).first()
    if slug is not None:
        return query.filter(product.Product.slug == slug).first()
    return None

def get_products(db: Session,
                 skip: int = 0,
                 limit: int = 100):
    """Retrieve multiple products."""
    return db.query(product.Product).offset(skip).limit(limit).all()


def create_product(db: Session,
                   product_in: schemas.ProductCreate) -> product.Product:
    """Create a new product."""
    product_data = product_in.model_dump(exclude_unset=True)
    category_ids = product_data.pop('category_ids', [])
    tag_ids = product_data.pop('tag_ids', [])

    db_product = product.Product(**product_data)

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


def update_product(db: Session,
                   db_product: product.Product,
                   product_in: schemas.ProductUpdate) -> product.Product:
    """Update an existing product."""
    update_data = product_in.model_dump(exclude_unset=True)

    if "category_ids" in update_data:
        new_category_ids = update_data.pop("category_ids")
        db_product.categories = []  # Clear existing categories
        for category_id in new_category_ids:
            category = db.query(Category).filter(Category.id == category_id).first()
            if category:
                db_product.categories.append(category)

    if "tag_ids" in update_data:
        new_tag_ids = update_data.pop("tag_ids")
        db_product.tags = []  # Clear existing tags
        for tag_id in new_tag_ids:
            tag = db.query(Tag).filter(Tag.id == tag_id).first()
            if tag:
                db_product.tags.append(tag)

    for field, value in update_data.items():
        setattr(db_product, field, value)

    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
