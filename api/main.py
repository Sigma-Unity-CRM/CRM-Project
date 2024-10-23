from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.account_router import router as account_router
from routers.activity_router import router as activity_router
from routers.activity_type_router import router as activity_type_router
from routers.activity_user_router import router as activity_user_router
from routers.activity_contact_router import router as activity_contact_router
from routers.contact_router import router as contact_router
from routers.country_router import router as country_router
from routers.forecast_category_router import router as forecast_category_router
from routers.opportunity_router import router as opportunity_router
from routers.opportunity_contact_router import router as opportunity_contact_router
from routers.opportunity_owner_router import router as opportunity_owner_router
from routers.stage_router import router as stage_router
from routers.user_router import router as user_router

import os

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("CORS_HOST", "http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(account_router)
app.include_router(activity_router)
app.include_router(activity_type_router)
app.include_router(activity_user_router)
app.include_router(activity_contact_router)
app.include_router(contact_router)
app.include_router(country_router)
app.include_router(forecast_category_router)
app.include_router(opportunity_router)
app.include_router(opportunity_contact_router)
app.include_router(opportunity_owner_router)
app.include_router(stage_router)
app.include_router(user_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
