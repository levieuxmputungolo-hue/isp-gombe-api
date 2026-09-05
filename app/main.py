import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import init_db
from app.routers import results
from app.routers import payments

app = FastAPI(title="ISP-GOMBE API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(results.router)
app.include_router(payments.router)


@app.on_event("startup")
def on_startup():
    init_db()
    from app.db import SessionLocal
    from app.models import Student
    db = SessionLocal()
    if db.query(Student).count() == 0:
        from seed import seed
        seed()
    db.close()


@app.get("/ping")
def ping():
    return {"ok": True}
