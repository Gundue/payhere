import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette import status
from datetime import datetime

import models
from crud.crud_product import create_product, update_product, read_product_name, product_pagination
from core.auth.jwt import encode_jwt
from db.database import engine
from schemas import product_schema
from routers import get_db

prefix = "prodcut"
models.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix=f"/{prefix}", responses={401: {"a": "a"}})


@router.post("/create")
async def product_create(product: product_schema.Product,  db: Session = Depends(get_db)):
    """
    `상품 등록`
    """
    return create_product(db, product)


@router.put("/update")
async def product_update(
        id: int = Form(example=1, description="index"),
        user_id: int = Form(example=1, description="user index"),
        category: str = Form(example="디저트", description="product category"),
        price: str = Form(example="5000", description="product price"),
        cost: str = Form(example="2500", description="product cost"),
        name: str = Form(example="마카롱", description="product name"),
        description: str = Form(example="달달한 마카롱", description="product description"),
        barcode: str = Form(example="바코드", description="product barcode"),
        expration_date: str = Form(example=datetime.now(), description="product expration_date"),
        size: str = Form(example="small", description="product size"),
        db: Session = Depends(get_db)):
    """
    `상품 수정`
    """
    product = product_schema.Product(
        id=id,
        user_id=user_id,
        category=category,
        price=price,
        cost=cost,
        name=name,
        description=description,
        barcode=barcode,
        expration_date=expration_date,
        size=size
    )

    return update_product(db, product)


@router.get("/user_id/{user_id}/cursor/{cursor}/limit/{limit}", response_model=product_schema.Product)
async def product_get(user_id: int, cursor: int, limit: int, db: Session = Depends(get_db)):
    """
    `상품 조회`
    """
    content = product_pagination(db, user_id, cursor, limit)
    if len(content):
        product_info = {
            f"{i + 1}": {"category": content[i][0], "name": content[i][1]}
            for i in range(len(content))
        }
        if len(product_info):
            return JSONResponse(content=jsonable_encoder(product_info))
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No data")




@router.get("/product_name/{product_name}")
async def product_search_get(product_name: str,  db: Session = Depends(get_db)):
    """
    `상품 like 조회`
    """
    content = read_product_name(db, product_name)

    if len(content):
        product_info = {
            item.id: jsonable_encoder(item)
            for item in content
        }
        if len(product_info):
            return JSONResponse(jsonable_encoder(product_info))
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No data")


