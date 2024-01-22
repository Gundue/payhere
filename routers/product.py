from fastapi import APIRouter, Depends, HTTPException, Form, Header
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette import status

import models
from crud.crud_product import (
    create_product, update_product, read_product_name, read_product_lists, product_detail, delete_product
)
from crud.crud_token import find_token_exists
from utils.chk_access_token import chk_access_token
from db.database import engine
from schemas import product_schema
from routers import get_db
from utils.response import custom_response

prefix = "product"
models.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix=f"/{prefix}")


@router.post("/create")
async def product_create(
        product: product_schema.CreateProduct,
        db: Session = Depends(get_db),
        access_token: str = Header(None, convert_underscores=False)
):
    """
    `상품 등록`
    """
    try:
        get_token = find_token_exists(db, access_token)
        check_token = chk_access_token(get_token, access_token)
        if check_token == "Token valid":
            create_product(db, product)
            return custom_response(code=200, message="Product create success")
        else:
            return custom_response(code=401, message=check_token)
    except Exception as e:
        return custom_response(code=500, message=str(e))


@router.put("/update")
async def product_update(
        product: product_schema.Product,
        db: Session = Depends(get_db),
        access_token: str = Header(None, convert_underscores=False)
):
    """
    `상품 수정`
    """
    try:
        get_token = find_token_exists(db, access_token)
        check_token = chk_access_token(get_token, access_token)
        if check_token == "Token valid":
            update_product(db, product)
            return custom_response(code=200, message="Product update success")
        else:
            return custom_response(code=401, message=check_token)
    except Exception as e:
        return custom_response(code=500, message=str(e))


@router.get("/user_id/{user_id}/cursor/{cursor}/limit/{limit}", response_model=product_schema.Product)
async def product_get_lists(
        user_id: int,
        cursor: int,
        limit: int,
        access_token: str = Header(None, convert_underscores=False),
        db: Session = Depends(get_db)):
    """
    `상품 리스트 조회`
    """
    get_token = find_token_exists(db, access_token)
    check_token = chk_access_token(get_token, access_token)
    if check_token == "Token valid":
        content = read_product_lists(db, user_id, cursor, limit)
        product_data = []
        for item in content:
            product_data.append({"category": item[0], "name": item[1]})
        response_data = {"products": product_data}
        return custom_response(code=200, message="Product list success", data=response_data)
    else:
        return custom_response(code=401, message=check_token)


@router.get("/user_id/{user_id}/product_id/{product_id}")
async def product_get_detail(
        user_id: int,
        product_id: int,
        db: Session = Depends(get_db),
        access_token: str = Header(None, convert_underscores=False)
):
    """
    `상품 상세 내역 조회`
    """
    get_token = find_token_exists(db, access_token)
    check_token = chk_access_token(get_token, access_token)
    if check_token == "Token valid":
        content = product_detail(db, user_id, product_id)
        response_data = {"products": [jsonable_encoder(content[0])]} if content else []
        return custom_response(code=200, message="Product detail success", data=response_data)
    else:
        return custom_response(code=401, message=check_token)


@router.get("/user_id/{user_id}/product_name/{product_name}")
async def product_get_search(
        user_id: int,
        product_name: str,
        db: Session = Depends(get_db),
        access_token: str = Header(None, convert_underscores=False)
):
    """
    `상품 like 조회`
    """
    get_token = find_token_exists(db, access_token)
    check_token = chk_access_token(get_token, access_token)
    if check_token == "Token valid":
        content = read_product_name(db, user_id, product_name)
        response_data = {"products": [jsonable_encoder(item) for item in content]} if content else []
        return custom_response(code=200, message="Product search success", data=response_data)
    else:
        return custom_response(code=401, message=check_token)


@router.delete("/user_id/{user_id}/product_id/{product_id}")
async def product_delete(
        user_id: int,
        product_id: int,
        db: Session = Depends(get_db),
        access_token: str = Header(None, convert_underscores=False)
):
    """
    `상품 삭제`
    """
    get_token = find_token_exists(db, access_token)
    check_token = chk_access_token(get_token, access_token)
    if check_token == "Token valid":
        delete_product(db, user_id, product_id)
        return custom_response(code=200, message="Product delete")
    else:
        return custom_response(code=401, message=check_token)
