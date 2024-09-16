from sqlalchemy import asc, func
from sqlalchemy.orm import Session

from app.models import CompanyName, Language, Tag, Company, CompanyTag
from app.schemas import CompanySearchByCompanyNameRes, CompanyCreateReq


def get_company_name_by_contain_company_name(db: Session, company_name: str, language_code: str):
    return db \
        .query(CompanyName) \
        .join(Language) \
        .filter(CompanyName.name.ilike(f"%{company_name}%"), Language.code == language_code) \
        .all()


def find_company_by_exact_company_name(db: Session, company_name: str, language_code: str):
    company_name = db \
        .query(CompanyName) \
        .filter(CompanyName.name == company_name) \
        .first()
    if not company_name:
        return None

    company_id = company_name.company.id
    result_company_name = db \
        .query(CompanyName) \
        .join(Language) \
        .filter(CompanyName.company_id == company_id, Language.code == language_code) \
        .first()
    result_lang_tags = db \
        .query(Tag) \
        .join(CompanyTag, CompanyTag.tag_id == Tag.id) \
        .join(Tag.companies) \
        .join(Language, Tag.language_id == Language.id) \
        .filter(Company.id == company_id, Language.code == language_code) \
        .order_by(asc(CompanyTag.id)) \
        .all()
    return CompanySearchByCompanyNameRes(
        company_name=result_company_name.name,
        tags=[tag.name for tag in result_lang_tags]
    )


def create_company(db: Session, company_data: CompanyCreateReq, language_code: str):
    # 회사 추가
    company = Company()
    db.add(company)
    db.commit()
    db.refresh(company)

    # 언어별 회사 이름 저장
    for lang_code, name in company_data.company_name.items():
        language = db.query(Language).filter(Language.code == lang_code).first()
        if not language:
            language = Language(code=lang_code, name=lang_code)
            db.add(language)
            db.commit()
            db.refresh(language)

        company_name = CompanyName(company_id=company.id, language_id=language.id, name=name)
        db.add(company_name)

    # 태그 추가
    for tag_data in company_data.tags:
        for lang_code, tag_name in tag_data.tag_name.items():
            language = db.query(Language).filter(Language.code == lang_code).first()
            if not language:
                language = Language(code=lang_code, name=lang_code)
                db.add(language)
                db.commit()
                db.refresh(language)

            tag = db.query(Tag).join(Language).filter(Tag.name == tag_name, Language.code == lang_code).first()
            if not tag:
                tag = Tag(name=tag_name, language_id=language.id)
                db.add(tag)
                db.commit()
                db.refresh(tag)

            company_tag = CompanyTag(company_id=company.id, tag_id=tag.id)
            db.add(company_tag)

    db.commit()

    # 헤더에 따라 원하는 언어의 회사명과 태그 선택
    company_name = db.query(CompanyName).join(Language).filter(CompanyName.company_id == company.id,
                                                               Language.code == language_code).first()
    tags = db.query(Tag).join(Language).join(CompanyTag).filter(CompanyTag.company_id == company.id,
                                                                Language.code == language_code).all()

    return {
        "company_name": company_name.name if company_name else "",
        "tags": [tag.name for tag in tags]
    }


def search_companies_by_tag_name(db: Session, tag_query: str, language_code: str):
    # 태그명으로 회사 검색
    subquery = (
        db.query(
            Company.id,
            func.coalesce(
                db.query(CompanyName.name)
                .join(Language)
                .filter(
                    CompanyName.company_id == Company.id,
                    Language.code == language_code
                )
                .scalar_subquery(),
                db.query(CompanyName.name)
                .filter(CompanyName.company_id == Company.id)
                .limit(1)
                .scalar_subquery()
            ).label("company_name")
        )
        .join(CompanyTag, CompanyTag.company_id == Company.id)
        .join(Tag, Tag.id == CompanyTag.tag_id)
        .filter(Tag.name.ilike(f"%{tag_query}%"))
        .distinct(Company.id)
        .subquery()
    )

    # 서브 쿼리에서 선택한 이름을 가져옴
    results = db.query(subquery.c.company_name).all()
    return [{"company_name": row.company_name} for row in results]
