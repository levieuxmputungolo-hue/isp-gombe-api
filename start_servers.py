import os
import sys
import subprocess
import threading
import time


def run_fastapi():
    port = os.environ.get('PORT', '8000')
    admin_port = os.environ.get('ADMIN_PORT', '8001')
    subprocess.run([
        sys.executable, '-m', 'uvicorn', 'app.main:app',
        '--host', '0.0.0.0', '--port', port,
    ])


def run_django():
    admin_port = os.environ.get('ADMIN_PORT', '8001')
    django_dir = os.path.join(os.path.dirname(__file__), 'django_admin')
    subprocess.run([
        sys.executable, 'manage.py', 'runserver', f'0.0.0.0:{admin_port}',
    ], cwd=django_dir)


def create_superuser():
    django_dir = os.path.join(os.path.dirname(__file__), 'django_admin')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'isp_gombe.settings'
    sys.path.insert(0, django_dir)
    try:
        import django
        django.setup()
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@isp-gombe.cd', 'isp-gombe-2025')
            print('[Django] Superuser created: admin / isp-gombe-2025')
    except Exception as e:
        print(f'[Django] Superuser creation error: {e}')
    finally:
        sys.path.pop(0)


if __name__ == '__main__':
    create_superuser()

    print('[ISP-GOMBE] Starting FastAPI on port', os.environ.get('PORT', '8000'))
    print('[ISP-GOMBE] Starting Django admin on port', os.environ.get('ADMIN_PORT', '8001'))

    t1 = threading.Thread(target=run_fastapi, daemon=True)
    t2 = threading.Thread(target=run_django, daemon=True)
    t1.start()
    t2.start()

    t1.join()
    t2.join()
