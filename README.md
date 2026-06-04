# calil-aceron-portfolio

My personal portfolio site. Built with Django on the backend and React on the frontend, with content managed through the Django admin.

## Setup

```bash
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
python manage.py runserver
```

Site runs at `http://127.0.0.1:8000` locally, admin at `/admin`.

Deployed at https://calil-aceron.up.railway.app

## Environment variables

`SECRET_KEY`, `DEBUG`, `DATABASE_URL` (defaults to SQLite locally), `CSRF_TRUSTED_ORIGINS`
