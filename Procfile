web: gunicorn WindWalker:server --workers 4 --timeout 1200
worker-default: celery -A tasks:celery_app worker --loglevel=INFO --concurrency=1
worker-beat: celery -A tasks:celery_app beat --loglevel=INFO
