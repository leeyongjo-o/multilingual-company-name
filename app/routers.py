from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app import schemas, crud
from app.database import get_db
from app.schemas import CompanyAddTagsReq

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

@company_router.get(
    "/tags",
    response_model=list[schemas.CompanySearchByTagRes],
    summary="4. 태그명으로 회사 검색",
)
def search_companies_by_tag(
    query: str,
    x_wanted_language: str = Header("ko"),
    db: Session = Depends(get_db),
):
    """
    태그로 검색 관련된 회사가 검색되어야 합니다.\n
    다국어로 검색이 가능해야 합니다.\n
    일본어 태그로 검색을 해도 language가 ko이면 한국 회사명이 노출이 되어야 합니다.\n
    ko언어가 없을경우 노출가능한 언어로 출력합니다.\n
    동일한 회사는 한번만 노출이 되어야합니다.
    """
    companies = crud.search_companies_by_tag_name(db, tag_query=query, language_code=x_wanted_language)
    return companies


@company_router.put(
    "/companies/{company_name}/tags",
    response_model=schemas.CompanyAddTagsRes,
    summary="5. 회사 태그 정보 추가",
)
def add_tags_to_company(
    company_name: str,
    req: CompanyAddTagsReq,
    x_wanted_language: str = Header("en"),
    db: Session = Depends(get_db),
):
    """
    저장 완료후 header의 x-wanted-language 언어값에 따라 해당 언어로 출력되어야 합니다.
    """
    result = crud.add_tags_to_company(db=db, company_name=company_name, tag_data_list=req, language_code=x_wanted_language)
    if not result:
        return {"detail": "없는 회사입니다."}, 404
    return result
