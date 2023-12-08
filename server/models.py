import datetime
import re

from peewee import *

from db_config import db


class UserSession(Model):
    session_id = CharField(max_length=64, unique=True)
    first_visit = DateTimeField(default=datetime.datetime.now)
    quota_left = BigIntegerField(default=1)
    
    class Meta:
        database = db


class Task(Model):
    STATUS_IN_QUEUE = 1
    STATUS_PROCESSING = 2
    STATUS_COMPLETED = 9

    session = CharField(max_length=64, unique=False)
    timestamp = DateTimeField(default=datetime.datetime.now)
    status = IntegerField(default=STATUS_IN_QUEUE, index=True)
    entry_count = IntegerField(default=0, index=True)
    data_entries = TextField()
    svg_output = BlobField(null=True)

    class Meta:
        database = db

    def is_finished(self):
        return self.status == Task.STATUS_COMPLETED

    def get_csv_data(self):
        return self.data_entries.split(',')

    @classmethod
    def pending(cls):
        return (Task
                .select()
                .where(Task.status == Task.STATUS_IN_QUEUE)
                .order_by(Task.timestamp.desc()))

    @classmethod
    def processing(cls):
        return (Task
                .select()
                .where(Task.status == Task.STATUS_PROCESSING)
                .order_by(Task.timestamp.desc()))

    @classmethod
    def finished(cls):
        return (Task
                .select()
                .where(Task.status == Task.STATUS_COMPLETED)
                .order_by(Task.timestamp.desc()))
