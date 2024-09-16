from sqlalchemy import asc
from sqlalchemy.orm import Session

from app.models import CompanyName, Language, Tag, Company, CompanyTag
from app.schemas import CompanySearchByCompanyNameRes


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
