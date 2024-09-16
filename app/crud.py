from sqlalchemy.orm import Session

from app import models


def get_company_by_name(db: Session, name: str, language_code: str):
    return db \
        .query(models.CompanyName) \
        .join(models.Language) \
        .filter(models.CompanyName.name.ilike(f"%{name}%"), models.Language.code == language_code) \
        .all()
