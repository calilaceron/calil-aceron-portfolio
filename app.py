import os
import django
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.settings')
django.setup()

# Ensure migrations and staticfiles are prepared on startup (e.g. Render / cloud deploys)
try:
    call_command('migrate', interactive=False)
except Exception as e:
    print('Startup migration notice:', e)

try:
    if not os.path.exists('staticfiles') or not os.listdir('staticfiles'):
        call_command('collectstatic', interactive=False)
except Exception as e:
    print('Startup collectstatic notice:', e)

application = get_wsgi_application()
app = application
