from pydantic import BaseModel, Field


class CompanySearchRes(BaseModel):
    name: str = Field(serialization_alias='company_name')


class CompanySearchByCompanyNameRes(BaseModel):
    company_name: str
    tags: list[str]
