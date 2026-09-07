import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import init_db
from app.routers import results, admin

app = FastAPI(title="ISP-GOMBE API", version="3.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(results.router)
app.include_router(admin.router)


@app.on_event("startup")
def on_startup():
    from app.db import engine, SessionLocal
    from sqlalchemy import text
    try:
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS results CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS students CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS universities CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS semester_reports CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS payments CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS result_access CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS payment_audit CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS payment_config CASCADE"))
            conn.commit()
    except Exception:
        pass
    init_db()
    from seed import seed
    seed()


@app.get("/ping")
def ping():
    return {"ok": True, "version": "3.1.0"}
