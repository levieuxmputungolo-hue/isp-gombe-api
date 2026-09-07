import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

DJANGO_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'django_admin')
sys.path.insert(0, DJANGO_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'isp_gombe.settings')

app = FastAPI(title="ISP-GOMBE API", version="3.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.routers import results, admin
app.include_router(results.router)
app.include_router(admin.router)


@app.on_event("startup")
def on_startup():
    from app.db import engine, init_db
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

    try:
        import django
        django.setup()
        from django.core.management import call_command
        call_command('migrate', '--run-syncdb', verbosity=0)
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@isp-gombe.cd', 'isp-gombe-2025')
            print('[Django] Superuser created: admin / isp-gombe-2025')
        from django.core.wsgi import get_wsgi_application
        from a2wsgi import WSGIMiddleware
        django_app = get_wsgi_application()
        app.mount("/django-admin", WSGIMiddleware(django_app))
        print("[Django] Admin panel mounted at /django-admin")
    except Exception as e:
        print(f"[Django] Setup error: {e}")


@app.get("/ping")
def ping():
    return {"ok": True, "version": "3.2.0"}
