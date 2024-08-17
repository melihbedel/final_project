from fastapi import FastAPI
from routers.authentication import authentication_router
from routers.companies import companies_router
from routers.professionals import professionals_router
from routers.search import search_router


app = FastAPI()

app.include_router(authentication_router)
app.include_router(companies_router)
app.include_router(professionals_router)
app.include_router(search_router)