from fastapi import FastAPI

from . import models
from .database import engine
from .routers import company_router

# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=engine)

# FastAPI 애플리케이션 생성
app = FastAPI(
    title="다국어 회사명 관리 프로젝트",
    description="""

- 회사명 자동완성
    - 회사명의 일부만 들어가도 검색이 되어야 합니다.
    
- 회사 이름으로 회사 검색
- 태그명으로 회사 검색
    - 태그로 검색 관련된 회사가 검색되어야 합니다.
    - 다국어로 검색이 가능해야 합니다.
        - 일본어 태그로 검색을 해도 한국 회사가 노출이 되어야 합니다.
        - タグ_4로 검색 했을 때, 원티드랩 회사 정보가 노출이 되어야 합니다.
    - 동일한 회사는 한번만 노출이 되어야합니다.

- 회사 태그 정보 추가
- 회사 태그 정보 삭제
    
    """,
    version="1.0.0"
)

# 라우터 등록
app.include_router(company_router)


@app.get("/ping", include_in_schema=False)
def root():
    return {"message": "SUCCESS"}
