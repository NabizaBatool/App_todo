web: gunicorn todoSite.wsgi
celery: celery -A todoSite.celery worker --pool=solo -1 info