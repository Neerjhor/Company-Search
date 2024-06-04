from sqlmodel import Session, create_engine, SQLModel, select
from config import settings
from .models import Company, User

class CompanyNotFoundError(Exception):
    pass

engine = create_engine(settings.database_url)
session = Session(engine)

def create_tables():
    SQLModel.metadata.create_all(engine)

def drop_all_tables():
    SQLModel.metadata.drop_all(engine)

def get_session():
    return session

def add_company(name: str, parent_name: str = None):
    if parent_name:
        parent_company = session.exec(select(Company).where(Company.name == parent_name)).one_or_none()
        if not parent_company:
            raise CompanyNotFoundError("Parent company not found.")
        company = Company(name=name, parent_id=parent_company.id)
    else:
        company = Company(name=name)
    session.add(company)
    session.commit()

def add_user(username: str, company_name: str):
    company = session.exec(select(Company).where(Company.name == company_name)).one_or_none()
    if not company:
        raise CompanyNotFoundError("Company not found.")
    user = User(username=username, company_id=company.id)
    session.add(user)
    session.commit()