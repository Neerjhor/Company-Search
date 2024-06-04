from fastapi import APIRouter, HTTPException, Depends
from services.company_service import get_descendants, search_companies, CompanyNotFoundError
from data.database import get_session

router = APIRouter()

@router.get("/companies/{company_id}/descendants")
def get_descendants_route(company_id: int, session = Depends(get_session)):
    try:
        descendants = get_descendants(company_id, session)
    except CompanyNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return descendants

@router.get("/users/{user_id}/companies")
def search_companies_route(user_id: int, q: str = "", session = Depends(get_session)):
    results = search_companies(user_id, q, session)
    return results
