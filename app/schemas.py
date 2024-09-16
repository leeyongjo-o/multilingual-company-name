from pydantic import BaseModel, Field


class CompanySearchRes(BaseModel):
    name: str = Field(serialization_alias='company_name')


class CompanySearchByCompanyNameRes(BaseModel):
    company_name: str
    tags: list[str]


class TagName(BaseModel):
    tag_name: dict[str, str]


class CompanyCreateReq(BaseModel):
    company_name: dict[str, str]
    tags: list[TagName]


class CompanyCreateRes(BaseModel):
    company_name: str
    tags: list[str]


class CompanySearchByTagRes(BaseModel):
    company_name: str


CompanyAddTagsReq = list[TagName]


class CompanyAddTagsRes(BaseModel):
    company_name: str
    tags: list[str]


class CompanyRemoveTagsRes(CompanyAddTagsRes):
    pass
