import logging
import os

workers = os.getenv('GUNICORN_WORKERS', 1)
timeout = os.getenv('GUNICORN_TIMEOUT', 120)
port = os.getenv('GUNICORN_PORT', 5000)
bind = f'0.0.0.0:{port}'
accesslog = '-'


def on_starting(_):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(name)s] %(levelname)s: %(message)s')
