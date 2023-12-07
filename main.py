from fastapi import FastAPI

from routers.companies import companies_router
from routers.proffessionals import professionals_router
from routers.login import login_router
from routers.skill import skill_router
from routers.searching import searching_router

app = FastAPI()

app.include_router(companies_router)
app.include_router(professionals_router)
app.include_router(login_router)
app.include_router(skill_router)
app.include_router(searching_router)