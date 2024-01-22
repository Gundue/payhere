from sqlalchemy import update
from sqlalchemy.orm import Session
from schemas import product_schema
import models

"""
product create method
"""


def create_product(db: Session, product: product_schema.CreateProduct):
    db_product = models.Product(
        user_id=product.user_id,
        category=product.category,
        price=product.price,
        cost=product.cost,
        name=product.name,
        description=product.description,
        barcode=product.barcode,
        expiration_date=product.expiration_date,
        size=product.size
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return {"success": "Product create"}


"""
product update method
"""


def update_product(db: Session, product: product_schema.Product):
    db_prodcut = (
        update(models.Product)
        .where(
            models.Product.id == product.id,
            models.Product.user_id == product.user_id
        )
        .values(
            category=product.category,
            price=product.price,
            cost=product.cost,
            name=product.name,
            description=product.description,
            barcode=product.barcode,
            expiration_date=product.expiration_date,
            size=product.size
        )
        .execution_options(synchronize_session="fetch")
    )

    db.execute(db_prodcut)
    db.commit()

    return {"success": "Product updated successfully"}


"""
product get method
"""


def read_product(db: Session, user_id: int):
    return (
        db.query(models.Product)
        .filter(
            (models.Product.user_id == user_id)
        )
        .all()
    )


"""
product like search method
"""


def read_product_name(db: Session, user_id: int, product_name: str):
    return search_by_initials(product_name, db.query(models.Product)
                              .filter(models.Product.user_id == user_id)
        .all())


"""
prodcut cursor based pagination method
"""


def read_product_lists(db: Session, user_id: int, cursor: int, limit: int):
    return (
        db.query(models.Product)
        .filter(models.Product.user_id == user_id)
        .filter(models.Product.id > cursor)
        .limit(limit)
        .with_entities(models.Product.id, models.Product.category, models.Product.name)
        .all()
    )


"""
product detail method
"""


def product_detail(db: Session, user_id: int, product_id: int):
    return (
        db.query(models.Product)
        .filter(
            models.Product.user_id == user_id,
            models.Product.id == product_id
        )
        .all()
    )


"""
product delete method
"""


def delete_product(db: Session, user_id: int, product_id: int):
    db.query(models.Product).filter(
            models.Product.user_id == user_id,
            models.Product.id == product_id
        ).delete()
    db.commit()

    return {"success": "Product delete"}

# 한글 초성 추출
def extract_initials(char):
    if '가' <= char <= '힣':
        char_code = ord(char) - 44032
        initial_index = char_code // (21 * 28)
        initials = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
        return initials[initial_index]
    else:
        return char

# 초성이 포함된 항목 반환
def search_by_initials(keyword, data):
    keyword_initials = ''.join([extract_initials(char) for char in keyword])
    result = [item for item in data if keyword_initials in ''.join([extract_initials(char) for char in item.name])]
    return result

