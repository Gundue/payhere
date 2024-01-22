# payhere - 카페 관리 프로그램
<br/>
## Skills
- python 3.9
- fastapi=0.109.0
- mysql 5.7
<br/>
## API 명세서
<br/>
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
<br/>
## ERD
![ERD](https://github.com/Gundue/restapi/assets/66405643/67ecb7a8-f937-4d75-8df4-22ae1772d78d)

### USER TABLE
- 유저의 전화번호, 해쉬 비밀번호, 유저의 이름을 저장

### PRODUCT TABLE
- 유저의 Index값, 카테고리, 가격, 원가, 상품명, 상품 설명, 바코드, 유통기한, 사이즈를 저장

### TOKEN TALBE
- 유저의 Index값, access 토큰, 저장시각을 저장
  
<br/>
## 프로젝트 Docker 실행 방법
- 도커 이미지 빌드
```
docker build -t cafe_server .
```
- 도커 서버 실행
```
docker run -p 8000:8000 cafe_server
```
도커 이미지 주소
https://hub.docker.com/repository/docker/gunw/cafe_server/general
- 도커 이미지 pull
```
docker pull gunw/cafe_server:latest
```
<br/>
## 프로젝트 관리
### 브랜치 관리
개인 브런치를 생성하여 개별적으로 작업후, 기능 완료 시 main 브런치에 pull request 생성
### 의존성관리
Poetry를 활용하여 프로젝트의 의존성을 정확하게 관리하고, 팀원들 간에 일관된 개발 환경을 유지
### 모듈화
자주 사용하는 기능은 utils 폴더에 모듈화하여 별도의 모듈로 분리
### ORM 사용
모델 클래스를 통해 데이터베이스 테이블을 정의

