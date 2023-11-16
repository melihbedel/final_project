from fastapi import FastAPI

from routers.companies import companies_router
from routers.proffessionals import professionals_router
from routers.login import login_router

app = FastAPI()

app.include_router(companies_router)
app.include_router(professionals_router)
app.include_router(login_router)