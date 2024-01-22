# payhere - 카페 관리 프로그램

## Skills

- python 3.9
- mysql 5.7

## API 명세서

|구분|메서드|요청 URL|
|------|---|---|
|회원가입|post|/user/create|
|로그인|post|/user/login|
|로그아웃|get|/user/logout|
|상품 등록|post|/product/create|
|상품 속성 수정|put|/product/update|
|상품 삭제|delete|/product/user_id/{user_id}/product_id/{product_id}|
|등록 상품 리스트|get|/product/user_id/{user_id}/cursor/{cursor}/limit/{limit}|
|등록 상품 상세 조회|get|/product/user_id/{user_id}/product_id/{product_id}|
|등록 상품 검색|get|/product/user_id/{user_id}/product_name/{product_name}|

## ERD

![ERD](https://github.com/Gundue/restapi/assets/66405643/67ecb7a8-f937-4d75-8df4-22ae1772d78d)

## Docker 실행 방법
```
docker build -t cafe_server .
```



## 프로젝트 설정
### 1. 의존성관리
팀원간의 협업을 위해 Poetry를 사용하여 의존성을 해결하고 프로젝트의 가상환경을 관리.
