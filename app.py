from fastapi import FastAPI
from api.router import router
from data.database import get_session, create_tables, drop_all_tables
from data.seed import seed_database
from services.company_service import index_companies

session = get_session()
app = FastAPI()

@app.on_event("startup")
def startup_event():
    create_tables()
    seed_database()
    index_companies(session)

@app.on_event("shutdown")
def shutdown_event():
    drop_all_tables()
    session.close()

app.include_router(router)


