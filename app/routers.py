from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from app import schemas, crud
from app.database import get_db

company_router = APIRouter(tags=["회사"])


@company_router.get(
    "/search",
    response_model=list[schemas.CompanySearchRes],
    summary="회사명 자동 완성",
)
def search_companies(query: str, x_wanted_language: str = Header("ko"), db: Session = Depends(get_db)):
    """
    회사명의 일부만 들어가도 검색이 되어야 합니다.\n
    header의 x-wanted-language 언어값에 따라 해당 언어로 출력되어야 합니다.
    """
    companies = crud.get_company_by_name(db, name=query, language_code=x_wanted_language)
    return companies

