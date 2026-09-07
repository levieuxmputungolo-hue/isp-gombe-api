import os
import sys

DJANGO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'django_admin')
sys.path.insert(0, DJANGO_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'isp_gombe.settings')

import django
django.setup()

from django.core.management import call_command
call_command('migrate', '--run-syncdb', verbosity=0)

from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@isp-gombe.cd', 'isp-gombe-2025')
    print('[Django] Superuser created: admin / isp-gombe-2025')
