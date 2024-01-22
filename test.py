from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from main import app
from db.database import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import *
from routers import get_db

DATABASE_URL = (
    f"mysql+pymysql://{DB_ID}:{DB_PW}@"
    f"{DB_HOST}:{DB_PORT}/{TEST_DB}"
)
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


client = TestClient(app)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.mark.run(order=1)
def test_user_create():
    test_user_data = {
        "phone": "01011111111",
        "password": "test",
        "name": "park"
    }

    response = client.post("/user/create", json=test_user_data)

    assert response.status_code == 200
    assert response.json()['meta'] == {'code': 200, 'message': 'Success Create'}


@pytest.mark.run(order=2)
def test_login():
    test_login_data = {
        "phone": "01011111111",
        "password": "test"
    }

    response = client.post("/user/login", json=test_login_data)

    assert response.status_code == 200
    assert response.json()['meta']['code'] == 200


@pytest.mark.run(order=3)
def test_product_create():
    # 테스트 상품 데이터
    test_product_data = {
        "user_id": 1,
        "category": "음료",
        "name": "슈크림 라떼",
        "price": "5000",
        "cost": "1000",
        "description": "슈크림",
        "barcode": "001010101",
        "expiration_date": "2024-01-22T15:38:00",
        "size": "small"
    }

    response_login = client.post("/user/login", json={"phone": "01011111111", "password": "test"})
    access_token = response_login.json()['meta']["message"]

    response = client.post("/product/create", json=test_product_data, headers={"access_token": access_token})

    assert response.status_code == 200
    assert response.json()['meta'] == {"code": 200, "message": "Product create success"}


@pytest.mark.run(order=4)
def test_product_get_lists():
    response_login = client.post("/user/login", json={"phone": "01011111111", "password": "test"})
    access_token = response_login.json()['meta']["message"]

    response = client.get("/product/user_id/1/cursor/0/limit/10", headers={"access_token": access_token})

    assert response.status_code == 200
    assert response.json()['meta'] == {"code": 200, "message": "Product list success"}


@pytest.mark.run(order=5)
def test_product_get_search():
    response_login = client.post("/user/login", json={"phone": "01011111111", "password": "test"})
    access_token = response_login.json()['meta']["message"]

    response = client.get("/product/user_id/1/product_name/ㅅㅋㄹ", headers={"access_token": access_token})

    assert response.status_code == 200
    assert "products" in response.json()["data"]


@pytest.mark.run(order=6)
def test_product_get_detail():
    response_login = client.post("/user/login", json={"phone": "01011111111", "password": "test"})
    access_token = response_login.json()['meta']["message"]

    response = client.get("/product/user_id/1/product_id/1", headers={"access_token": access_token})

    assert response.status_code == 200
    assert "products" in response.json()["data"]


@pytest.mark.run(order=7)
def test_product_update():
    test_update_data = {
        "id": 1,
        "user_id": 1,
        "category": "커피",
        "name": "아메리카노",
        "price": "4500",
        "cost": "1000",
        "description": "아메리카노",
        "barcode": "1010110",
        "expiration_date": "2024-01-22T15:38:00",
        "size": "large"
    }
    response_login = client.post("/user/login", json={"phone": "01011111111", "password": "test"})
    access_token = response_login.json()['meta']["message"]

    response = client.put("/product/update", json=test_update_data, headers={"access_token": access_token})

    assert response.status_code == 200
    assert response.json()['meta'] == {"code": 200, "message": "Product update success"}


@pytest.mark.run(order=8)
def test_product_delete():
    response_login = client.post("/user/login", json={"phone": "01011111111", "password": "test"})
    access_token = response_login.json()['meta']["message"]

    response = client.delete("/product/user_id/1/product_id/1", headers={"access_token": access_token})

    assert response.status_code == 200
    assert response.json()['meta'] == {"code": 200, "message": "Product delete"}


@pytest.mark.run(order=9)
def test_logout():
    response = client.get("/user/logout", headers={"access_token": "test_access_token"})

    assert response.status_code == 200
    assert response.json()['meta'] == {"code": 401, "message": "No token provided"}