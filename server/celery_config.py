from flask import Flask
from celery import Celery, Task

def celery_init_app(app: Flask) -> Celery:
    celery_app = Celery(app.name, include=['activity'])
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    celery_app.autodiscover_tasks()
    return celery_app