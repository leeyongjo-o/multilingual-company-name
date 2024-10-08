from sqlalchemy import Column, BigInteger, DateTime, func, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base


class Company(Base):
    __tablename__ = 'company'

    id = Column(BigInteger, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    names = relationship("CompanyName", back_populates="company")
    tags = relationship("Tag", secondary="company_tag", back_populates="companies")


class CompanyName(Base):
    __tablename__ = 'company_name'

    id = Column(BigInteger, primary_key=True, index=True)
    company_id = Column(BigInteger, ForeignKey('company.id'))
    language_id = Column(BigInteger, ForeignKey('language.id'))
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    company = relationship("Company", back_populates="names")
    language = relationship("Language", back_populates="company_names")


class Tag(Base):
    __tablename__ = 'tag'

    id = Column(BigInteger, primary_key=True, index=True)
    language_id = Column(BigInteger, ForeignKey('language.id'))
    tag_group_id = Column(BigInteger, ForeignKey('tag_group.id'))
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    group = relationship("TagGroup", back_populates="tags")
    language = relationship("Language", back_populates="tags")
    companies = relationship("Company", secondary="company_tag", back_populates="tags")


class TagGroup(Base):
    __tablename__ = 'tag_group'

    id = Column(BigInteger, primary_key=True, index=True)

    tags = relationship("Tag", back_populates="group")


class Language(Base):
    __tablename__ = 'language'

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    company_names = relationship("CompanyName", back_populates="language")
    tags = relationship("Tag", back_populates="language")


class CompanyTag(Base):
    __tablename__ = 'company_tag'

    id = Column(BigInteger, primary_key=True, index=True)
    company_id = Column(BigInteger, ForeignKey('company.id'), nullable=False)
    tag_id = Column(BigInteger, ForeignKey('tag.id'), nullable=False)

    __table_args__ = (
        UniqueConstraint('company_id', 'tag_id', name='_company_tag_uc'),
    )
