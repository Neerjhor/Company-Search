from sqlmodel import SQLModel, Field
from typing import Optional

class Company(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    parent_id: Optional[int] = Field(default=None, foreign_key="company.id", index=True)

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    company_id: int = Field(default=None, foreign_key="company.id")
