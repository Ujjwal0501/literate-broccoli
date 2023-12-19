
from models import Task
from activity import validate_query_src, handle_qrcode_proc, handle_barcode_proc

from flask import request, send_file, Blueprint, session
from config import MAX_REQUEST_SIZE
import csv, io, json, peewee
from hashlib import sha1


api = Blueprint("api", __name__)


@api.route('/csv-to-barcode', methods=['POST'])
def handle_barcode_reqeust():
    user, task_id = validate_query_src(request.args)

    if 'file' not in request.files:
        return 'No file part in the request', 400

    file = request.files['file']
    if file.filename == '' or not file:
        return 'No file selected for uploading', 400

    task = None
    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    data = list(csv.reader(stream))
    data = [item for sublist in data for item in sublist]
    if len(data) > MAX_REQUEST_SIZE:
        return f'Entry limit exceeded. Maximum entry allowed is {MAX_REQUEST_SIZE}', 400

    try:
        task = Task.create(entry_count = len(data), data_entries = ','.join(data))
    except peewee.IntegrityError as e:
        task = Task.get_or_none(task_id = sha1(bytes(','.join(data), 'utf-8')).hexdigest())
    finally:
        handle_barcode_proc.delay(task.task_id, task.data_entries)
        

    if user:
        user.update(quota_left=user.quota_left-1).execute()

    return json.dumps({'status': "OK", 'task_id': task.task_id}), 200



@api.route('/csv-to-qrcode', methods=['POST'])
def handle_qrcode_reqeust():
    user, task_id = validate_query_src(request.args)

    if 'file' not in request.files:
        return 'No file part in the request', 400

    file = request.files['file']
    if file.filename == '' or not file:
        return 'No file selected for uploading', 400

    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    data = list(csv.reader(stream))
    data = [item for sublist in data for item in sublist]
    if len(data) > MAX_REQUEST_SIZE:
        return f'Entry limit exceeded. Maximum entry allowed is {MAX_REQUEST_SIZE}', 400

    try:
        task = Task.create(entry_count = len(data), data_entries = ','.join(data))
    except peewee.IntegrityError as e:
        task = Task.get_or_none(task_id = sha1(bytes(','.join(data), 'utf-8')).hexdigest())
    finally:
        handle_qrcode_proc.delay(task.task_id, task.data_entries)

    if user:
        user.update(quota_left=user.quota_left-1).execute()

    return json.dumps({'status': "OK", 'task_id': task.task_id}), 200


@api.route('/csv-to-barcode', methods=['GET'])
def download_barcode():
    user, task_id = validate_query_src(request.args)

    task = Task.get_or_none(task_id=task_id)
    if not task:
        return 'No task received', 400

    if task.status == Task.STATUS_IN_QUEUE or task.status == Task.STATUS_PROCESSING:
        progress = task.processed * 100 / task.entry_count
        return json.dumps({'status': 'Processing', 'progress': progress}), 206

    if task.status == Task.STATUS_COMPLETED:
        zip_ = io.BytesIO(task.svg_output)
        return send_file(zip_, mimetype='application/zip', as_attachment=True, download_name='content.zip')
    else:
        return "Fail", 400


@api.route('/csv-to-qrcode', methods=['GET'])
def download_qrcode():
    user, task_id = validate_query_src(request.args)

    task = Task.get_or_none(task_id=task_id)
    if not task:
        return 'No task received', 400

    if task.status == Task.STATUS_IN_QUEUE or task.status == Task.STATUS_PROCESSING:
        progress = task.processed * 100 / task.entry_count
        return json.dumps({'status': 'Processing', 'progress': progress}), 206

    if task.status == Task.STATUS_COMPLETED:
        zip_ = io.BytesIO(task.svg_output)
        return send_file(zip_, mimetype='application/zip', as_attachment=True, download_name='content.zip')
    else:
        return "Fail", 400
