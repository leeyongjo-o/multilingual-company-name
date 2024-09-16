from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app import schemas, crud
from app.database import get_db

company_router = APIRouter(tags=["회사"])


@company_router.get(
    "/search",
    response_model=list[schemas.CompanySearchRes],
    summary="1. 회사명 자동 완성",
)
def search_companies(query: str, x_wanted_language: str = Header("ko"), db: Session = Depends(get_db)):
    """
    회사명의 일부만 들어가도 검색이 되어야 합니다.\n
    header의 x-wanted-language 언어값에 따라 해당 언어로 출력되어야 합니다.
    """
    companies = crud.get_company_name_by_contain_company_name(db, company_name=query, language_code=x_wanted_language)
    return companies


@company_router.get(
    "/companies/{company_name}",
    response_model=schemas.CompanySearchByCompanyNameRes,
    summary="2. 회사 이름으로 회사 검색",
)
def search_companies_by_company_name(company_name: str, x_wanted_language: str = Header("ko"), db: Session = Depends(get_db)):
    """
    header의 x-wanted-language 언어값에 따라 해당 언어로 출력되어야 합니다.
    """
    company = crud.find_company_by_exact_company_name(db, company_name=company_name, language_code=x_wanted_language)
    if not company:
        raise HTTPException(status_code=404, detail="결과가 없습니다.")
    return company


@company_router.post(
    "/companies",
    response_model=schemas.CompanyCreateRes,
    summary="3. 새로운 회사 추가",
)
def create_company(
    company_data: schemas.CompanyCreateReq,
    x_wanted_language: str = Header("tw"),
    db: Session = Depends(get_db),
):
    """
    새로운 언어(tw)도 같이 추가 될 수 있습니다. \n
    저장 완료후 header의 x-wanted-language 언어값에 따라 해당 언어로 출력되어야 합니다.
    """
    result = crud.create_company(db=db, company_data=company_data, language_code=x_wanted_language)
    return result
