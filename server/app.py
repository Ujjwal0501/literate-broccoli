from flask import Flask
from huey import RedisHuey
from db_config import db
from celery_config import celery_init_app


server = Flask(__name__)
server.config.from_mapping(
    CELERY=dict(
        broker_url="redis://localhost",
        result_backend="redis://localhost",
        task_ignore_result=True,
    ),
)
celery_app = celery_init_app(server)
huey = RedisHuey()
