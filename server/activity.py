import uuid
from celery import shared_task
from app import celery_app
from sqlite3 import Binary

from models import UserSession, Task
from utils.genlabel import *
from utils.genpages import page_svg_from_svg_list
from utils.genzipped import zip_list_of_contents


def handle_visit(session):

    if not 'uuid' in session:
        session['uuid'] = uuid.uuid4()
        UserSession.create(session_id=session['uuid'])


def handle_proc(task_id, data_entries, label_type):
    final_svgs = None
    task = Task.get_or_none(task_id=task_id)
    task.update(status = Task.STATUS_PROCESSING).execute()
    data = data_entries.split(',')
    individual_svgs = create_label_svg(data, label_type=label_type)
    if task.pages:
        task.update(processed = task.entry_count / 2).execute()
        final_svgs = page_svg_from_svg_list(individual_svgs)
        filename_prefix = 'page'
    else:
        task.update(processed = task.entry_count).execute()
        final_svgs = individual_svgs
        filename_prefix = 'barcode' if label_type == LABEL_TYPE_BARCODE else 'qrcode'

    zip_ = zip_list_of_contents(filename_prefix, final_svgs)
    if not task:
        return
    task.update(status = Task.STATUS_COMPLETED, svg_output=Binary(zip_.read())).execute()
    zip_.close()



@shared_task(ignore_result=True)
def handle_barcode_proc(task_id, data_entries):
    handle_proc(task_id, data_entries, LABEL_TYPE_BARCODE)


@shared_task(ignore_result=True)
def handle_qrcode_proc(task_id, data_entries):
    handle_proc(task_id, data_entries, LABEL_TYPE_QRCODE)


def validate_query_src(req_args):
    # TODO move this to auth moduel
    user = None
    task_id = None
    if 'access_key' in req_args:
        user = UserSession.get_or_none(session_id=req_args['access_key'])

    if 'task_id' in req_args:
        task_id = req_args['task_id']

    return user, task_id