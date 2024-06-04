from data.models import Company, User
from sqlmodel import select
from config import settings
from elasticsearch import Elasticsearch, helpers
from collections import deque

es = Elasticsearch(settings.elastic_search_url)

class CompanyNotFoundError(Exception):
    pass

def get_descendants(company_id, session) -> list[Company]:
    company = session.get(Company, company_id)
    if not company:
        raise CompanyNotFoundError("Company does not exit.")
    descendants = [session.exec(select(Company).where(Company.id == company_id)).one_or_none()]

    queue = deque([company_id])

    while queue:
        current_id = queue.popleft()
        children_companies = session.exec(select(Company).where(Company.parent_id == current_id)).all()
        for child_company in children_companies:
            descendants.append(child_company)
            queue.append(child_company.id)
    
    return descendants

def index_companies(session):
    companies = session.exec(select(Company)).all()
    actions = [
        {
            "_index": "companies",
            "_id": company.id,
            "_source": {
                "name": company.name,
                "id": company.id
            }
        }
        for company in companies
    ]
    helpers.bulk(es, actions)

def search_companies(user_id: int, query: str, session):

    user = session.get(User, user_id)

    accessible_companies = get_descendants(user.company_id, session)
    accessible_company_ids = [company.id for company in accessible_companies]

    response = es.search(index="companies", body={
        "query": {
            "bool": {
                "must": {
                    "query_string": {
                        "query": f"*{query}*",
                        "fields": ["name"]
                    }
                },
                "filter": {
                    "terms": {"id": accessible_company_ids}
                }
            }
        }
    })
    return [hit["_source"] for hit in response['hits']['hits']]

