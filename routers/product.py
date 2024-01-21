import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Form, Header
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette import status
from datetime import datetime

import models
from crud.crud_product import \
    create_product, update_product, read_product_name, product_pagination, product_detail, delete_product
from crud.crud_token import read_token_chk
from core.auth.jwt import chk_access_token
from db.database import engine
from schemas import product_schema
from routers import get_db
from utils.response import custom_response

prefix = "prodcut"
models.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix=f"/{prefix}", responses={401: {"description": "product"}})


@router.post("/create")
async def product_create(
        product: product_schema.CreateProduct,
        db: Session = Depends(get_db),
        access_token: str = Header(None, convert_underscores=False)
):
    """
    `상품 등록`
    """
    get_token = read_token_chk(db, access_token)
    if get_token:
        is_token_valid = chk_access_token(get_token, access_token)
        if is_token_valid:
            response_message = create_product(db, product)
            return custom_response(code=200, message="ok")
        else:
            return custom_response(code=401, message="Invalid access token")
    else:
        return custom_response(code=401, message="No token provided")


@router.put("/update")
async def product_update(
        product: product_schema.Product,
        db: Session = Depends(get_db),
        access_token: str = Header(None, convert_underscores=False)
):
    """
    `상품 수정`
    """
    get_token = read_token_chk(db, access_token)
    if get_token:
        is_token_valid = chk_access_token(get_token, access_token)
        if is_token_valid:
            response_message = update_product(db, product)
            if "success" in response_message:
                return custom_response(code=200, message="ok")
            else:
                return custom_response(code=400, message="Invalid response from update_product")
        else:
            return custom_response(code=401, message="Invalid access token")
    else:
        return custom_response(code=401, message="No token provided")


@router.get("/user_id/{user_id}/cursor/{cursor}/limit/{limit}", response_model=product_schema.Product)
async def product_get(
        user_id: int,
        cursor: int,
        limit: int,
        access_token: str = Header(None, convert_underscores=False),
        db: Session = Depends(get_db)):
    """
    `상품 조회`
    """
    get_token = read_token_chk(db, access_token)
    if get_token:
        is_token_valid = chk_access_token(get_token, access_token)
        if is_token_valid:
            content = product_pagination(db, user_id, cursor, limit)
            if len(content):
                product_info = {
                    f"{i + 1}": {"category": content[i][0], "name": content[i][1]}
                    for i in range(len(content))
                }
                if len(product_info):
                    return custom_response(code=200, message="ok", data=product_info)
            else:
                return custom_response(code=400, message="Invalid response from update_product")
        else:
            return custom_response(code=401, message="Invalid access token")
    else:
        return custom_response(code=401, message="No token provided")
    return custom_response(code=400, message="No data")


@router.get("/user_id/{user_id}/product_id/{product_id}")
async def product_detail_get(
        user_id: int,
        product_id: int,
        db: Session = Depends(get_db),
        access_token: str = Header(None, convert_underscores=False)
):
    """
    `상품 상세 내역 조회`
    """
    get_token = read_token_chk(db, access_token)
    if get_token:
        is_token_valid = chk_access_token(get_token, access_token)
        if is_token_valid:
            content = product_detail(db, user_id, product_id)
            response_data = {"products": [jsonable_encoder(content[0])]}
            if len(content):
                return custom_response(code=200, message="ok", data=response_data)
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No data")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token provided")


@router.get("/user_id/{user_id}/product_name/{product_name}")
async def product_search_get(
        user_id: int,
        product_name: str,
        db: Session = Depends(get_db),
        access_token: str = Header(None, convert_underscores=False)
):
    """
    `상품 like 조회`
    """
    get_token = read_token_chk(db, access_token)
    if get_token:
        is_token_valid = chk_access_token(get_token, access_token)
        if is_token_valid:
            content = read_product_name(db, user_id, product_name)
            product_data = []

            if len(content):
                for item in content:
                    product_data.append(jsonable_encoder(item))
                response_data = {"products": product_data}
                return custom_response(code=200, message="ok", data=response_data)
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No data")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token provided")


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
    get_token = read_token_chk(db, access_token)
    if get_token:
        is_token_valid = chk_access_token(get_token, access_token)
        if is_token_valid:
            delete_product(db, user_id, product_id)
            return custom_response(code=200, message="ok")
        else:
            return custom_response(code=401, message="Invalid access token")
    else:
        return custom_response(code=401, message="No token provided")