from sqlalchemy import Column, BigInteger, DateTime, func, ForeignKey, String, Table
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
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    language = relationship("Language", back_populates="tags")
    companies = relationship("Company", secondary="company_tag", back_populates="tags")


class Language(Base):
    __tablename__ = 'language'

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    company_names = relationship("CompanyName", back_populates="language")
    tags = relationship("Tag", back_populates="language")


company_tag = Table(
    'company_tag',
    Base.metadata,
    Column('company_id', BigInteger, ForeignKey('company.id'), primary_key=True),
    Column('tag_id', BigInteger, ForeignKey('tag.id'), primary_key=True)
)
