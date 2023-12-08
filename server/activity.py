import uuid
from celery import shared_task
from app import celery_app
from sqlite3 import Binary

from models import UserSession, Task
from utils.genbarcode import create_barcode_svg
from utils.genpages import page_svg_from_svg_list
from utils.genzipped import zip_list_of_contents


def handle_visit(session):

    if not 'uuid' in session:
        session['uuid'] = uuid.uuid4()
        UserSession.create(session_id=session['uuid'])


@shared_task(ignore_result=True)
def handle_output_req(session, data_entries):
    data = data_entries.split(',')
    zip_ = zip_list_of_contents('page', page_svg_from_svg_list(create_barcode_svg(data)))
    task = Task.get_or_none(session=session)
    if not task:
        return
    task.update(status = Task.STATUS_COMPLETED, svg_output=Binary(zip_.read())).execute()
    zip_.close()


def validate_query_src(req_args):
    # TODO move this to auth moduel
    if not 'access-key' in req_args:
        return None

    return UserSession.get_or_none(session_id=req_args['access-key'])